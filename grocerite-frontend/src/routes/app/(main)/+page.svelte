<script>
	import { onDestroy, onMount } from "svelte";
	import { _, locale, locales } from 'svelte-i18n';
	import { GroceryList } from "$lib/models/groceryList";
	import { Household } from "$lib/models/household";
	import { Member } from "$lib/models/household";
	import PlusButton from "$lib/components/PlusButton.svelte";
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  	import { faAsterisk, faUser, faCalendar, faBagShopping } from '@fortawesome/free-solid-svg-icons';
	import { lc } from '$lib/stores/general';
    import { goto } from "$app/navigation";
	import { authStore } from "$lib/stores/authStore";
    import { AuthService } from "$lib/services/auth";
    import { toast } from "@zerodevx/svelte-toast";
    import { dashboard, wakeUp } from "$lib/api/home";

	onMount(async () => {
		// console.log(await $authStore.user?.getIdToken())

		
	});
	
	// const dashboardGroceryLists = [];
	const dashboardHouseholds = [];
	

	const dashboardGroceryLists = [
		new GroceryList({
			idx: 1,
			name: 'starving to death im  so hunnnngry oh my  god',
			householdIdx: 1,
			iconIdx: 2,
			starred: true,
			asignee: new Member({
				userIdx: 1,
				name: 'You',
			}),
		}),
		new GroceryList({
			idx: 1,
			name: 'Baking supplies',
			householdIdx: 1,
			iconIdx: 12,
			asignee: new Member({
				userIdx: 1,
				name: 'Jeanne',
			}),
		}),
	];

	// const mockHouseholds = [
	// 	new Household({
	// 		idx: 1,
	// 		name: 'Home',
	// 		iconIdx: 1,
	// 		members: [
	// 			new Member({
	// 				userIdx: 1,
	// 				name: 'You',
	// 			}),
	// 			new Member({
	// 				userIdx: 2,
	// 				name: 'Jeanne',
	// 			}),
	// 		],
	// 	}),
	// ]

	let unsubscribe = null;
	let serverWokeUp = false;
	let dashData = null;
	
	onMount(async () => {
		// let authService = AuthService.getInstance();
		// console.log(authService);
		// try {
		// 	const greet = await wakeUp();
		// 	if (greet.status === 'S') {
		// 		try {
		// 			console.log('dashboard');
		// 			serverWokeUp = true;
		// 			const dashRes = await dashboard();
		// 			if (dashRes.status === 'S') {
		// 				dashData = dashRes.data[0];
		// 			}
		// 		} catch (e) {
		// 			console.error(e);
		// 			toast.push('failed to fetch dashboard data', {duration: 9999});
		// 		}
		// 	}
		// } catch (e) {
		// 	console.error(e);
		// 	toast.push('failed to wake up server', {duration: 9999});
		// }
		// docRef = doc(db, 'test', 'wfiQlTREK4Z0LVbWm9E6');
		// unsubscribe = onSnapshot(docRef, (doc) => {
		// 	console.log('Current data: ', doc.data());
		// });
	})

	onDestroy(() => {
		// if (unsubscribe) unsubscribe();
	})

</script>

