<script lang="ts">
    import { goto } from '$app/navigation';
    import Button from '$lib/components/Button.svelte';
    import { AuthService } from '$lib/services/auth';
    import { lc } from '$lib/stores/general';
    import { _ } from 'svelte-i18n';
    import { dialog } from '$lib/stores/dialogStore';
    import DeleteAccountDialog from '$lib/components/DeleteAccountDialog.svelte';
    import LocaleSwitch from '$lib/components/LocaleSwitch.svelte';

    let showDeleteDialog = false;

    const deleteAccount = async () => {
        dialog.openDialog({
            title: $_('settings_confirmDeleteAccountTitle1'),
            message: $_('settings_confirmDeleteAccountMessage1'),
            messageTextAlign: 'text-left',
            onConfirm: async () => {
                dialog.closeDialog();
                dialog.openDialog({
                    title: $_('settings_confirmDeleteAccountTitle2'),
                    message: $_('settings_confirmDeleteAccountMessage2'),
                    messageTextAlign: 'text-left',
                    onConfirm: async () => {
                        dialog.closeDialog();
                        showDeleteDialog = true;
                    },
                })
            },
        });
    };

    const signOut = async () => {
        dialog.openDialog({
            title: 'Signing Out',
            message: 'Are you sure you want to sign out?',
            confirmText: 'Sign Out',
            onConfirm: async () => {
                await AuthService.getInstance().signOutUser();
                goto('/app/login');
            },
        });
        // await AuthService.getInstance().signOutUser();
        // goto('/app/login');
    };

    const getLocale = (event) => {
        console.log(event.detail.locale);
    }
</script>



<div class="flex flex-col w-full gap-3 {$lc.text}">
    <DeleteAccountDialog 
        showDialog={showDeleteDialog}
        on:click:closeDialog={() => showDeleteDialog = false}
    />

    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('settings_pageTitle')}
        </span>
    </div>
    <div class="flex flex-col w-full px-3 gap-7">
        <div class="flex items-center justify-between mt-5 h-8">
            <span>{$_('settings_appLanguage')}</span>
            <LocaleSwitch 
                leftMenu={true} 
                wide={true}
                on:localeSelected={getLocale}
                />
        </div>
        <div class="flex items-center justify-between h-8">
            {$_('settings_termsAndConditions')}
        </div>
        <div class="flex items-center justify-between h-8">
            {$_('settings_privacyPolicy')}
        </div>
    
        <div class="flex items-center justify-between h-8">
            <button type="button" class="text-red-500" on:click={deleteAccount}>
                {$_('settings_deleteAccount')}
            </button>
        </div>
        <div class="flex items-center justify-between h-8">
            <button type="button" class="text-red-500" on:click={signOut}>
                {$_('settings_signOut')}
            </button>
        </div>

    </div>
</div>