<script>
	import { onMount } from "svelte";
	import { _, locale, locales } from 'svelte-i18n';
	import { GroceryList } from "$lib/models/groceryList";
	import PlusButton from "$lib/components/PlusButton.svelte";
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  	import { faAsterisk } from '@fortawesome/free-solid-svg-icons';

	onMount(() => {
	});
	
	
	$: l = $locale;

	$: fontFamilyCls = l == 'ja-JP' || l == 'zh-TW' ? 'font-sans text-2xl font-bold -top-5' : 'font-berkshire text-3xl -top-6';
	$: normalTextCls = l == 'ja-JP' || l == 'zh-TW' ? 'font-sans' : 'font-serif';

	const mockActiveLists = [
		new GroceryList({
			idx: 1,
			name: 'starving to death im  so hunnnngry oh my  god',
			householdIdx: 1,
			iconIdx: 12,
			starred: true,
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
			px-4 my-2
			lg:px-5 lg:mb-2
			flex-col items-center gap-3
		">
			{#each mockActiveLists as list}
				<div class="bg-orange-100 rounded-xl relative w-full px-3 py-3 flex">
					{#if list.starred}
						<div class="text-yellow-400 text-3xl absolute -top-3 -left-1">
							<FontAwesomeIcon icon={faAsterisk} />
						</div>
					{/if}
					<div class="flex flex-col w-full justify-center grow-0 overflow-hidden pr-1">
						<div class="
							text-lg font-bold text-neutral-800 {normalTextCls} 
							text-ellipsis text-nowrap whitespace-nowrap overflow-hidden break-all
							">
							{list.name}
						</div>
						<div class="flex">

						</div>
					</div>
					<div class="relative ml-auto w-[4rem] h-[4rem] shrink-0">
						<div class="absolute -bottom-1 left-[50%] -translate-x-1/2 w-[2rem] h-[2rem] rounded-full bg-neutral-700/10 scale-y-[20%] origin-bottom z-0"></div>
						<img src={list.getIcon()} alt={`icon for ${list.name}`} class="ml-auto w-[4rem] h-[4rem] z-10 relative"/>
					</div>
				</div>
			{/each}
			<PlusButton cls="mt-1" onClick={() => console.log('134')} />
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
