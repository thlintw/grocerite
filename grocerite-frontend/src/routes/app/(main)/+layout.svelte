<script lang="ts">
	import '../../styles.css';
  	import { waitLocale } from 'svelte-i18n';
	import { onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import LocaleSwitch from '$lib/components/LocaleSwitch.svelte';
	import { scaleFade } from '$lib/transitions';
	import LoadingOverlay from '$lib/components/LoadingOverlay.svelte';
	import Dialogue from '$lib/components/Dialogue.svelte';
	import { lc } from '$lib/stores/general';
	import { _ } from 'svelte-i18n';
	import { fade } from 'svelte/transition';
	import { cubicIn, cubicOut } from 'svelte/easing';
	import { authStore } from '$lib/stores/authStore';
    import { faClose } from '@fortawesome/free-solid-svg-icons';
    import LoadingDots from '$lib/components/LoadingDots.svelte';
	import { getUserProfileFromFbUid } from '$lib/api/user';

	export let data;
	export async function preload() {
		return waitLocale()
	}

	onMount(() => {
		if (!$authStore.user) {
			authStore.subscribe(async ($authStore) => {
				if ($authStore.authStateChecked) {
					if (!$authStore.user) {
						goto('/app/login');
					}
				}
			});

		}
	});

	let showMobileMenu = false;

</script>
  

<!-- {#if $authStore.userProfile && $authStore.authStateChecked} -->
<div in:fade={{ duration: 400, delay: 400 }} out:fade={{ duration: 400 }}
	class="w-full h-full flex absolute left-0 top-0">

	<LoadingOverlay />
	<Dialogue />
	<nav class="
		flex
		fixed w-36 h-36 bg-orange-50 rounded-[60%] rounded-tl-[50%] rounded-br-[50%] border-2 border-orange-200 border-t-[.5rem]
		-bottom-10 -left-10 items-center justify-center
		lg:relative lg:h-[calc(100dvh)] lg:w-3/12 lg:rounded-none lg:border-none lg:top-0 lg:left-0 lg:flex-col 
		lg:items-end  z-[9999]
		">
		<button class="flex lg:hidden" type="button" on:click={() => showMobileMenu = true}>
			<img src='/image/logo-small.png' alt="Logo" class="h-14 ml-4 mb-6" />
		</button>

		{#if showMobileMenu}
			<button 
				transition:scaleFade
				class="
					fixed w-screen h-screen bg-opacity-50 left-0 top-0 z-[10000]
				"
				on:click={() => showMobileMenu = false}
			>

			</button>
		{/if}

		{#if showMobileMenu}
			<div class="
				transition:scaleFade
				nav-menu-sm flex
				fixed bottom-32 left-0
				flex-col items-center gap-5 p-4
				w-20 z-[10001]
			">
				<LocaleSwitch
					cls="relative"
				/>
			</div>
		{/if}

		<div class="
			hidden lg:flex
			nav-menu-lg flex-col items-end gap-5  p-4
		">
			<a class="" href="/app">
				<img src='/image/logo-full.png' alt="Logo" class="max-h-16" />
			</a>
			<a class="{$lc.title} text-base text-orange-300 
			hover:text-orange-500
			pr-2" href="/app/grocery_list">
				{$_('common_navGroceryList')}
			</a>
			<a class="{$lc.title} text-base text-orange-300 
			hover:text-orange-500
			pr-2" href="/app/household">
				{$_('common_navHousehold')}
			</a>
			<a class="{$lc.title} text-base text-orange-300 
			hover:text-orange-500
			pr-2" href="/app/settings">
				{$_('common_navSettings')}
			</a>
		</div>

		<LocaleSwitch
			cls="hidden lg:flex lg:fixed lg:top-5 lg:right-5"
			leftMenu={true}
		/>
	</nav>
	<main class="
		flex
		w-full 
		lg:w-6/12 
		lg:max-h-dvh lg:grow-0 lg:py-5
		">
		<div class="
			w-full bg-orange-100 p-3 lg:p-5 lg:rounded-[2rem]
			lg:overflow-y-auto lg:max-h-full no-scrollbar
			lg:border-4 border-orange-100
		">
		{#key data.pathname}
			<div in:fade={{ easing: cubicOut, duration: 200, delay: 200 }} out:fade={{ easing: cubicIn, duration: 200 }} class="w-full h-full">
				<slot />
			</div>
		{/key}
		</div>
	</main>

</div>
<!-- {:else}
<div in:fade={{ duration: 400, delay: 400 }} out:fade={{ duration: 400 }}
class="w-full h-screen flex justify-center items-center absolute left-0 top-0">
	<LoadingDots size="lg" />
</div>
{/if} -->
  