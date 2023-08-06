# imagscrapper.py

"""A utility for scrapping images from a HTML doc from  a URL.
"""

import os
import uuid
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional

import bs4
import httpx
import asyncio
import aiofiles

from .errors import HTMLDocFetchError, InvalidURLError, NoImgTagError


class ImgScrapper:
    """Image Scrapper Class.

    ...

    Attributes
    ----------
    url : str
        HTML document download URL
    attrs : dict
        HTML element attributes
    max : int
        Maximum number of image to scrape
    path : str
        Image download directory

    Methods
    -------
    download(url=None)
        Starts the image downloading process, optionally takes
        HTML document download `url` string if it is not initialized
        with constructor or instance variable and overrides if exists.
    """

    # http request header if you want to specify
    request_header: Optional[Dict[str, str]] = None

    def __init__(
        self,
        url: Optional[str] = None,
        attrs: Optional[dict] = None,
        max: Optional[int] = None,
        path: str = "imgs",  # default download path
    ) -> None:
        self.url = url
        self.attrs = attrs
        self.max = max
        self.path = os.path.join(os.getcwd(), path)

        self.img_urls: List[str] = []
        self.count: int = 0

    def _get_HTML_doc(self) -> Any:
        """Fetches HTML doc from the URL.

        Returns
        -------
        str
            Downloaded HTML document string.
        """

        if self.url is None:
            raise InvalidURLError("Pass valid URL")
        try:
            res = httpx.get(self.url, headers=self.request_header)
            res.raise_for_status()
            if res.status_code >= 200 and res.status_code < 300:
                return res.text
        except httpx.HTTPError as exc:
            raise HTMLDocFetchError(f"HTTP Exception for {exc.request.url} - {exc}")
        raise HTMLDocFetchError(
            f"Error fetching HTML Document from the URL - "
            f"response status {res.status_code}"
        )

    def _get_img_tags(self, html_doc: str) -> bs4.ResultSet:
        """Extracts <img> tags from the fetched HTML doc.

        Parameters
        ----------
        html_doc : str
            HTML document string.

        Returns
        -------
        bs4.ResultSet
            A sequence containing list of <img> tags as strings,
            `beautifulsoup4` result set object to be specific.
        """

        soup = bs4.BeautifulSoup(markup=html_doc, features="lxml")
        img_tags = soup.find_all(name="img", attrs=self.attrs)
        return img_tags

    def _get_img_urls(self) -> None:
        """Extracts image links from <img> tags and stores in
        `img_urls` instance variable.
        """

        parsed_url = urlparse(self.url)
        response_text = self._get_HTML_doc()
        img_tags = self._get_img_tags(response_text)
        if not img_tags:
            raise NoImgTagError("No img tags found with given search parameter")
        for img_tag in img_tags:
            try:
                tmp = str(img_tag["src"])  # <img src="foo/bar.jpg"> => "foo/bar.jpg"
            except KeyError:
                continue

            if tmp.startswith("http"):  # <img src="https://foo.com/bar.jpg">
                self.img_urls.append(tmp)
                continue
            if tmp.startswith("//"):  # <img src="//foo.com/bar.jpg">
                self.img_urls.append(str(parsed_url.scheme) + ":" + tmp)
                continue
            if tmp.startswith("/"):  # <img src="/foo/bar.jpg">
                self.img_urls.append(
                    str(parsed_url.scheme) + "://" + str(parsed_url.netloc) + tmp
                )
                continue
            if tmp.startswith("./"):  # <img src="./bar.jpg">
                self.img_urls.append(
                    str(parsed_url.scheme) + "://" + str(parsed_url.netloc) + tmp[1:]
                )
                continue
            # <img src="bar.jpg">
            self.img_urls.append(
                str(parsed_url.scheme) + "://" + str(parsed_url.netloc) + "/" + tmp
            )

    async def _download_img(self, url: str) -> None:
        """Asynchronous image downloader coroutine.

        Parameters
        ----------
        url : str
            URL of image to download.
        """
        async with httpx.AsyncClient() as client:
            res = await client.get(url=url, headers=self.request_header)
            if res.status_code == 200:
                ext = res.headers["content-type"].split("/")[-1]
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                file_path = os.path.join(self.path, str(uuid.uuid4()) + "." + ext)
                async with aiofiles.open(file_path, "wb") as fp:
                    await fp.write(res.content)
                    self.count += 1

    async def _task_runner(self) -> None:
        """Creates and gathers all concurrent image downloader coroutines."""

        if not self.img_urls:
            self._get_img_urls()
        if self.max:
            self.img_urls = self.img_urls[: self.max]
        tasks = [
            asyncio.create_task(self._download_img(img_url))
            for img_url in self.img_urls
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    def download(self, url: Optional[str] = None) -> int:
        """Starts the image downloading process.

        Parameters
        ----------
        url : str, optional
            HTML document download URL,
            Overrides the URL passed with constructor.

        Returns
        -------
        int
            Total number of successfull image downloads.
        """
        if url is not None:
            self.url = url
        asyncio.run(self._task_runner())
        return self.count
