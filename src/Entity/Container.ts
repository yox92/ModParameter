export interface IContainer {
    resolve<T>(name: string): T;
}

export class Container implements IContainer {
    private readonly services: Map<string, unknown>;

    constructor() {
        this.services = new Map<string, unknown>();
    }

    /**
     * Registers a service instance under a given name.
     * @param name service name.
     * @param instance service instance.
     */
    public register<T>(name: string, instance: T): void {
        this.services.set(name, instance);
    }

    /**
     * Retrieves a registered service instance.
     * @param name service name.
     * @returns The registered instance.
     * @throws Error if the service does not exist or is `undefined`.
     */
    public resolve<T>(name: string): T {
        if (!this.services.has(name)) {
            throw new Error(`Service '${name}' non enregistré dans le conteneur.`);
        }

        const service = this.services.get(name);
        if (service === undefined) {
            throw new Error(`Service '${name}' est enregistré mais a une valeur undefined.`);
        }

        return service as T;
    }
}
