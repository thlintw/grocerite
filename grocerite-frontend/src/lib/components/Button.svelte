<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import type { IconDefinition } from '@fortawesome/fontawesome-svg-core';
    import { crossfade, fade } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
    
    const dispatch = createEventDispatcher();

    const onButtonClick = (event: MouseEvent) => {
        dispatch('click', event);
    };

    export let size = 'base'; 
    export let color = 'orange'; 
    export let text = ''; 
    export let outline = false;
    export let icon: IconDefinition | null = null;
    export let cls = '';
    export let disabled = false;
    export let loading = false;
    
    const sizeClass = (size: string) => {
        switch (size) {
            case 'xs': return 'px-3  h-10 text-xs';
            case 'sm': return 'px-3 h-10 text-sm';
            case 'base': return 'px-5 h-12 text-sm';
            case 'lg': return 'px-5  h-14 text-base';
            case 'xl': return 'px-6 h-16 text-base';
            default: return 'px-5 h-14 text-sm'; 
        }
    }
  
    const colorClass = (color: string) => {
        if (outline) {
            return `border-2 border-${color}-500 text-${color}-500 hover:bg-${color}-500 hover:text-white focus:ring-${color}-300 dark:border-${color}-300 dark:text-${color}-300 dark:hover:bg-${color}-300 dark:hover:text-white dark:focus:ring-${color}-800`;
        } else {
            if (disabled || loading) {
                return `text-white bg-${color}-100 dark:bg-${color}-800`;
            }
            return `text-white bg-${color}-500 hover:bg-${color}-600 focus:ring-${color}-300 dark:bg-${color}-600 dark:hover:bg-${color}-700 dark:focus:ring-${color}-800`;
        }
    }

    $: colorClasses = disabled || loading ? colorClass(color) : colorClass(color);

    $: sizeClasses = sizeClass(size);

    let startFading = false;

</script>

<button
    type="button"
    class="
        flex transition-all duration-300 items-center justify-center gap-2
        font-medium rounded-full text-center focus:ring-4 focus:outline-none relative
        {startFading ? 'min-w-28' : 'min-w-0'}
        {colorClasses} {sizeClasses}
        {cls}
    "
    disabled={disabled || loading}
    on:click={onButtonClick}>
    {#if loading}
        <div class="flex gap-1  {startFading ? 'absolute' : 'relative'}" 
            transition:fade 
            on:outrostart={() => startFading = true}
            on:outroend={() => startFading = false}
            >
            <img src="/image/leaf_or.png" alt="spin-leaf" class="w-3 animate-bs0"/>
            <img src="/image/leaf_or.png" alt="spin-leaf" class="w-3 animate-bs1"/>
            <img src="/image/leaf_or.png" alt="spin-leaf" class="w-3 animate-bs2"/>
        </div>
    {/if}
    {#if !loading}
        <div class="flex gap-1 {startFading ? 'absolute' : ''}" 
            transition:fade 
            on:outrostart={() => startFading = true}
            on:outroend={() => startFading = false}
            >
            {#if icon}
                <FontAwesomeIcon icon={icon} class="" />
            {/if}
            {text}
        </div>
    {/if}
</button>