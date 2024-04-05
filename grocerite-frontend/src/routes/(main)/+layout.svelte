<script>
	import '../styles.css';
  	import { waitLocale } from 'svelte-i18n';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import logoFull from '$lib/images/logo-full.png';
	import logoSmall from '$lib/images/logo-small.png';

	export async function preload() {
		// awaits for the loading of the 'en-US' and 'en' dictionaries
		return waitLocale()
	}
</script>
  
<style>
/* You can also write additional styles here */
</style>
  
<nav class="
	flex
	fixed w-40 h-40 bg-orange-50 rounded-[60%] rounded-tl-[50%] rounded-br-[50%] border-2 border-orange-200 border-t-[.5rem]
	-bottom-10 -left-10 items-center justify-center
	lg:h-full lg:w-2/12 lg:rounded-none lg:border-none lg:top-0 lg:left-0 lg:flex-col 
	
">
	<div class="flex lg:hidden">
		<img src={logoSmall} alt="Logo" class="h-16 ml-4 mb-6" />
	</div>
	<div class="hidden lg:flex flex-col p-4">
		<div class="">
			<img src={logoFull} alt="Logo" class="max-h-16" />
		</div>
	</div>
</nav>
<main class="p-5 w-full flex bg-orange-100">
	<slot></slot>
</main>