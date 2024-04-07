<script>
	import { onMount } from "svelte";
	import { _, locale, locales } from 'svelte-i18n';
	import { GroceryList } from "$lib/models/groceryList";

	onMount(() => {
	});
	
	
	$: l = $locale;

	$: fontFamilyCls = l == 'ja-JP' || l == 'zh-TW' ? 'font-sans text-2xl font-bold -top-5' : 'font-berkshire text-3xl -top-6';

	const mockActiveLists = [
		new GroceryList({
			idx: 1,
			name: 'Active List 1',
			householdIdx: 1,
			iconIdx: 1,
		}),
	];

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
			{fontFamilyCls} text-orange-500 drop-shadow-grocerite-orange-100-md relative pl-5
		">
			{$_('home_activeList')}
		</div>
		<div class="
			flex relative -top-4 w-full
			px-5 my-2
			lg:px-6 lg:mb-2
		">
			{#each mockActiveLists as list}
				<div class="bg-orange-100 rounded-xl relative w-full px-3 py-3">
					<div class="relative ml-auto w-[4rem] h-[4rem] -top-1">
						<div class="absolute -bottom-1 left-[50%] -translate-x-1/2 w-[2rem] h-[2rem] rounded-full bg-neutral-700/10 scale-y-[20%] origin-bottom z-0"></div>
						<img src={list.getIcon()} alt={`icon for ${list.name}`} class="ml-auto w-[4rem] h-[4rem] z-10 relative"/>
					</div>
				</div>
			{/each}
		</div>
	</div>
	<div class="
		flex relative
		w-full flex-col bg-orange-50 mt-8 rounded-3xl shadow-grocerite-orange-200-md
	">
		<div class="
			{fontFamilyCls} text-orange-500 drop-shadow-grocerite-orange-100-md relative pl-5
		">
			{$_('home_householdList')}
		</div>

	</div>

</div>
