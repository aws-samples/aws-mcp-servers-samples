You can use this to deploy the S3 upload MCP server to Amazon Bedrock AgentCore MCP runtime,
to use it as a remote MCP server

Procedures:
1. start an virtual python environment and pip install -r requirements.txt
2. cd to the folder s3_upload_for_agentcore
3. run python remote_deploy.py
4. Automatic deploy to your account (Please make sure you have sufficient permissions)
5. Clean up resources with python clean-up.py
