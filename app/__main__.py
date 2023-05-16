#!/usr/bin/env python3
import click

from app.desk_assistance.app import App


@click.command()
def main():
    app = App.create()
    app.run()


if __name__ == '__main__':
    main()
