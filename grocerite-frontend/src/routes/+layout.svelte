<script>
	import './styles.css';
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
  
<div class="min-h-[calc(100dvh)] bg-orange-50 flex dark:bg-neutral-900">
    <slot></slot>
</div>