<script>
	import { onMount } from "svelte";
	/** @type {import('./$types').PageData} */
	export let data;

	onMount(() => {
		console.log("mounted");
	});

</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
{data?.post.url}
</section>
