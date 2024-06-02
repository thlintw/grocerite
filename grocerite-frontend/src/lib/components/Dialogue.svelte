<script lang="ts">
    import { fade } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
    import { dialog } from '$lib/stores/dialogStore';
    import { lc } from '$lib/stores/general';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { _ } from 'svelte-i18n';
</script>

{#if $dialog.showDialog}
    <button transition:fade on:click={dialog.closeDialog} disabled={!$dialog.barrierDismiss}
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col w-[25rem]
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                <span class="drop-shadow-title">{ $_($dialog.title) }</span>
            </div>
            <div class="bg-orange-50 rounded-2xl flex flex-col gap-3 px-3 py-3 pt-4
                shadow-grocerite-orange-200-sm {$lc.text} flex flex-col items-center">
                <span class="w-full max-w-full mt-4 break-words min-w-0 {$dialog.messageTextAlign} px-5">
                    {@html $_($dialog.message)}
                </span>
                
                <div class="flex gap-3 justify-center mt-3 w-11/12 mb-1">
                    {#if $dialog.showCancel}
                        <button type="button" class="border-orange-500 border-2 text-orange-500 rounded-full py-1 basis-1/2"
                            on:click={$dialog.onCancel}>
                            { $_($dialog.cancelText) }
                        </button>
                    {/if}
                    {#if $dialog.onConfirm}
                        <button type="button" class="bg-orange-500 text-white rounded-full py-1 basis-1/2"
                            on:click={$dialog.onConfirm}>
                            { $_($dialog.confirmText) }
                        </button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}