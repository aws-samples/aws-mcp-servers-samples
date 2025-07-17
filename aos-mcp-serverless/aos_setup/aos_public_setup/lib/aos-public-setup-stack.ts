import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as opensearch from 'aws-cdk-lib/aws-opensearchservice';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as fs from 'fs';
import * as path from 'path';

export interface AosPublicSetupStackProps extends cdk.StackProps {
  openSearchUsername: string;
  openSearchPassword: string;
}

export class AosPublicSetupStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AosPublicSetupStackProps) {
    super(scope, id, props);

    // 创建OpenSearch域 - 使用公共访问模式（不在VPC内）
    const domain = new opensearch.Domain(this, 'OpenSearchDomain', {
      version: opensearch.EngineVersion.openSearch('2.19'),
      capacity: {
        masterNodes: 0,
        dataNodes: 1,
        dataNodeInstanceType: 't3.small.search',
      },
      ebs: {
        volumeSize: 10,
        volumeType: ec2.EbsDeviceVolumeType.GP3,
      },
      zoneAwareness: {
        enabled: false,
      },
      enforceHttps: true,
      nodeToNodeEncryption: true,
      encryptionAtRest: {
        enabled: true,
      },
      fineGrainedAccessControl: {
        masterUserName: props.openSearchUsername,
        masterUserPassword: cdk.SecretValue.unsafePlainText(props.openSearchPassword),
      },
      accessPolicies: [
        new iam.PolicyStatement({
          actions: ['es:*'],
          resources: ['*'],
          effect: iam.Effect.ALLOW,
          principals: [new iam.AnyPrincipal()],
        }),
      ],
      // 移除VPC相关配置，使用公共访问模式
      removalPolicy: cdk.RemovalPolicy.DESTROY, // 注意：生产环境不建议使用DESTROY
    });

    // 创建配置文件
    const configFilePath = path.join(__dirname, '..', 'opensearch-config.json');
    const configContent = {
      domain: domain.domainName,
      endpoint: domain.domainEndpoint,
      username: props.openSearchUsername,
      password: '******', // 不存储实际密码
      version: '2.19',
      region: this.region || 'cn-northwest-1',
      accessType: 'PUBLIC', // 标记为公共访问模式
    };

    // 输出配置到文件
    fs.writeFileSync(configFilePath, JSON.stringify(configContent, null, 2));

    // 输出重要信息
    new cdk.CfnOutput(this, 'OpenSearchDomainEndpoint', {
      value: domain.domainEndpoint,
      description: 'OpenSearch domain endpoint',
    });

    new cdk.CfnOutput(this, 'OpenSearchDashboardsURL', {
      value: `https://${domain.domainEndpoint}/_dashboards/`,
      description: 'OpenSearch Dashboards URL',
    });

    new cdk.CfnOutput(this, 'OpenSearchUsername', {
      value: props.openSearchUsername,
      description: 'OpenSearch master username',
    });

    new cdk.CfnOutput(this, 'ConfigFilePath', {
      value: configFilePath,
      description: 'Path to the OpenSearch configuration file',
    });
  }
}
