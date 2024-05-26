<script lang="ts">
    import { Container, ContainerItem, ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import type { IconDefinition, icon } from '@fortawesome/fontawesome-svg-core';
    import { faUserAltSlash, faXmark } from '@fortawesome/free-solid-svg-icons';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import SearchableFormInput from './SearchableFormInput.svelte';
    import { createEventDispatcher, onMount } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';
    import type { SelectCandidate } from '$lib/types/general';
    import IconSelectionDialog from './IconSelectionDialog.svelte';
    import ScrollableSelectDialog from './ScrollableSelectDialog.svelte';
    import { ItemCategory } from '$lib/models/item';
    import Button from './Button.svelte';
    import QuantitySelectionDialog from './QuantitySelectionDialog.svelte';
    import type { GroceryListItem } from '$lib/models/groceryList';
    import FormInput from './FormInput.svelte';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title: string = '';
    export let availableItems: SelectCandidate[] = [];
    export let availableContainers: Container[] = [];

    let memberName = '';
    let buttonLoading = false;

    const onAddItem = () => {
        // const item: GroceryListItem = {
        //     idx: -1,
        //     name: containerName,
        //     category: itemCategory,
        //     quantity: itemQuantity,
        //     targetContainerIdx: itemContainer!.idx,
        //     ticked: false,
        //     storeIdx: -1,
        // };
        dispatch('click:addItem', {  });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    const onSelectColor = (color) => {
        dispatch('click:selectColor', { color });
    };

    const reset = () => {
        // memberName = '';
        // containerType = ContainerType.Refrigerator;
        // itemQuantity = 1;
        // itemContainer = null;
    };

    $: {
        if (!showDialog) {
            reset();
        }
    }

    const paletteColors = [
        "#0f264e", "#efba33", "#b8922b", "#f2dfc6", "#407f75", "#faa96e", "#739bb0",
        "#c6e9e6", "#384563", "#601707", "#f39c3c", "#fac85c", "#cb2c28", "#dbb17f",
        "#ced7cb", "#125470", "#ed6c3c", "#244b47", "#f3785f", "#1d438b", "#cf533b",
        "#cc6460", "#006e92", "#377b8b", "#ee3d29", "#fcdcb0", "#028b98", "#71aea3",
        "#a3260c", "#fdd887"
    ]
    
    
</script>

{#if showDialog}



    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[10011] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[10012] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[10013] flex flex-col lg:w-[30rem] 2xl:w-[55rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                <div class="drop-shadow-title">{ $_(title) }</div>
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-9 px-5
                shadow-grocerite-orange-200-sm {$lc.text} flex-col items-center">

                <div class="grid grid-cols-6 grid-rows-5 gap-3">
                    {#each paletteColors as color}
                        <button class="w-12 h-10 rounded-full"
                            style="background-color: {color}"
                            on:click={()=>onSelectColor(color)}>
                        </button>
                    {/each}
                </div>
                
            </div>
        </div>
    </div>
{/if}