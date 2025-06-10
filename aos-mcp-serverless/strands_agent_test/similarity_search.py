"""
External Knowledge Base similarity search tool for Strands Agent.

This module provides functionality to perform similarity search against external
knowledge bases via MCP (Model Context Protocol) API endpoints. It uses text-based
similarity matching to find relevant information and returns results ordered by
relevance score.

Key Features:
1. Similarity Search:
   • Text-based similarity matching
   • Relevance scoring (0.0-1.0)
   • Score-based filtering

2. Advanced Configuration:
   • Custom result limits
   • Score thresholds
   • API endpoint configuration
   • Authentication support

3. Response Format:
   • Sorted by relevance
   • Includes metadata
   • Source tracking
   • Score visibility

Usage with Strands Agent:
```python
from strands import Agent
from strands_tools import similarity_search

agent = Agent(tools=[similarity_search])

# Basic search with default parameters
results = agent.tool.similarity_search(
    text="What is machine learning?",
    api_endpoint="https://your-api-endpoint.com/mcp",
    auth_token="your-auth-token"
)

# Advanced search with custom parameters
results = agent.tool.similarity_search(
    text="deployment best practices",
    k=10,
    score=0.7,
    api_endpoint="https://your-api-endpoint.com/mcp",
    auth_token="your-auth-token"
)
```

See the similarity_search function docstring for more details on available parameters and options.
"""

import json
import requests
from typing import Any, Dict
from strands.types.tools import ToolResult, ToolUse

TOOL_SPEC = {
    "name": "similarity_search",
    "description": """Performs similarity search against external aws opensearch knowledge bases via MCP API.

Key Features:
1. Similarity Search:
   - Text-based similarity matching
   - Relevance scoring (0.0-1.0)
   - Score-based filtering
   
2. Advanced Configuration:
   - Custom result limits
   - Score thresholds
   - API endpoint configuration
   - Authentication support

3. Response Format:
   - Sorted by relevance
   - Includes metadata
   - Source tracking
   - Score visibility

4. Example Response:
   {
	'toolUseId': 'tooluse_similarity_search_459545352',
	'status': 'success',
	'results': {
		'type': 'text',
		'text': '{
		'status': 'success',
		'query_text': '厄尔尼诺监测系统包括',
		'results': [{
			'id': 'LgKXU5cBgk3SeTlCSB7V',
			'score': 1.59251,
			'text': 'xxx',
			'metadata': {}
		}]
	}
}

Usage Examples:
1. Basic search:
   similarity_search(text="What is AI?", api_endpoint="...", auth_token="...")

2. With score threshold:
   similarity_search(text="best practices", score=0.7, api_endpoint="...", auth_token="...")

3. Limited results:
   similarity_search(text="deployment", k=5, api_endpoint="...", auth_token="...")""",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The query text to search for similar content.",
                },
                "k": {
                    "type": "integer",
                    "description": "The maximum number of results to return. Default is 5.",
                    "default": 5,
                },
                "score": {
                    "type": "number",
                    "description": (
                        "Minimum relevance score threshold (0.0-1.0). Results below this score will be filtered out. "
                        "Default is 0.0."
                    ),
                    "default": 0.0,
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "api_endpoint": {
                    "type": "string",
                    "description": "The MCP API endpoint URL for the external knowledge base.",
                },
                "auth_token": {
                    "type": "string",
                    "description": "Authentication token for accessing the MCP API.",
                },
            },
            "required": ["text", "api_endpoint", "auth_token"],
        }
    },
}

