export class ItemCategory {
    idx: number;
    name: string;
    image: string;

    constructor({
        idx = -1,
        name = '',
        image = ''
    } : {
        idx?: number,
        name?: string,
        image?: string
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.image = image;
    }

    static fromJson(json: any): ItemCategory {
        return new ItemCategory({
            idx: json.idx,
            name: json.name,
            image: json.image
        });
    }
}

export enum ItemIcon {

}

export class Item {
    idx: number;
    name: string;
    category: ItemCategory;
    icon: ItemIcon | null;

    constructor({
        idx = -1,
        name = '',
        category = new ItemCategory(),
        icon = null
    } : {
        idx?: number,
        name?: string,
        category?: ItemCategory,
        icon?: ItemIcon | null
    } = {}) {
        this.idx = idx;
        this.name = name;
        this.category = category;
        this.icon = icon;
    }

    static fromJson(json: any): Item {
        return new Item({
            idx: json.idx,
            name: json.name,
            category: ItemCategory.fromJson(json.category),
            icon: json.icon
        });
    }

}
