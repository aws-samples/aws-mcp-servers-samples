from lambda_mcp.lambda_mcp import LambdaMCPServer
import os
import json
from typing import Dict, List, Optional, Any
from common.aos_client import OpenSearchClient
import requests

# Get configuration from environment variables
opensearch_host = os.environ.get('OPENSEARCH_HOST', '')
opensearch_port = int(os.environ.get('OPENSEARCH_PORT', '443'))
opensearch_index = os.environ.get('OPENSEARCH_INDEX', 'default')
opensearch_username = os.environ.get('OPENSEARCH_USERNAME', '')
opensearch_password = os.environ.get('OPENSEARCH_PASSWORD', '')
embedding_api_token = os.environ.get('EMBEDDING_API_TOKEN', '')
session_table = os.environ.get('MCP_SESSION_TABLE', 'mcp_sessions')

# Create the MCP server instance
mcp_server = LambdaMCPServer(name="aos-mcp-lambda-server", version="1.0.0", session_table=session_table)

# Initialize OpenSearch client
aos_client = OpenSearchClient(
    opensearch_host=opensearch_host,
    opensearch_port=opensearch_port,
    index_name=opensearch_index,
    username=opensearch_username,
    password=opensearch_password,
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=True
)

# Embedding configuration
EMBEDDING_API_URL = "https://api.siliconflow.cn/v1/embeddings"
DEFAULT_MODEL = "Pro/BAAI/bge-m3"
VECTOR_FIELD = "dense_vector"
VECTOR_DIMENSION = 1024


async def generate_embedding(text: str, model: str = None) -> Dict:
    """Generate vector embedding for the provided text using Silicon Flow API."""
    if not embedding_api_token:
        return {"status": "error", "message": "API token not configured for embedding service"}

    try:
        model_name = model if model else DEFAULT_MODEL

        payload = {
            "model": model_name,
            "input": text,
            "encoding_format": "float"
        }

        headers = {
            "Authorization": f"Bearer {embedding_api_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(EMBEDDING_API_URL, json=payload, headers=headers)
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


async def knn_search(vector: List[float], k: int = 10) -> Dict:
    """Perform k-nearest neighbors search using a vector."""
    try:
        # Validate vector dimension
        if len(vector) != VECTOR_DIMENSION:
            return {
                "status": "error",
                "message": f"Vector dimension mismatch. Expected {VECTOR_DIMENSION}, got {len(vector)}"
            }

        # Construct kNN query
        query = {
            "size": k,
            "query": {
                "knn": {
                    VECTOR_FIELD: {
                        "vector": vector,
                        "k": k
                    }
                }
            },
            "_source": {
                "excludes": [VECTOR_FIELD]  # Always exclude the vector field
            }
        }

        # Execute search
        result = await aos_client.search_documents(json.dumps(query), k)

        # Process results to extract only text content
        if result["status"] == "success" and "results" in result:
            hits = result["results"].get("hits", {}).get("hits", [])
            simplified_results = []

            for hit in hits:
                source = hit.get("_source", {})
                simplified_results.append({
                    "id": hit.get("_id"),
                    "score": hit.get("_score"),
                    "text": source.get("text", ""),
                    "metadata": {k: v for k, v in source.items() if k != "text" and k != VECTOR_FIELD}
                })

            return {
                "status": "success",
                "results": simplified_results,
                "total": len(simplified_results)
            }

        return result

    except Exception as e:
        return {"status": "error", "message": f"kNN search error: {str(e)}"}


@mcp_server.tool()
def index_text_with_embedding(text: str, document_id: str = None, metadata: str = "{}") -> Dict:
    """
    Ingest doc into Knowledge Base by convert text to embedding and then write text and embedding to OpenSearch vector database.

    Args:
        text: The text to convert and index
        document_id: Optional ID for the document (auto-generated if not provided)
        metadata: Optional metadata to store with the document as JSON string

    Returns:
        Dictionary containing the response or error information
    """
    import asyncio

    async def _index_text():
        # Generate embedding
        embedding_result = await generate_embedding(text)

        if embedding_result["status"] != "success":
            return embedding_result

        # Parse metadata
        try:
            metadata_dict = json.loads(metadata) if metadata != "{}" else {}
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid metadata JSON format"}

        # Prepare document with embedding vector
        document = metadata_dict.copy()
        document["text"] = text
        document[VECTOR_FIELD] = embedding_result["embedding"]

        # Index document with or without ID
        if document_id:
            return await aos_client.write_document(document_id, document)
        else:
            return await aos_client.index_document(document)

    # Run async function in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_index_text())
    finally:
        loop.close()


@mcp_server.tool()
def text_similarity_search(text: str, k: int = 10, score: float = 0.0) -> Dict:
    """
    Search in Knowledge Base by searching for similar documents by converting text to embedding and performing kNN search.

    Args:
        text: The text to search for similar documents
        k: Number of similar documents to return
        score: Minimum similarity score threshold (only return results with score > this value)

    Returns:
        Dictionary containing search results or error information
    """
    import asyncio

    async def _similarity_search():
        # Generate embedding for query text
        embedding_result = await generate_embedding(text)

        if embedding_result["status"] != "success":
            return embedding_result

        # Perform kNN search with the generated embedding
        search_result = await knn_search(embedding_result["embedding"], k)

        if search_result["status"] == "success":
            # Filter results based on score threshold
            filtered_results = [
                result for result in search_result["results"]
                if result.get("score", 0) > score
            ]

            return {
                "status": "success",
                "query_text": text,
                "results": filtered_results,
                "total": len(filtered_results),
                "score_threshold": score,
                "original_total": search_result.get("total", 0)
            }
        else:
            return search_result

    # Run async function in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_similarity_search())
    finally:
        loop.close()


def lambda_handler(event, context):
    """AWS Lambda handler function."""
    return mcp_server.handle_request(event, context)
