from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from typing import List, Optional
from copy import deepcopy


class LoadDoc:
    """
    A class to handle the loading and processing of documents.

    Attributes:
    paper_id : str
        ID of the paper to be loaded.
    paper_path : str
        Path of the paper to be loaded.
    loader : PyPDFLoader
        Instance of PyPDFLoader to load the document.
    pages : list
        Pages of the loaded document.
    """

    def __init__(self, path: str, paper_id: str):
        """
        Constructs the necessary attributes for the LoadDoc object.

        Parameters:
        path : str
            Base path of the documents.
        paper_id : str
            ID of the paper.
        """
        self.paper_id = paper_id
        self.paper_path = path + self.paper_id + ".pdf"
        self.loader = PyPDFLoader(self.paper_path)
        self.pages = self.loader.load_and_split()

    @staticmethod
    def cut_text(text: str, keywords: List[str]) -> str:
        """
        Cuts the given text up to the first found keyword.

        Parameters:
        text : str
            The text to be cut.
        keywords : List[str]
            List of keywords to find in the text.

        Returns:
        str
            The cut text.
        """
        lower_text = text.lower()
        indices = [
            lower_text.find(keyword)
            for keyword in keywords
            if lower_text.find(keyword) != -1
        ]
        min_index = min(indices)
        return text[:min_index].strip()  # remove any trailing spaces

    @staticmethod
    def find_in_document(document: Document, search_strings: List[str]) -> bool:
        """
        Searches for the given strings in the document content.

        Parameters:
        document : Document
            Document in which to search.
        search_strings : List[str]
            List of strings to search for.

        Returns:
        bool
            True if any of the search strings are found, False otherwise.
        """
        return any(
            search_string.lower() in document.page_content.lower()
            for search_string in search_strings
        )

    def filter_documents(
        self, documents: List[Document], search_strings: List[str]
    ) -> List[Document]:
        """
        Filters documents based on the presence of search strings.

        Parameters:
        documents : List[Document]
            List of documents to filter.
        search_strings : List[str]
            List of strings to search for.

        Returns:
        List[Document]
            List of filtered documents.
        """
        filtered_documents = deepcopy(documents)  # Create a deep copy of documents
        for i, doc in enumerate(filtered_documents):
            if self.find_in_document(doc, search_strings):
                filtered_documents[i].page_content = self.cut_text(
                    filtered_documents[i].page_content,
                    keywords=search_strings,
                )
                filtered_documents = filtered_documents[: i + 1]
                break
        return filtered_documents

    def process(
        self,
        search_strings: List[str],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = 0,
        chunking_type="fixed-size",
    ) -> List[Document]:
        """
        Process the document pages based on the search strings. Additionally, this function
        will split the document into chunks if a chunk size is provided.

        Parameters:
        search_strings : List[str]
            List of strings to search for.
        chunk_size : Optional[int]
            The size of the chunks in which the document will be split. If this parameter
            is not provided, the document will not be split into chunks.
        chunk_overlap : Optional[int]
            The size of the overlap between chunks. If chunk_size is not provided, this
            parameter will not be used.

        Returns:
        List[Document]
            List of processed document chunks.
        """
        sliced_pages = self.filter_documents(self.pages, search_strings)
        text_splitter = None
        if chunk_size is not None:
            if chunking_type == "fixed-size":
                from langchain.text_splitter import (
                    CharacterTextSplitter,
                )

                text_splitter = CharacterTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
            if chunking_type == "latex":
                from langchain.text_splitter import LatexTextSplitter

                text_splitter = LatexTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
            if chunking_type == "NLTK":
                from langchain.text_splitter import NLTKTextSplitter

                text_splitter = NLTKTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
            if chunking_type == "spacy":
                from langchain.text_splitter import SpacyTextSplitter

                text_splitter = SpacyTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )

            sliced_pages = text_splitter.split_documents(sliced_pages)

        return sliced_pages
