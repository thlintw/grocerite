<script lang="ts">
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import type { IconDefinition } from '@fortawesome/fontawesome-svg-core';
    import { faPen } from '@fortawesome/free-solid-svg-icons';
    import { _ } from 'svelte-i18n';
    
    export let onClick = () => {};
    export let icon: IconDefinition;
    export let headerText: string;
    export let error: string = '';
    export let optional: boolean = false;

</script>

<button class="relative flex flex-col rounded-xl border-2 bg-orange-50 p-1.5 shrink-0 {error ? ' border-red-400' : 'border-orange-50'}"
    on:click={onClick}>
    <div class="flex items-center gap-2 text-sm w-full px-2">
        <FontAwesomeIcon
            icon={icon}
            class="text-emerald-700 text-2xl"
            />
        <div class="text-neutral-600 span flex items-center grow flex-wrap">
            <span class="text-left basis-full lg:basis-auto">{headerText}</span>
            {#if optional}
                <span class="text-xs text-emerald-600 lg:ml-auto font-light">{$_('common_optional')}</span>
            {/if}
        </div>
        <div class="ml-auto">
            <FontAwesomeIcon
                icon={faPen}
                class="text-orange-500"
                />
        </div>
    </div>
    <div class="flex w-full grow font-bold px-3 py-1 justify-center items-center text-left min-h-20">
        <slot></slot>
    </div>
    <div class="absolute left-4 bottom-0">
        <span class="text-red-400 text-sm">{error}</span>
    </div>
</button>