from utils import create_agentcore_role, setup_cognito_user_pool
from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import time, os, boto3, logging, json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Cognito 
logger.info("Setting up Amazon Cognito user pool...")
cognito_config = setup_cognito_user_pool()
logger.info("Cognito setup completed ✓")
logger.info(f"User Pool ID: {cognito_config.get('user_pool_id', 'N/A')}")
logger.info(f"Client ID: {cognito_config.get('client_id', 'N/A')}")


# AgentCore Role with S3 permissions
tool_name = "mcp_server_s3_upload"
logger.info(f"Creating IAM role for {tool_name}...")
agentcore_iam_role = create_agentcore_role(agent_name=tool_name)
logger.info(f"IAM role created ✓")
logger.info(f"Role ARN: {agentcore_iam_role['Role']['Arn']}")


# AgentCore Configure
boto_session = Session()
region = boto_session.region_name
logger.info(f"Using AWS region: {region}")

required_files = ['mcp_server.py', 'requirements.txt']
for file in required_files:
    if not os.path.exists(file):
        raise FileNotFoundError(f"Required file {file} not found")
logger.info("All required files found ✓")

agentcore_runtime = Runtime()

auth_config = {
    "customJWTAuthorizer": {
        "allowedClients": [
            cognito_config['client_id']
        ],
        "discoveryUrl": cognito_config['discovery_url'],
    }
}

logger.info("Configuring AgentCore Runtime...")
response = agentcore_runtime.configure(
    entrypoint="mcp_server.py",
    execution_role=agentcore_iam_role['Role']['Arn'],
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region=region,
    authorizer_configuration=auth_config,
    protocol="MCP",
    agent_name=tool_name
)
logger.info("Configuration completed ✓")


# AgentCore Launch
logger.info("Launching MCP server to AgentCore Runtime...")
logger.info("This may take several minutes...")
launch_result = agentcore_runtime.launch()
logger.info("Launch completed ✓")
logger.info(f"Agent ARN: {launch_result.agent_arn}")
logger.info(f"Agent ID: {launch_result.agent_id}")


# AgentCore Runtime Status
logger.info("Checking AgentCore Runtime status...")
status_response = agentcore_runtime.status()
status = status_response.endpoint['status']
logger.info(f"Initial status: {status}")

end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
while status not in end_status:
    logger.info(f"Status: {status} - waiting...")
    time.sleep(10)
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']

if status == 'READY':
    logger.info("✓ AgentCore Runtime is READY!")
else:
    logger.info(f"⚠ AgentCore Runtime status: {status}")
    
logger.info(f"Final status: {status}")


# Save credentials/ARN
ssm_client = boto3.client('ssm', region_name=region)
secrets_client = boto3.client('secretsmanager', region_name=region)

try:
    cognito_credentials_response = secrets_client.create_secret(
        Name='mcp_server/cognito/credentials',
        Description='Cognito credentials for MCP server',
        SecretString=json.dumps(cognito_config)
    )
    logger.info("✓ Cognito credentials stored in Secrets Manager")
except secrets_client.exceptions.ResourceExistsException:
    secrets_client.update_secret(
        SecretId='mcp_server/cognito/credentials',
        SecretString=json.dumps(cognito_config)
    )
    logger.info("✓ Cognito credentials updated in Secrets Manager")

agent_arn_response = ssm_client.put_parameter(
    Name='/mcp_server/runtime/agent_arn',
    Value=launch_result.agent_arn,
    Type='String',
    Description='Agent ARN for MCP server',
    Overwrite=True
)

encoded_arn = launch_result.agent_arn.replace(':', '%3A').replace('/', '%2F')
mcp_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
endpoint_url_response = ssm_client.put_parameter(
    Name='/mcp_server/runtime/endpoint_url',
    Value=mcp_url,
    Type='String',
    Description='Endpoint URL for MCP server',
    Overwrite=True
)

logger.info("✓ Agent ARN stored in Parameter Store")
logger.info("\nConfiguration stored successfully!")
logger.info(f"Agent ARN: {launch_result.agent_arn}")
logger.info(f"Endpoint URL: {mcp_url}")


# save info for resource release
with open(".cleanup_info", "w") as f:
    f.write("\n")
    f.write(f"agent_id={launch_result.agent_id}")
    f.write("\n")
    f.write(f"repo_name={launch_result.ecr_uri.split('/')[1]}")
    f.write("\n")
    f.write(f"role_name={agentcore_iam_role['Role']['RoleName']}")
    f.write("\n")
    f.write("ssm_name=/mcp_server/runtime/agent_arn")
    f.write("\n")
    f.write("secret_id=mcp_server/cognito/credentials")






