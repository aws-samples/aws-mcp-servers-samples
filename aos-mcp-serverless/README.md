# AOS MCP Server (Amazon OpenSearch Model Context Protocol)

This project is a Lambda-based MCP (Model Context Protocol) server designed for Amazon OpenSearch Service, supporting vector search and knowledge base management capabilities. The server can be deployed in AWS China regions and integrates with embedding services available in China regions.

## Key Features

- Based on AWS Serverless architecture using Lambda and API Gateway
- Supports text-to-vector embedding conversion
- Provides vector similarity search functionality
- Integrates with Amazon OpenSearch Service
- Supports session management and authentication

## Technology Stack

- Python 3.12
- AWS Serverless Application Model (SAM)
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon OpenSearch Service
- Silicon Flow Embedding API (China region)

## Project Structure

```
.
├── app.py                  # Main application entry point
├── template.yaml           # SAM template
├── requirements.txt        # Python dependencies
├── lambda_mcp/             # MCP server core code
├── authorizer/             # API authentication handler
└── common/                 # Shared components and utilities
```

## Installation and Deployment

### Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Valid AWS account (China region)
- Amazon OpenSearch Service cluster created
- Silicon Flow API token
  
    
Create Index in AWS OpenSearch
```bash
PUT dockb-index
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "refresh_interval": "60s",
      "knn": true,
      "knn.algo_param.ef_search": 32
    }
  },
  "mappings": {
    "properties": {
      "dense_vector": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "ef_construction": 32,
            "m": 16
          }
        }
      }
    }
  }
}

```

### Deployment Steps

1. Clone the repository

```bash
git clone <repository-url>
```

2. Build the project

```bash
sam build
```

3. Deploy the project

```bash
sam deploy --profile cn
```

Or with parameter overrides:

```bash
sam deploy --profile cn --parameter-overrides \
  "McpAuthToken=your-auth-token" \
  "OpenSearchHost=your-opensearch-endpoint" \
  "OpenSearchUsername=your-username" \
  "OpenSearchPassword=your-password" \
  "EmbeddingApiToken=your-embedding-api-token"
```

## Usage

After deployment, you will receive an API Gateway endpoint URL. You can use this URL to interact with the MCP server.

### Searching Similar Documents

```bash
export API_ENDPOINT=https://xxxxx/Prod/mcp
export AUTH_TOKEN=xxxx
    
python strands_agent_test/similarity_search_demo.py
```

## Configuration Parameters

| Parameter Name | Description | Default Value |
|----------------|-------------|---------------|
| McpAuthToken | Authentication token for the MCP server | - |
| OpenSearchHost | OpenSearch cluster endpoint | - |
| OpenSearchPort | OpenSearch port | 443 |
| OpenSearchIndex | OpenSearch index name | dockb-index |
| OpenSearchUsername | OpenSearch username | - |
| OpenSearchPassword | OpenSearch password | - |
| EmbeddingApiToken | API token for embedding service | - |

## China Region Specific Notes

- The project is optimized for AWS China regions
- Uses the China region Silicon Flow API endpoint (`https://api.siliconflow.cn/v1/embeddings`)
- Default model for text embedding is `Pro/BAAI/bge-m3`

## Security Considerations

- Sensitive credentials are passed through environment variables
- API authentication uses a token mechanism
- AWS Secrets Manager is recommended for managing sensitive information in production environments



