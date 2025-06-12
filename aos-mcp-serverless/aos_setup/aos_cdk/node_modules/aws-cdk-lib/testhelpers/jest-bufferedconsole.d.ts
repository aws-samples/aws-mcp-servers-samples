/**
 * A Jest environment that buffers outputs to `console.log()` and only shows it for failing tests.
 */
import type { EnvironmentContext, JestEnvironment, JestEnvironmentConfig } from '@jest/environment';
import { TestEnvironment as NodeEnvironment } from 'jest-environment-node';
export default class TestEnvironment extends NodeEnvironment implements JestEnvironment<unknown> {
    private log;
    private originalConsole;
    private originalStdoutWrite;
    private originalStderrWrite;
    constructor(config: JestEnvironmentConfig, context: EnvironmentContext);
    setup(): Promise<void>;
    teardown(): Promise<void>;
    private startCapture;
    private stopCapture;
}
