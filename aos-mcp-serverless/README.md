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
├── common/                 # Shared components and utilities
└── aos_setup/              # OpenSearch setup and document ingestion tools
    ├── aos_cdk/            # CDK project for OpenSearch deployment
    └── doc_ingest/         # Document ingestion utility
```

## Installation and Deployment

### Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Valid AWS account (China region)
- Amazon OpenSearch Service cluster created (or use the provided CDK project to deploy one)
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
cd aos-mcp-serverless
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

## OpenSearch Setup and Document Ingestion

The project includes tools for setting up Amazon OpenSearch Service and ingesting documents:

### OpenSearch Deployment with CDK

The `aos_setup/aos_cdk` directory contains a CDK project for deploying Amazon OpenSearch Service in AWS China regions:

```bash
cd aos_setup/aos_cdk
npm install
npm run build
cdk deploy --profile cn
```

Configuration options are available in `opensearch-config.json`:
- Cluster name, domain name
- Instance type and count
- Volume size and availability zones
- Security settings (encryption, HTTPS)

### Document Ingestion

The `aos_setup/doc_ingest` directory contains a Python utility for ingesting documents into OpenSearch:

```bash
cd aos_setup/doc_ingest
python doc_ingest.py --file /path/to/document.txt --host your-opensearch-endpoint \
  --username admin --password your-password --token your-embedding-api-token
```

Features:
- Reads text files and splits them into chunks
- Converts text to vector embeddings
- Stores documents with metadata in OpenSearch
- Configurable chunk size and overlap

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



