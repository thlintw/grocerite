<script lang="ts">
    import { onMount } from 'svelte';
    import { Member } from '$lib/models/household';
    import { GroceryList, GroceryListItem } from '$lib/models/groceryList';
    import { ItemCategory, getItemCategoryIcon } from '$lib/models/item';
    import { _ } from 'svelte-i18n';
	import { lc } from '$lib/stores/general';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { faCheck, faEllipsisVertical, faUser, faCalendar, faBagShopping, faAsterisk, faPen, faTrash, faBars } from '@fortawesome/free-solid-svg-icons';
    import { properCapitalize } from '$lib/utilities';
    import { fade, scale } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
    import ActionMenu from '$lib/components/ActionMenu.svelte';
    import { showLoadingOverlay } from '$lib/stores/general';
    import { dialog } from '$lib/stores/dialogStore';
    import { getItemsCategoryOrder } from '$lib/utilities';
    import GroceryListCategoryPlaceholder from '$lib/components/GroceryListCategoryPlaceholder.svelte';

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
                tickedBy: new Member({
                    userIdx: 1,
                    name: 'Annie',
                }),
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

    let groupedItems = getItemsCategoryOrder(mockList.items);

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

    let showActionMenu = false;
    
    const openActionMenu = () => {
        console.log('open action menu');
        showActionMenu = true;
    };

    const closeActionMenu = () => {
        showActionMenu = false;
    };

    const actionMenuItems = [
        {
            title: 'groceryList_completeThisList',
            icon: faCheck,
            action: () => {
                closeActionMenu();
                dialog.openDialog({
                    title: 'common_confirm',
                    message: 'groceryList_sureWantToComplete',
                    onConfirm: () => {
                        console.log('complete this list');
                        dialog.closeDialog();
                        showLoading();
                        let ival = setInterval(() => {
                            hideLoading();
                            clearInterval(ival);
                        }, 4000);
                    }
                });
            }
        },
        {
            title: 'groceryList_editThisList',
            icon: faPen,
            action: () => {
                console.log('delete this list');
            }
        },
        {
            title: 'groceryList_deleteThisList',
            icon: faTrash,
            action: () => {
                closeActionMenu();
                dialog.openDialog({
                    title: 'common_confirm',
                    message: 'groceryList_sureWantToDelete',
                    onConfirm: () => {
                        console.log('delete this list');
                        dialog.closeDialog();
                    }
                });
            }
        },
    ];


    const showLoading = () => {
        showLoadingOverlay.set(true);
    };

    const hideLoading = () => {
        showLoadingOverlay.set(false);
    };
</script>

<div class="flex flex-col w-full gap-3">
    <ActionMenu
        showActionMenu={showActionMenu}
        menuTitle={'common_actions'}
        actionMenuItems={actionMenuItems}
        on:click:closeMenu={closeActionMenu}
        />

    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        {#if mockList.starred}
            <div class="text-yellow-400 text-3xl mr-2">
                <FontAwesomeIcon icon={faAsterisk} />
            </div>
        {/if}
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">{properCapitalize(mockList.name)}</span>
    </div>
    <div class="flex text-sm gap-3 {$lc.text}">
        {#if mockList.asignee}
            <div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1 text-base lg:text-lg items-center">
                <div class="text-emerald-600">
                    <FontAwesomeIcon
                        icon={faUser}
                        class="text-emerald-600"
                    />
                </div>
                <div class="text-neutral-800">
                    {mockList.asignee.name}
                </div>
            </div>
        {/if}
        <div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1 text-base lg:text-lg items-center">
            <div class="text-emerald-600">
                <FontAwesomeIcon
                    icon={faCalendar}
                    class="text-emerald-600"
                />
            </div>
            <div class="text-neutral-800">
                2024-12-31
            </div>
        </div>
        <div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1 text-base lg:text-lg items-center">
            <div class="text-emerald-600">
                <FontAwesomeIcon
                    icon={faBagShopping}
                    class="text-emerald-600"
                />
            </div>
            <div class="text-neutral-800">
                {tickedCount.toLocaleString()} / {totalItemCount.toLocaleString()}
            </div>
        </div>
        <button type="button" class="bg-orange-50 rounded-md px-1.5 py-0.5 ml-auto text-orange-500 flex items-center"
            on:click={openActionMenu} on:touchstart={openActionMenu}>
            <FontAwesomeIcon icon={faBars} class="w-6 h-6"/>
        </button>
    </div>
    
    <div class="
        flex flex-col
        w-full h-full gap-5
        pb-32 lg:pb-3
        mt-2
    "> 
        <GroceryListCategoryPlaceholder />
        {#each Object.values(ItemCategory) as category}
            {#if groupedItems[category]}
                <div class="w-full bg-orange-50 px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl shadow-grocerite-orange-200-sm">
                    <div class="flex items-center w-full gap-2 border-b-2 border-b-orange-100 pb-2">
                        <h3 class="text-xl lg:text-2xl text-orange-500 {$lc.title}">{$_(`common_category_${category}`)}</h3>
                        <img src={getItemCategoryIcon(category)} alt="{category}" class="ml-auto w-8 lg:w-10" />
                    </div>
                    <div class="flex flex-col gap-2 mb-2">
                        {#each groupedItems[category] as item}
                            <div class="flex items-center text-neutral-700">
                                <button type="button" class="relative border-2 bg-orange-100 border-orange-200 w-8 h-8 rounded-lg shrink-0
                                    flex justify-center items-center"
                                    on:click={() => item instanceof GroceryListItem ? tickingHandler(item) : null}>
                                    {#if apiLoading.includes(item.idx)}
                                        <div 
                                            class="animate-spin rounded-full h-4 w-4 border-2 border-b-transparent border-orange-200"></div>
                                    {:else if tickedItemIdxs.includes(item.idx) && !apiLoading.includes(item.idx)}
                                        <div class="absolute -top-[2px] -left-[2px] w-9 h-9 text-emerald-600"
                                        transition:fade>
                                            <FontAwesomeIcon 
                                                icon={faCheck}
                                                class="w-9 h-9"
                                                />
                                        </div>
                                    {/if}
                                </button>
                                <div class="text-xl {$lc.text} font-mono text-center w-16 font-bold shrink-0">{item.quantity}</div>
                                <div class="{$lc.text} text-base lg:text-lg overflow-hidden text-ellipsis text-nowrap pr-2 flex items-center">
                                    {#if tickedItemIdxs.includes(item.idx)}
                                        <span class="line-through text-neutral-400">{item.name}</span>
                                    {:else}
                                        <span class="">{item.name}</span>
                                    {/if}
                                    {#if item instanceof GroceryListItem && item.tickedBy}
                                        <span class="ml-2 border-2 border-neutral-300 rounded-md text-neutral-400 text-sm px-1.5 py-0.5 flex gap-1">
                                            <span>
                                                <FontAwesomeIcon
                                                    icon={faCheck}
                                                />
                                            </span>
                                            <span>{$_('common_by')} {item.tickedBy.name}</span>
                                        </span>
                                    {/if}
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
        {/each}
    </div>
</div>
