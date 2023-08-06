import click
from click import Path

from .run import Run


@click.command()
@click.option("-s", type=str or Path(exists=False), help="脚本路径")
@click.option("--url", default=None, help="url")
@click.option("--headless", is_flag=True, help="无头/有头模式")
def main(s, url, headless):
    Run.run(s, url, headless=headless)
