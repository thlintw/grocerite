<script lang="ts">
    import { onMount } from 'svelte';
    import { GroceryList, GroceryListItem } from '$lib/models/groceryList';
    import { ItemCategory, getItemCategoryIcon } from '$lib/models/item';
    import { _ } from 'svelte-i18n';
	import { lc } from '$lib/stores/general';

    onMount(() => {
        console.log('onMount');
    });

    const mockList = new GroceryList({
        idx: 1,
        name: 'starving to death im  so hunnnngry oh my  god',
        householdIdx: 1,
        iconIdx: 2,
        starred: true,
        items: [
            new GroceryListItem({
                idx: 1,
                name: 'Bread',
                quantity: 1,
                ticked: false,
                category: ItemCategory.BakeryAndBread
            }),
            new GroceryListItem({
                idx: 6,
                name: 'Tissue paper',
                quantity: 1,
                ticked: false,
                category: ItemCategory.HouseholdEssentials
            }),
            new GroceryListItem({
                idx: 12,
                name: 'Potato',
                quantity: 1,
                ticked: false,
                category: ItemCategory.Vegetables
            }),
            new GroceryListItem({
                idx: 13,
                name: 'Brussel sprouts',
                quantity: 1,
                ticked: false,
                category: ItemCategory.Vegetables
            }),
            new GroceryListItem({
                idx: 133,
                name: 'Apple pie',
                quantity: 1,
                ticked: false,
                category: ItemCategory.BakeryAndBread
            }),
            new GroceryListItem({
                idx: 1,
                name: 'drrrrrillll',
                quantity: 1,
                ticked: false,
                category: ItemCategory.ToolsAndHomeImprovement
            }),
            new GroceryListItem({
                idx: 1,
                name: '槓片',
                quantity: 1,
                ticked: false,
                category: ItemCategory.FitnessAndSports
            }),
            new GroceryListItem({
                idx: 13,
                name: 'appple',
                quantity: 1,
                ticked: false,
                category: ItemCategory.Fruits
            }),
            new GroceryListItem({
                idx: 138,
                name: 'bananna',
                quantity: 1,
                ticked: false,
                category: ItemCategory.Fruits
            }),
        ]
    });
    
    // Assuming GroceryListItem and mockList are defined as before
    
    // Create an array of enum values in the order they were declared
    const categoryOrder = Object.values(ItemCategory);

    // Function to get ordinal of category based on enum declaration
    const getCategoryOrdinal = (category) => categoryOrder.indexOf(category);

    // Group items by category
    let groupedItems = mockList.items.reduce((acc, item) => {
        (acc[item.category] = acc[item.category] || []).push(item);
        return acc;
    }, {});

    // Sort categories by enum order and items within each category by idx
    let sortedCategories = Object.keys(groupedItems).sort(
        (a, b) => getCategoryOrdinal(a) - getCategoryOrdinal(b)
    );

</script>

<div class="flex flex-col w-full">
    <div class="{$lc.title} text-2xl text-orange-500">
        {mockList.name}

    </div>
    
    <div class="
        flex flex-col
        w-full h-full gap-5
        pb-32 lg:pb-3
        mt-5
    ">
        {#each sortedCategories as category}
            <div class="w-full bg-orange-50 px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl shadow-grocerite-orange-200-sm">
                <div class="flex items-center w-full gap-2 border-b-2 border-b-orange-100 pb-1">
                    <h3 class="text-lg lg:text-xl text-orange-500 {$lc.title}">{$_(`common_category_${category}`)}</h3>
                    <img src={getItemCategoryIcon(category)} alt="{category}" class="ml-auto w-8 lg:w-10" />
                </div>
                <ul class="">
                {#each groupedItems[category].sort((a, b) => a.idx - b.idx) as item}
                    <li>{item.idx} - {item.name} ({item.quantity})</li>
                {/each}
                </ul>
            </div>
        {/each}
    </div>
</div>
