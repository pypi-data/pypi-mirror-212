import os
import re
from asyncio import Semaphore
from pathlib import Path
from typing import Generator

import httpx


async def upload_file(semaphore: Semaphore, file_path: str, url: str) -> str:
    """Asynchronously upload a file to a given URL."""
    with open(file_path, 'rb') as fp:
        files = {'file': (fp.name, fp)}

        async with httpx.AsyncClient() as client:
            async with semaphore:
                async with client.stream('POST', url, files=files) as response:
                    response.raise_for_status()  # Ensure we get a 2xx response
                    return file_path


def find_files(filepath: Path) -> Generator[str, None, None]:
    pattern = re.compile(r'\.(jpeg|jpg|png|mp4|mov)$')

    for root, dirs, files in os.walk(filepath.absolute()):
        for file in files:
            lowered = file.lower()

            if re.search(pattern, lowered):
                yield os.path.join(root, file)
