<script>
	import '../styles.css';
  	import { waitLocale } from 'svelte-i18n';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import logoFull from '$lib/images/logo-full.png';
	import logoSmall from '$lib/images/logo-small.png';
	import LocaleSwitch from '$lib/components/LocaleSwitch.svelte';
	import { scaleFade } from '$lib/transitions';

	export async function preload() {
		return waitLocale()
	}

	let showMobileMenu = false;
</script>
  
<style>
/* You can also write additional styles here */
</style>
  
<nav class="
	flex
	fixed w-40 h-40 bg-orange-50 rounded-[60%] rounded-tl-[50%] rounded-br-[50%] border-2 border-orange-200 border-t-[.5rem]
	-bottom-10 -left-10 items-center justify-center
	lg:relative lg:h-[calc(100dvh)] lg:w-3/12 lg:rounded-none lg:border-none lg:top-0 lg:left-0 lg:flex-col 
	lg:items-end 
">
	<button class="flex lg:hidden" type="button" on:click={() => showMobileMenu = true}>
		<img src={logoSmall} alt="Logo" class="h-16 ml-4 mb-6" />
	</button>

	{#if showMobileMenu}
		<button 
			transition:scaleFade
			class="
				fixed w-screen h-screen bg-blue-500 bg-opacity-50 left-0 top-0
			"
			on:click={() => showMobileMenu = false}
		>

		</button>
	{/if}

	{#if showMobileMenu}
		<div class="
			transition:scaleFade
			nav-menu-sm flex
			fixed bottom-0 left-0 bg-red-200
			flex-col items-center gap-5 p-4
		">
			<LocaleSwitch
				cls="relative"
			/>
		</div>
	{/if}

	<div class="
		hidden lg:flex
		nav-menu-lg flex-col items-center gap-5  p-4
	">
		<div class="">
			<img src={logoFull} alt="Logo" class="max-h-16 mr-4" />
		</div>
	</div>
	
	<LocaleSwitch
		cls="hidden lg:flex lg:fixed lg:top-5 lg:right-5"
		leftMenu={true}
	/>
</nav>
<main class="
	flex
	p-5 w-full bg-orange-100
	lg:w-6/12 lg:border-r-4 lg:border-l-4 lg:border-orange-200
">
	<slot></slot>
</main>