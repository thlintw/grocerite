<script lang="ts">
    import { DatePicker } from "@svelte-plugins/datepicker";
    import { format } from 'date-fns';
    import { scaleFade } from '$lib/transitions';
    import { fade } from 'svelte/transition';
    import { lc } from '$lib/stores/general';
    import { _ } from 'svelte-i18n';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title = '';

    let startDate = new Date();
    let dateFormat = 'MM/dd/yy';
    let isOpen = false;
    
    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };


    const setDate = (date) => {
        startDate = new Date(date.startDate);
        dispatch('click:selectDate', { date: startDate });
    };

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
                shadow-grocerite-orange-200-sm {$lc.text}">
                <div class="flex flex-col items-center justify-center w-full">
                    <DatePicker 
                        isOpen
                        alwaysShow
                        enableFutureDates={true}
                        enablePastDates={false}
                        bind:startDate
                        onDayClick={setDate}
                        />
                </div>
                
            </div>
        </div>
    </div>
{/if}

<style>
    :root {
        --datepicker-container-position: relative;
        --datepicker-calendar-position: relative;
        --datepicker-container-box-shadow: none;
        --datepicker-container-border: none;
        --datepicker-container-background: theme('colors.orange.50');
        --datepicker-state-active: theme('colors.orange.500');
    }
    .calendars-container {
        top: 0 !important;
    }
</style>