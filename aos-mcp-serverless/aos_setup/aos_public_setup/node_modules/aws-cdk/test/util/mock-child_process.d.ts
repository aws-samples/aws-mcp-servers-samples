export interface Invocation {
    commandLine: string;
    cwd?: string;
    exitCode?: number;
    stdout?: string;
    /**
     * Run this function as a side effect, if present
     */
    sideEffect?: () => void;
}
export declare function mockSpawn(...invocations: Invocation[]): void;
