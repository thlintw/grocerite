<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
	import { lc } from '$lib/stores/general';
    import { type IconDefinition } from '@fortawesome/fontawesome-svg-core';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';

    export let showActionMenu = false;

    export let menuTitle = '';

    interface ActionMenuItems {
        title: string;
        icon?: IconDefinition;
        action: () => void;
    }

    export let actionMenuItems: ActionMenuItems[] = [];

    const dispatch = createEventDispatcher();

    const handleCloseMenu = () => {
        dispatch('click:closeMenu', {})
    };
</script>

{#if showActionMenu}
    <button transition:fade
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20" 
        on:click={handleCloseMenu}></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002]flex flex-col
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                { $_(menuTitle) }
            </div>
            <div class="bg-orange-50 rounded-xl flex flex-col gap-3 px-3 py-3 pt-4
                shadow-grocerite-orange-200-sm items-start">
                {#each actionMenuItems as item}
                    <div class="hover:bg-orange-100 rounded-md flex pr-2">
                        <button type="button" class="w-full flex  {$lc.text} text-xl items-center"
                            on:click={item.action}>
                            <div class="w-8 text-base text-orange-500">
                                {#if item.icon}
                                    <FontAwesomeIcon icon={item.icon} />
                                {/if}
                            </div>
                            <span class="text-neutral-700 hover:text-orange-500">{ $_(item.title) }</span>
                        </button>
                    </div>
                {/each}
            </div>
        </div>
    </div>
{/if}