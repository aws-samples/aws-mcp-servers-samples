import os
import asyncio
import json
from opensearchpy import OpenSearch, exceptions

class OpenSearchClient:
    def __init__(
            self,
            opensearch_host: str,
            opensearch_port: int,
            index_name: str,
            username: str = None,
            password: str = None,
            http_compress: bool = True,
            use_ssl: bool = True,
            verify_certs: bool = True,
            ssl_assert_hostname: bool = True,
            ssl_show_warn: bool = True
    ):
        self._index_name = index_name
        self._host = opensearch_host
        self._port = opensearch_port
        
        # Authentication configuration
        http_auth = None
        if username and password:
            http_auth = (username, password)
        
        # Initialize OpenSearch client
        self._client = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': opensearch_port}],
            http_compress=http_compress,
            http_auth=http_auth,
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            ssl_assert_hostname=ssl_assert_hostname,
            ssl_show_warn=ssl_show_warn
        )

    def get_client(self) -> OpenSearch:
        """Get the underlying OpenSearch client instance."""
        return self._client


    async def search_documents(self, query: str, size: int = 10) -> dict:
        """
        Find documents in the OpenSearch index.

        Args:
            query: The query to use for the search
            size: Maximum number of results to return

        Returns:
            A dictionary containing search results or error information
        """
        try:
            # Check if index exists
            index_exists = self._client.indices.exists(index=self._index_name)
            if not index_exists:
                return {"status": "error", "message": f"Index {self._index_name} does not exist", "results": []}

            # Execute search
            search_results = self._client.search(
                body=query,
                index=self._index_name,
                size=size
            )

            return {"status": "success", "results": search_results}

        except exceptions.ConnectionError as e:
            return {"status": "error", "message": f"Connection error: {str(e)}", "results": []}
        except exceptions.RequestError as e:
            return {"status": "error", "message": f"Invalid query: {str(e)}", "results": []}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}", "results": []}

    async def write_document(self, document_id: str, document: dict) -> dict:
        """
        Write a document to the OpenSearch index.

        Args:
            document_id: The ID for the document
            document: The document to write

        Returns:
            A dictionary containing the response or error information
        """
        try:
            # Create the index if it doesn't exist
            index_exists = self._client.indices.exists(index=self._index_name)
            if not index_exists:
                self._client.indices.create(index=self._index_name)

            # Write the document
            response = self._client.index(
                index=self._index_name,
                id=document_id,
                body=document,
                refresh=True  # Make the document immediately available for search
            )

            return {"status": "success", "response": response}

        except exceptions.ConnectionError as e:
            return {"status": "error", "message": f"Connection error: {str(e)}"}
        except exceptions.RequestError as e:
            return {"status": "error", "message": f"Invalid document: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}
            
    async def index_document(self, document: dict) -> dict:
        """
        Index a document without specifying an ID (OpenSearch will generate one).
        
        Args:
            document: The document to index
            
        Returns:
            A dictionary containing the response or error information
        """
        try:
            # Create the index if it doesn't exist
            index_exists = self._client.indices.exists(index=self._index_name)
            if not index_exists:
                self._client.indices.create(index=self._index_name)
                
            # Index without ID (OpenSearch will generate one)
            response = self._client.index(
                index=self._index_name,
                body=document,
                refresh=True  # Make the document immediately available for search
            )
            
            return {"status": "success", "response": response}
            
        except exceptions.ConnectionError as e:
            return {"status": "error", "message": f"Connection error: {str(e)}"}
        except exceptions.RequestError as e:
            return {"status": "error", "message": f"Invalid document: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

    async def delete_document(self, document_id: str) -> dict:
        """
        Delete a document from the OpenSearch index.

        Args:
            document_id: The ID of the document to delete

        Returns:
            A dictionary containing the response or error information
        """
        try:
            # Check if index exists
            index_exists = self._client.indices.exists(index=self._index_name)
            if not index_exists:
                return {"status": "error", "message": f"Index {self._index_name} does not exist"}

            # Delete the document
            response = self._client.delete(
                index=self._index_name,
                id=document_id,
                refresh=True
            )

            return {"status": "success", "response": response}

        except exceptions.NotFoundError:
            return {"status": "error", "message": f"Document with ID {document_id} not found"}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}



