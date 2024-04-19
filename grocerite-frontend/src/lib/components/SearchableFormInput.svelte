<script lang="ts">
    import { lc } from "$lib/stores/general";
    import type { SelectCandidate } from "$lib/types/general";
    import { faTimes } from "@fortawesome/free-solid-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import { se } from "date-fns/locale";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    // props
    export let required: boolean = false;
    export let id: string = "";
    export let label: string | null = "";
    export let error: string | null = "";
    export let placeholder: string | null = "";
    export let value: string | null = "";
    export let disabled: boolean = false;
    export let candidates: SelectCandidate[] = [];
    export let maxSelections: number = 1;

    let filteredCandidates: SelectCandidate[] = [];

    const filterCandidates = () => {
        if (!value) {
            filteredCandidates = [];
            return;
        } else {
            filteredCandidates = candidates.filter((candidate) => {
                return candidate.label.toLowerCase().includes(value!.toLowerCase());
            });
        }
    };

    let selection: SelectCandidate[] = [];

    let inputDisabled = false;

    $: if (selection.length >= maxSelections) {
        inputDisabled = true;
        if (disabled) inputDisabled = true;
    } else {
        inputDisabled = false;
        if (disabled) inputDisabled = true;
    }



    const onKeyDown = (event: KeyboardEvent) => {
        dispatch('keydown', event);
    };

    const onKeyUp = (event: KeyboardEvent) => {
        filterCandidates();
        dispatch('keyup', event);
    };

    const onBlur = (event: Event) => {
        dispatch('blur', event);
    };

    const onSelect = (selected: SelectCandidate) => {
        if (disabled) return;
        if (selection.includes(selected)) return;
        selection = [...selection, selected];
        value = '';
        filteredCandidates = [];
        dispatch('select', selected);
    };

    const deselectSelf = (selected: SelectCandidate) => {
        selection = selection.filter((s) => s !== selected);
    };

    $: actualPlaceholder = selection.length > 0 ? '' : placeholder;

    let dummyInput: HTMLInputElement;
    let actualInput: HTMLInputElement;


</script>

<div class="w-full {$lc.text} flex flex-col gap-1 relative">
    {#if label}
        <label for={id} class="block text-lg text-emerald-700 font-bold { error? ' text-red-500' : '' }">
            {label}
        </label>
    {/if}
    <div class="px-2 relative">
        <input 
            id={id}
            type="text" 
            aria-required={required}
            class="
                bg-orange-50
                w-full px-3 py-2 border-2 border-neutral-300 rounded-md 
                focus:outline-none focus:ring focus:ring-orange-300 focus:border-orange-500
            "
            placeholder={actualPlaceholder}
            disabled={inputDisabled}
            bind:this={actualInput}
            bind:value={value}
            on:keydown={onKeyDown}
            on:keyup={onKeyUp}
            on:blur={onBlur}
            />

        <div class="absolute top-0 right-0 h-full w-full flex items-center pointer-events-none px-5 gap-2">
            {#each selection as selected}
                <div class="bg-orange-500 text-white rounded-lg p-0.5 px-2 flex items-center">
                    <span class="text-lg">{selected.label}</span>
                    <button class="pointer-events-auto ml-2" on:click={() => deselectSelf(selected)}>
                        <FontAwesomeIcon icon={faTimes} class="text-white" />
                    </button>
                </div>
            {/each}
            {#if selection.length > 0 && selection.length < maxSelections}
                <div class="pointer-events-auto">
                    <input 
                        type="text"
                        class="bg-transparent ring-0 focus:outline-none focus:ring-0 focus:border-0 w-full border-0"
                        bind:this={dummyInput}
                        on:focus={() => actualInput.focus()}
                        bind:value={value}
                        />
                </div>
            {/if}
    
        </div>
        
    </div>
    
    {#if filteredCandidates.length > 0}
        <div class="absolute top-12 bg-orange-50 shadow-lg rounded-lg z-[11003] w-full
            border-2 border-orange-200 flex flex-col gap-1">
            {#each filteredCandidates as candidate}
                <button class="p-2 hover:bg-orange-100 w-full text-left"
                    on:click={() => onSelect(candidate)}>
                    {candidate.label}
                </button>
            {/each}
        </div>
    {/if}
    {#if error}
        <div class="text-red-500 text-sm ml-2">
            {error}
        </div>
    {/if}
</div>