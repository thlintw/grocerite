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
    Fridge,
    Freezer,
    Pantry,
    Cupboard,
    Drawer,
    Other
}

export enum ContainerIcon {

}

export class Container {
    idx: number;
    name: string;
    type: ContainerType;
    icon: ContainerIcon | null;
    householdIdx: number;
    comment: string;

    constructor({
        idx = -1,
        name = '',
        type = ContainerType.Other,
        icon = null,
        householdIdx = -1,
        comment = ''
    } : {
        idx?: number,
        name?: string,
        type?: ContainerType,
        icon?: ContainerIcon | null,
        householdIdx?: number,
        comment?: string
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.type = type;
        this.icon = icon;
        this.householdIdx = householdIdx;
        this.comment = comment;
    }

    static fromJson(json: any): Container {
        return new Container({
            idx: json.idx,
            name: json.name,
            type: json.type,
            icon: json.icon,
            householdIdx: json.householdIdx,
            comment: json.comment
        });
    }

}