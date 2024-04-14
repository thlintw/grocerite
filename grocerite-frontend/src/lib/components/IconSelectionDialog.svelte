<script lang="ts">
    import { fade } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
    import { dialog } from '$lib/stores/dialogStore';
    import { lc } from '$lib/stores/general';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { _ } from 'svelte-i18n';
    import { ContainerType } from '$lib/models/container';
    import { createEventDispatcher, onMount } from 'svelte';

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
                return Array.from({ length: 7 }, (_, i) => `/icons/household/household-icon-${i + 1}.png`);
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

    const watchIconsInner = () => {
        if (iconsInner) {
            iconsInner.addEventListener('scroll', () => {
                innerAtStart = iconsInner.scrollLeft <= 0;
                innerAtEnd = iconsInner.scrollLeft + iconsInner.clientWidth >= iconsInner.scrollWidth;
            });
        }
    };

    onMount(() => {
        if (iconsInner) watchIconsInner();
    });

    
</script>

{#if showDialog}
    <button transition:fade on:click={onBarrierDismiss} disabled={!$dialog.barrierDismiss}
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col lg:w-[40rem] xl:w-[50rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                { $_(title) }
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 px-3 py-5
                shadow-grocerite-orange-200-sm {$lc.text} overflow-hidden">

                <div bind:this={iconsOuter}
                    class="overflow-y-scroll {!innerAtStart ? 'left-mask' : ''}">
                    <div bind:this={iconsInner} 
                        class="w-full flex-nowrap flex no-scrollbar overflow-y-scroll {!innerAtEnd ? 'right-mask' : ''}">
                        {#each iconList as icon}
                            <div class="hover:bg-orange-100 rounded-md flex pr-2">
                                <button type="button" class="w-full flex  text-lg items-center"
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