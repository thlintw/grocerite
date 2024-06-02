import { UserProfile } from "./userProfile";
import { GroceryList } from "./groceryList";
import { Container } from "./container";
import { Store } from "./store";

export interface Pfp {
    presenting: 'mp' | 'fp' | 'nb';
    idx: number;
    bgColor: string;
}

export class Member {
    user?: UserProfile | null;
    userIdx: number;
    pfp: Pfp;
    householdIdx: number;
    name: string;
    isCreator: boolean;

    constructor({
        user = null,
        userIdx = -1,
        pfp = {} as Pfp,
        householdIdx = -1,
        name = '',
        isCreator = false
    } : {
        user?: UserProfile | null,
        userIdx?: number,
        pfp?: Pfp,
        householdIdx?: number,
        name?: string,
        isCreator? : boolean
    } = {}) {
        this.user = user;
        this.userIdx = userIdx;
        this.pfp = pfp;
        this.householdIdx = householdIdx;
        this.name = name;
        this.isCreator = isCreator;
    }


    static fromJson(json: any): Member {
        return new Member({
            // user: UserProfile.fromJson(json.user),
            userIdx: json.userIdx,
            pfp: json.pfp,
            householdIdx: json.householdIdx,
            name: json.name,
            isCreator: json.isCreator
        });
    }
}


export class Household {
    idx: number;
    householdId: string;
    name: string;
    members: Member[];
    containers: Container[];
    groceryLists: GroceryList[];
    iconIdx: number;
    stores: Store[];

    constructor({
        idx = -1,
        householdId = 'H-',
        name = '',
        members = [],
        containers = [],
        groceryLists = [],
        iconIdx = -1,
        stores = []
    } : {
        idx?: number,
        householdId?: string,
        name?: string,
        members?: Member[],
        containers?: Container[],
        groceryLists?: GroceryList[],
        iconIdx?: number,
        stores?: Store[]
    } = {}) {
        this.idx = idx;
        this.householdId = householdId;
        this.name = name;
        this.members = members;
        this.containers = containers;
        this.groceryLists = groceryLists;
        this.iconIdx = iconIdx;
        this.stores = stores;
    }

    public get icon(): string {
        const paddedIdx = this.iconIdx.toString().padStart(2, '0');
        return `./icons/household/household-icon-${paddedIdx}.png`;
    }

    static fromJson(json: any): Household {
        return new Household({
            idx: json.idx,
            householdId: json.householdId,
            name: json.name,
            members: json.members.map((member: any) => Member.fromJson(member)),
            containers: json.containers.map((container: any) => Container.fromJson(container)),
            groceryLists: json.groceryLists.map((groceryList: any) => GroceryList.fromJson(groceryList)),
            iconIdx: json.iconIdx,
            // stores: json.stores.map((store: any) => Store.fromJson(store))
        });
    }
}