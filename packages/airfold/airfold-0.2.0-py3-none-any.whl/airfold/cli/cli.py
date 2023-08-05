#!/usr/bin/env python3

import typer
from rich.traceback import install

from airfold.cli.pipe import app as pipe

install()

app = typer.Typer()
app.add_typer(pipe, name="pipe")

if __name__ == "__main__":
    app()
