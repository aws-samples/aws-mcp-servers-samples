#!/bin/bash
set -e

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --McpAuthToken)
      MCP_AUTH_TOKEN="$2"
      shift 2
      ;;
    --OpenSearchUsername)
      OPENSEARCH_USERNAME="$2"
      shift 2
      ;;
    --OpenSearchPassword)
      OPENSEARCH_PASSWORD="$2"
      shift 2
      ;;
    --EmbeddingApiToken)
      EMBEDDING_API_TOKEN="$2"
      shift 2
      ;;
    --profile)
      AWS_PROFILE="$2"
      shift 2
      ;;
    --region)
      AWS_REGION="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Set default values for optional parameters
AWS_PROFILE=${AWS_PROFILE:-"default"}
AWS_REGION=${AWS_REGION:-"cn-northwest-1"}

# Check required parameters
if [[ -z "$MCP_AUTH_TOKEN" || -z "$OPENSEARCH_USERNAME" || -z "$OPENSEARCH_PASSWORD" || -z "$EMBEDDING_API_TOKEN" ]]; then
  echo "Error: Missing required parameters"
  echo "Usage: $0 --McpAuthToken <token> --OpenSearchUsername <username> --OpenSearchPassword <password> --EmbeddingApiToken <token> [--profile <aws-profile>] [--region <aws-region>]"
  exit 1
fi

# Set AWS profile and region
export AWS_PROFILE=$AWS_PROFILE
export AWS_REGION=$AWS_REGION

echo "=== Starting AOS MCP Serverless Deployment ==="
echo "Using AWS Profile: $AWS_PROFILE"
echo "Using AWS Region: $AWS_REGION"

# Step 1: Check if OpenSearch is already deployed
echo "=== Step 1: Checking if OpenSearch is already deployed ==="
CONFIG_FILE="./aos_setup/aos_public_setup/opensearch-config.json"
OPENSEARCH_DEPLOYED=false
OPENSEARCH_ENDPOINT=""

if [ -f "$CONFIG_FILE" ]; then
  echo "Found existing OpenSearch configuration file"
  
  # Check if the domain exists in AWS
  DOMAIN_NAME=$(jq -r '.domain' "$CONFIG_FILE")
  if [ ! -z "$DOMAIN_NAME" ]; then
    echo "Checking if domain $DOMAIN_NAME exists..."
    if aws opensearch describe-domain --domain-name "$DOMAIN_NAME" --profile $AWS_PROFILE --region $AWS_REGION &> /dev/null; then
      echo "OpenSearch domain $DOMAIN_NAME exists"
      OPENSEARCH_DEPLOYED=true
      OPENSEARCH_ENDPOINT=$(jq -r '.endpoint' "$CONFIG_FILE")
      EXISTING_USERNAME=$(jq -r '.username' "$CONFIG_FILE")
      EXISTING_PASSWORD=$(jq -r '.password' "$CONFIG_FILE")
      
      # Use existing credentials if not provided
      if [[ "$OPENSEARCH_USERNAME" == "xxxx" ]]; then
        OPENSEARCH_USERNAME=$EXISTING_USERNAME
        echo "Using existing OpenSearch username: $OPENSEARCH_USERNAME"
      fi
      
      if [[ "$OPENSEARCH_PASSWORD" == "xxxx" ]]; then
        OPENSEARCH_PASSWORD=$EXISTING_PASSWORD
        echo "Using existing OpenSearch password: $OPENSEARCH_PASSWORD"
      fi
    else
      echo "OpenSearch domain $DOMAIN_NAME does not exist, will deploy a new one"
    fi
  fi
fi

# Step 2: Deploy OpenSearch if not already deployed
if [ "$OPENSEARCH_DEPLOYED" = false ]; then
  echo "=== Step 2: Deploying OpenSearch Cluster ==="
  cd ./aos_setup/aos_public_setup
  
  # Run the deploy script
  echo "Running OpenSearch deployment script..."
  ./deploy.sh "$OPENSEARCH_USERNAME" "$OPENSEARCH_PASSWORD" "$AWS_REGION" "$AWS_PROFILE"
  
  # Wait for OpenSearch to be available
  echo "Waiting for OpenSearch to be available..."
  sleep 60  # Initial wait
  
  # Get the OpenSearch endpoint from CloudFormation outputs
  echo "Getting OpenSearch endpoint from CloudFormation..."
  OPENSEARCH_ENDPOINT=$(aws cloudformation describe-stacks --stack-name AosPublicSetupStack-New --query "Stacks[0].Outputs[?OutputKey=='OpenSearchDomainEndpoint'].OutputValue" --output text --profile $AWS_PROFILE --region $AWS_REGION)
  
  if [ -z "$OPENSEARCH_ENDPOINT" ]; then
    echo "Error: Failed to get OpenSearch endpoint from CloudFormation"
    exit 1
  fi
  
  echo "OpenSearch endpoint: $OPENSEARCH_ENDPOINT"
  
  # Update the config file if it exists
  if [ -f "$CONFIG_FILE" ]; then
    echo "Updating OpenSearch configuration file..."
    jq --arg endpoint "$OPENSEARCH_ENDPOINT" '.endpoint = $endpoint' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
  fi
  
  # Check if OpenSearch is available
  MAX_RETRIES=10
  RETRY_COUNT=0
  OPENSEARCH_AVAILABLE=false
  
  while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -k -u "$OPENSEARCH_USERNAME:$OPENSEARCH_PASSWORD" "https://$OPENSEARCH_ENDPOINT/_cluster/health" | grep -q "status"; then
      OPENSEARCH_AVAILABLE=true
      break
    fi
    echo "OpenSearch not yet available, waiting..."
    sleep 30
    RETRY_COUNT=$((RETRY_COUNT + 1))
  done
  
  if [ "$OPENSEARCH_AVAILABLE" = false ]; then
    echo "Error: OpenSearch cluster is not available after waiting"
    exit 1
  fi
  
  echo "OpenSearch cluster is available"
  cd ../..
