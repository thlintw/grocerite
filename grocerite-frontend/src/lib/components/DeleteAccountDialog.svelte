<script lang="ts">
    import { fade } from 'svelte/transition';
    import { scaleFade } from '$lib/transitions';
    import { dialog } from '$lib/stores/dialogStore';
    import { lc } from '$lib/stores/general';
    import { _ } from 'svelte-i18n';
    import { createEventDispatcher } from 'svelte';
    import FormInput from './FormInput.svelte';

    const dispatch = createEventDispatcher();

    export let showDialog: boolean;

    const generateDeleteCode = () => {
        const randomCode = Math.floor(100000 + Math.random() * 900000);
        return randomCode;
    };

    let deleteCode = generateDeleteCode();

    let codeInput = '';

    $: codeInput = codeInput.replace(/\D/g, '');

    $: if (codeInput.length > 6) {
        codeInput = codeInput.slice(0, 6);
    }

    $: if (codeInput) {
        errorMessage = '';
    }

    let errorMessage = '';

    const handleCloseDialog = () => {
        dispatch('click:closeDialog', {})
    };

    const actuallyDeleteAccount = () => {
        if (codeInput === deleteCode.toString()) {
            dispatch('click:closeDialog', {});
        } else if (!codeInput){
            errorMessage = $_('settings_confirmDeleteCodeNotEntered');
        } else if (codeInput.length < 6 || codeInput !== deleteCode.toString()) {
            errorMessage = $_('settings_confirmDeleteCodeMismatch');
        } 
    };
</script>

{#if showDialog}
    <button transition:fade on:click={handleCloseDialog} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[11000] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[11001] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[11002] flex flex-col w-[30rem]
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                <span class="drop-shadow-title">{$_('settings_confirmDeleteAccountTitle3')}</span>
            </div>
            <div class="bg-orange-50 rounded-2xl flex flex-col gap-3 px-3 py-3 pt-4
                shadow-grocerite-orange-200-sm {$lc.text} flex flex-col items-center">
                <span class="w-full mt-4 text-left px-5">
                    {@html $_('settings_confirmDeleteAccountMessage3')}
                </span>
                <span class="font-bold text-2xl text-orange-500">
                    { deleteCode }
                </span>
                <span class="w-full text-left px-5">
                    {@html $_('settings_confirmDeleteAccountMessageEnterCode')}
                </span>
                <FormInput
                    bind:value={codeInput}
                    textAlign="text-center"
                    error={errorMessage}
                 />
                
                <div class="flex gap-3 justify-center mt-3 w-11/12 mb-1">
                    <button type="button" class="border-orange-500 border-2 text-orange-500 rounded-full py-1 basis-1/2"
                        on:click={handleCloseDialog}>
                        {$_('common_cancel')}
                    </button>
                    <button type="button" class="bg-orange-500 text-white rounded-full py-1 basis-1/2"
                        on:click={actuallyDeleteAccount}>
                        { $_('settings_confirmDeleteAccount') }
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}