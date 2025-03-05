export interface ILogger {
    info(message: string): void;
    warning(message: string): void;
    error(message: string): void;
}

export class Logger implements ILogger {
    public info(message: string): void {
        console.log(`[INFO] ${message}`);
    }

    public warning(message: string): void {
        console.warn(`[WARNING] ${message}`);
    }

    public error(message: string): void {
        console.error(`[ERROR] ${message}`);
    }
}
