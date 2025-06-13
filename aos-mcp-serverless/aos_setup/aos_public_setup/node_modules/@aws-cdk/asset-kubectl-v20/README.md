# Asset with KubeCtl v1.20
<!--BEGIN STABILITY BANNER-->

---

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---

<!--END STABILITY BANNER-->

This module bundles the
[`kubectl`](https://kubernetes.io/docs/reference/kubectl/kubectl/) and the
[`helm`](https://helm.sh/) command line as a local asset. It exposes constants
`ASSET_FILE` and `LAYER_SOURCE_DIR` that can be consumed via the cdk `Asset`
construct.

> - Helm Version: 3.8.1
> - Kubectl Version: 1.20.0
> 

Usage:

```ts
// ASSET_FILE bundles the 'kubectl' and 'helm' command lines
import { ASSET_FILE, LAYER_SOURCE_DIR } from '@aws-cdk/asset-kubectl-v20';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3_assets from 'aws-cdk-lib/aws-s3-assets';
import { FileSystem } from 'aws-cdk-lib';

declare const fn: lambda.Function;
const asset = new s3_assets.Asset(this, 'layer-asset', {
  path: ASSET_FILE,
  assetHash: FileSystem.fingerprint(LAYER_SOURCE_DIR),
});

fn.addLayers(new lambda.LayerVersion(this, 'KubectlLayer', {
  code: lambda.Code.fromBucket(asset.bucket, asset.s3ObjectKey),
  description: '/opt/kubectl/kubectl and /opt/helm/helm',
}));
```

`kubectl` will be installed under `/opt/kubectl/kubectl`, and `helm` will be installed under `/opt/helm/helm`.
