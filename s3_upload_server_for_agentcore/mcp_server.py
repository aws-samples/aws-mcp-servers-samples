#!/usr/bin/env python3
import json
import mimetypes
import os
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP, Context
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import logging

# Constants
DEFAULT_AWS_REGION = 'us-east-1'

# Required AWS permissions:
# - sts:GetCallerIdentity
# - s3:CreateBucket
# - s3:ListBucket
# - s3:PutObject
# - s3:GetObject (for presigned URL generation)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
expire_hours = int(os.environ.get('EXPIRE_HOURS',144))

mcp = FastMCP(host="0.0.0.0", stateless_http=True)

def get_aws_credentials() -> Dict[str, str]:
    """Get AWS credentials from environment variables"""
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    session_token = os.environ.get('AWS_SESSION_TOKEN')  # Optional    
    if not access_key or not secret_key:
        return None
    
    credentials = {
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key
    }
    
    if session_token:
        credentials['aws_session_token'] = session_token
        
    return credentials

def get_aws_region() -> str:
    """Get AWS region from environment variable or use default"""
    return os.environ.get('AWS_DEFAULT_REGION', os.environ.get('AWS_REGION', DEFAULT_AWS_REGION))

def get_account_id(region: str = None) -> str:
    """Get current AWS account ID using STS"""
    try:
        credentials = get_aws_credentials()
        if credentials:
            if region:
                sts_client = boto3.client('sts', region_name=region, **credentials)
            else:
                sts_client = boto3.client('sts', **credentials)
        else:
            if region:
                sts_client = boto3.client('sts', region_name=region)
            else:
                sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        return response['Account']
    except NoCredentialsError as e:
        raise ValueError(f"AWS credentials not configured. Please configure AWS credentials {str(e)}.")
    except Exception as e:
        raise ValueError(f"Failed to get AWS account ID: {str(e)}")

def get_content_type(file_name: str) -> str:
    """Get content type based on file extension with proper charset for text files"""
    content_type, _ = mimetypes.guess_type(file_name)
    if not content_type:
        content_type = 'application/octet-stream'
    
    # Add charset=utf-8 for text-based content types to ensure proper Unicode display
    if content_type.startswith(('text/', 'application/json', 'application/xml', 'application/javascript')):
        if 'charset' not in content_type:
            content_type += '; charset=utf-8'
    elif content_type == 'text/html' or file_name.lower().endswith('.html'):
        content_type = 'text/html; charset=utf-8'
    
    return content_type

def create_bucket_if_not_exists(s3_client, bucket_name: str, region: str) -> bool:
    """Create S3 bucket if it doesn't exist"""
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} already exists")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            # Bucket doesn't exist, create it
            try:
                if region == 'us-east-1':
                    # For us-east-1, don't specify LocationConstraint
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                logger.info(f"Created bucket {bucket_name}")
                return True
            except ClientError as create_error:
                raise ValueError(f"Failed to create bucket {bucket_name}: {str(create_error)}")
        else:
            raise ValueError(f"Failed to check bucket {bucket_name}: {str(e)}")

def upload_file_to_s3(s3_client, bucket_name: str, file_name: str, file_content: str, folder: str = 'files') -> str:
    """Upload file to S3 and return a presigned URL with 1-hour expiration"""
    try:
        # Prepare the S3 key (file path)
        s3_key = f"{folder}/{file_name}"
        
        # Get content type
        content_type = get_content_type(file_name)
        
        # Encode content as UTF-8 bytes
        file_bytes = file_content.encode('utf-8')
        
        # Upload file with proper content type
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type
        )
        
        # Generate presigned URL with 1-hour expiration
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=3600*expire_hours # 7 days in seconds (maximum allowed)
        )
        
        logger.info(f"Successfully uploaded {file_name} with content type {content_type} and generated presigned URL")
        return presigned_url
        
    except ClientError as e:
        raise ValueError(f"Failed to upload file to S3: {str(e)}")

@mcp.tool()
def upload_file(file_name: str, file_content: str) -> str:
    """Upload a file to S3 bucket and return a presigned URL with expiration
    
    Args:
        file_name: Name of the file to upload (including extension)
        file_content: Content of the file as a string
    
    Returns:
        presigned S3 URL of the uploaded file
    """
    try:
        # Get AWS credentials
        credentials = get_aws_credentials()
        
        # Get AWS region
        region = get_aws_region()
        
        # Get current AWS account ID
        account_id = get_account_id(region)
        
        # Create bucket name
        bucket_name = f"agentcore-demo-{account_id}"
        
        # Initialize S3 client with region and explicit credentials
        if credentials:
            s3_client = boto3.client('s3', region_name=region, **credentials)
        else:
            s3_client = boto3.client('s3', region_name=region)
        
        # Create bucket if it doesn't exist
        create_bucket_if_not_exists(s3_client, bucket_name, region)
        
        # Upload file to S3
        s3_url = upload_file_to_s3(s3_client, bucket_name, file_name, file_content)
        
        return s3_url
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")