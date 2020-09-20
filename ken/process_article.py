from readability import Document

def get_document_from_html(html_text: str):
    doc = Document(html_text)
    return doc
