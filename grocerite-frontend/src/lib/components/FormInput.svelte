<script lang="ts">
    import { lc } from "$lib/stores/general";

    export let required: boolean = false;
    export let id: string = "";
    export let label: string | null = "";
    export let error: string | null = "";
    export let placeholder: string | null = "";
</script>

<div class="w-full {$lc.text} flex flex-col gap-1">
    {#if label}
        <label for={id} class="block text-base text-neutral-700 { error? ' text-red-500' : '' }">
            {label}
        </label>
    {/if}
    <input 
        id={id}
        type="text" 
        aria-required={required}
        class="
            bg-orange-50
            w-full px-3 py-2 border-2 border-neutral-300 rounded-md 
            focus:outline-none focus:ring focus:ring-orange-300 focus:border-orange-500
        "
        placeholder={placeholder}
        />
    {#if error}
        <div class="text-red-500 text-sm ml-2">
            {error}
        </div>
    {/if}
</div>