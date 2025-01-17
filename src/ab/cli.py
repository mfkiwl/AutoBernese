"""
Command-line interface

"""
import logging
import pathlib
import json
from typing import Any

import click
from rich import print

from ab import (
    configuration,
    bsw,
    organiser,
)
from ab.data import (
    ftp,
    http,
)
from ab.station import (
    sitelog,
    sta,
)

log = logging.getLogger(__name__)


@click.group
def main() -> None:
    """
    Root command group for subsequent groups and actions.

    """


@main.command
def env() -> None:
    """
    Show BSW environment loaded into autobernese configuration

    """
    print(configuration.load().get("bsw_env"))


@main.command
def config() -> None:
    """
    Show configuration

    """
    print(configuration.load())


@main.command
@click.argument("filename", type=pathlib.Path)
def parse_sitelog(filename: pathlib.Path) -> None:
    """
    Parse sitelog and print it to the screen

    """
    print(json.dumps(sitelog.Sitelog(filename).sections_extracted, indent=2))


@main.command
# @click.argument("sitelog_filenames", type=list[pathlib.Path])
# @click.argument("individually_calibrated", type=list[str])
# @click.argument("filename", type=pathlib.Path)
def sitelogs2sta(
    # sitelog_filenames: list[pathlib.Path],
    # individually_calibrated: list[str],
    # filename: pathlib.Path,
) -> None:
    """
    Create STA file from sitelogs

    """
    sta.create_sta_file_from_sitelogs(**configuration.load().get("station"))


@main.command
def download_sources() -> None:
    """
    Download sources based on campaign configuration file.

    So far a source entry is assumed to be a Source instance.

    """
    sources = configuration.load().get("data").get("sources")
    for source in sources:
        msg = f"Download source: {source.name}"
        print(msg)
        log.debug(msg)
        match source.protocol:
            case "ftp":
                ftp.download(source)
            case "http" | "https":
                http.download(source)
    else:
        msg = "Finished downloading sources"
        print(msg)
        log.debug(msg)


@main.command
def logfile() -> None:
    """
    Follow log file (run `tail -f path/to/logfile.log`).

    """
    filename = configuration.load().get("environment").get("logging").get("filename")
    import subprocess as sub

    try:
        log.debug(f"Show log tail ...")
        process = sub.Popen(["/usr/bin/tail", "-f", f"{filename}"])
        process.wait()

    except KeyboardInterrupt:
        log.debug(f"Log tail finished ...")

    finally:
        process.terminate()
        process.kill()


@main.group
def campaign() -> None:
    """
    Command group for campaign-specific actions.

    """


@campaign.command
def get_list() -> None:
    """
    List campaigns

    """
    log.debug("List campaigns ...")
    from ab import campaign

    print(campaign.get_list())


@campaign.command
def create() -> None:
    """
    Create campaign

    """
    log.debug("Create campaign ...")
    bsw.create_campaign()


# @main.command
# def prepare_campaign_data(*args: list[Any], **kwargs: dict[Any, Any]) -> None:
#     """
#     Organises campaign data

#     """
#     organiser.prepare_campaign_data(*args, **kwargs)


@main.group(invoke_without_command=True)
def bpe() -> None:
    """
    Tools for the Bernese Processing Engine [BPE].

    """
    print("BPE")


@bpe.command
def recipes() -> None:
    """
    Show the recipes for the active campaign.

    """
    # active = state.active_campaign()
    for recipe in bpe.get_recipes():
        print(recipe)


@bpe.command
def run(**bpe_settings: dict[Any, Any]) -> None:
    """
    Run Bernese Processing Engine [BPE].

    """
    # bsw.runbpe(bpe_settings)
    bsw.runbpe()


# @main.command
# def prepare_end_products(*args: list[Any], **kwargs: dict[Any, Any]) -> None:
#     """
#     Organises campaign end products.

#     """
#     organiser.prepare_end_products(*args, **kwargs)


# @main.command
# def submit_end_products(*args: list[Any], **kwargs: dict[Any, Any]) -> None:
#     """
#     Submits campaign end products.

#     """
#     organiser.submit_end_products(*args, **kwargs)
