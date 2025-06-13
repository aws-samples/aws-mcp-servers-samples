# Amazon OpenSearch MCP Serverless 部署指南

本指南将帮助您部署基于 Amazon OpenSearch 的 MCP (Model Context Protocol) 服务器，该服务器支持向量搜索和知识库管理功能。

## 前提条件

在开始部署之前，请确保您已经满足以下条件：

- 已安装并配置 AWS CLI
- 已安装 AWS SAM CLI
- 有效的 AWS 账户（支持中国区域）
- Python 3.8 或更高版本
- 嵌入 API 令牌（用于文本向量转换）
- 基本的 bash 和命令行知识

## 部署步骤

### 步骤 1：克隆代码库

```bash
git clone <repository-url>
cd aos-mcp-serverless
```

### 步骤 2：准备部署参数

部署过程需要以下参数：

- `McpAuthToken`: MCP 服务器的认证令牌（您可以自定义）
- `OpenSearchUsername`: OpenSearch 用户名（您可以自定义）
- `OpenSearchPassword`: OpenSearch 密码（您可以自定义）
- `EmbeddingApiToken`: 嵌入 API 令牌（需要从嵌入服务提供商获取）
- `AWS_PROFILE`: AWS 配置文件名称（可选，默认为 "default"）
- `AWS_REGION`: AWS 区域（可选，默认为 "cn-northwest-1"）

### 步骤 3：执行部署脚本

使用以下命令执行部署脚本：

```bash
./aos_serverless_mcp_setup.sh \
  --McpAuthToken "your-mcp-auth-token" \
  --OpenSearchUsername "your-opensearch-username" \
  --OpenSearchPassword "your-opensearch-password" \
  --EmbeddingApiToken "your-embedding-api-token" \
  --region "your-aws-region"
```

例如：

```bash
./aos_serverless_mcp_setup.sh \
  --McpAuthToken "mcp-token-123456" \
  --OpenSearchUsername "admin" \
  --OpenSearchPassword "Admin@123" \
  --EmbeddingApiToken "sf-api-token-123456" \
  --region "cn-northwest-1"
```

### 步骤 4：部署过程详解

部署脚本将执行以下操作：

1. **检查 OpenSearch 是否已部署**
   - 如果已部署，将使用现有的 OpenSearch 集群
   - 如果未部署，将创建新的 OpenSearch 集群

2. **部署 OpenSearch 集群（如果需要）**
   - 使用 CDK 部署 OpenSearch 集群
   - 等待集群可用
   - 获取 OpenSearch 端点

3. **导入文档到 OpenSearch**
   - 安装必要的 Python 依赖
   - 设置目录结构
   - 将示例知识文档导入到 OpenSearch

4. **部署无服务器 MCP 设置**
   - 更新 SAM 配置
   - 构建 SAM 项目
   - 部署 SAM 项目
   - 获取 API Gateway 端点

### 步骤 5：验证部署

部署完成后，您将看到以下输出：

```
=== Deployment Complete ===
OpenSearch Endpoint: your-opensearch-endpoint
MCP API Endpoint: your-mcp-api-endpoint

```

## 使用示例

### 搜索相似文档

```bash
export API_ENDPOINT=https://xxxxx/Prod/mcp
export AUTH_TOKEN=your-mcp-auth-token
    
python strands_agent_test/similarity_search_demo.py
```

## 清理资源

当您不再需要这些资源时，可以使用清理脚本删除它们：

```bash
./cleanup_aos_mcp.sh --profile your-aws-profile --region your-aws-region
```

例如：

```bash
./cleanup_aos_mcp.sh --profile cn --region cn-northwest-1
```

清理脚本将执行以下操作：

1. 删除 MCP Serverless 堆栈
2. 删除 OpenSearch 堆栈
