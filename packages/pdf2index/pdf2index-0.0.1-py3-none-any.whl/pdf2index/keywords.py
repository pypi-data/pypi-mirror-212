from keybert import KeyBERT
from collections import defaultdict
import re


kw_model = KeyBERT(model="paraphrase-mpnet-base-v2")


def keyex_keybert_single(text: str, **kwargs) -> set[str]:
    del kwargs
    keywords_tuple_list = kw_model.extract_keywords(text, stop_words="english", top_n=15, keyphrase_ngram_range=(1,1))
    return set(keyword_tuple[0] for keyword_tuple in keywords_tuple_list)


def keyex_keybert_double(text: str, **kwargs) -> set[str]:
    del kwargs
    keywords_tuple_list = kw_model.extract_keywords(text, stop_words="english", top_n=5, keyphrase_ngram_range=(2,2))
    return set(keyword_tuple[0] for keyword_tuple in keywords_tuple_list)


def remove_whitespace(text:str) -> str:
    return " ".join(text.split())

def keyex_abbreviations(text: str, **kwargs) -> set[str]:
    del kwargs
    reg = r"(?P<abr>[A-Z]+)\s*\((?P<name>.*?)\)"
    regex = re.compile(reg, re.MULTILINE | re.DOTALL)
    matches = regex.finditer(text)
    keywords = set()
    for match in matches:
        match_dict = match.groupdict()
        abr = match_dict["abr"]
        name = remove_whitespace(match_dict["name"])
        keywords.add(f"{name} ({abr})")
        keywords.add(f"{abr} ({name})")
    return keywords


def keyex_capitalized(text: str, **kwargs) -> set[str]:
    del kwargs
    reg = r"(?P<abr>[A-Z]{2,})"
    regex = re.compile(reg, re.MULTILINE | re.DOTALL)
    matches = regex.finditer(text)
    keywords = set()
    for match in matches:
        match_dict = match.groupdict()
        abr = match_dict["abr"]
        keywords.add(abr)
    return keywords


strategies = [keyex_keybert_single, keyex_keybert_double, keyex_abbreviations, keyex_capitalized]


def extract_keywords_from_text_list(text_list: list[str]) -> dict[str, set[int]]:
    index = defaultdict(set)
    for page_number, page in enumerate(text_list):
        if page_number < 2:
            continue
        for keyword in extract_keywords_from_text(page):
            index[keyword].add(page_number)
    return index


def sanetize(text:str) -> str:
    return text.replace("-", "_")


def extract_keywords_from_text(text: str) -> set[str]:
    keywords = set()
    sanetized_text = sanetize(text)
    for strategy in strategies:
        keywords |= strategy(sanetized_text)
    return keywords
