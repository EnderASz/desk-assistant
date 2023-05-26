#!/usr/bin/env python3
import asyncio

import click

from desk_assistance.app import App
from desk_assistance.config import AppConfig


@click.command()
def main():
    config = AppConfig()
    app = App.create(config=config)
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
