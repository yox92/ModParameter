export interface IBuffJson {
    absoluteValue: boolean;
    buffType: string;
    chance: number;
    delay: number;
    duration: number;
    skillName: string;
    value: number;
    change?: boolean;
    add?: boolean;
}

export class Buff {
    absoluteValue: boolean;
    buffType: string;
    chance: number;
    delay: number;
    duration: number;
    skillName: string;
    value: number;
    change: boolean;
    add: boolean;

    constructor(data: any) {
        this.absoluteValue = data.AbsoluteValue ?? data.absoluteValue;
        this.buffType = data.BuffType ?? data.buffType;
        this.chance = data.Chance ?? data.chance;
        this.delay = data.Delay ?? data.delay;
        this.duration = data.Duration ?? data.duration;
        this.skillName = data.SkillName ?? data.skillName;
        this.value = data.Value ?? data.value;
        this.change = data.change ?? false;
        this.add = data.add ?? false;
    }

    toJson(): IBuffJson {
        return {
            absoluteValue: this.absoluteValue,
            buffType: this.buffType,
            chance: this.chance,
            delay: this.delay,
            duration: this.duration,
            skillName: this.skillName,
            value: this.value,
            change: this.change,
            add: this.add
        };
    }
}

export class BuffGroup {
    name: string;
    buffs: Buff[];

    constructor(name: string, buffList: IBuffJson[]) {
        this.name = name;
        this.buffs = buffList.map(buff => new Buff(buff));
    }

    toJson(): IBuffJson[] {
        return this.buffs.map(buff => buff.toJson());
    }

    findBuff(buffType: string, skillName: string): Buff | undefined {
        return this.buffs.find(b => b.buffType === buffType && b.skillName === skillName);
    }

    hasChangedBuffs(): boolean {
        return this.buffs.some(b => b.change);
    }

    getChangedBuffs(): Buff[] {
        return this.buffs.filter(b => b.change);
    }
}
export type BuffsJsonFile = {
    Buffs: Record<string, IBuffJson[]>;
};

export class BuffCollection {
    groups: BuffGroup[];

    constructor(data: BuffsJsonFile) {
        this.groups = Object.entries(data.Buffs).map(
            ([groupName, buffList]) => new BuffGroup(groupName, buffList)
        );
    }

    toJson(): BuffsJsonFile {
        const result: Record<string, IBuffJson[]> = {};
        for (const group of this.groups) {
            result[group.name] = group.toJson();
        }
        return { Buffs: result };
    }

    getGroup(name: string): BuffGroup | undefined {
        return this.groups.find(group => group.name === name);
    }

    getAllBuffs(): Buff[] {
        return this.groups.flatMap(group => group.buffs);
    }

    areAllBuffsUnchanged(): boolean {
        return this.getAllBuffs().every(buff => !buff.change);
    }

    getModifiedBuffs(): Buff[] {
        return this.getAllBuffs().filter(buff => buff.change);
    }

    getGroupsWithChanges(): BuffGroup[] {
        return this.groups.filter(group => group.hasChangedBuffs());
    }
}
