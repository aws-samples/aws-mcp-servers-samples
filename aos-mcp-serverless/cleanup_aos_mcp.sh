#!/bin/bash
set -e

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
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

# Set AWS profile and region
export AWS_PROFILE=$AWS_PROFILE
export AWS_REGION=$AWS_REGION

echo "=== Starting AOS MCP Serverless Cleanup ==="
echo "Using AWS Profile: $AWS_PROFILE"
echo "Using AWS Region: $AWS_REGION"

# Step 1: Delete the SAM/CloudFormation stack for MCP Serverless
echo "=== Step 1: Deleting MCP Serverless Stack ==="
aws cloudformation delete-stack --stack-name aos-mcp-serverless --profile $AWS_PROFILE --region $AWS_REGION
echo "Waiting for MCP Serverless stack deletion to complete..."
aws cloudformation wait stack-delete-complete --stack-name aos-mcp-serverless --profile $AWS_PROFILE --region $AWS_REGION

# Step 2: Delete the OpenSearch CDK stack
echo "=== Step 2: Deleting OpenSearch Stack ==="
cd aos_setup/aos_public_setup
npx cdk destroy AosPublicSetupStack-New --force --profile $AWS_PROFILE
cd ../..

echo "=== Cleanup Complete ==="
echo "All resources have been deleted."
