import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
export interface AosPublicSetupStackProps extends cdk.StackProps {
    openSearchUsername: string;
    openSearchPassword: string;
}
export declare class AosPublicSetupStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props: AosPublicSetupStackProps);
}
