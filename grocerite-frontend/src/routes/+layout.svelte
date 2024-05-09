<script>
	import './styles.css';
  	import { waitLocale } from 'svelte-i18n';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { AuthService } from '$lib/services/auth';
	import { authStore } from '$lib/stores/authStore';
	import { SvelteToast } from '@zerodevx/svelte-toast'
	import '@fortawesome/fontawesome-svg-core/styles.css';
	import { fade } from 'svelte/transition';
	import { cubicIn, cubicOut } from 'svelte/easing';

	export let data;


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

	const options = {
  	}

</script>
  
<SvelteToast {options} />
<!-- {#key data.pathname} -->
	<div class="min-h-[calc(100dvh)] bg-orange-50 flex dark:bg-neutral-900 w-full"
		in:fade={{ duration: 200, delay: 200 }} out:fade={{ duration: 200 }}>
		<slot></slot>
	</div>
<!-- {/key} -->