import { Item } from './item';
import { Member } from './household';

export class GroceryListItem extends Item {
    idx: number;
    label: string;
    quantity: number;
    ticked: boolean;
    tickedBy?: Member | null;
    storeIdx: number;
    targetContainerIdx: number;
    iconIdx: number;

    constructor({
        idx = -1,
        name = '',
        category = null,
        icon = null,
        label = '',
        quantity = 0,
        ticked = false,
        tickedBy = null,
        storeIdx = -1,
        targetContainerIdx = -1,
        iconIdx = -1
    } : {
        idx?: number,
        name?: string,
        category?: any,
        icon?: any,
        label?: string,
        quantity?: number,
        ticked?: boolean,
        tickedBy?: Member | null,
        storeIdx?: number,
        targetContainerIdx?: number,
        iconIdx?: number
    } = {}) {
        super({name, category, icon});
        this.idx = idx;
        this.label = label;
        this.quantity = quantity;
        this.ticked = ticked;
        this.tickedBy = tickedBy;
        this.storeIdx = storeIdx;
        this.targetContainerIdx = targetContainerIdx;
        this.iconIdx = iconIdx;
    }

    static fromJson(json: any): GroceryListItem {
        return new GroceryListItem({
            idx: json.idx,
            name: json.name,
            category: json.category,
            icon: json.icon,
            label: json.label,
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
    starred: boolean; // meaning asignee = currentUser
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
        starred = false,
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
        this.starred = starred;
        this.name = name;
        this.description = description;
        this.asignee = asignee;
        this.items = items;
        this.householdIdx = householdIdx;
        this.deadline = deadline;
        this.deadlineString = deadlineString;
        this.iconIdx = iconIdx;
    }

    public get icon(): string {
        const paddedIdx = this.iconIdx.toString().padStart(2, '0');
        return `./icons/groceryList/groceryList-icon-${paddedIdx}.png`;
    }

    static fromJson(json: any): GroceryList {
        return new GroceryList({
            idx: json.idx,
            starred: json.starred,
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