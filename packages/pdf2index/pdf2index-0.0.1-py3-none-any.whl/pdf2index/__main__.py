import typer
from typing_extensions import Annotated
from pathlib import Path
from collections import defaultdict

from pdf2index.pdf import extract_text
from pdf2index.keywords import extract_keywords_from_text_list


app = typer.Typer()


def files_to_text(file_paths: list[Path], password: str):
    return [extract_text(file_path, password=password) for file_path in file_paths]


def get_index_dictionary_per_book(books: list[list[str]]):
    per_book_index_list = []
    for book in books:
        per_book_index_list.append(extract_keywords_from_text_list(book))
    return per_book_index_list


def combine_indices(per_book_index_list: list[dict[str, set[int]]]):
    index = defaultdict(dict)
    for book_id, book_index in enumerate(per_book_index_list):
        for keyword, pages in book_index.items():
            index[keyword][book_id] = pages
    return index


def sort_index(index: dict[str, dict[int, set[int]]]):
    return dict(sorted(index.items(), key=lambda entry: entry[0].lower()))


def create_book_string(book_id: int, pages: set[int]) -> str:
    return f"{book_id + 1}({', '.join(str(page - 1) for page in sorted(pages) if page >= 2)})"


def index_to_text(sorted_index: dict[str, dict[int, set[int]]]):
    index_txt = ""
    for keyword, books in sorted_index.items():
        index_txt += f"{keyword}: {' | '.join(create_book_string(book_id, pages) for book_id, pages in books.items())}\n"
    return index_txt


def save_index(index: str, file_path: Path):
    with open(file_path, "w") as fp:
        fp.write(index)


@app.command()
def main(
    filenames: Annotated[list[Path], typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
    out: Annotated[Path, typer.Option(exists=False, writable=True)],
    password: Annotated[str, typer.Option("--password", "-p")] = "",
):
    books = files_to_text(filenames, password)
    index_dictionary_per_book = get_index_dictionary_per_book(books)
    combined_indices = combine_indices(index_dictionary_per_book)
    sorted_combined_indices = sort_index(combined_indices)
    index_as_text = index_to_text(sorted_combined_indices)
    save_index(index_as_text, out)
