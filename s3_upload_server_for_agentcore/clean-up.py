from dotenv import load_dotenv
import os
import boto3

load_dotenv(dotenv_path=".cleanup_info")

agentID = os.getenv("agent_id")
repoName = os.getenv("repo_name")
roleName = os.getenv("role_name")
ssmName = os.getenv("ssm_name")
secretID = os.getenv("secret_id")

print("🗑️  Starting cleanup process...")

region='us-east-1'
agentcore_control_client = boto3.client('bedrock-agentcore-control', region_name=region)
ecr_client = boto3.client('ecr', region_name=region)
iam_client = boto3.client('iam', region_name=region)
ssm_client = boto3.client('ssm', region_name=region)
secrets_client = boto3.client('secretsmanager', region_name=region)

#response = cognito_client.delete_user_pool(UserPoolId=userpoolID)
#print("✅ User Pool deleted:", response)

try:
    print("Deleting AgentCore Runtime...")
    runtime_delete_response = agentcore_control_client.delete_agent_runtime(
        agentRuntimeId=agentID,
    )
    print("✓ AgentCore Runtime deletion initiated")

    print("Deleting ECR repository...")
    ecr_client.delete_repository(
        repositoryName=repoName,
        force=True
    )
    print("✓ ECR repository deleted")

    print("Deleting IAM role policies...")
    policies = iam_client.list_role_policies(
        RoleName=roleName,
        MaxItems=100
    )

    for policy_name in policies['PolicyNames']:
        iam_client.delete_role_policy(
            RoleName=roleName,
            PolicyName=policy_name
        )
    
    iam_client.delete_role(
        RoleName=roleName
    )
    print("✓ IAM role deleted")

    try:
        ssm_client.delete_parameter(Name=ssmName)
        print("✓ Parameter Store parameter deleted")
    except ssm_client.exceptions.ParameterNotFound:
        print("ℹ️  Parameter Store parameter not found")

    try:
        secrets_client.delete_secret(
            SecretId=secretID,
            ForceDeleteWithoutRecovery=True
        )
        print("✓ Secrets Manager secret deleted")
    except secrets_client.exceptions.ResourceNotFoundException:
        print("ℹ️  Secrets Manager secret not found")

    print("\n✅ Cleanup completed successfully!")
    
except Exception as e:
    print(f"❌ Error during cleanup: {e}")
    print("You may need to manually clean up some resources.")