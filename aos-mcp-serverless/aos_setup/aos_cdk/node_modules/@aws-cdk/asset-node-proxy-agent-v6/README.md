# AWS Lambda Layer with the NPM dependency proxy-agent
<!--BEGIN STABILITY BANNER-->

---

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---

<!--END STABILITY BANNER-->

This module bundles the NPM dependency [`proxy-agent`](https://www.npmjs.com/package/proxy-agent)
as a local asset. It exposes constants `ASSET_FILE` and `LAYER_SOURCE_DIR` that can be consumed
via the CDK `Asset` construct.

> - proxy-agent Version: 6.3.0

Usage:

```ts
import { ASSET_FILE, LAYER_SOURCE_DIR } from '@aws-cdk/asset-node-proxy-agent-v6';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3_assets from 'aws-cdk-lib/aws-s3-assets';
import { FileSystem } from 'aws-cdk-lib';

declare const fn: lambda.Function;
const asset = new s3_assets.Asset(this, 'layer-asset', {
  path: ASSET_FILE,
  assetHash: FileSystem.fingerprint(LAYER_SOURCE_DIR),
});

fn.addLayers(new lambda.LayerVersion(this, 'ProxyAgentLayer', {
  code: lambda.Code.fromBucket(asset.bucket, asset.s3ObjectKey),
}));
```

[`proxy-agent`](https://www.npmjs.com/package/proxy-agent) will be installed under `/nodejs/node_modules`.
