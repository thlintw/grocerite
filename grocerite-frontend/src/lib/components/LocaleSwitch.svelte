<script lang="ts">
	import { locale, locales } from 'svelte-i18n';
	import flagEnUs from '$lib/images/flag-en-US.png';
	import flagJaJp from '$lib/images/flag-ja-JP.png';
	import flagSvSe from '$lib/images/flag-sv-SE.png';
	import flagZhTw from '$lib/images/flag-zh-TW.png';
	import flagFrFr from '$lib/images/flag-fr-FR.png';
	import { scaleFade } from '$lib/transitions';
    import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	$: l = $locale;
    
	let showLocaleDropdown = false;

	const getLocaleFlag = (locale: string | null | undefined) => {
		switch (locale) {
			case 'en-US':
				return flagEnUs;
			case 'ja-JP':
				return flagJaJp;
			case 'sv-SE':
				return flagSvSe;
			case 'zh-TW':
				return flagZhTw;
			case 'fr-FR':
				return flagFrFr;
			default:
				return flagEnUs;
		}
	};

	const getLocaleName = (locale: string | null | undefined) => {
		switch (locale) {
			case 'en-US':
				return 'English';
			case 'ja-JP':
				return '日本語';
			case 'sv-SE':
				return 'Svenska';
			case 'zh-TW':
				return '正體中文';
			case 'fr-FR':
				return 'Français';
			default:
				return 'English';
		}
	};

	const setLocale = (lString: string) => {
		locale.set(lString);
		dispatchSelection(lString);
		showLocaleDropdown = false;
	};

    export let cls = '';

    export let leftMenu = false;

	export let wide = false;

	const dispatchSelection = (locale: string) => {
		dispatch('localeSelected', { locale });
	};
</script>

<div class="
    {cls} w-12 h-12 bg-orange-200 rounded-full z-30
	flex cursor-pointer relative items-center justify-center
	{wide ? 'w-32 h-12' : 'w-12 h-12'}
	">

	<button type="button" on:click={() => showLocaleDropdown = !showLocaleDropdown}
		class="flex items-center gap-2">
		<img src={getLocaleFlag(l)} alt={l} class="w-8 opacity-50 "/>
		{#if wide}
			<div class="text-neutral-800 text-sm">{getLocaleName(l)}</div>
		{/if}
	</button>

	{#if showLocaleDropdown}
		<button transition:scaleFade type="button" 
			class="fixed inset-0 w-screen h-screen" on:click={() => showLocaleDropdown = false}></button>
		<div transition:scaleFade 
			class="absolute {leftMenu ? 'right-2' : ''} top-2 w-32
            bg-orange-50 rounded-xl flex flex-col gap-1 py-2 px-1 shadow-grocerite-orange-200-md">
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
