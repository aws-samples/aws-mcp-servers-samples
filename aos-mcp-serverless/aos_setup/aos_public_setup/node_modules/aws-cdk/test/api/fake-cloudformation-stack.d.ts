/// <reference types="jest" />
import { CloudFormation } from 'aws-sdk';
import { CloudFormationStack, Template } from '../../lib/api/util/cloudformation';
export interface FakeCloudFormationStackProps {
    readonly stackName: string;
    readonly stackId: string;
}
export declare class FakeCloudformationStack extends CloudFormationStack {
    readonly cfnMock: jest.Mocked<CloudFormation>;
    private readonly props;
    private __template;
    constructor(props: FakeCloudFormationStackProps);
    setTemplate(template: Template): void;
    template(): Promise<Template>;
    get stackId(): string;
}