class MCPClient:
    """Client for interacting with MCP (Model Context Protocol) API endpoints."""
    
    def __init__(self, endpoint: str, auth_token: str):
        """
        Initialize MCP client.
        
        Args:
            endpoint: The MCP API endpoint URL
            auth_token: Authentication token for API access
        """
        self.endpoint = endpoint
        self.auth_token = auth_token
        self.session_id = None
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }
    
    def make_request(self, method: str, params: Dict[str, Any] = None, request_id: int = 1) -> tuple:
        """
        Send MCP request to the API endpoint.
        
        Args:
            method: The MCP method to call
            params: Parameters for the method call
            request_id: Request ID for tracking
            
        Returns:
            Tuple of (status_code, response_data)
        """
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        
        if params:
            payload["params"] = params
        
        # Add session ID to headers if available
        headers = self.headers.copy()
        if self.session_id:
            headers['Mcp-Session-Id'] = self.session_id
        
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=30)
            
            # Extract session ID from response headers
            if 'mcp-session-id' in response.headers:
                self.session_id = response.headers['mcp-session-id']
            
            return response.status_code, response.json()
        except Exception as e:
            return None, {"error": str(e)}
    
    def initialize(self) -> bool:
        """
        Initialize MCP session.
        
        Returns:
            True if initialization successful, False otherwise
        """
        status_code, response = self.make_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "strands-similarity-search", "version": "1.0.0"}
        })
        
        return status_code == 200 and "result" in response
    
    def similarity_search(self, text: str, k: int = 5, score: float = 0.0) -> Dict[str, Any]:
        """
        Perform similarity search using the MCP API.
        
        Args:
            text: Query text to search for
            k: Maximum number of results to return
            score: Minimum score threshold for filtering results
            
        Returns:
            Dictionary containing search results and metadata
        """
        status_code, response = self.make_request("tools/call", {
            "name": "textSimilaritySearch",
            "arguments": {
                "text": text,
                "k": k,
                "score": score
            }
        })

        # reponse is a dict
        # {'jsonrpc': '2.0', 'id': 1, 'result': {'content': [{'type': 'text', 'text': "{'status': 'success', 'query_text': 'machine learning algorithms', 'results': [...]
        if status_code == 200 and "result" in response:
            content = response["result"]['content']

            if content:
                result_text = content[0]

                return result_text
            else:
                return {"error": "No content in response"}
        else:
            return {"error": f"API call failed: {response}"}

def similarity_search(tool: ToolUse, **kwargs: Any) -> ToolResult:
    """
    Perform similarity search against external knowledge base via MCP API.
    
    This tool connects to external knowledge bases through MCP (Model Context Protocol)
    API endpoints to perform text-based similarity search. It returns results sorted by
    relevance score, with the ability to filter results that don't meet a minimum score threshold.
    
    How It Works:
    ------------
    1. Initialize connection to the MCP API endpoint
    2. Send similarity search request with query text and parameters
    3. Receive results with relevance scores (0.0-1.0) indicating match quality
    4. Filter results based on minimum score threshold
    5. Format and return results for readability
    
    Common Usage Scenarios:
    ---------------------
    - Searching for relevant information in external document repositories
    - Finding similar content across distributed knowledge bases
    - Retrieving context from specialized domain-specific databases
    - Querying external research databases or archives
    - Accessing third-party knowledge management systems
    
    Args:
        tool: Tool use information containing input parameters:
            text: The query text to search for similar content
            k: Maximum number of results to return (default: 5)
            score: Minimum relevance score threshold (default: 0.0)
            api_endpoint: The MCP API endpoint URL
            auth_token: Authentication token for API access
    
    Returns:
        Dictionary containing status and response content in the format:
        {
            "toolUseId": "unique_id",
            "status": "success|error",
            "content": [{"text": "Search results or error message"}]
        }
        
        Success case: Returns formatted search results from the external knowledge base
        Error case: Returns information about what went wrong during the search
    
    Notes:
        - The MCP API endpoint must support the textSimilaritySearch tool
        - Authentication token must be valid for the specified endpoint
        - Results are automatically filtered based on the minimum score threshold
        - Network connectivity is required to access the external knowledge base
    """
    tool_use_id = tool["toolUseId"]
    tool_input = tool["input"]
    
    try:
        # Extract parameters
        query_text = tool_input["text"]
        k = tool_input.get("k", 5)
        score_threshold = tool_input.get("score", 0.0)
        api_endpoint = tool_input["api_endpoint"]
        auth_token = tool_input["auth_token"]
        
        # Initialize MCP client
        client = MCPClient(api_endpoint, auth_token)
        
        # Initialize session
        if not client.initialize():
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": "Failed to initialize MCP session"}],
            }
        
        # Perform similarity search
        results = client.similarity_search(query_text, k, score_threshold)

        formatted = {
            "toolUseId": tool_use_id,
            "status": "success",
            "results": results
        }

        return formatted
        
    except Exception as e:
        # Return error with details
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Error during similarity search: {str(e)}"}],
        }
