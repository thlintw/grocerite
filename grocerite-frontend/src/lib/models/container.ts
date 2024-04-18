import { ItemCategory } from "./item";

export class ContainerItem{
    idx: number;
    name: string;
    quantity: number;
    comment: string;
    isRemoved: boolean;
    storeIdx: number;
    category: ItemCategory;

    constructor({
        idx = -1,
        name = '',
        quantity = 0,
        comment = '',
        isRemoved = false,
        storeIdx = -1,
        category = ItemCategory.Other
    } : {
        idx?: number,
        name?: string,
        quantity?: number,
        comment?: string,
        isRemoved?: boolean,
        storeIdx?: number,
        category?: ItemCategory
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.quantity = quantity;
        this.comment = comment;
        this.isRemoved = isRemoved;
        this.storeIdx = storeIdx;
        this.category = category;
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
            category: cate
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