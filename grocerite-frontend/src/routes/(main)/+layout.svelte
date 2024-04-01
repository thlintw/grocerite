<script>
	import '../styles.css';
  	import { waitLocale } from 'svelte-i18n';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	export async function preload() {
		// awaits for the loading of the 'en-US' and 'en' dictionaries
		return waitLocale()
	}
</script>
  
<style>
/* You can also write additional styles here */
</style>
  
<nav class="p-4 xl:w-52 2xl:w-64">Navigation</nav>
<main class="p-5 w-full flex">
	<div class="bg-orange-100 w-full h-full rounded-2xl">
		<slot></slot>
	</div>
</main>