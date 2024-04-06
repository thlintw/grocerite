<script>
	import { onMount } from "svelte";
	/** @type {import('./$types').PageData} */
	export let data;

	onMount(() => {
	});

</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<div class="
	flex
	w-full h-full flex-col gap-4
">
	<div class="
		flex relative
		w-full flex-col bg-orange-50 mt-8 rounded-3xl shadow-grocerite-orange-200-md
	">
		<div class="
			font-berkshire text-orange-500 text-3xl drop-shadow-grocerite-orange-100-md relative -top-6 pl-5
		">
			Active
		</div>

	</div>
	<div class="
		flex relative
		w-full flex-col bg-orange-50 mt-8 rounded-3xl shadow-grocerite-orange-200-md
	">
		<div class="
			font-berkshire text-orange-500 text-3xl drop-shadow-grocerite-orange-100-md relative -top-6 pl-5
		">
			Households
		</div>

	</div>

</div>
