import os

import pytest

from langchain.text_splitter import RecursiveCharacterTextSplitter
from personal_pdf_assistant.preprocess import (
    config_text_splitter,
    get_pdf_embeddings,
    preprocess_pdf,
    preprocess_pdf_from_directory,
)

"""
Tests generated by Co pilot
Need to review
"""


@pytest.fixture
def pdf_path():
    return os.path.join(os.path.dirname(__file__), "test_files", "test.pdf")


@pytest.fixture
def dir_path():
    return os.path.join(os.path.dirname(__file__), "test_files")


@pytest.fixture
def text_splitter():
    return config_text_splitter()


def test_config_text_splitter(text_splitter):
    assert isinstance(text_splitter, RecursiveCharacterTextSplitter)


def test_preprocess_pdf(pdf_path, text_splitter):
    pages = preprocess_pdf(pdf_path, text_splitter)
    assert len(pages) == 1
    assert pages[0].page_number == 1  # type: ignore
    assert pages[0].page_content.startswith("This is a test PDF file.")


def test_preprocess_pdf_from_directory(dir_path, text_splitter):
    pages = preprocess_pdf_from_directory(text_splitter, dir_path)
    assert len(pages) == 1
    assert pages[0].page_number == 1  # type: ignore
    assert pages[0].page_content.startswith("This is a test PDF file.")


def test_get_pdf_embeddings(pdf_path, text_splitter):
    pages = preprocess_pdf(pdf_path, text_splitter)
    embeddings = get_pdf_embeddings(pages)
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 768