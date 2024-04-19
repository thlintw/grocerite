<script lang="ts">
    import { ContainerItem, ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import type { IconDefinition, icon } from '@fortawesome/fontawesome-svg-core';
    import { faUserAltSlash } from '@fortawesome/free-solid-svg-icons';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import SearchableFormInput from './SearchableFormInput.svelte';
    import { createEventDispatcher } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';
    import type { SelectCandidate } from '$lib/types/general';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title: string = '';
    export let availableItems: SelectCandidate[] = [];

    let itemName = '';


    const onSelect = (selected) => {
        dispatch('click:selectOption', { selected });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    
</script>

{#if showDialog}
    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col lg:w-[40rem] 2xl:w-[55rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                { $_(title) }
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-4 py-7 px-5
                shadow-grocerite-orange-200-sm {$lc.text} flex-col items-center">

                <div class="relative flex w-full">

                    <SearchableFormInput 
                        label={$_('groceryList_addListItemsName')}
                        placeholder={$_('groceryList_addListItemsNamePlaceholder')}
                        bind:value={itemName}
                        candidates={availableItems}
                    />
                </div>

                <div class="flex w-full flex-col">
                    <div class="text-lg text-emerald-700 font-bold">
                        Category
                    </div>
                    <div class="px-3">
                        cate
                    </div>
                </div>

                <div class="flex w-full flex-col">
                    <div class="text-lg text-emerald-700 font-bold">
                        Quantity
                    </div>
                    <div class="px-3">
                        cate
                    </div>
                </div>

                <div class="flex w-full flex-col">
                    <div class="text-lg text-emerald-700 font-bold">
                        Target Container
                    </div>
                    <div class="px-3">
                        cate
                    </div>
                </div>



                
            </div>
        </div>
    </div>
{/if}