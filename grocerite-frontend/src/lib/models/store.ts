export class Store {
    idx: number;
    name: string;
    location?: string;
    householdIdx: number;

    constructor({
        idx = -1,
        name = '',
        location = '',
        householdIdx = -1
    } : {
        idx?: number,
        name?: string,
        location?: string,
        householdIdx?: number
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.location = location;
        this.householdIdx = householdIdx;
    }

    static fromJson(json: any): Store {
        return new Store({
            idx: json.idx,
            name: json.name,
            location: json.location,
            householdIdx: json.householdIdx
        });
    }
}