<script lang="ts">
    import { ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import type { IconDefinition, icon } from '@fortawesome/fontawesome-svg-core';
    import { faUserAltSlash } from '@fortawesome/free-solid-svg-icons';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { createEventDispatcher } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title: string = '';

    interface SelectOption {
        iconPath?: string;
        icon?: IconDefinition;
        iconBg?: string;
        value: string;
        label: string;
    }

    export let options: SelectOption[] = [];


    const onSelect = (option: SelectOption) => {
        dispatch('click:selectOption', { option });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    let optionsInner: HTMLDivElement;
    let optionsOuter: HTMLDivElement;

    let innerAtStart: boolean = true;
    let innerAtEnd: boolean = false;

    const changeStartEnd = () => {
        innerAtStart = optionsInner.scrollTop <= 0;
        innerAtEnd = optionsInner.scrollTop + optionsInner.clientHeight >= optionsInner.scrollHeight;
    };

    $: if (!showDialog) {
        innerAtStart = true;
        innerAtEnd = false;
    }
    
</script>

{#if showDialog}
    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col lg:w-[30rem] 2xl:w-[35rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                { $_(title) }
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-5 pb-2
                shadow-grocerite-orange-200-sm {$lc.text} overflow-hidden">
                {#if options.length > 0}
                    <div bind:this={optionsOuter}
                        class="overflow-x-scroll no-scrollbar overscroll-none w-full flex 
                        { options.length >= 3 ? 'items-start' : 'items-center' }
                        { options.length >= 3 ? ' h-48' :
                            options.length >= 2 ? 'h-40' : 'h-20'}">
                        <div bind:this={optionsInner} 
                            on:scroll={changeStartEnd}
                            class="
                                w-full flex-col no-scrollbar overflow-x-scroll overscroll-none px-5 max-h-full
                                { innerAtStart && options.length >= 3 ? 'top-mask' : '' }
                                { !innerAtEnd && options.length > 2 && !innerAtStart ? 'both-v-mask' : '' }
                                { innerAtEnd && options.length > 2 ? 'bottom-mask' : '' }
                            ">
                                {#each options as opt}
                                    <div class="rounded-md flex p-2 hover:bg-orange-100">
                                        <button type="button" class="w-full h-full flex text-lg items-center justify-center"
                                            on:click={() => onSelect(opt)}>
                                            <div class="lg:w-9/12 w-11/12 flex justify-start items-center gap-3">
                                                {#if opt.icon}
                                                    <div class="w-16 text-base text-orange-500 bg-blue-300">
                                                        <FontAwesomeIcon
                                                            icon={opt.icon}
                                                            class="text-2xl"
                                                            />
                                                    </div>
                                                {/if}
                                                {#if opt.iconPath}
                                                    {#if opt.iconPath === 'x'}
                                                        <div class="w-14 text-base text-neutral-300 bg-neutral-200 rounded-full h-14 flex items-center justify-center">
                                                            <FontAwesomeIcon
                                                                icon={faUserAltSlash}
                                                                class="text-2xl"
                                                                />
                                                        </div>
                                                    {:else}
                                                        <div class="w-14 text-base text-orange-500 rounded-full overflow-hidden"
                                                            style={opt.iconBg ? `background-color: ${opt.iconBg}` : ''}>
                                                            <img src={opt.iconPath} alt="icon" />
                                                        </div>
                                                    {/if}
                                                {/if}
                                                <span>{opt.iconPath !== 'x' ? opt.label : $_(opt.label)}</span>
                                            </div>
                                        </button>
                                    </div>
                                {/each}
                        </div>
                    </div>

                {:else}
                    <div class="flex justify-center items-center w-full h-20 text-neutral-500">
                        <span>{$_('groceryList_noOtherMember')}</span>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}