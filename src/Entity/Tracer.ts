export class Tracer {
    Tracer: boolean;
    TracerColor: string;

    constructor(tracer: Partial<Tracer>) {
        Object.assign(this, tracer);
    }
}

export function creatTracer(data: any) {
    return new Tracer({
        Tracer: data.Tracer,
        TracerColor: data.TracerColor
    });
}