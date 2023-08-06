import typer

from .commands import search, upload

app = typer.Typer()
app.add_typer(search.app, name="search")
app.add_typer(upload.app, name="upload")

if __name__ == "__main__":
    app()
