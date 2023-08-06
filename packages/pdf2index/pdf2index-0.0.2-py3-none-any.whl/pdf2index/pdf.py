from pathlib import Path
from pdfminer.high_level import extract_pages


def get_raw_pages(filepath: Path, password: str):
    page_iter = extract_pages(filepath, password=password)
    pages = [*page_iter]
    return pages


def element_to_text(element):
    text = ""
    try:
        text += element.get_text()
    except:
        pass
    try:
        for child in element:
            text += "🧨"
            text += element_to_text(child)
    except:
        pass
    return text


def page_to_text(page):
    text = element_to_text(page)
    text = text.replace("🧨🧨", "\n")
    text = text.replace("🧨", "")
    text = text.replace("•", "\n")
    return text


def extract_text(filepath: Path, password: str):
    pages = get_raw_pages(filepath, password)
    text_list = [page_to_text(page) for page in pages]
    return text_list
