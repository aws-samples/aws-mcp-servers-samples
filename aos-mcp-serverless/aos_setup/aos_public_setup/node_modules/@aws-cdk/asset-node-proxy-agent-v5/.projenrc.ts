import { CdklabsConstructLibrary } from 'cdklabs-projen-project-types';
import { DependencyType } from 'projen';

// the version of proxy-agent that this branch supports
const SPEC_VERSION = '5';
const releaseWorkflowName = `release-node-proxy-agent-v${SPEC_VERSION}`;

const project = new CdklabsConstructLibrary({
  projenrcTs: true,
  private: false,
  author: 'Amazon Web Services',
  authorAddress: 'aws-cdk-dev@amazon.com',
  cdkVersion: '2.0.0',
  defaultReleaseBranch: 'main',
  name: `@aws-cdk/asset-node-proxy-agent-v${SPEC_VERSION}`,
  repositoryUrl: 'https://github.com/cdklabs/awscdk-asset-node-proxy-agent.git',
  homepage: 'https://github.com/cdklabs/awscdk-asset-node-proxy-agent#readme',
  majorVersion: 2,
  stability: 'stable',
  enablePRAutoMerge: true,
  minNodeVersion: '16.0.0',
  workflowNodeVersion: '16.x',
  setNodeEngineVersion: false,
  devDeps: [
    'cdklabs-projen-project-types',
  ],
  releaseTagPrefix: `node-proxy-agent-v${SPEC_VERSION}`,
  releaseWorkflowName: releaseWorkflowName,
  publishToPypi: {
    distName: `aws-cdk.asset-node-proxy-agent-v${SPEC_VERSION}`,
    module: `aws_cdk.asset_node_proxy_agent_v${SPEC_VERSION}`,
  },
  publishToMaven: {
    javaPackage: `software.amazon.awscdk.cdk.asset.node.proxy.agent.v${SPEC_VERSION}`,
    mavenGroupId: 'software.amazon.awscdk',
    mavenArtifactId: `cdk-asset-node-proxy-agent-v${SPEC_VERSION}`,
    mavenEndpoint: 'https://aws.oss.sonatype.org',
  },
  publishToNuget: {
    dotNetNamespace: `Amazon.CDK.Asset.NodeProxyAgentV${SPEC_VERSION}`,
    packageId: `Amazon.CDK.Asset.NodeProxyAgentV${SPEC_VERSION}`,
  },
  publishToGo: {
    moduleName: 'github.com/cdklabs/awscdk-asset-node-proxy-agent-go',
    packageName: `nodeproxyagentv${SPEC_VERSION}`,
    gitUserName: 'AWS CDK Team',
    gitUserEmail: 'aws-cdk@amazon.com',
    githubTokenSecret: 'PROJEN_GITHUB_TOKEN',
  },
});

// We only need aws-cdk-lib and constructs for testing. Neither library is used
// in the public API.
project.deps.removeDependency('constructs', DependencyType.PEER);
project.deps.addDependency('constructs@^10.0.5', DependencyType.DEVENV);
project.deps.removeDependency('aws-cdk-lib', DependencyType.PEER);
project.deps.addDependency('aws-cdk-lib@^2.0.0', DependencyType.DEVENV);

project.package.addField('jsiiRosetta', {
  exampleDependencies: {
    'aws-cdk-lib': '^2.0.0',
    'constructs': '^10.0.5',
  },
});

project.preCompileTask.exec('layer/build.sh');

project.synth();
