<script lang="ts">
    import { lc } from "$lib/stores/general";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    // props
    export let required: boolean = false;
    export let id: string = "";
    export let label: string | null = "";
    export let error: string | null = "";
    export let placeholder: string | null = "";
    export let value: string | null = "";
    export let textAlign: string = "text-left";

    
    const onKeyDown = (event: KeyboardEvent) => {
        dispatch('keydown', event);
    };

    const onKeyUp = (event: KeyboardEvent) => {
        dispatch('keyup', event);
    };

    const onBlur = (event: Event) => {
        dispatch('blur', event);
    };
</script>

<div class="w-full {$lc.text} flex flex-col gap-1">
    {#if label}
        <label for={id} class="block text-lg text-emerald-700 font-bold { error? ' text-red-500' : '' }">
            {label}
        </label>
    {/if}
    <div class="px-2">
        <input 
            id={id}
            type="text" 
            aria-required={required}
            class="
                bg-orange-50
                w-full px-3 py-2 border-2 border-neutral-300 rounded-xl
                focus:outline-none focus:ring focus:ring-orange-300 focus:border-orange-500
                { textAlign }
            "
            placeholder={placeholder}
            bind:value={value}
            on:keydown={onKeyDown}
            on:keyup={onKeyUp}
            on:blur={onBlur}
            />

    </div>
    {#if error}
        <div class="text-red-500 text-sm ml-2 px-3">
            {error}
        </div>
    {/if}
</div>