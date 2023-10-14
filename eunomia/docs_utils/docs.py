from langchain.schema import Document
from typing import List, Optional
from copy import deepcopy


class LoadDoc:
    """
    A class to handle the loading and processing of different Docs.

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

    def __init__(self, file_name: str = None, text_input: str = None, **kwargs):
        """
        Parameters:
        file_name : str
            Path to file.
        text_input : str
            Direct text input.
        **kwargs are passed to the CSVLoader class.
        """
        if file_name is None and text_input is None:
            raise ValueError("Either 'file_name' or 'text_input' must be provided.")
        elif file_name and text_input:
            raise ValueError(
                "Only one of 'file_name' or 'text_input' should be provided as input."
            )

        if file_name:
            extension = file_name.split(".")[-1].lower()
            self._check_extension(extension)
            self.doc_path = file_name
            if self.type == "pdf":
                from langchain.document_loaders import PyPDFLoader

                self.loader = PyPDFLoader(file_name)
            if self.type == "md":
                from langchain.document_loaders import UnstructuredMarkdownLoader

                self.loader = UnstructuredMarkdownLoader(file_name)
            if self.type == "csv":
                from langchain.document_loaders.csv_loader import CSVLoader

                self.loader = CSVLoader(file_name, **kwargs)
            if self.type == "txt":
                from langchain.document_loaders import TextLoader

                self.loader = TextLoader(file_name)
            self.pages = self.loader.load_and_split()
        else:
            self.pages = [
                Document(page_content=text_input, metadata={"source": "local"})
            ]

    def _check_extension(self, extension: str):
        """
        Checks the provided file extension against the supported extensions.

        Parameters:
        extension : str
            File extension to check.

        Raises:
        Exception:
            If the file extension is not supported.
        NotImplementedError:
            If the file extension is 'xml', which is not yet implemented.
        """
        supported_extensions = {"pdf", "txt", "md", "csv"}
        if extension in supported_extensions:
            self.type = extension
        elif extension == "xml":
            raise NotImplementedError
        else:
            raise Exception(f"Eunomia supports {supported_extensions} doc files.")

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
        use this if you wish to remove "Acknowledgments or "References"
        in a long research article.

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
        filter_words: List[str] = [],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = 0,
        chunking_type="fixed-size",
    ) -> List[Document]:
        """
        Process the document pages based on the search strings. Additionally, this function
        will split the document into chunks if a chunk size is provided.

        Parameters:
        filter_words : List[str]
            List of words to search and filter.
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
        sliced_pages = self.filter_documents(self.pages, filter_words)
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