<svelte:head>
	<title>{$_('home_metaTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="{$_('home_metaDescription')}" />
</svelte:head>

<div class="
	flex
	w-full h-full flex-col gap-4
">
	<div class="
		flex relative
		w-full flex-col bg-orange-50 mt-8 rounded-[2.5rem] shadow-grocerite-orange-200-md
	">
		<div class="
			{$lc.title} text-orange-500 drop-shadow-grocerite-orange-100-md relative pl-5 -top-6
		">
			{$_('home_activeList')}
		</div>
		<div class="
			flex relative -top-4 w-full
			px-4 my-2
			lg:px-5 lg:mb-2
			flex-col items-center gap-3
		">
			{#if dashboardGroceryLists.length}

				{#each dashboardGroceryLists as list}
					<div class="bg-orange-100 rounded-xl relative w-full px-3 py-3 flex">
						{#if list.starred}
							<div class="text-yellow-400 text-3xl absolute -top-3 -left-1">
								<FontAwesomeIcon icon={faAsterisk} />
							</div>
						{/if}
						<div class="flex flex-col w-full justify-center grow-0 overflow-hidden pr-1 gap-1">
							<div class="
								text-lg font-bold text-neutral-800 {$lc.text} 
								text-ellipsis text-nowrap whitespace-nowrap overflow-hidden break-all
								">
								{list.name}
							</div>
							<div class="flex text-sm gap-1 {$lc.text}">
								{#if list.asignee}
									<div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1">
										<div class="text-emerald-600">
											<FontAwesomeIcon
												icon={faUser}
												class="text-emerald-600"
											/>
										</div>
										<div class="text-neutral-800">
											{list.asignee.name}
										</div>
									</div>
								{/if}
								<div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1">
									<div class="text-emerald-600">
										<FontAwesomeIcon
											icon={faCalendar}
											class="text-emerald-600"
										/>
									</div>
									<div class="text-neutral-800">
										2024-12-31
									</div>
								</div>
								<div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1">
									<div class="text-emerald-600">
										<FontAwesomeIcon
											icon={faBagShopping}
											class="text-emerald-600"
										/>
									</div>
									<div class="text-neutral-800">
										70%
									</div>
								</div>
							</div>
						</div>
						<div class="relative ml-auto w-[4rem] h-[4rem] shrink-0">
							<div class="absolute -bottom-1 left-[50%] -translate-x-1/2 w-[2rem] h-[2rem] rounded-full bg-neutral-700/10 scale-y-[20%] origin-bottom z-0"></div>
							<img src={list.icon} alt={`icon for ${list.name}`} class="ml-auto w-[4rem] h-[4rem] z-10 relative"/>
						</div>
					</div>
				{/each}
			{:else}
				<div class="text-neutral-500">
					{$_('home_noActiveList')}
				</div>
			{/if}
			<PlusButton cls="mt-2" onClick={() => goto('/app/grocery_list/new')} />
		</div>
	</div>
	<div class="
		flex relative
		w-full flex-col bg-orange-50 mt-8 rounded-[2.5rem] shadow-grocerite-orange-200-md 
	">
		<div class="
			{$lc.title} text-orange-500 drop-shadow-grocerite-orange-100-md relative pl-5  -top-6
		">
			{$_('home_householdList')}
		</div>
		<div class="
			flex relative -top-4 w-full
			px-4 my-2
			lg:px-5 lg:mb-2
			flex-col items-center gap-3
		">
			{#if dashboardHouseholds.length}

				{#each dashboardHouseholds as household}
					<!-- <div class="bg-orange-100 rounded-xl relative w-full px-3 py-3 flex">
						{#if list.starred}
							<div class="text-yellow-400 text-3xl absolute -top-3 -left-1">
								<FontAwesomeIcon icon={faAsterisk} />
							</div>
						{/if}
						<div class="flex flex-col w-full justify-center grow-0 overflow-hidden pr-1 gap-1">
							<div class="
								text-lg font-bold text-neutral-800 {$lc.text} 
								text-ellipsis text-nowrap whitespace-nowrap overflow-hidden break-all
								">
								{list.name}
							</div>
							<div class="flex text-sm gap-1 {$lc.text}">
								{#if list.asignee}
									<div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1">
										<div class="text-emerald-600">
											<FontAwesomeIcon
												icon={faUser}
												class="text-emerald-600"
											/>
										</div>
										<div class="text-neutral-800">
											{list.asignee.name}
										</div>
									</div>
								{/if}
								<div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1">
									<div class="text-emerald-600">
										<FontAwesomeIcon
											icon={faCalendar}
											class="text-emerald-600"
										/>
									</div>
									<div class="text-neutral-800">
										2024-12-31
									</div>
								</div>
								<div class="bg-orange-50 rounded-md px-2 py-0.5 flex gap-1">
									<div class="text-emerald-600">
										<FontAwesomeIcon
											icon={faBagShopping}
											class="text-emerald-600"
										/>
									</div>
									<div class="text-neutral-800">
										70%
									</div>
								</div>
							</div>
						</div>
						<div class="relative ml-auto w-[4rem] h-[4rem] shrink-0">
							<div class="absolute -bottom-1 left-[50%] -translate-x-1/2 w-[2rem] h-[2rem] rounded-full bg-neutral-700/10 scale-y-[20%] origin-bottom z-0"></div>
							<img src={list.icon} alt={`icon for ${list.name}`} class="ml-auto w-[4rem] h-[4rem] z-10 relative"/>
						</div>
					</div> -->
				{/each}
			{:else}
				<div class="text-neutral-500">
					{$_('home_noHousehold')}
				</div>
			{/if}
			<PlusButton cls="mt-2" onClick={() => goto('/app/grocery_list/new')} />
		</div>
	</div>

</div>
