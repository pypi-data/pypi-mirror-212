# __init__.py

__version__ = "0.1.1"

from .imgscrapper import ImgScrapper

from .errors import (
    ImgScrapperError,
    InvalidURLError,
    HTMLDocFetchError,
    NoImgTagError,
)
