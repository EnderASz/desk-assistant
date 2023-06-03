#!/usr/bin/env python3
import asyncio

import typer

from desk_assistance.app import App
from desk_assistance.config import AppConfig


cli = typer.Typer()


@cli.command()
def main():
    config = AppConfig()
    app = App.create(config=config)

    async def _app_run():
        async with app:
            await app.run()

    asyncio.run(_app_run())


if __name__ == "__main__":
    cli()
