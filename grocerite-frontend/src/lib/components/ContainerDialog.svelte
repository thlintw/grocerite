<script lang="ts">
    import { Container, ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import type { SelectCandidate } from '$lib/types/general';
    import { createEventDispatcher } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';
    import Button from './Button.svelte';
    import FormInput from './FormInput.svelte';
    import ScrollableSelectDialog from './ScrollableSelectDialog.svelte';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title: string = '';
    export let currentEditItem: Container | null;

    let containerName = '';
    let containerType: ContainerType = ContainerType.Refrigerator;
    let itemQuantity = 1;
    let itemContainer: Container | null = null;

    let showCategoryDialog = false;
    const setCategoryDialog = (value) => {
        showCategoryDialog = value;
    };

    const onAddItem = () => {
        let container: Container;
        if (!currentEditItem) {
            container = new Container({
                idx: -1,
                name: containerName,
                type: containerType,
                householdIdx: -1,
            });
        } else {
            currentEditItem.name = containerName;
            currentEditItem.type = containerType;
            container = currentEditItem;
        }
        dispatch('click:addItem', { container });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    const getContainerTypeOptions = () => {
        return Object.values(ContainerType).map((category) => {
            return {
                value: category,
                label: $_(`common_containerType_${category}`),
                iconPath: `/icons/container/container-icon-${category}.png`,
            };
        });
    };

    const getContainerType = (value: string) => {
        containerType = value as ContainerType;
        setCategoryDialog(false);
    };



    let buttonLoading = false;

    const reset = () => {
        containerName = '';
        containerType = ContainerType.Refrigerator;
        itemQuantity = 1;
        itemContainer = null;
    };


    $: {
        if (showDialog) {
            console.log('showDialog');
            reset();
            console.log(currentEditItem);
            if (currentEditItem) {
                containerName = currentEditItem.name;
                containerType = currentEditItem.type;
            }
        }
    }
    
    
</script>

{#if showDialog}


    <ScrollableSelectDialog 
        showDialog={showCategoryDialog}
        options={getContainerTypeOptions()}
        title="groceryList_addListItemsCategorySelect"
        hasFilter={true}
        on:click:selectOption={(e) => {
            getContainerType(e.detail.option.value);
        }}
        on:click:barrierDismiss={(e) => {
            setCategoryDialog(false);
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

                    <FormInput 
                        label={$_('groceryList_addListItemsName')}
                        placeholder={$_('groceryList_addListItemsNamePlaceholder')}
                        bind:value={containerName}
                        on:select={(e) => {
                            containerName = e.detail[0].label;
                        }}
                    />
                </div>
                <div class="w-full grid grid-cols-1 2xl:grid-cols-3 gap-3">
                
                    <div class="flex w-full flex-col">
                        <div class="text-lg text-emerald-700 font-bold">
                            {$_('household_newHouseholdContanerType')}
                        </div>
                        <div class="px-3">
                            <button type="button" 
                                class="flex items-center gap-2 rounded-xl px-3 py-2 bg-orange-100"
                                on:click={() => setCategoryDialog(true)}>
                                <div>
                                    <img src="/icons/container/container-icon-{containerType}.png" 
                                        alt="category icon" class="w-12" />
                                </div>
                                <div class="text-left text-neutral-700">{$_(`common_containerType_${containerType}`)}</div>
                            </button>
                        </div>
                    </div>



                </div>
                
                <div>
                    <Button 
                        loading={buttonLoading}
                        text={$_('household_newHouseholdContainerAdd')}
                        on:click={onAddItem}
                    />
                </div>
                
            </div>
        </div>
    </div>
{/if}