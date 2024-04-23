<script lang="ts">
    import { Container, ContainerItem, ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import type { IconDefinition, icon } from '@fortawesome/fontawesome-svg-core';
    import { faUserAltSlash, faXmark } from '@fortawesome/free-solid-svg-icons';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import SearchableFormInput from './SearchableFormInput.svelte';
    import { createEventDispatcher } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';
    import type { SelectCandidate } from '$lib/types/general';
    import IconSelectionDialog from './IconSelectionDialog.svelte';
    import ScrollableSelectDialog from './ScrollableSelectDialog.svelte';
    import { ItemCategory } from '$lib/models/item';
    import Button from './Button.svelte';
    import QuantitySelectionDialog from './QuantitySelectionDialog.svelte';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title: string = '';
    export let availableItems: SelectCandidate[] = [];
    export let availableContainers: Container[] = [];

    let itemName = '';
    let itemCategory: ItemCategory = ItemCategory.Vegetables;
    let itemQuantity = 1;
    let itemContainer: Container | null = null;

    let showCategoryDialog = false;
    const setCategoryDialog = (value) => {
        showCategoryDialog = value;
    };

    let showQuantityDialog = false;
    const setQuantityDialog = (value) => {
        showQuantityDialog = value;
    };

    let showContainerDialog = false;
    const setContainerDialog = (value) => {
        showContainerDialog = value;
    };

    const onSelect = (selected) => {
        dispatch('click:selectOption', { selected });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    const getCategoryOptions = () => {
        return Object.values(ItemCategory).map((category) => {
            return {
                value: category,
                label: $_(`common_category_${category}`),
                iconPath: `/icons/itemCategory/itemCategory-icon-${category}.png`,
            };
        });
    };

    const getItemCategory = (value: string) => {
        itemCategory = value as ItemCategory;
        setCategoryDialog(false);
    };

    const getContainer = (value: string) => {
        itemContainer = availableContainers.find((container) => container.idx.toString() === value) || null;
        setContainerDialog(false);
    };

    const itemQuantityControl = (mode: '--' | '-' | '+' | '++') => {
        switch (mode) {
            case '--':
                if (itemQuantity > 10) {
                    itemQuantity -= 10;
                } else {
                    itemQuantity = 1;
                }
                break;
            case '-':
                if (itemQuantity > 1) {
                    itemQuantity--;
                }
                break;
            case '+':
                itemQuantity++;
                break;
            case '++':
                itemQuantity += 10;
                break;
        }
    };

    const getContainerOptions = () => {
        return availableContainers.map((container) => {
            return {
                value: container.idx.toString(),
                label: container.name,
                iconPath: `/icons/container/container-icon-${container.type}.png`,
            };
        });
    };

    
</script>

{#if showDialog}

    <QuantitySelectionDialog
        showDialog={showQuantityDialog}
        title="groceryList_addListItemsQuantityPlaceholder"
        value={itemQuantity}
        on:click:barrierDismiss={(e) => {
            setQuantityDialog(false);
        }}
        on:click:minus={() => itemQuantityControl('-')}
        on:click:doubleMinus={() => itemQuantityControl('--')}
        on:click:plus={() => itemQuantityControl('+')}
        on:click:doublePlus={() => itemQuantityControl('++')}
        />


    <ScrollableSelectDialog 
        showDialog={showCategoryDialog}
        options={getCategoryOptions()}
        title="groceryList_addListItemsCategorySelect"
        hasFilter={true}
        on:click:selectOption={(e) => {
            getItemCategory(e.detail.option.value);
        }}
        on:click:barrierDismiss={(e) => {
            setCategoryDialog(false);
        }}
    />


    <ScrollableSelectDialog 
        showDialog={showContainerDialog}
        options={getContainerOptions()}
        title="groceryList_addListItemsContainerSelect"
        hasFilter={true}
        on:click:selectOption={(e) => {
            getContainer(e.detail.option.value);
        }}
        on:click:barrierDismiss={(e) => {
            setContainerDialog(false);
        }}
    />

    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[10008] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[10009] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[10010] flex flex-col lg:w-[40rem] 2xl:w-[55rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                <div class="drop-shadow-title">{ $_(title) }</div>
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-7 px-5
                shadow-grocerite-orange-200-sm {$lc.text} flex-col items-center">

                <div class="relative flex w-full">

                    <SearchableFormInput 
                        label={$_('groceryList_addListItemsName')}
                        placeholder={$_('groceryList_addListItemsNamePlaceholder')}
                        bind:value={itemName}
                        candidates={availableItems}
                    />
                </div>
                <div class="w-full grid grid-cols-1 2xl:grid-cols-3 gap-3">
                
                    <div class="flex w-full flex-col">
                        <div class="text-lg text-emerald-700 font-bold">
                            Category
                        </div>
                        <div class="px-3">
                            <button type="button" 
                                class="flex items-center gap-2 rounded-xl px-3 py-2 bg-orange-100"
                                on:click={() => setCategoryDialog(true)}>
                                <div>
                                    <img src="/icons/itemCategory/itemCategory-icon-{itemCategory}.png" 
                                        alt="category icon" class="w-12" />
                                </div>
                                <div class="text-left text-neutral-700">{$_(`common_category_${itemCategory}`)}</div>
                            </button>
                        </div>
                    </div>

                    <div class="flex w-full flex-col">
                        <div class="text-lg text-emerald-700 font-bold">
                            Quantity
                        </div>
                        <div class="px-3">
                            <button type="button" 
                                class="flex items-center gap-2 rounded-xl px-3 py-2 bg-orange-100"
                                on:click={() => setQuantityDialog(true)}>
                                <div class="text-xl h-12 font-bold flex items-center justify-center">
                                    {itemQuantity}
                                </div>
                            </button>
                        </div>
                    </div>

                    <div class="flex w-full flex-col">
                        <div class="text-lg text-emerald-700 font-bold">
                            Target Container
                        </div>
                        <div class="px-3">
                            <button type="button" 
                                class="flex items-center gap-2 rounded-xl px-3 py-2 bg-orange-100"
                                on:click={() => setContainerDialog(true)}>
                                <div class="flex items-center gap-2">
                                    {#if !itemContainer}
                                        <div class="h-12 font-normal text-base text-neutral-400 flex justify-center items-center ">{$_('groceryList_addListItemsContainerSelectPrompt')}</div>
                                    {:else}
                                    <div>
                                        <img src="/icons/container/container-icon-{itemContainer.type}.png" 
                                            alt="category icon" class="w-12" />
                                    </div>
                                    <div class="text-left text-neutral-700">{itemContainer.name}</div>
                                    {/if}
                                </div>
                            </button>
                        </div>
                    </div>


                </div>

                
            </div>
        </div>
    </div>
{/if}