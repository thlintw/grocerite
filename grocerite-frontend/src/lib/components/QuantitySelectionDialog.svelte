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
    import { faArrowsRotate, faMinus, faPlus } from '@fortawesome/free-solid-svg-icons';

    const dispatch = createEventDispatcher();

    export let title = '';
    export let showDialog = false;
    export let value: number = 0;
    export let placeholder = '';

    const onSelect = (iconPath: string) => {
        dispatch('click:selectIcon', { iconPath });
    };

    const onPlusClick = () => {
        dispatch('click:plus');
    };

    const onDoublePlusClick = () => {
        dispatch('click:doublePlus');
    };

    const onMinusClick = () => {
        dispatch('click:minus');
    };

    const onDoubleMinusClick = () => {
        dispatch('click:doubleMinus');
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

    let touchStartX: number = 0;
    let touchEndX: number = 0;

    const setTouchStart = (e: TouchEvent) => {
        touchStartX = e.touches[0].clientX;
    };

    const setTouchMove = (e: TouchEvent) => {
        touchEndX = e.touches[0].clientX;
        if (touchStartX - touchEndX > 50) {
            onMinusClick();
        }
        if (touchStartX - touchEndX < -50) {
            onPlusClick();
        }
    };

    
</script>

{#if showDialog}
    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none  
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col lg:w-[30rem] 2xl:w-[35rem] w-11/12">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1 ">
                <div class="drop-shadow-title">{ $_(title) }</div>
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-5 px-5 
                shadow-grocerite-orange-200-sm {$lc.text} overflow-hidden flex flex-col items-center">

                <div class="flex w-full mt-3 relative items-center justify-center gap-2 ">
                    <button type="button" class="bg-orange-100 rounded-full p-2 w-16 h-10 text-orange-500 cursor-pointer"
                        on:click={onDoubleMinusClick}>
                        <FontAwesomeIcon
                            icon={faMinus}
                            />
                        10
                    </button>
                    <button type="button" class="bg-orange-100 rounded-full p-2 w-10 h-10 text-orange-500 cursor-pointer"
                        on:click={onMinusClick}>
                        <FontAwesomeIcon
                            icon={faMinus}
                            />
                    </button>
                    <div on:touchstart={setTouchStart}
                        on:touchmove={setTouchMove}
                        class="w-24 h-20 relative text-2xl font-bold flex items-center justify-center">
                        <span class="">{value}</span>
                        <!-- <FormInput 
                            placeholder={$_(placeholder)}
                            bind:value={value}
                            on:keyup={onKeyUp}
                            on:keydown={onKeyDown}
                            on:blur={onBlur}
                            /> -->
                    </div>
                    <button type="button" class="bg-orange-100 rounded-full p-2 w-10 h-10 text-orange-500 cursor-pointer"
                        on:click={onPlusClick}>
                        <FontAwesomeIcon
                            icon={faPlus}
                            />
                    </button>
                    <button type="button" class="bg-orange-100 rounded-full p-2 w-16 h-10 text-orange-500 cursor-pointer"
                        on:click={onDoublePlusClick}>
                        <FontAwesomeIcon
                            icon={faPlus}
                            />
                            10
                    </button>
                </div>
                
                <div class="grid w-5/12 gap-3 grid-cols-1 mt-3">
                    <!-- <Button
                        text={$_('common_cancel')}
                        size="sm"
                        outline={true}
                        on:click={onBarrierDismiss}
                        cls="basis-1/2"
                        />
                         -->
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