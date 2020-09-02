import logging

import click
import click_log

from tools_impl import Tools

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option()
def cli():
    pass


@cli.command(name='show-passed-situations')
def show_passed_situations():
    tools = Tools().passed_situations()
    logger.info(tools)


if __name__ == '__main__':
    cli()
