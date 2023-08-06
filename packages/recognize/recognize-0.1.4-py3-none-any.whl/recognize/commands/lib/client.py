import asyncio
import os
from pathlib import Path
from typing import List, IO, Generator
from urllib.parse import urljoin

import httpx
import rich

from .entries import LabelEntryType
from .helpers import upload_file


class DataAPI:
    def __init__(self):
        self.url = os.getenv("ML_API_URL", "https://xxihhslish.execute-api.eu-west-2.amazonaws.com/prod/")

    def keyword_search(self, keywords: List[str], output_file: Path, response_type: str):
        url = urljoin(self.url, "search/")

        with httpx.stream("GET", url, params={
            "keywords": ",".join(keywords),
            "response_type": response_type
        }) as response, \
                open(output_file, "wb") as output:
            self._process_response(output, response)

    def entry_search(self, entry: LabelEntryType, output_file: Path, response_type: str):
        url = urljoin(self.url, "search/")

        with httpx.stream("GET", url, params={
            "entry_type": entry.value,
            "response_type": response_type
        }) as response, \
                open(output_file, "wb") as output:
            self._process_response(output, response)

    def faces_search(self, image: IO[bytes], output_file: Path, response_type: str):
        files = {'file': (image.name, image)}
        url = urljoin(self.url, "search/faces/")

        with httpx.stream("POST", url, params={
            "response_type": response_type
        }, files=files) as response, \
                open(output_file, "wb") as output:
            self._process_response(output, response)

    async def upload_files(self, base_path, file_paths: Generator[str, None, None], max_concurrent_uploads: int = 50) -> None:
        """Upload files concurrently to a given URL."""
        url = urljoin(self.url, f"upload/{base_path}")
        semaphore = asyncio.Semaphore(max_concurrent_uploads)

        tasks = [upload_file(semaphore, file_path, url) for file_path in file_paths]

        with rich.progress.Progress(
                "[progress.percentage]{task.percentage:>3.0f}%",
                rich.progress.BarColumn(bar_width=None),
                rich.progress.MofNCompleteColumn(),
                rich.progress.TimeRemainingColumn(),
        ) as progress:
            download_task = progress.add_task(description="Uploading files...", total=len(tasks))

            for task in asyncio.as_completed(tasks):
                path, success = await task
                progress.console.print(f"{'[bold blue]Uploaded' if success else '[bold red]Failed'}: {path}")
                progress.update(download_task, advance=1)

    @staticmethod
    def _process_response(output, response):
        total = int(response.headers.get("Content-Length"))

        with rich.progress.Progress(
                "[progress.percentage]{task.percentage:>3.0f}%",
                rich.progress.BarColumn(bar_width=None),
                rich.progress.DownloadColumn(),
                rich.progress.TransferSpeedColumn(),
        ) as progress:
            download_task = progress.add_task("Download", total=total)

            for chunk in response.iter_bytes():
                output.write(chunk)
                progress.update(download_task, completed=response.num_bytes_downloaded)
