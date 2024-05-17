<svelte:head>
	<title>{$_('settings_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="login" />
</svelte:head>

<script lang="ts">
    import { goto } from '$app/navigation';
    import Button from '$lib/components/Button.svelte';
    import { AuthService } from '$lib/services/auth';
    import { lc } from '$lib/stores/general';
    import { _ } from 'svelte-i18n';
    import { dialog } from '$lib/stores/dialogStore';
    import DeleteAccountDialog from '$lib/components/DeleteAccountDialog.svelte';
    import LocaleSwitch from '$lib/components/LocaleSwitch.svelte';
    import { authStore } from '$lib/stores/authStore';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { faFileSignature, faFont, faGlobe, faLanguage, faRightFromBracket, faShield, faUserXmark } from '@fortawesome/free-solid-svg-icons';

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
            title: $_('settings_signOutTitle'),
            message: $_('settings_signOutMessage'),
            confirmText: $_('settings_signOutConfirm'),
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
        {#if $authStore.userProfile}
            <button type="button" class="flex px-3 ml-auto font-sans items-center gap-2 text-neutral-600 text-sm"
                on:click={signOut}>
                {$authStore.userProfile?.email}
                {#if $authStore.user?.photoURL}
                    <img src={$authStore.user?.photoURL} alt="Your profile pic" class="w-7 h-7 rounded-full"/>
                {/if}
            </button>
        {/if}
    </div>
    <div class="flex flex-col w-full px-3 gap-7">
        <div class="flex items-center mt-10 h-8 gap-5">
            <FontAwesomeIcon icon={faFont} class="text-neutral-600 text-3xl w-12"/>
            <span class="text-neutral-600 mr-auto font-bold">{$_('settings_appLanguage')}</span>
            <LocaleSwitch 
                leftMenu={true} 
                wide={true}
                on:localeSelected={getLocale}
                />
        </div>
        <div class="w-full my-5 h-1 bg-neutral-900/10 rounded-full">

        </div>
        <div class="
            flex items-center gap-5 h-8 transition-all duration-200 no-underline
            text-neutral-600 hover:text-orange-500 hover:underline font-bold
            active:text-orange-500
            ">
            <FontAwesomeIcon icon={faFileSignature} class="text-3xl w-12"/>
            <a href="#">
                {$_('settings_termsAndConditions')}
            </a>
        </div>
        <div class="
            flex items-center gap-5 h-8 transition-all duration-200 no-underline
            text-neutral-600 hover:text-orange-500 hover:underline font-bold
            active:text-orange-500
            ">
            <FontAwesomeIcon icon={faShield} class="text-3xl w-12"/>
            <a href="#" class="">
                {$_('settings_privacyPolicy')}
            </a>
        </div>
    
        <div class="flex items-center justify-between h-8">
            <button type="button" class="text-red-500 no-underline hover:underline flex gap-5 font-bold items-center" on:click={deleteAccount}>
                <FontAwesomeIcon icon={faUserXmark} class="text-3xl w-12"/>
                {$_('settings_deleteAccount')}
            </button>
        </div>
        <div class="flex items-center justify-between h-8">
            <button type="button" class="text-red-500 no-underline hover:underline flex gap-5 font-bold items-center" on:click={signOut}>
                <FontAwesomeIcon icon={faRightFromBracket} class="text-3xl w-12"/>
                {$_('settings_signOut')}
            </button>
        </div>

    </div>
</div>