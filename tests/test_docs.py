#!/usr/bin/env python

"""Tests for `eunomia` package."""

import unittest

import eunomia


class TestDocs(unittest.TestCase):
    def test_loadDocs(self):
        extensions = ["csv", "txt", "md", "pdf"]
        test_results = [
            ["name:", "description:"],
            ["thermospheric", "models."],
            ["Mehrad", "Ansari."],
            ["bioRxiv", "preprint"],
        ]
        for i, e in enumerate(extensions):
            test_file_name = f"test_files/test_docs.{e}"
            docs_processor = eunomia.LoadDoc(file_name=test_file_name, encoding="utf8", csv_args={
                "delimiter": ","})
            doc_pages = docs_processor.process(
                filter_words=[
                    "references ",
                    "acknowledgement",
                    "acknowledgments",
                    "references\n",
                ],
                chunk_size=1000,
                chunk_overlap=20,
                chunking_type="fixed-size",
            )
            assert (
                doc_pages[-1].page_content.split()[-2:] == test_results[i]
            ), f"Test fails for {e} file extension."

        # testing for text_input
        with open("test_files/test_docs.txt", "rb") as f:
            text_input = f.read()
        docs_processor = eunomia.LoadDoc(text_input=text_input, encoding="utf8")
        doc_pages = docs_processor.process(
            filter_words=[
                "references ",
                "acknowledgement",
                "acknowledgments",
                "references\n",
            ],
            chunk_size=1000,
            chunk_overlap=20,
            chunking_type="fixed-size",
        )
        assert (
            doc_pages[-1].page_content.split()[-2:] == test_results[1]
        ), "Test fails for text_input."


if __name__ == "__main__":
    unittest.main()
