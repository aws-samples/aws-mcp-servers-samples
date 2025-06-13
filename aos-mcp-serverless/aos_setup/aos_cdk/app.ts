#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { OpenSearchStack } from './lib/opensearch-stack';
import * as fs from 'fs';
import * as path from 'path';

const app = new cdk.App();

// 读取配置文件
const configPath = path.join(__dirname, 'opensearch-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// 创建OpenSearch堆栈
new OpenSearchStack(app, 'OpenSearchStackNew', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'cn-north-1', // 默认使用中国北京区域
  },
  opensearchConfig: config,
});
