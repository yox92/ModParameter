import {Aiming} from "./Aiming";

export interface IDatabaseServer {
    getTables(): {
        templates: {
            items: Record<string, any>;
            name: string;
        };
        globals: {
            config: {
                Aiming: Aiming;
            };
        };
    };
}

export class DatabaseServer implements IDatabaseServer {
    private tables: {
        templates: {
            items: Record<string, any>;
            name: string;
        };
        globals: {
            config: {
                Aiming: Aiming;
            };
        };
    };

    constructor() {
        this.tables = {
            templates: {
                items: {},
                name: ""
            },
            globals: {
                config: {
                    Aiming: new Aiming({})
                }
            }
        };
    }

    public getTables(): {
        templates: {
            items: Record<string, any>;
            name: string;
        };
        globals: {
            config: {
                Aiming: Aiming;
            };
        };
    } {
        return this.tables;
    }
}
