"""Console script for sqlachemy_cruder."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("sqlachemy_cruder")
    click.echo("=" * len("sqlachemy_cruder"))
    click.echo("provide crud utils")


if __name__ == "__main__":
    main()  # pragma: no cover
