<script lang="ts">
    import { fade } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
    import { dialog } from '$lib/stores/dialogStore';
    import { lc } from '$lib/stores/general';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { _ } from 'svelte-i18n';
    import { ContainerType } from '$lib/models/container';
    import { createEventDispatcher, onMount, afterUpdate, onDestroy } from 'svelte';
    import type { UIEventHandler } from 'svelte/elements';
    import FormInput from './FormInput.svelte';
    import Button from './Button.svelte';
    import { faArrowsRotate } from '@fortawesome/free-solid-svg-icons';

    const dispatch = createEventDispatcher();

    export let title = '';
    export let showDialog = false;
    export let value = '';
    export let placeholder = '';
    export let showRefreshButton = false;

    const onSelect = (iconPath: string) => {
        dispatch('click:selectIcon', { iconPath });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    const onKeyDown = (event: CustomEvent) => {
        dispatch('keydown', event.detail);
    };

    const onKeyUp = (event: CustomEvent) => {
        dispatch('keyup', event.detail);
    };

    const onBlur = (event: CustomEvent) => {
        dispatch('blur', event.detail);
    };

    const onRefreshClick = () => {
        dispatch('click:refresh');
    };

    $: showDialog && afterUpdate(() => {
        const input = document.querySelector('input');
        if (input) {
            input.focus();
        }
    });
    
</script>

{#if showDialog}
    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col lg:w-[40rem] 2xl:w-[55rem] w-11/12
            mb-36 lg:mb-0
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                { $_(title) }
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-5 px-5
                shadow-grocerite-orange-200-sm {$lc.text} overflow-hidden flex flex-col items-center">

                <div class="flex w-full mt-3 relative">
                    <FormInput 
                        placeholder={placeholder}
                        bind:value={value}
                        on:keyup={onKeyUp}
                        on:keydown={onKeyDown}
                        on:blur={onBlur}
                        />
                    {#if showRefreshButton}
                        <button class="absolute right-5 top-1/2 transform -translate-y-1/2 text-orange-500 cursor-pointer"
                            on:click={onRefreshClick}>
                            <FontAwesomeIcon
                                icon={faArrowsRotate}
                                />
                        </button>
                    {/if}
                </div>
                
                <div class="grid w-8/12 gap-3 grid-cols-2 mt-3">
                    <Button
                        text={$_('common_cancel')}
                        size="sm"
                        outline={true}
                        on:click={onBarrierDismiss}
                        cls="basis-1/2"
                        />
                        
                    <Button
                        text={$_('common_confirm')}
                        size="sm"
                        on:click={onBarrierDismiss}
                        cls="basis-1/2"
                        />
                </div>
            </div>
        </div>
    </div>
{/if}