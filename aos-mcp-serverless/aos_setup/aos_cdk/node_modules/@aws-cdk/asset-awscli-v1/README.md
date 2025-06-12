# Asset with AWS CLI v1
<!--BEGIN STABILITY BANNER-->

---

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---

<!--END STABILITY BANNER-->

This module bundles the AWS CLI v1 as a local asset. It exposes
constants `ASSET_FILE` and `LAYER_SOURCE_DIR` that can be consumed
via the CDK `Asset` construct.

Any Lambda Function that uses uses this asset must use a Python 3.x
runtime.

Usage:

```ts
// AwsCliLayer bundles the AWS CLI in a lambda layer
import { ASSET_FILE, LAYER_SOURCE_DIR } from '@aws-cdk/asset-awscli-v1';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3_assets from 'aws-cdk-lib/aws-s3-assets';
import { FileSystem } from 'aws-cdk-lib';

declare const fn: lambda.Function;
const asset = new s3_assets.Asset(this, 'layer-asset', {
  path: ASSET_FILE,
  assetHash: FileSystem.fingerprint(LAYER_SOURCE_DIR),
});
fn.addLayers(new lambda.LayerVersion(this, 'AwsCliLayer', {
  code: lambda.Code.fromBucket(asset.bucket, asset.s3ObjectKey),
}));
```

The CLI will be installed under `/opt/awscli/aws`.
