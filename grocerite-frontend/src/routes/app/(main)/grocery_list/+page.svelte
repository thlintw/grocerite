
<svelte:head>
	<title>{$_('groceryList_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="household" />
</svelte:head>

<script lang="ts">
	import { _, locale, locales } from 'svelte-i18n';
	import { lc } from '$lib/stores/general';
    import PlusButton from '$lib/components/PlusButton.svelte';
	import { authStore } from '$lib/stores/authStore';
    import { apiListHouseholds, apiSetActiveHousehold } from '$lib/api/household';
    import { Household } from '$lib/models/household';
    import type { RES } from '$lib/services/api';
    import { toast } from '@zerodevx/svelte-toast';
    import { onMount } from 'svelte';
    import LoadingDotsOrange from '$lib/components/LoadingDotsOrange.svelte';
    import Button from '$lib/components/Button.svelte';
    import { reloadUserProfile } from '$lib/api/user';

	let apiLoading = true;
	let loadFailed = false;
	let householdListData: Household[] | null = null;


	const setActiveHousehold = async (householdId: string) => {
		try {
			const res: RES = await apiSetActiveHousehold(householdId);
			if (res.status === 'S') {
				const reloaded = reloadUserProfile();
				if (!reloaded) {
					toast.push($_('household_setActiveFailed'));
				}
			} else {
				toast.push($_('household_setActiveFailed'));
			}
		} catch (error) {
			console.error(error);
			toast.push($_('household_setActiveFailed'));
		}
	}
	

    const loadApiHouseholdListData = async () => {
        apiLoading = true;
        loadFailed = false;
        try {
            const res: RES = await apiListHouseholds();
            apiLoading = false;
            console.log(res);
            if (res.status === 'S') {
                householdListData = res.data.map((item: any) => Household.fromJson(item));
            } else {
                loadFailed = true;
                toast.push($_('household_getFailed'))
            }

        } catch (error) {
            apiLoading = false;
            loadFailed = true;
            console.error(error);
            toast.push($_('household_getFailed'))
        }
    }

	onMount(async () => {
		if (!$authStore.userProfile?.lastUsedHousehold) {
			loadApiHouseholdListData();
		}
	});


</script>


<div class="flex flex-col w-full h-full gap-3 {$lc.text}">
    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('groceryList_pageTitle')}
        </span>
    </div>
	{#if !$authStore.userProfile?.lastUsedHousehold}
		
		<div class="flex flex-col w-full px-3 gap-7 h-full justify-center items-center">
			<div class="text-center flex flex-col gap-4 text-neutral-500">
				<span class="font-bold text-2xl">{$_('groceryList_noActiveHousehold')}</span>
				<span class="text-lg">{$_('groceryList_noActiveHouseholdLine2')}</span>
				<div class="mt-5 flex flex-col items-center">
				{#if apiLoading}
					<LoadingDotsOrange size="sm" />
				{:else if loadFailed}
					<span>{$_('groceryList_householdLoadFailed')}</span>
					<Button
						text={$_('groceryList_retryLoading')}
						on:click={() => loadApiHouseholdListData()}
						/>
				{:else if !apiLoading && !loadFailed && householdListData && householdListData.length > 0}
					{#each householdListData as household, i}
						<button class="w-full flex justify-center items-center drop-shadow-md drop-shadow-grocerite-orange-200-lg bg-orange-50 px-5 py-3 rounded-xl"
							on:click={() => setActiveHousehold(household.householdId)}>
							<div class="w-full flex gap-2 items-center">
								<div class="flex gap-3 flex-col">
									<div class="text-lg font-bold text-neutral-800 text-start">
										{household.name}
									</div>
									
								</div>
								
								<div class="relative ml-auto shrink-0">
									<div class="absolute -bottom-1 left-[50%] -translate-x-1/2 w-[2rem] h-[2rem] rounded-full bg-neutral-700/10 scale-y-[20%] origin-bottom z-0"></div>
									<img src={`/icons/household/household-icon-${String(household.iconIdx).padStart(2, '0')}.png`} alt="household icon" class="ml-auto w-[4rem] h-[4rem] z-10 relative"/>
								</div>
							</div>
						</button>
					{/each}
					
				{:else if !apiLoading && !loadFailed && householdListData && !householdListData.length}
					<span>{$_('groceryList_noHousehold')}</span>
				{:else}
					<span>{$_('groceryList_noHousehold')}</span>
				{/if}
				</div>
			</div>
		</div>
	{:else if !$authStore.userProfile?.lastUsedHousehold && $authStore.userProfile.lastUsedHousehold.groceryLists.length < 1 }
	
		<div class="flex flex-col w-full px-3 gap-7 h-full justify-center items-center">
			<div class="text-center flex flex-col gap-4 text-neutral-500">
				<span class="font-bold text-2xl">{$_('groceryList_noListsInHousehold')}</span>
				<span>{$_('groceryList_noListsInHouseholdLine2')}</span>
			</div>
			<div class="flex justify-center mt-3">
				<PlusButton />
			</div>
		</div>

	{/if}
</div>