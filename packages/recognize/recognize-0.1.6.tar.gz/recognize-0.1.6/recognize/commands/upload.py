import asyncio
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .lib.client import DataAPI
from .lib.helpers import find_files

short_help_description = "Commands that allow you to upload to files and folders into the S3 bucket for analysis."
help_description = "Commands that allow you to upload to files and folders into the S3 bucket for analysis."
app = typer.Typer(help=help_description, short_help=short_help_description)


@app.command()
def directory(
        path: Annotated[Path, typer.Argument()],
        dev: Annotated[bool, typer.Option("--dev")] = False,
        url: Annotated[Optional[str], typer.Option()] = None
):
    """
    Uploads all files of types mp4, and mov from a given directory. In the future we will handle: png, jpeg

    :param url: URL override for the API.
    :param path: The directory path from which files will be retrieved and uploaded.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: None
    """
    api = DataAPI(dev=dev, url=url)
    files = find_files(path)
    asyncio.run(api.upload_files(path.absolute().name, files))

#
# @app.command()
# def url(
#         dev: Annotated[bool, typer.Option("--dev")] = False,
#         url: Annotated[Optional[str], typer.Option()] = None
# ):
#     """
#     Gets the upload url of the S3 bucket to upload the videos in.
#
#     :param url: URL override for the API.
#     :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
#     :return: None
#     """
#     api = DataAPI(dev=dev)
#     data = api.get_upload_url()
#     print(f"Upload URL: {data.get('message')}")
