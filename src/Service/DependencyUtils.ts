import { DatabaseServer } from "@spt-server/servers/DatabaseServer";
import { IDatabaseTables } from "@spt-server/models/spt/server/IDatabaseTables";
import { ILogger } from "@spt-server/models/spt/utils/ILogger";
import { DependencyContainer, InjectionToken } from "tsyringe";

/**
 * managing dependency resolution ==> DependencyContainer.
 */
export class DependencyUtils {
    private static dependencyContainer: DependencyContainer;

    /**
     * Initializes the dependency container.
     * @param dependencyContainer The instance of the dependency container.
     */
    public static initialize(dependencyContainer: DependencyContainer): void {
        this.dependencyContainer = dependencyContainer;
    }

    /**
     * resolves a dependency.
     * @param token The name of the service or class to resolve.
     * @returns The resolved instance if available <> `null`.
     */
    public static resolveDependency<T>(token: InjectionToken<T>): T | null {
        if (!this.dependencyContainer) {
            console.error(`[DependencyUtils] DependencyContainer is not initialized.`);
            return null;
        }

        if (!this.dependencyContainer.isRegistered<T>(token)) {
            console.warn(`[DependencyUtils] Warning: token is not registered.`);
            return null;
        }

        try {
            return this.dependencyContainer.resolve<T>(token);
        } catch (error) {
            console.error(`[DependencyUtils] Error resolving}':`, error);
            return null;
        }
    }

    /**
     * Retrieves the database tables.
     * @returns {IDatabaseTables} The tables if available, <> `null`.
     */
    public static getTableData(): IDatabaseTables | null {
        const dbServer = DependencyUtils.resolveDependency<DatabaseServer>(DatabaseServer);
        if (!dbServer) {
            console.error(`[DependencyUtils] Failed to resolve DatabaseServer.`);
            return null;
        }
        return dbServer.getTables();
    }

    /**
     * Retrieves the logger instance.
     * @returns {ILogger} The logger instance if available, <> `null`.
     */
    public static getLogger(): ILogger | null {
        const logger = DependencyUtils.resolveDependency<ILogger>("WinstonLogger");
        if (!logger) {
            console.error(`[DependencyUtils] Failed to resolve WinstonLogger.`);
            return null;
        }
        return logger;
    }
}
