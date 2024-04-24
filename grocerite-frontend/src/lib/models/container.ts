import { Item, ItemCategory } from "./item";

export class ContainerItem extends Item{
    idx: number;
    quantity: number;
    isRemoved: boolean;
    storeIdx: number;

    constructor({
        idx = -1,
        name = '',
        quantity = 0,
        isRemoved = false,
        storeIdx = -1,
        ...itemProps
    } : {
        idx?: number,
        name?: string,
        quantity?: number,
        comment?: string,
        isRemoved?: boolean,
        storeIdx?: number,
    } & Partial<Item> = {}) {
        super({...itemProps, name})
        this.idx = idx;
        this.quantity = quantity;
        this.isRemoved = isRemoved;
        this.storeIdx = storeIdx;
    }

    static fromJson(json: any): ContainerItem {
        const cateIdx = json.categoryIdx;
        const cate = ItemCategory[cateIdx];
        return new ContainerItem({
            idx: json.idx,
            name: json.name,
            quantity: json.quantity,
            comment: json.comment,
            isRemoved: json.isRemoved,
            storeIdx: json.storeIdx,
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
    iconIdx: number;

    constructor({
        idx = -1,
        name = '',
        type = ContainerType.Other,
        householdIdx = -1,
        comment = '',
        iconIdx = -1
    } : {
        idx?: number,
        name?: string,
        type?: ContainerType,
        householdIdx?: number,
        comment?: string,
        iconIdx?: number
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.type = type;
        this.householdIdx = householdIdx;
        this.comment = comment;
        this.iconIdx = iconIdx;
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
            comment: json.comment,
            iconIdx: json.iconIdx
        });
    }

}