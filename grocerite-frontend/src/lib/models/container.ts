export class ContainerItem{
    idx: number;
    label: string;
    quantity: number;
    comment: string;
    isRemoved: boolean;
    storeIdx: number;

    constructor({
        idx = -1,
        label = '',
        quantity = 0,
        comment = '',
        isRemoved = false,
        storeIdx = -1
    } : {
        idx?: number,
        label?: string,
        quantity?: number,
        comment?: string,
        isRemoved?: boolean,
        storeIdx?: number
    } = {}) {
        this.idx = idx;
        this.label = label;
        this.quantity = quantity;
        this.comment = comment;
        this.isRemoved = isRemoved;
        this.storeIdx = storeIdx;
    }

    static fromJson(json: any): ContainerItem {
        return new ContainerItem({
            idx: json.idx,
            label: json.label,
            quantity: json.quantity,
            comment: json.comment,
            isRemoved: json.isRemoved,
            storeIdx: json.storeIdx
        });
    }
}

export enum ContainerType {
    Refridgerator = 'refridgerator',
    Freezer = 'freezer',
    Pantry = 'pantry',
    Cupboard = 'cupboard',
    Drawer = 'drawer',
    Other = 'other'
}


export class Container {
    idx: number;
    name: string;
    type: ContainerType;
    householdIdx: number;
    comment: string;

    constructor({
        idx = -1,
        name = '',
        type = ContainerType.Other,
        householdIdx = -1,
        comment = ''
    } : {
        idx?: number,
        name?: string,
        type?: ContainerType,
        householdIdx?: number,
        comment?: string
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.type = type;
        this.householdIdx = householdIdx;
        this.comment = comment;
    }

    public get icon(): string {
        return `./icons/container/container-icon-${this.type}.png`;
    };

    static fromJson(json: any): Container {
        return new Container({
            idx: json.idx,
            name: json.name,
            type: json.type,
            householdIdx: json.householdIdx,
            comment: json.comment
        });
    }

}