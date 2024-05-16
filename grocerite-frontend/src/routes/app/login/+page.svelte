<svelte:head>
	<title>{$_('login_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="login" />
</svelte:head>

<script lang="ts">
	import { _ } from 'svelte-i18n';
	import login1 from '$lib/images/login1.png';
	import swoosh from '$lib/images/swoosh.svg';
	import logoFull from '$lib/images/logo-full.png';
	import google from '$lib/images/google.png';
	import { AuthService } from '$lib/services/auth';
	import LocaleSwitch from '$lib/components/LocaleSwitch.svelte';
	import { lc } from '$lib/stores/general';
	import { authStore } from '$lib/stores/authStore';
    import { onMount } from 'svelte';
    import LoadingDots from '$lib/components/LoadingDots.svelte';
    import { goto } from '$app/navigation';

	let loginLoading = false;

	const loginGoogle = async () => {
		loginLoading = true;
		await AuthService.getInstance().signInWithGoogle();
		if ($authStore.user) goto('/app');
	};

	onMount(() => {
		const unsubscribe = authStore.subscribe(async ($authStore) => {
			const userProfile = $authStore.userProfile;
			if (userProfile) {
				unsubscribe();
				goto('/app');
			}
		});
	});

</script>

<div class="bg-orange-100 lg:bg-orange-50 w-full min-h-full max-h-full flex overflow-hidden relative">
	<LocaleSwitch
		cls="absolute right-3 top-3 lg:top-10 lg:right-10"
	 />
	<div class="w-full lg:w-7/12 h-full max-h-full flex flex-col lg:flex-row absolute lg:relative lg:bg-orange-50 z-10">
		<div class="h-full w-[28rem] absolute bottom-0 right-0 z-10 hidden lg:block">
			<img src={swoosh} alt="swoosh" class="h-full w-full"/>
		</div>
		<div class="h-full w-full z-20 flex items-center relative">
			<img src={login1} alt="login" class="w-[40rem] lg:w-[36rem] lg:ml-auto lg:mt-16 lg:mr-56 absolute lg:relative -bottom-32 -right-20"/>	
		</div>
	</div>
	<div class="flex justify-start bg-transparent absolute lg:relative lg:bg-orange-100 h-full w-full lg:w-5/12 z-20">
		<div class="flex flex-col justify-center items-center w-full lg:w-auto">
			<div class="flex flex-col items-center">
				<div class="relative">
					<img src={logoFull} alt="logo" class="w-[22rem]"/>
					<div class="text-[1.4rem] mt-8 
						absolute bottom-0 w-full h-full flex items-end justify-end -top-5
						{$lc.title} text-orange-500">
						{$_('login_catchPhrase')}
					</div>
				</div>
			</div>
			<div class="flex flex-col gap-5 mt-72 lg:mt-32">
				<button class="bg-white w-72 h-12 py-3 rounded-lg flex items-center justify-center shadow-md"
					disabled={loginLoading}
					on:click={() => loginGoogle()}>
					{#if loginLoading}
						<LoadingDots size="md"/>
					{:else}
						<img src={google} alt="google" class="w-6 h-6"/>
						<span class="text-neutral-500 font-bold ml-4 text-base">{$_('login_continueWithGoogle')}</span>
					{/if}
				</button>
				<a class="bg-orange-100/50 h-12 lg:bg-transparent border-2 border-orange-500 w-72 py-3 rounded-lg flex items-center justify-center"
					href="/app">
					<span class="text-orange-500 font-bold text-base">{$_('login_lookingAround')}</span>
				</a>
			</div>
		</div>
	</div>

</div>