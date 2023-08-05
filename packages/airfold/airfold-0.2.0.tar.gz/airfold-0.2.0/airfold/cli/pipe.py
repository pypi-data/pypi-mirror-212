#!/usr/bin/env python3

from pathlib import Path

import typer
import yaml
from rich.traceback import install

from airfold.config import Profile, load_profile
from airfold.context import Airfold, AirfoldContext
from airfold.format import normalize_format, is_source
from airfold.log import log

install()


app = typer.Typer()


@app.command()
def push(path: str, profile: str = "") -> None:
    """Push an object, defined by path, through the runtime.

    Args:
        path: path to the object definition
        profile: Airfold profile to use, use default if empty

    """
    # path = Path("../../test/e2e/pipes/pipe.yaml")
    # path = Path("../../test/e2e/sources/kv.yaml")
    prof: Profile = load_profile(profile)

    log.info(f"Parsing: {path}")

    name: str = Path(path).stem
    log.info(f"Name: {name}")

    log.info(f"Loading data: {path}")
    data: dict = yaml.safe_load(open(path))

    af: AirfoldContext
    with Airfold(prof) as af:
        new_data: dict = normalize_format(data)
        if is_source(new_data):
            return af.push_source(new_data, name)
        elif new_data["type"] == "Pipe":
            return af.push_pipe(new_data, name)

        raise ValueError("Invalid input file")


if __name__ == "__main__":
    app()
