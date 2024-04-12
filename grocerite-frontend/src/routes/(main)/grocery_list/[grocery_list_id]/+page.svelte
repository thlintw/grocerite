<script lang="ts">
    import { onMount } from 'svelte';
    import { Member } from '$lib/models/household';
    import { GroceryList, GroceryListItem } from '$lib/models/groceryList';
    import { ItemCategory, getItemCategoryIcon } from '$lib/models/item';
    import { _ } from 'svelte-i18n';
	import { lc } from '$lib/stores/general';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { faCheck, faEllipsisVertical, faUser, faCalendar, faBagShopping, faAsterisk, faTimes } from '@fortawesome/free-solid-svg-icons';
    import { properCapitalize } from '$lib/utilities';
    import { fade, scale } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';

    onMount(() => {
        console.log('onMount');
    });

    const mockList = new GroceryList({
        idx: 1,
        name: 'Sample list barstarotn aroiuftnorabh aorfuntoara aorfutnorafntora',
        deadlineString: '2024-12-31',
        asignee: new Member({
            userIdx: 1,
            name: 'Steve Jobs',
        }),
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
                ticked: true,
                category: ItemCategory.HouseholdEssentials
            }),
            new GroceryListItem({
                idx: 112,
                name: 'Potato',
                quantity: 1,
                ticked: true,
                category: ItemCategory.Vegetables
            }),
            new GroceryListItem({
                idx: 1335,
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
                quantity: 14,
                ticked: false,
                category: ItemCategory.ToolsAndHomeImprovement
            }),
            new GroceryListItem({
                idx: 1344,
                name: '槓片',
                quantity: 1,
                ticked: false,
                category: ItemCategory.FitnessAndSports
            }),
            new GroceryListItem({
                idx: 123,
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
            new GroceryListItem({
                idx: 1385,
                name: 'bananna anana nanrsot arosentofuav aornfoatunrtao rufarobaorufs',
                quantity: 1,
                ticked: false,
                category: ItemCategory.BakeryAndBread
            }),
        ]
    });
    
    const categoryOrder = Object.values(ItemCategory);

    const getCategoryOrdinal = (category) => categoryOrder.indexOf(category);

    let groupedItems = mockList.items.reduce((acc, item) => {
        (acc[item.category] = acc[item.category] || []).push(item);
        return acc;
    }, {});

    let sortedCategories = Object.keys(groupedItems).sort(
        (a, b) => getCategoryOrdinal(a) - getCategoryOrdinal(b)
    );

    let apiLoading: number[] = [];

    const pushApiLoading = (idx: number) => {
        if (!apiLoading.includes(idx)) apiLoading = [...apiLoading, idx];
    };

    let intervals: {[key: number]: NodeJS.Timeout} = {};

    let tickedItemIdxs: number[] = mockList.items.filter((i) => i.ticked).map((i) => i.idx);

    const tickingHandler = (item: GroceryListItem) => {
        pushApiLoading(item.idx);
        intervals[item.idx] = setInterval(() => {
            apiLoading = apiLoading.filter((i) => i !== item.idx);
            item.ticked = !item.ticked;
            tickedItemIdxs = item.ticked ? [...tickedItemIdxs, item.idx] : tickedItemIdxs.filter((i) => i !== item.idx);
            clearInterval(intervals[item.idx]);
        }, 1000);
    };

    $: tickedCount = mockList.items.filter((i) => i.ticked).length;
    $: totalItemCount = mockList.items.length;

    let showActionDialog = false;

    const openActionDialog = () => {
        showActionDialog = true;
    };

    const closeActionDialog = () => {
        showActionDialog = false;
    };

</script>

