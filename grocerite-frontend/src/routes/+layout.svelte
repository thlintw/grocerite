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
  
<div class="min-h-screen bg-gray-100">
	<header class="bg-blue-500 text-white p-4">Header</header>
	<nav class="bg-gray-200 p-4">Navigation</nav>
	<main class="p-8 h-full">
		<slot></slot> <!-- This is where nested routes will be rendered -->
	</main>
	<footer class="bg-gray-800 text-white p-4">Footer</footer>
</div>