import { writable } from "svelte/store";
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
    const output: Record<string, GroceryListItem[] | ContainerItem[]> = {};
    items.forEach(item => {
        const category = item.category;
        if (!output[category]) {
            output[category] = [];
        }
        output[category].push(item);
    });
    return output;
}
