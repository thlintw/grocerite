<script lang="ts">
    import { fade } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
    import { showLoadingOverlay, overlayText } from '$lib/stores/general';
</script>

{#if $showLoadingOverlay}
    <button transition:fade
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="z-[11002] flex flex-col items-center
            ">
            <!-- <div class="border-4 w-10 h-10 border-b-transparent border-orange-500 rounded-full animate-spin"></div> -->
            <div class="flex gap-2">
                <img src="/image/leaf.png" alt="spin-leaf" class="w-5 animate-b0"/>
                <img src="/image/leaf.png" alt="spin-leaf" class="w-5 animate-b1"/>
                <img src="/image/leaf.png" alt="spin-leaf" class="w-5 animate-b2"/>
            </div>
            {#if $overlayText}
                <div class="text-orange-500 text-2xl mt-5">
                    {$overlayText}
                </div>
            {/if}
        </div>
    </div>
{/if}