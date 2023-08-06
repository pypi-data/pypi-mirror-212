# errors.py

"""
Exception classes for `imgscrapper` module.
"""


class ImgScrapperError(Exception):
    """Base Exception class for Image Scrapper module"""


class InvalidURLError(ImgScrapperError):
    """Exception class for invalid URL of any kind"""


class HTMLDocFetchError(ImgScrapperError):
    """Error fetching HTML response from the URL"""


class NoImgTagError(ImgScrapperError):
    """
    Exception if no image tags found with given search condition
    in the downloaded html markup from the URL.
    """
