import type { ContainerItem } from "./models/container";
import type { GroceryListItem } from "./models/groceryList";
import { ItemCategory } from "./models/item";

export const properCapitalize = (str: string): string => {
    return str
        .toLowerCase()
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) 
        .join(' ');
}

export const getItemsCategoryOrder = (items: GroceryListItem[] | ContainerItem[])  => {
    const categoryOrder = Object.values(ItemCategory);
    const groupedItems = items.reduce((acc, item) => {
        if (!acc[item.category]) {
            acc[item.category] = [];
        }
        acc[item.category].push(item);
        return acc;
    });
    return groupedItems;
}