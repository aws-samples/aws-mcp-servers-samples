#!/bin/bash

# 检查是否提供了用户名和密码参数
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <OpenSearchUsername> <OpenSearchPassword> [AWS_REGION] [AWS_PROFILE]"
  echo "Example: $0 admin Admin@123456 cn-northwest-1 default"
  exit 1
fi

USERNAME=$1
PASSWORD=$2
REGION=${3:-cn-northwest-1}  # 默认使用cn-northwest-1区域，如果提供了第三个参数则使用指定区域
PROFILE=${4:-default}        # 如果没有提供第四个参数，默认使用default配置文件
STACK_NAME="AosPublicSetupStack-New"  # 使用新的堆栈名称

# 安装依赖
echo "Installing dependencies..."
npm install

# 构建项目
echo "Building project..."
npm run build

# 部署堆栈 - 使用新的堆栈名称
echo "Deploying OpenSearch cluster with username: $USERNAME in region: $REGION with stack name: $STACK_NAME"
npx cdk deploy --context OpenSearchUsername=$USERNAME --context OpenSearchPassword=$PASSWORD --context Region=$REGION --context StackName=$STACK_NAME --profile $PROFILE

echo "Deployment completed!"
