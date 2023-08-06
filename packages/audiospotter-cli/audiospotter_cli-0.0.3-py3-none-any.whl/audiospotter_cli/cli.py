import click
from audiospotter_cli.client import OrganizationClient
from audiospotter_cli.utils import (
    upload_file,
    get_files_by_extensions,
    get_config,
    put_config,
)
from audiospotter_cli.sources import select_source
from audiospotter_cli.config import return_client_or_configure
from rich.console import Console
from rich.prompt import Confirm
from rich.progress import track
import hashlib

console = Console()

@click.group()
def run():
    pass


@run.command()
@click.argument("path", default=".")
@click.option("--extensions", default="flac,mp3")
@click.option("--omit-duplicates", default=True)
def upload(path, extensions, omit_duplicates):
    """Upload a directory to your project's source bucket."""

    console.print("Finding file source ...")
    client = return_client_or_configure()

    file_source_id = select_source(client)
    # console.print(file_source_id)

    console.print("Parsing the file path ...")
    console.print(f"{path}")
    extensions = extensions.split(",")
    dir_list = get_files_by_extensions(path, extensions)

    # prints all files
    console.print(dir_list)

    if not Confirm.ask("Are you sure you want to upload these files?"):
        console.print("Upload cancelled.")
        exit()

    duplicates_skipped = 0
    files_uploaded = 0

    for file_name in track(dir_list, description="Uploading..."):
        checksum = hashlib.md5(open(file_name, "rb").read()).hexdigest()
        response = client.get_signed_path(
            file_source_id, path=file_name, checksum=checksum
        )
        data = response.json()
        # console.print(data)
        if data["checksum_exists_in_project"]:
            # console.print("Checksum already exists!")
            if omit_duplicates:
                duplicates_skipped = duplicates_skipped + 1
                continue

        presigned_url = data["url"]
        presigned_fields = data["fields"]
        response = upload_file(presigned_url, presigned_fields, f"{path}/{file_name}")

        response = client.ingest_file_source(
            file_source_id, path=file_name, checksum=checksum
        )

        files_uploaded = files_uploaded + 1

    console.print(f"Files uploaded: {files_uploaded}")
    if duplicates_skipped > 0:
        console.print(f"Duplicates skipped: {duplicates_skipped}")


@run.command()
def connect():
    """Verify the connection to the AudioSpotter API."""
    client = return_client_or_configure()
    response = client.get_organization()
    console.print(response.json())


@run.command()
def configure():
    """Configure your credentials to the AudioSpotter API."""
    client = return_client_or_configure()
    response = client.get_organization()
    console.print(response.json())


if __name__ == "__main__":
    run()