<div class="flex flex-col w-full gap-3">
    {#if showActionDialog}
        <button transition:fade
            class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20" 
            on:click={closeActionDialog}></button>
        <div transition:scaleFade
            class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
                flex items-center justify-center">
            <div class="pointer-events-auto z-[11002]flex flex-col
                ">
                <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                    relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                    {$_('common_actions')}
                </div>
                <div class="bg-orange-50 rounded-xl flex flex-col gap-3 px-3 py-3 pt-4
                    shadow-grocerite-orange-200-sm">
                    <div class="hover:bg-orange-100 rounded-md">
                        <button type="button" class="w-full flex text-orange-500 {$lc.text} text-xl">
                            {$_('groceryList_completeThisList')}
                        </button>
                    </div>

                </div>
            </div>
        </div>
    {/if}

    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        {#if mockList.starred}
            <div class="text-yellow-400 text-3xl mr-2">
                <FontAwesomeIcon icon={faAsterisk} />
            </div>
        {/if}
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">{properCapitalize(mockList.name)}</span>
        <button type="button" class="ml-auto"
            on:click={openActionDialog}>
            <FontAwesomeIcon icon={faEllipsisVertical} class="w-6 h-6"/>
        </button>
    </div>
    <div class="flex text-sm gap-3 {$lc.text}">
        {#if mockList.asignee}
            <div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1 text-base lg:text-lg items-center">
                <div class="text-lime-600">
                    <FontAwesomeIcon
                        icon={faUser}
                        class="text-lime-600"
                    />
                </div>
                <div class="text-neutral-800">
                    {mockList.asignee.name}
                </div>
            </div>
        {/if}
        <div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1 text-base lg:text-lg items-center">
            <div class="text-lime-600">
                <FontAwesomeIcon
                    icon={faCalendar}
                    class="text-lime-600"
                />
            </div>
            <div class="text-neutral-800">
                2024-12-31
            </div>
        </div>
        <div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1 text-base lg:text-lg items-center">
            <div class="text-lime-600">
                <FontAwesomeIcon
                    icon={faBagShopping}
                    class="text-lime-600"
                />
            </div>
            <div class="text-neutral-800">
                {tickedCount.toLocaleString()} / {totalItemCount.toLocaleString()}
            </div>
        </div>
    </div>
    
    <div class="
        flex flex-col
        w-full h-full gap-5
        pb-32 lg:pb-3
        mt-2
    ">
        {#each sortedCategories as category}
            <div class="w-full bg-orange-50 px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl shadow-grocerite-orange-200-sm">
                <div class="flex items-center w-full gap-2 border-b-2 border-b-orange-100 pb-2">
                    <h3 class="text-xl lg:text-2xl text-orange-500 {$lc.title}">{$_(`common_category_${category}`)}</h3>
                    <img src={getItemCategoryIcon(category)} alt="{category}" class="ml-auto w-8 lg:w-10" />
                </div>
                <div class="flex flex-col gap-2 mb-2">
                {#each groupedItems[category].sort((a, b) => a.idx - b.idx) as item}
                    <div class="flex items-center text-neutral-700">
                        <button type="button" class="relative border-2 bg-orange-100 border-orange-200 w-8 h-8 rounded-lg shrink-0
                            flex justify-center items-center"
                            on:click={() => tickingHandler(item)}>
                            {#if apiLoading.includes(item.idx)}
                                <div 
                                    class="animate-spin rounded-full h-4 w-4 border-2 border-b-transparent border-orange-200"></div>
                            {:else if tickedItemIdxs.includes(item.idx) && !apiLoading.includes(item.idx)}
                                <div class="absolute -top-[2px] -left-[2px] w-9 h-9 text-lime-600"
                                transition:fade>
                                    <FontAwesomeIcon 
                                        icon={faCheck}
                                        class="w-9 h-9"
                                        />
                                </div>
                            {/if}
                        </button>
                        <div class="text-xl {$lc.text} font-mono text-center w-16 font-bold shrink-0">{item.quantity}</div>
                        <div class="{$lc.text} text-base lg:text-lg overflow-hidden text-ellipsis text-nowrap pr-2">
                            {#if tickedItemIdxs.includes(item.idx)}
                                <span class="line-through text-neutral-400">{item.name}</span>
                            {:else}
                                <span class="">{item.name}</span>
                            {/if}
                        </div>
                    </div>
                {/each}
                </div>
            </div>
        {/each}
    </div>
</div>
