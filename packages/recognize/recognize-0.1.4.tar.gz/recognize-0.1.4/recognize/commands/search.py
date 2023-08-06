from pathlib import Path
from typing import List

import typer
from typing_extensions import Annotated

from .lib.client import DataAPI
from .lib.entries import LabelEntryType

short_help_description = "Commands that allow you to search through analysed content."
app = typer.Typer(help=short_help_description, short_help=short_help_description)
api = DataAPI()


@app.command()
def keywords(
        words: Annotated[List[str], typer.Argument()],
        output: Annotated[Path, typer.Option()],
        json: Annotated[bool, typer.Option("--json")] = False
):
    """
    Execute a keyword search.

    :param words: A list of keywords to search for.
    :param output: The output path where the search results will be stored.
    :param json: An optional flag indicating whether the output should be in JSON format. If False, the output is CSV.
    :return: The result of the search operation.
    """
    return api.keyword_search(words, output, response_type="csv" if not json else "json")


@app.command()
def entry(
        entry_type: Annotated[LabelEntryType, typer.Argument()],
        output: Annotated[Path, typer.Option()],
        json: Annotated[bool, typer.Option("--json")] = False
):
    """
    Execute a search for entries of a specific type.

    :param entry_type: The type of entries to search for.
    :param output: The output path where the search results will be stored.
    :param json: An optional flag indicating whether the output should be in JSON format. If False, the output is CSV.
    :return: The result of the search operation.
    """
    return api.entry_search(entry_type, output, response_type="csv" if not json else "json")


@app.command()
def faces(
        image_file: Annotated[Path, typer.Argument()],
        output: Annotated[Path, typer.Option()],
        json: Annotated[bool, typer.Option("--json")] = False
):
    """
    Execute a face search using a provided image file.

    :param image_file: The path to the image file that will be used for the face search.
    :param output: The output path where the search results will be stored.
    :param json: An optional flag indicating whether the output should be in JSON format. If False, the output is CSV.
    :return: The result of the search operation.
    """
    with open(image_file, 'rb') as fp:
        return api.faces_search(fp, output, response_type="csv" if not json else "json")
