<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import type { IconDefinition } from '@fortawesome/fontawesome-svg-core';
    
    const dispatch = createEventDispatcher();

    const onButtonClick = (event: MouseEvent) => {
        dispatch('click', event);
    };

    export let size = 'base'; 
    export let color = 'orange'; 
    export let text = ''; 
    export let outline = false;
    export let icon: IconDefinition | null = null;
    
    const sizeClass = (size: string) => {
        switch (size) {
            case 'xs': return 'px-3 py-2 text-xs';
            case 'sm': return 'px-3 py-2 text-sm';
            case 'base': return 'px-5 py-2.5 text-sm';
            case 'lg': return 'px-5 py-3 text-base';
            case 'xl': return 'px-6 py-3.5 text-base';
            default: return 'px-5 py-2.5 text-sm'; 
        }
    }
  
    const colorClass = (color: string) => {
        if (outline) {
            return `border-${color}-500 text-${color}-500 hover:bg-${color}-500 hover:text-white focus:ring-${color}-300 dark:border-${color}-300 dark:text-${color}-300 dark:hover:bg-${color}-300 dark:hover:text-white dark:focus:ring-${color}-800`;
        } else {
            return `bg-${color}-500 hover:bg-${color}-600 focus:ring-${color}-300 dark:bg-${color}-600 dark:hover:bg-${color}-700 dark:focus:ring-${color}-800`;
        }
    }
</script>

<button
    type="button"
    class="
        flex transition-all duration-300 items-center justify-center
        font-medium rounded-lg text-center text-white focus:ring-4 focus:outline-none
        {colorClass(color)} {sizeClass(size)}
    "
    on:click={onButtonClick}>
    {#if icon}
        <FontAwesomeIcon icon={icon} class="mr-2" />
    {/if}
    {text}
</button>