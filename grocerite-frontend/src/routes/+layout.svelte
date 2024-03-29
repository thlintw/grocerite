<script>
	import Header from './Header.svelte';
	import './styles.css';
  	import { waitLocale } from 'svelte-i18n';

	export async function preload() {
		// awaits for the loading of the 'en-US' and 'en' dictionaries
		return waitLocale()
	}
</script>
  
<style>
/* You can also write additional styles here */
</style>
  
<div class="min-h-[calc(100dvh)] bg-orange-50 flex dark:bg-neutral-900">
	<nav class="p-4 xl:w-52 2xl:w-64">Navigation</nav>
	<main class="p-5 w-full flex">
		<div class="bg-orange-100 w-full h-full rounded-2xl">
			<slot></slot>
		</div>
	</main>
</div>