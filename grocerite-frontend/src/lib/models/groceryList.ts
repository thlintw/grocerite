import { Item } from './item';
import { Member } from './household';
import type { ContainerItem } from './container';

export class GroceryListItem extends Item {
    idx: number;
    quantity: number;
    ticked: boolean;
    tickedBy?: Member | null;
    storeIdx: number;
    targetContainerIdx: number;

    constructor({
        idx = -1,
        name = '',
        quantity = 0,
        ticked = false,
        tickedBy = null,
        storeIdx = -1,
        targetContainerIdx = -1,
        ...itemProps
    } : {
        idx?: number,
        name?: string,
        quantity?: number,
        ticked?: boolean,
        tickedBy?: Member | null,
        storeIdx?: number,
        targetContainerIdx?: number,
    } & Partial<Item> = {}) {
        super({...itemProps, name});
        this.idx = idx;
        this.quantity = quantity;
        this.ticked = ticked;
        this.tickedBy = tickedBy;
        this.storeIdx = storeIdx;
        this.targetContainerIdx = targetContainerIdx;
    }

    static fromJson(json: any): GroceryListItem {
        return new GroceryListItem({
            idx: json.idx,
            name: json.name,
            category: json.category,
            quantity: json.quantity,
            ticked: json.ticked,
            tickedBy: json.tickedBy,
            storeIdx: json.storeIdx,
            targetContainerIdx: json.targetContainerIdx
        });
    }
}

export class GroceryList {
    idx: number;
    name: string;
    description: string;
    asignee: Member | null;
    items: GroceryListItem[];
    householdIdx: number;
    deadline: Date;
    deadlineString: string;
    iconIdx: number;

    constructor({
        idx = -1,
        name = '',
        description = '',
        asignee = null,
        items = [],
        householdIdx = -1,
        deadline = new Date(),
        deadlineString = '',
        iconIdx = -1
    } : {
        idx?: number,
        starred?: boolean,
        name?: string,
        description?: string,
        asignee?: Member | null,
        items?: GroceryListItem[],
        householdIdx?: number,
        deadline?: Date,
        deadlineString?: string,
        iconIdx?: number
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.description = description;
        this.asignee = asignee;
        this.items = items;
        this.householdIdx = householdIdx;
        this.deadline = deadline;
        this.deadlineString = deadlineString;
        this.iconIdx = iconIdx;
    }

    public get starred(): boolean {
        // to be implemented
        return false;
    }

    public get icon(): string {
        const paddedIdx = this.iconIdx.toString().padStart(2, '0');
        return `/icons/groceryList/groceryList-icon-${paddedIdx}.png`;
    }

    static fromJson(json: any): GroceryList {
        return new GroceryList({
            idx: json.idx,
            name: json.name,
            description: json.description,
            asignee: json.asignee,
            items: json.items.map((item: any) => GroceryListItem.fromJson(item)),
            householdIdx: json.householdIdx,
            deadline: json.deadline,
            deadlineString: json.deadlineString
        });
    }

}