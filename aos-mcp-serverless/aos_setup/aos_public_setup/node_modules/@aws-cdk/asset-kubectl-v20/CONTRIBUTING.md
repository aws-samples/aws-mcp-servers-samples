# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional
documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary
information to effectively respond to your bug report or contribution.

Specifically, if you wish to contribute a new Kubectl Asset with a different kubectl version, jump to [Contributing a new Kubectl Asset](#contributing-a-new-kubectl-asset).


## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of our code being used
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment


## Contributing via Pull Requests
Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the *kubectl-v20/main* branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source; please focus on the specific change you are contributing. If you also reformat all the code, it will be hard for us to focus on your change.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages.
5. Send us a pull request, answering any default questions in the pull request interface.
6. Pay attention to any automated CI failures reported in the pull request, and stay involved in the conversation.

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contributing a new Kubectl Asset
If you would like to contribute a new Kubectl Asset with a different kubectl version, please follow these steps:

1. Open a new GitHub issue titled `Feature Request: Asset with kubectl vX.Y.Z`. We will track the progress of the new
Asset in the issue.
2. If we decide to support the requested version, a maintainer will open a new branch, `kubectl-vY/main`
(Y is the minor version) and update the issue accordingly. The maintainer will also open a branch called `kubectl.vY`
in the corresponding go binding repository, [`cdklabs/awscdk-kubectl-go`](https://github.com/cdklabs/awscdk-kubectl-go/branches).
3. Create a fork of the repository and fetch the `kubectl-vY/main` branch locally, and modify the source off of that.
4. Specifically: 
    - change `README.md` to reflect the new versions of kubectl and helm that the asset will include.
    - change `KUBECTL_VERSION` and `HELM_VERSION` in `layer/Dockerfile` to reflect the new versions.
    The `HELM_VERSION` you select should be the highest version compatible with the `KUBECTL_VERSION`
    according to the helm [docs](https://helm.sh/docs/topics/version_skew/). For example, if
    `KUBECTL_VERSION` is v1.20.x, then the `HELM_VERSION` should be v3.8.x.
    - change `SPEC_VERSION` in `.projenrc.js` to reflect the new minor version of kubectl.
    For example, if `KUBECTL_VERSION` is v1.25.0, then `SPEC_VERSION` should be 25.
    - change the Kubectl Lambda layer class in `src/kubectl-layer.ts` to `KubectlV##Layer`, and its `description` field to reflect the latest versions of Kubectl and Helm being supported.
    - change `test/kubectl-layer.test.ts` to reflect the new construct's name (changed in the previous step) and that the description
    verifies the correct versions of Kubectl and Helm.
    - change `test/kubectl-layer.integ.ts` to reflect the new construct's name (changed in the previous step).
    - for an example of code changes done for Kubectl v1.22.0, see this [PR](https://github.com/cdklabs/awscdk-asset-kubectl/pull/7).
5. Run `npx projen compile` to generate the Lambda layer constructs that will be tested.
6. Run `npx projen` to update the github workflows.
7. Run `npx projen integ:kubectl-layer:deploy` to ensure that the new versions in the Dockerfile can be successfully downloaded.
This stage _must succeed_ before proceeding. 
When it succeeds, confirm that the snapshot in `test/kubectl-layer.integ.snapshot` has been updated. If not, run `npx projen integ:kubectl-layer:snapshot` to update it.
8. Run `yarn build` to ensure everything builds correctly.
9. Commit to your fork and submit a pull request to the repository, _ensuring that you are targeting the correct `kubectl-vY/main` branch_.
10. A maintainer will review your contribution from there!
11. ⚠️ **IMPORTANT FOR THE MAINTAINER** ⚠️ The maintainer should go into the repository settings and update the default branch to this new, latest version that has just been merged in. This is because GitHub only runs actions on default branches, and we want to ensure dependencies are updated in the latest version + the previous 3 versions.

## Backporting changes to branches with different Kubectl versions
This repository consists of multiple branches, with each branch corresponding to a specific Kubectl version.
For example, `kubectl-v24/main` is the branch that releases a Lambda Layer that bundles Kubectl version 1.24.
Sometimes, a contribution made to a specific branch should be propogated to other branches in this repository as well.
To do this, you can add `backport-to-kubectl-v21+` as a label to the PR that tells Mergify to backport when the PR is merged.
This will backport to all versions of kubectl except kubectl v1.20, which is special and does not expose a Lambda Layer.

If you think you need to backport to a specific subset of branches instead, you can ask a maintainer to backport via
a mergify comment:

```
@Mergifyio backport kubectl-v21/main kubectl-v22/main
```

## Finding contributions to work on
Looking at the existing issues is a great way to find something to contribute on. As our projects, by default, use the default GitHub issue labels (enhancement/bug/duplicate/help wanted/invalid/question/wontfix), looking at any 'help wanted' issues is a great place to start.


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security issue notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.
