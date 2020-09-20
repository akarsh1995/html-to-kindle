from pathlib import Path
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import requests
from urllib.parse import urlparse, urljoin
from base64 import b64encode
from html.parser import HTMLParser
from dataclasses import dataclass


class Browser(webdriver.WebDriver):
    def wait_and_find_elem(self, xpath) -> WebElement:
        elem = WebDriverWait(self, 5).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
        return elem


@dataclass
class ImageSrcUrl:
    src: str
    domain: str

    def __post_init__(self):
        self._parsed_url = urlparse(urljoin(self.domain, self.src))

    @property
    def image_path(self):
        return Path(self._parsed_url.path)

    @property
    def image_name(self):
        return self.image_path.name

    def download_image(self):
        response = requests.get(self._parsed_url.geturl())
        if response.ok:
            return response.content
        return ""

    @property
    def base_64_image(self):
        return "data:image/jpeg;base64," + b64encode(self.download_image()).decode(
            "utf-8"
        )


class Parser(HTMLParser):
    def __init__(self, domain: str, *args, **kwargs):
        self.image_srcs = []
        self.domain = domain
        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    src_obj = ImageSrcUrl(attr[1], self.domain)
                    self.image_srcs.append(src_obj)

    def get_image_src_base64_map(self):
        mapping = {}
        for image_src_obj in self.image_srcs:
            mapping[image_src_obj.src] = image_src_obj.base_64_image
        return mapping


def main():
    with Browser() as b:
        url = "https://www.google.com"
        parse_url = urlparse(url)
        print(parse_url.hostname)
        b.get(url)
        html_parser = Parser(domain=url)
        html_parser.feed(b.page_source)
        new_html = b.page_source
        images_map = html_parser.get_image_src_base64_map()
        for src, base64image in images_map.items():
            new_html = new_html.replace(src, base64image)
        import pdb

        pdb.set_trace()


if __name__ == "__main__":
    main()
