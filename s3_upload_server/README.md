# S3 Upload Server

An MCP server that provides file upload functionality to AWS S3 with presigned URL access.

## Features

- Uploads files to S3 bucket named `strands-agent-cn-demo-{accountId}`
- Automatically creates the bucket if it doesn't exist
- Uploads files to the `files/` folder within the bucket
- Sets correct content type based on file extension
- Returns a presigned URL with 1-hour expiration for secure access
- Files remain private in S3 but accessible via presigned URL

## Prerequisites

- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- ICP Recordal for AWS account (if using AWS China account) https://www.amazonaws.cn/en/about-aws/china/faqs/#do-i-need-icp-recordal
- Required AWS permissions:
  - `sts:GetCallerIdentity`
  - `s3:CreateBucket`
  - `s3:ListBucket`
  - `s3:PutObject`
  - `s3:GetObject` (for presigned URL generation)

## Setup

1. Clone the repository to your local machine or server
2. Install dependencies:
   ```bash
   cd s3_upload_server
   uv sync
   ```

3. Add to your MCP client configuration:
   ```json
   {
     "mcpServers": {
       "s3-upload": {
         "command": "uv",
         "args": [
           "--directory", "/path/to/s3_upload_server",
           "run", "src/server.py"
         ]
       }
     }
   }
   ```

## Usage

The server provides one tool:

### upload_file

Uploads a file to S3 and returns a presigned URL with 1-hour expiration.

**Parameters:**
- `file_name` (string): Name of the file including extension
- `file_content` (string): Content of the file as a string

**Returns:**
JSON object with:
- `success`: Boolean indicating success/failure
- `message`: Success message
- `s3_url`: Presigned URL of the uploaded file (expires in 1 hour)
- `bucket_name`: Name of the S3 bucket used
- `account_id`: AWS account ID
- `error`: Error message (if failed)

**Example:**
```python
# Upload a text file
upload_file("hello.txt", "Hello, World!")

# Upload an HTML file
upload_file("index.html", "<html><body><h1>Hello</h1></body></html>")
```

## Security Notes

- Files are uploaded as private objects in S3
- Access is provided through presigned URLs that expire after 1 hour
- This provides better security than public objects as access is time-limited
- Ensure you don't upload sensitive information that shouldn't be accessible even temporarily
- Consider implementing additional access controls if needed
