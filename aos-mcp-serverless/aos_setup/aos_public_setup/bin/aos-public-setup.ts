#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AosPublicSetupStack } from '../lib/aos-public-setup-stack';

const app = new cdk.App();

// 获取命令行参数
const openSearchUsername = app.node.tryGetContext('OpenSearchUsername') || 'admin';
const openSearchPassword = app.node.tryGetContext('OpenSearchPassword') || 'Admin@123456';
const region = app.node.tryGetContext('Region') || process.env.CDK_DEFAULT_REGION || 'cn-northwest-1';
const stackName = app.node.tryGetContext('StackName') || 'AosPublicSetupStack-New';

new AosPublicSetupStack(app, stackName, {
  // 指定环境配置，只包括区域，账户使用当前默认账户
  env: { 
    region: region
  },
  
  // 传递参数到堆栈
  openSearchUsername,
  openSearchPassword,
});
