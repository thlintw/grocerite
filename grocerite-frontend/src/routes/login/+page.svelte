<svelte:head>
	<title>{$_('login_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="household" />
</svelte:head>

<script lang="ts">
	import { _, locale, locales } from 'svelte-i18n';
	import login1 from '$lib/images/login1.png';
	import swoosh from '$lib/images/swoosh.svg';
	import logoFull from '$lib/images/logo-full.png';
	import google from '$lib/images/google.png';
	import flagEnUs from '$lib/images/flag-en-US.png';
	import flagJaJp from '$lib/images/flag-ja-JP.png';
	import flagSvSe from '$lib/images/flag-sv-SE.png';
	import flagZhTw from '$lib/images/flag-zh-TW.png';
	import { scaleFade } from '$lib/transitions';
    import { getFirebaseClient } from "$lib/firebaseClient";
    import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";

    let form: HTMLFormElement;
    async function login(): Promise<void> {
        try {
            const auth = getFirebaseClient();
            if (auth.error) {
                return alert("Error: " + auth.msg);
            }
            const cred = await signInWithPopup(auth.data, new GoogleAuthProvider());
            const token = await cred.user.getIdToken();
            await auth.data.signOut();
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "token";
            input.value = token;
            form.appendChild(input);
            form.submit();
        } catch (err) {
            console.error(err);
        }
    }
	
	$: l = $locale;

	$: fontFamilyCls = l == 'ja-JP' || l == 'zh-TW' ? 'font-sans' : 'font-berkshire';


	const getLocaleFlag = (locale: string) => {
		switch (locale) {
			case 'en-US':
				return flagEnUs;
			case 'ja-JP':
				return flagJaJp;
			case 'sv-SE':
				return flagSvSe;
			case 'zh-TW':
				return flagZhTw;
			default:
				return flagEnUs;
		}
	};

	const getLocaleName = (locale: string) => {
		switch (locale) {
			case 'en-US':
				return 'English';
			case 'ja-JP':
				return '日本語';
			case 'sv-SE':
				return 'Svenska';
			case 'zh-TW':
				return '正體中文';
			default:
				return 'English';
		}
	};

	const setLocale = (lString: string) => {
		locale.set(lString);
		showLocaleDropdown = false;
	};

	let showLocaleDropdown = false;

</script>

<div class="bg-orange-100 lg:bg-orange-50 w-full min-h-full max-h-full flex overflow-hidden relative">
	<div class="absolute right-3 top-3 lg:top-10 lg:right-10 w-12 h-12 bg-orange-200 rounded-full z-30
		flex items-center justify-center cursor-pointer">

		<button type="button" on:click={() => showLocaleDropdown = true}>
			<img src={getLocaleFlag(l ? l : 'en-US')} alt={l} class="w-8 opacity-50"/>
		</button>

		<button type="button" class="fixed w-screen h-screen left-0 top-0 {showLocaleDropdown ? 'block': 'hidden'}"
			on:click={() => showLocaleDropdown = false}></button>

		{#if showLocaleDropdown}
		<div transition:scaleFade 
			class="absolute right-2 top-2 w-32 bg-orange-50 rounded-xl flex flex-col gap-1 py-2 px-1 shadow-grocerite-orange-200-md">
			{#each $locales as locale}
			<button class="flex items-center gap-2 hover:bg-orange-100 rounded-md pl-3 pr-2 py-1"
				on:click={() => setLocale(locale)} type="button">
				<img src={getLocaleFlag(locale)} alt={locale} class="w-6">
				<div class="text-neutral-600 text-sm">{getLocaleName(locale)}</div>
			</button>
			{/each}
		</div>
		{/if}
	</div>
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
					<span class="text-2xl font-bold text-center mt-8
						absolute right-5 -bottom-4
						{fontFamilyCls} text-orange-500">
						{$_('login_catchPhrase')}
					</span>
				</div>
			</div>
			<div class="flex flex-col gap-5 mt-72 lg:mt-32">
				<button class="bg-white w-72 py-3 rounded-lg flex items-center justify-center shadow-md"
				on:click={login}>
					<img src={google} alt="google" class="w-6 h-6"/>
					<span class="text-neutral-500 font-bold ml-4 text-base">{$_('login_continueWithGoogle')}</span>
				</button>
				<div class="bg-orange-100/50 lg:bg-transparent border-2 border-orange-500 w-72 py-3 rounded-lg flex items-center justify-center">
					<span class="text-orange-500 font-bold text-base">{$_('login_lookingAround')}</span>
				</div>
			</div>
		</div>
	</div>

</div>