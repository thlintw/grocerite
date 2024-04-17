<script lang="ts">
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import type { IconDefinition } from '@fortawesome/fontawesome-svg-core';
    import { faPen } from '@fortawesome/free-solid-svg-icons';
    
    export let onClick = () => {};
    export let icon: IconDefinition;
    export let headerText: string;

</script>

<button class="flex flex-col rounded-xl bg-orange-50 p-2 shrink-0"
    on:click={onClick}>
    <div class="flex items-center gap-2 text-sm lg:text-base w-full px-2">
        <FontAwesomeIcon
            icon={icon}
            class="text-emerald-700"
            />
        <span>{headerText}</span>
        <div class="ml-auto">
            <FontAwesomeIcon
                icon={faPen}
                class="text-orange-500"
                />
        </div>
    </div>
    <div class="flex w-full grow font-bold px-3 py-1 justify-center items-center text-left">
        <slot></slot>
    </div>
</button>