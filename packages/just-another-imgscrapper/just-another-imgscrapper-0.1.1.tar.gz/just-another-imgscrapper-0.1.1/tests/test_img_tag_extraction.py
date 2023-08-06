import unittest
from unittest.mock import patch

from imgscrapper import ImgScrapper


class TestImgTagExtraction(unittest.TestCase):
    def setUp(self):
        self.scrapper = ImgScrapper()
        self.scrapper.url = "http://imgscrapper.com/"
        self.html_doc = """
        <html>
        <body>
            <h1>Hello World</h1>
            <img src="https://foo.com.np/bar.jpg" alt="type 1">
            <img src="http://foo.com.np/bar.jpg" alt="type 2">
            <img src="//foo.com.np/bar.jpg" alt="type 3">
            <img src="/bar.jpg" alt="type 4">
            <img src="./bar.jpg" alt="type 5">
            <img src="bar.jpg" alt="type 6">
        </body>
        </html>
        """

    def test_total_img_tag_extraction(self):
        expected_output = 6
        output = self.scrapper._get_img_tags(self.html_doc)
        self.assertEqual(len(output), expected_output)

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_img_url_extraction_type_one(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = """
        <html>
        <body>
            <img src="https://foo.com.np/bar.jpg" alt="type 1">
        </body>
        </html>
        """
        self.scrapper._get_img_urls()
        self.assertEqual(self.scrapper.img_urls[0], "https://foo.com.np/bar.jpg")

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_img_url_extraction_type_two(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = """
        <html>
        <body>
            <img src="http://foo.com.np/bar.jpg" alt="type 2">
        </body>
        </html>
        """
        self.scrapper._get_img_urls()
        self.assertEqual(self.scrapper.img_urls[0], "http://foo.com.np/bar.jpg")

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_img_url_extraction_type_three(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = """
        <html>
        <body>
            <img src="//foo.com.np/bar.jpg" alt="type 3">
        </body>
        </html>
        """
        self.scrapper._get_img_urls()
        self.assertEqual(self.scrapper.img_urls[0], "http://foo.com.np/bar.jpg")

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_img_url_extraction_type_four(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = """
        <html>
        <body>
            <img src="/bar.jpg" alt="type 4">
        </body>
        </html>
        """
        self.scrapper._get_img_urls()
        self.assertEqual(self.scrapper.img_urls[0], "http://imgscrapper.com/bar.jpg")

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_img_url_extraction_type_five(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = """
        <html>
        <body>
            <img src="./bar.jpg" alt="type 5">
        </body>
        </html>
        """
        self.scrapper._get_img_urls()
        self.assertEqual(self.scrapper.img_urls[0], "http://imgscrapper.com/bar.jpg")

    @patch("imgscrapper.ImgScrapper._get_HTML_doc")
    def test_img_url_extraction_type_six(self, mock_get_HTML_doc):
        mock_get_HTML_doc.return_value = """
        <html>
        <body>
            <img src="bar.jpg" alt="type 6">
        </body>
        </html>
        """
        self.scrapper._get_img_urls()
        self.assertEqual(self.scrapper.img_urls[0], "http://imgscrapper.com/bar.jpg")


if __name__ == "__main__":
    unittest.main()
