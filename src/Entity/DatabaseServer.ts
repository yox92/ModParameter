export interface IDatabaseServer {
    getTables(): {
        templates: {
            items: Record<string, any>;
            name: string
        };
    };
}

export class DatabaseServer implements IDatabaseServer {
    private tables: {
        templates: {
            items: Record<string, any>;
            name: string;
        };
    };

    constructor() {
        this.tables = {
            templates: {
                items: {},
                name: ""
            },
        };
    }

    public getTables(): {
        templates: {
            items: Record<string, any>;
            name: string;
        };
    } {
        return this.tables;
    }
}