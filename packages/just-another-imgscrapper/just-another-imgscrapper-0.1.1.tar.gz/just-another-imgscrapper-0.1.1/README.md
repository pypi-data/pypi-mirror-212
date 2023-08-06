# just-another-imgscrapper
![](https://github.com/deshrit/just-another-imgscrapper/actions/workflows/tests.yml/badge.svg)

A utility for scrapping images from a HTML doc.

Uses `asyncio` for fast concurrent download.

## Installation
```bash
$ pip install just-another-imgscrapper
```
## Usage
### 1. From cli
```bash
$ imgscrapper -h
```
To get HTML doc, extract image links from `src` attribute of `<img>` tags and download.
```
$ imgscrapper "http://foo.com/bar"
[2023-06-06 23:22:56] imgscrapper.utils:INFO: ### Initializing Scrapping ###
[2023-06-06 23:23:01] imgscrapper.utils:INFO: ### Downloaded 41 images out of extracted 41 links ###
```
Downloads to `imgs/` dir in working dir. If dir does not exists, creates.

### 2. From module
```python
>>> from imgscrapper import ImgScrapper
>>> d = ImgScrapper()
>>> d.download("http://foo.com/bar") 
>>> 3
```
Specify path to store downloaded images.
```python
>>> d = ImgScrapper()
>>> d.url = "http://foo.com/bar"
>>> d.path = "/path/download"
>>> d.download() # returns no. of successful downloads
>>> 3
```
Some servers will block the scrapping, respect robots.txt and only used in allowed hosts.

You can add request headers.
```python
>>> ...
>>> d.request_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'DNT': '1',
    }
>>> ...
```
You can specifically select specific type of `img` tags by specfying attribute of HTML element.
```html
<!-- >http://helloworld.com<-->
<html>
    <body>
        <img src="https://foo.com/bar.png" class="apple ball">
        <img src="/foo.jpg" class="cat bar">
    </body>
<html>
```
To select only images with `class: cat`
```python
>>> d = ImgScrapper()
>>> d.url = "http://helloworld.com"
>>> d.attrs = {
    'class': 'cat',
    }
>>> d.download()
>>> 1 # http://helloworld.com/foo.jpg
```
The downloader gives unique `uuid` to downloaded images preserving the image extension.
```python
>>> d = ImgScrapper(
    url = "http://helloworld.com",
    attrs = {'class': 'cat'},
    max = 5,
    path = "/home/images"
)
>>> d.download()
>>> 5
```
You can limit no. of image downloads by `max` value.

## Liscense
`just-another-imgscrapper` is released under the MIT liscense. See LISCENSE for details.

## Contact
Follow me on twitter ![@deshritbaral](https://twitter.com/deshritbaral)
