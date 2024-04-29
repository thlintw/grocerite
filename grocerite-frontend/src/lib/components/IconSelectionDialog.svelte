<script lang="ts">
    import { ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import { createEventDispatcher } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    
    export let mode: 'avatar' | 'household' | 'container' | 'groceryList' = 'avatar';

    export let appearance: 'femalePresenting' | 'malePresenting' | 'neutral' = 'neutral';

    export let title: string = '';

    const getIconList = () => {
        switch (mode) {
            case 'avatar':
                switch (appearance) {
                    case 'femalePresenting':
                        return Array.from({ length: 10 }, (_, i) => `/icons/avatar/fp/avatar-fp-${i + 1}.png`);
                    case 'malePresenting':
                        return Array.from({ length: 10 }, (_, i) => `/icons/avatar/mp/avatar-mp-${i + 1}.png`);
                    case 'neutral':
                        return Array.from({ length: 5 }, (_, i) => `/icons/avatar/nb/avatar-nb-${i + 1}.png`);
                }
            case 'household':
                return Array.from({ length: 9 }, (_, i) => `/icons/household/household-icon-${String(i + 1).padStart(2, '0')}.png`);
            case 'container':
                return Object.values(ContainerType).map((type) => `/icons/container/container-icon-${type}.png`);
            case 'groceryList':
                return Array.from({ length: 20 }, (_, i) => `/icons/groceryList/groceryList-icon-${String(i + 1).padStart(2, '0')}.png`);
            default:
                return [];
        }
    };

    const onSelect = (iconPath: string) => {
        dispatch('click:selectIcon', { iconPath });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    const iconList = getIconList();

    let iconsInner: HTMLDivElement;
    let iconsOuter: HTMLDivElement;

    let innerAtStart: boolean = true;
    let innerAtEnd: boolean = false;

    const changeStartEnd = () => {
        innerAtStart = iconsInner.scrollLeft <= 0;
        innerAtEnd = iconsInner.scrollLeft + iconsInner.clientWidth >= iconsInner.scrollWidth;
    };

    const detectTrackPad = (e: WheelEvent) => {
        if (e.deltaY) {
            if (Math.abs(e.deltaY) < 80) {
                return true;
            }
        }
        else if (e.deltaMode === 0) {
            return true;
        }
        return false;
    }

    const verticalToHorizontalScroll = (event: WheelEvent) => {
        let dy = event.deltaY;
        
        if (!detectTrackPad(event)) {
            event.preventDefault();
            iconsInner.scrollLeft += dy / 5;
        }
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
        <div class="pointer-events-auto z-[11002] flex flex-col lg:w-[40rem] 2xl:w-[55rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                <div class="drop-shadow-title">{ $_(title) }</div>
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-5
                shadow-grocerite-orange-200-sm {$lc.text} overflow-hidden">

                <div bind:this={iconsOuter}
                    class="overflow-y-scroll no-scrollbar ">
                    <div bind:this={iconsInner} 
                        on:scroll={changeStartEnd}
                        on:wheel={verticalToHorizontalScroll}
                        class="
                            w-full flex-nowrap flex no-scrollbar overflow-y-scroll  px-5
                            { innerAtStart ? 'right-mask' : '' }
                            { !innerAtEnd && !innerAtStart ? 'both-mask' : '' }
                            { innerAtEnd ? 'left-mask' : '' }
                        ">
                        {#each iconList as icon}
                            <div class="rounded-md flex p-2 hover:bg-orange-100">
                                <button type="button" class="w-full flex text-lg items-center justify-center "
                                    on:click={() => onSelect(icon)}>
                                    <div class="w-16 text-base text-orange-500">
                                        <img src={icon} alt="icon" />
                                    </div>
                                </button>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}