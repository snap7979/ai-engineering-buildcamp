from typing import Any


class SearchIndexTools:

    def __init__(self, index: Any):
        self.index = index

    def search(self, query: str):
        """
        Search the documentation database for relevant results.

        Args:
            query: The search query to look up in the index.
        """
        return self.index.search(
            query=query,
            num_results=5
        )

    def add_entry(
        self,
        filename: str,
        title: str,
        description: str,
        content: str
    ):
        """
        Add a new documentation entry to the index.

        Args:
            filename: The source filename associated with the entry.
            title: The title of the documentation entry.
            description: A short description summarizing the entry.
            content: The full content of the documentation entry.
        """
        entry = {
            "start": 0,
            "content": content,
            "title": title,
            "description": description,
            "filename": filename,
        }

        self.index.append(entry)

        return "OK"