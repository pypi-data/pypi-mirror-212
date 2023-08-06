# __main__.py

import sys
import argparse

from typing import Optional
from typing import Sequence

from .utils import get_logger
import imgscrapper


# logger
logger = get_logger()


def main(argv: Optional[Sequence[str]] = None) -> int:
    """This function runs when module is envoked from the cli."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url",
        help="URL link to scrape images from "
        '(provide in quotes "" to avoid shell '
        "special keywords conflict)",
    )
    parser.add_argument(
        "-c",
        metavar="CLASS",
        action="append",
        default=[],
        help="HTML class attribute - chain to add multiple classes",
    )
    parser.add_argument(
        "-a",
        "--attr",
        action="append",
        default=[],
        help="Used as `imgscrapper -a 'id' -a 'test' {url}` selects "
        "<img src='foo.jpg' id='test'> ,can be further chained for "
        "more but first is the unique attribute",
    )
    parser.add_argument("-p", "--path", help="Image download directory")
    parser.add_argument(
        "-m", "--max", type=int, help="Maximum number of images to download"
    )
    args = parser.parse_args(argv)

    try:
        scrapper = imgscrapper.ImgScrapper()
        scrapper.url = args.url

        attrs = {}
        if args.c:
            attrs["class"] = " ".join(args.c)
            scrapper.attrs = attrs

        if args.attr:
            key = args.attr[0]
            value = " ".join(args.attr[1:])
            attrs[key] = value
            scrapper.attrs = attrs

        if args.path:
            scrapper.path = args.path

        if args.max:
            scrapper.max = args.max

        logger.info("### Initializing Scrapping ###")
        count = scrapper.download()
        logger.info(
            f"### Downloaded {count} images out of extracted "
            f"{len(scrapper.img_urls)} links ###"
        )

    except Exception as e:
        logger.error(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
