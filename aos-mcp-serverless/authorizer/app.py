import os
import json

def lambda_handler(event, context):
    """
    Lambda authorizer for MCP API Gateway
    """
    # Get the auth token from environment
    expected_token = os.environ.get('MCP_AUTH_TOKEN')
    
    # Extract the token from the Authorization header
    token = event.get('authorizationToken', '')
    
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    # Check if token matches
    if token == expected_token:
        effect = 'Allow'
    else:
        effect = 'Deny'
    
    # Generate policy
    policy = {
        'principalId': 'mcp-user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': event['methodArn']
                }
            ]
        }
    }
    
    return policy
