import unittest
from unittest.mock import patch, MagicMock

from imgscrapper import ImgScrapper


class TestGetHTMLDoc(unittest.TestCase):
    def setUp(self):
        self.scrapper = ImgScrapper()
        self.scrapper.url = "http://imgscrapper.com"

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_get_HTML_doc(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = (
            "<html><body><img src='foo.png' alt='image'></body></html>"
        )
        self.assertEqual(
            self.scrapper._get_HTML_doc(),
            "<html><body><img src='foo.png' alt='image'></body></html>",
        )

    @patch("imgscrapper.imgscrapper.httpx")
    def test_httx_response(self, mock_httpx):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><img src='foo.png'></body></html>"
        mock_httpx.get.return_value = mock_response
        self.assertEqual(
            self.scrapper._get_HTML_doc(),
            "<html><body><img src='foo.png'></body></html>",
        )


if __name__ == "__main__":
    unittest.main()