else
  echo "Skipping OpenSearch deployment as it's already deployed"
fi

# Step 3: Ingest documents into OpenSearch
echo "=== Step 3: Ingesting documents into OpenSearch ==="
cd ./aos_setup/doc_ingest

# Install dependencies from requirements.txt
echo "Installing Python dependencies for document ingestion..."
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found, installing dependencies directly"
  pip install langchain==0.3.25 opensearch-py==2.8.0 requests pydantic langchain-text-splitters langchain-core
fi

# Create necessary directories if they don't exist
echo "Setting up directory structure for document ingestion..."
mkdir -p ../common
mkdir -p ../tools

# Copy necessary files from serverless-mcp-setup if they don't exist
if [ ! -f "../common/aos_client.py" ] && [ -f "../../serverless-mcp-setup/common/aos_client.py" ]; then
  echo "Copying aos_client.py from serverless-mcp-setup..."
  cp ../../serverless-mcp-setup/common/aos_client.py ../common/
fi

# Check if the document ingestion tool exists
if [ -f "doc_ingest.py" ]; then
  echo "Running document ingestion..."
  python doc_ingest.py --file knowledge.txt \
    --host $OPENSEARCH_ENDPOINT \
    --username $OPENSEARCH_USERNAME \
    --password $OPENSEARCH_PASSWORD \
    --token $EMBEDDING_API_TOKEN
else
  echo "Error: Document ingestion tool not found at aos_setup/doc_ingest/doc_ingest.py"
  exit 1
fi

cd ../..

# Step 4: Deploy the serverless MCP setup
echo "=== Step 4: Deploying Serverless MCP Setup ==="
cd ./serverless-mcp-setup

# Get AWS account ID
echo "Getting AWS account ID..."
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text --profile $AWS_PROFILE --region $AWS_REGION)
echo "AWS Account ID: $AWS_ACCOUNT_ID"

# Check if S3 bucket exists in the region
S3_BUCKET_NAME="aos-mcp-serverless-${AWS_ACCOUNT_ID}-${AWS_REGION}"
echo "Checking if S3 bucket exists: $S3_BUCKET_NAME"

# Check if bucket exists
if aws s3api head-bucket --bucket $S3_BUCKET_NAME --profile $AWS_PROFILE --region $AWS_REGION 2>/dev/null; then
  echo "S3 bucket $S3_BUCKET_NAME already exists"
else
  echo "S3 bucket $S3_BUCKET_NAME does not exist, creating it..."
  aws s3 mb s3://$S3_BUCKET_NAME --profile $AWS_PROFILE --region $AWS_REGION
  
  # Wait for bucket to be available
  echo "Waiting for S3 bucket to be available..."
  sleep 5
  
  # Enable versioning on the bucket
  aws s3api put-bucket-versioning --bucket $S3_BUCKET_NAME --versioning-configuration Status=Enabled --profile $AWS_PROFILE --region $AWS_REGION
  echo "S3 bucket created and versioning enabled"
fi

# Update samconfig.toml with the correct region and S3 bucket
echo "Updating SAM configuration..."
cat > samconfig.toml << EOL
version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "aos-mcp-serverless"
s3_bucket = "${S3_BUCKET_NAME}"
s3_prefix = "aos-mcp-serverless"
region = "${AWS_REGION}"
confirm_changeset = false
capabilities = "CAPABILITY_IAM"
parameter_overrides = "McpAuthToken=\"${MCP_AUTH_TOKEN}\" OpenSearchHost=\"${OPENSEARCH_ENDPOINT}\" OpenSearchIndex=\"dockb-index\" OpenSearchUsername=\"${OPENSEARCH_USERNAME}\" OpenSearchPassword=\"${OPENSEARCH_PASSWORD}\" EmbeddingApiToken=\"${EMBEDDING_API_TOKEN}\""
EOL

# Build the SAM project
echo "Building SAM project..."
sam build

# Deploy the SAM project
echo "Deploying SAM project..."
sam deploy --profile $AWS_PROFILE --region $AWS_REGION --parameter-overrides \
  "McpAuthToken=$MCP_AUTH_TOKEN" \
  "OpenSearchHost=$OPENSEARCH_ENDPOINT" \
  "OpenSearchUsername=$OPENSEARCH_USERNAME" \
  "OpenSearchPassword=$OPENSEARCH_PASSWORD" \
  "EmbeddingApiToken=$EMBEDDING_API_TOKEN"

# Get the API Gateway endpoint
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name aos-mcp-serverless --query "Stacks[0].Outputs[?OutputKey=='McpApiEndpoint'].OutputValue" --output text --profile $AWS_PROFILE --region $AWS_REGION)

cd ..

echo "=== Deployment Complete ==="
echo "OpenSearch Endpoint: $OPENSEARCH_ENDPOINT"
echo "MCP API Endpoint: $API_ENDPOINT"
echo ""
echo "To test the MCP server, use:"
echo "curl -H \"Authorization: Bearer $MCP_AUTH_TOKEN\" $API_ENDPOINT"
