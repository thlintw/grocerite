<script>
	import './styles.css';
  	import { waitLocale } from 'svelte-i18n';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { AuthService } from '$lib/services/auth';
	import { authStore } from '$lib/stores/authStore';
	import '@fortawesome/fontawesome-svg-core/styles.css';


	export async function preload() {
		// awaits for the loading of the 'en-US' and 'en' dictionaries
		return waitLocale()
	}

	onMount(() => {
    	AuthService.getInstance();
		// authStore.subscribe((value) => {
		// 	if (value.user) {
		// 		goto('/');
		// 	} else {
		// 		goto('/login');
		// 	}
		// });
	});

</script>
  
  
<div class="min-h-[calc(100dvh)] bg-orange-50 flex dark:bg-neutral-900 w-full">
    <slot></slot>
</div>