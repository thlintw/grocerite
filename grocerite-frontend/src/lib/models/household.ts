import { UserProfile } from "./userProfile";
import { GroceryList } from "./groceryList";
import { Container } from "./container";
import { Store } from "./store";

export class Member {
    user?: UserProfile | null;
    userIdx: number;
    pfpIdx: number;
    householdIdx: number;

    constructor({
        user = null,
        userIdx = -1,
        pfpIdx = -1,
        householdIdx = -1
    } : {
        user?: UserProfile | null,
        userIdx?: number,
        pfpIdx?: number,
        householdIdx?: number
    } = {}) {
        this.user = user;
        this.userIdx = userIdx;
        this.pfpIdx = pfpIdx;
        this.householdIdx = householdIdx;
    }

    static fromJson(json: any): Member {
        return new Member({
            user: UserProfile.fromJson(json.user),
            userIdx: json.userIdx,
            pfpIdx: json.pfpIdx,
            householdIdx: json.householdIdx
        });
    }
}


export class Household {
    idx: number;
    name: string;
    members: Member[];
    containers: Container[];
    groceryLists: GroceryList[];
    iconIdx: number;
    stores: Store[];

    constructor({
        idx = -1,
        name = '',
        members = [],
        containers = [],
        groceryLists = [],
        iconIdx = -1,
        stores = []
    } : {
        idx?: number,
        name?: string,
        members?: Member[],
        containers?: Container[],
        groceryLists?: GroceryList[],
        iconIdx?: number,
        stores?: Store[]
    } = {}) {
        this.idx = idx;
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
            name: json.name,
            members: json.members.map((member: any) => Member.fromJson(member)),
            containers: json.containers.map((container: any) => Container.fromJson(container)),
            groceryLists: json.groceryLists.map((groceryList: any) => GroceryList.fromJson(groceryList)),
            iconIdx: json.iconIdx,
            stores: json.stores.map((store: any) => Store.fromJson(store))
        });
    }
}