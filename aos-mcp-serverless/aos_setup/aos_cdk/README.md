# Amazon OpenSearch 中国区部署 CDK 项目

这个项目使用 AWS CDK 在中国区部署 Amazon OpenSearch 集群，使用 OpenSearch 2.19 版本。

## 项目结构

- `app.ts` - CDK 应用程序入口点
- `lib/opensearch-stack.ts` - OpenSearch 堆栈定义
- `opensearch-config.json` - OpenSearch 集群配置文件

## 配置文件

配置文件 `opensearch-config.json` 包含以下可配置项：

- `clusterName`: OpenSearch 集群名称
- `domainName`: OpenSearch 域名
- `instanceType`: 实例类型
- `instanceCount`: 实例数量
- `volumeSize`: 存储卷大小 (GB)
- `availabilityZoneCount`: 可用区数量
- `ebs`: 是否使用 EBS 存储
- `encryptionAtRest`: 是否启用静态加密
- `nodeToNodeEncryption`: 是否启用节点间加密
- `enforceHttps`: 是否强制使用 HTTPS
- `tags`: 资源标签

## 部署步骤

1. 安装依赖：

```bash
npm install
```

2. 编译 TypeScript 代码：

```bash
npm run build
```

3. 部署到中国区：

```bash
cdk deploy --profile <中国区配置文件>
```

## 注意事项

- 确保已配置中国区的 AWS 凭证
- 确保 VPC 配置正确，本示例使用默认 VPC
- 根据需要调整 `opensearch-config.json` 中的配置项
