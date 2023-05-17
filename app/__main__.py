#!/usr/bin/env python3
import click

from app.desk_assistance.app import App
from app.desk_assistance.config import AppConfig


@click.command()
def main():
    config = AppConfig()
    app = App.create(config=config, plugins=[])
    app.run()


if __name__ == "__main__":
    main()
