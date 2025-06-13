from typing import Dict, List, Optional, Any, Union
import json
import requests

class EmbeddingTools:
    def __init__(self, aos_client, api_token=None):
        self.aos_client = aos_client
        self.api_token = api_token
        self.embedding_api_url = "https://api.siliconflow.cn/v1/embeddings"
        self.default_model = "Pro/BAAI/bge-m3"
        self.vector_field = "dense_vector"
        self.vector_dimension = 1024

    async def generate_embedding(self, text: str, model: str = None) -> Dict:
        """
        Generate vector embedding for the provided text using Silicon Flow API.

        Args:
            text: The text to convert to a vector embedding
            model: The model to use for embedding (default: Pro/BAAI/bge-m3)

        Returns:
            Dictionary containing the embedding vector or error information
        """
        if not self.api_token:
            return {"status": "error", "message": "API token not configured for embedding service"}

        try:
            model_name = model if model else self.default_model

            payload = {
                "model": model_name,
                "input": text,
                "encoding_format": "float"
            }

            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }

            response = requests.post(self.embedding_api_url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            return {
                "status": "success",
                "embedding": result.get("data", [{}])[0].get("embedding", []),
                "model": model_name
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

    async def bulk_index_with_embeddings(self, documents: List[Dict], text_field: str = "text") -> Dict:
        """
        Generate embeddings for multiple documents and index them in bulk.

        Args:
            documents: List of documents to process and index
            text_field: The field name containing text to embed

        Returns:
            Dictionary containing the bulk operation results
        """
        try:
            processed_docs = []
            failed_docs = []

            for doc in documents:
                if text_field not in doc:
                    failed_docs.append({"doc": doc, "reason": f"Missing text field '{text_field}'"})
                    continue

                # Generate embedding
                embedding_result = await self.generate_embedding(doc[text_field])

                if embedding_result["status"] != "success":
                    failed_docs.append({"doc": doc, "reason": embedding_result["message"]})
                    continue

                # Add embedding to document
                doc_copy = doc.copy()
                doc_copy[self.vector_field] = embedding_result["embedding"]
                processed_docs.append(doc_copy)

            # If no documents were processed successfully
            if not processed_docs:
                return {
                    "status": "error",
                    "message": "No documents were processed successfully",
                    "failed_docs": failed_docs
                }

            # Bulk index the processed documents
            client = self.aos_client.get_client()
            bulk_data = []

            for doc in processed_docs:
                # If document has an ID
                if "_id" in doc:
                    doc_id = doc.pop("_id")
                    bulk_data.append({"index": {"_index": self.aos_client._index_name, "_id": doc_id}})
                else:
                    # Let OpenSearch generate an ID
                    bulk_data.append({"index": {"_index": self.aos_client._index_name}})
                bulk_data.append(doc)

            response = client.bulk(body=bulk_data, refresh=True)

            return {
                "status": "success",
                "response": response,
                "processed_count": len(processed_docs),
                "failed_count": len(failed_docs),
                "failed_docs": failed_docs if failed_docs else None
            }

        except Exception as e:
            return {"status": "error", "message": f"Bulk indexing error: {str(e)}"}

