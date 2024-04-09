import { UserProfile } from "./userProfile";
import { GroceryList } from "./groceryList";
import { Container } from "./container";
import { Store } from "./store";

export class Member {
    user?: UserProfile | null;
    userIdx: number;
    pfpIdx: number;
    householdIdx: number;
    name: string;

    constructor({
        user = null,
        userIdx = -1,
        pfpIdx = -1,
        householdIdx = -1,
        name = ''
    } : {
        user?: UserProfile | null,
        userIdx?: number,
        pfpIdx?: number,
        householdIdx?: number,
        name?: string
    } = {}) {
        this.user = user;
        this.userIdx = userIdx;
        this.pfpIdx = pfpIdx;
        this.householdIdx = householdIdx;
        this.name = name;
    }

    static fromJson(json: any): Member {
        return new Member({
            user: UserProfile.fromJson(json.user),
            userIdx: json.userIdx,
            pfpIdx: json.pfpIdx,
            householdIdx: json.householdIdx,
            name: json.name
        });
    }
}


export class Household {
    idx: number;
    name: string;
    members: Member[];
    containers: Container[];
    groceryLists: GroceryList[];
    stores: Store[];

    constructor({
        idx = -1,
        name = '',
        members = [],
        containers = [],
        groceryLists = [],
        stores = []
    } : {
        idx?: number,
        name?: string,
        members?: Member[],
        containers?: Container[],
        groceryLists?: GroceryList[],
        stores?: Store[]
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.members = members;
        this.containers = containers;
        this.groceryLists = groceryLists;
        this.stores = stores;
    }

    static fromJson(json: any): Household {
        return new Household({
            idx: json.idx,
            name: json.name,
            members: json.members.map((member: any) => Member.fromJson(member)),
            containers: json.containers.map((container: any) => Container.fromJson(container)),
            groceryLists: json.groceryLists.map((groceryList: any) => GroceryList.fromJson(groceryList)),
            stores: json.stores.map((store: any) => Store.fromJson(store))
        });
    }
}