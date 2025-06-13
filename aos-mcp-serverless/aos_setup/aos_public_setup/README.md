# OpenSearch 公开访问集群部署

这个项目使用AWS CDK部署一个可公开访问的Amazon OpenSearch Service集群。

## 功能特点

- 部署OpenSearch 2.19版本集群
- 单可用区部署
- 公共访问模式（无需VPC）
- 自动生成配置文件
- 可自定义管理员用户名和密码

## 前提条件

- Node.js 14.x 或更高版本
- AWS CLI 已配置
- AWS CDK 已安装 (`npm install -g aws-cdk`)
- 有效的AWS账户和权限

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 使用脚本部署

```bash
./deploy.sh <OpenSearchUsername> <OpenSearchPassword> [AWS_REGION] [AWS_PROFILE]
```

例如:

```bash
./deploy.sh admin Admin@123456 cn-northwest-1 default
```

如果不指定区域，默认使用`cn-northwest-1`（中国宁夏区域）。如果指定了区域，则使用指定的区域。

### 3. 手动部署

如果你想手动部署，可以按照以下步骤操作：

```bash
# 安装依赖
npm install

# 构建项目
npm run build

# 部署堆栈，传入用户名、密码和区域参数
npx cdk deploy --context OpenSearchUsername=admin --context OpenSearchPassword=Admin@123456 --context Region=cn-northwest-1
```

## 部署后

部署完成后，CDK将输出以下信息：

- OpenSearch域端点URL
- OpenSearch Dashboards URL
- 配置文件路径

你可以使用提供的用户名和密码登录OpenSearch Dashboards。

## 配置文件

部署过程会在项目根目录下生成`opensearch-config.json`文件，包含以下信息：

- 域名
- 端点URL
- 用户名
- 区域
- VPC ID
- 安全组ID

## 安全注意事项

此部署配置允许从任何IP地址访问OpenSearch集群。在生产环境中，建议限制访问来源IP。

## 清理资源

要删除部署的资源，运行：

```bash
npx cdk destroy
```
