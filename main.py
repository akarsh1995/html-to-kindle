from ken.the_ken import KenArticle
from pathlib import Path
import pdfkit
from ken.browser import Browser
from ken.process_article import get_document_from_html


if __name__ == "__main__":
    # with Browser() as browser:
    #     k = KenArticle('akarsh.1995.02@gmail.com',
    #                    'Jain_theken@akarsh',
    #                    browser)

    # pdfkit.from_string(get_document_from_html(
    #     k.get_latest_article_source()
    # ).summary(), 'out.pdf')

    text = get_document_from_html(
       Path('/Users/akarshjain/Downloads/theken/Independence, freedom, and incentives - The Ken.htm').read_text()
    ).summary()

    Path('/Users/akarshjain/Downloads/theken/Independence, freedom, and incentives - The Ken_mod.htm').write_text(text)
