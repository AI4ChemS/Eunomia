from langchain.text_splitter import CharacterTextSplitter
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
    text_splitter : CharacterTextSplitter
        Instance of CharacterTextSplitter to split the document text.
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
        self.paper_path = path + self.paper_id + '.pdf'
        self.loader = PyPDFLoader(self.paper_path)
        self.pages = self.loader.load_and_split()
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

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
        indices = [lower_text.find(keyword) for keyword in keywords if lower_text.find(keyword) != -1]
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
        return any(search_string.lower() in document.page_content.lower() for search_string in search_strings)

    def filter_documents(self, documents: List[Document], search_strings: List[str]) -> List[Document]:
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
                filtered_documents[i].page_content = self.cut_text(filtered_documents[i].page_content, keywords=search_strings)
                filtered_documents = filtered_documents[:i+1]
                break
        return filtered_documents

    def process(self, search_strings: List[str]):
        """
        Process the document pages based on the search strings.

        Parameters:
        search_strings : List[str]
            List of strings to search for.

        Returns:
        List[Document]
            List of processed document chunks.
        """
        sliced_pages = self.filter_documents(self.pages, search_strings)
        sliced_pages_chunks = self.text_splitter.split_documents(sliced_pages)
        return sliced_pages_chunks
