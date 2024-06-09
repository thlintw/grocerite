
<svelte:head>
	<title>{$_('household_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="household" />
</svelte:head>

<script lang="ts">
	import { _, locale, locales } from 'svelte-i18n';
	import { lc } from '$lib/stores/general';
    import PlusButton from '$lib/components/PlusButton.svelte';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Household } from '$lib/models/household';
    import { apiListHouseholds } from '$lib/api/household';
    import type { RES } from '$lib/services/api';
    import { toast } from '@zerodevx/svelte-toast';
    import { fade } from 'svelte/transition';
    import { cubicIn, cubicInOut, cubicOut } from 'svelte/easing';
    import LoadingDotsOrange from '$lib/components/LoadingDotsOrange.svelte';
    import Button from '$lib/components/Button.svelte';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { faBox, faFile, faList, faUser } from '@fortawesome/free-solid-svg-icons';

	const goCreateHousehold = () => {
		goto('/app/household/new');
	};

    let apiLoading = true;
    let loadFailed = false;
    let householdListData: Household[] | null = null;

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
		if (!householdListData) loadApiHouseholdListData();
	});

	const goHousehold = (householdId: string) => {
		goto(`/app/household/${householdId}`);
	}


</script>


<div class="flex flex-col w-full h-full gap-3 {$lc.text}">
    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('household_pageTitle')}
        </span>
    </div>
	<!-- {#if}
	{/if} -->

	<div class="flex flex-col w-full px-3 gap-7 h-full justify-center items-center">
		{#if apiLoading && !loadFailed}
			<div in:fade={{ easing: cubicOut, duration: 200, delay: 200 }} out:fade={{ easing: cubicIn, duration: 200 }}
				class="w-full h-full flex justify-center items-center absolute left-0 top-0">
				<div>
					<LoadingDotsOrange size="md" />
				</div>
		
			</div>
		{:else if loadFailed && !apiLoading}
			<div in:fade={{ easing: cubicOut, duration: 200, delay: 200 }} out:fade={{ easing: cubicIn, duration: 200 }} 
				class="w-full h-full flex justify-center items-center absolute left-0 top-0">
				<div class="flex flex-col">
					<div class="text-lg mb-12">
						{$_('household_getFailed')}
					</div>
					<Button
						text={$_('household_retryLoading')}
						on:click={() => loadApiHouseholdListData()}
						/>
				</div>
			</div>

		{:else if !loadFailed && !apiLoading && householdListData && householdListData.length === 0 || !householdListData}
			<div in:fade={{ easing: cubicOut, duration: 200, delay: 200 }} out:fade={{ easing: cubicIn, duration: 200 }} 
				class="w-full h-full flex justify-center items-center absolute left-0 top-0">


				<div class="text-center flex flex-col gap-4 text-neutral-500">
					<span class="font-bold text-2xl">You don't have any household yet</span>
					<span>Create one to start sharing your grocery lists with your family members</span>
				</div>
				<div class="flex justify-center mt-3">
					<PlusButton onClick={goCreateHousehold} />
				</div>
			</div>
    	{:else}
			<div in:fade={{ easing: cubicOut, duration: 200, delay: 200 }} out:fade={{ easing: cubicIn, duration: 200 }} 
				class="w-full h-full flex flex-col pt-3">

				{#each householdListData as household, i}
					<button class="w-full flex justify-center items-center drop-shadow-md drop-shadow-grocerite-orange-200-lg bg-orange-50 px-5 py-3 rounded-xl"
						on:click={() => goHousehold(household.householdId)}>
						<div class="w-full flex gap-2 items-center">
							<div class="flex gap-3 flex-col">
								<div class="text-lg font-bold text-neutral-800 text-start">
									{household.name}
								</div>
								<div class="flex gap-3 pl-1">
									<div class="text-sm text-neutral-500 flex">
										<div class="bg-orange-100 rounded-md px-2 py-0.5 flex gap-1">
											<div class="text-emerald-600">
												<FontAwesomeIcon
													icon={faUser}
													class="text-emerald-600"
												/>
											</div>
											<div class="text-neutral-800">
												{ household.members.length }
											</div>
										</div>
									</div>
									<div class="text-sm text-neutral-500 flex">
										<div class="bg-orange-100 rounded-md px-2 py-0.5 flex gap-1">
											<div class="text-emerald-600">
												<FontAwesomeIcon
													icon={faBox}
													class="text-emerald-600"
												/>
											</div>
											<div class="text-neutral-800">
												{ household.containers.length }
											</div>
										</div>
									</div>
									<div class="text-sm text-neutral-500 flex">
										<div class="bg-orange-100 rounded-md px-2 py-0.5 flex gap-1">
											<div class="text-emerald-600">
												<FontAwesomeIcon
													icon={faFile}
													class="text-emerald-600"
												/>
											</div>
											<div class="text-neutral-800">
												{ household.groceryLists.length }
											</div>
										</div>
									</div>

								</div>
							</div>
							
							<div class="relative ml-auto shrink-0">
								<div class="absolute -bottom-1 left-[50%] -translate-x-1/2 w-[2rem] h-[2rem] rounded-full bg-neutral-700/10 scale-y-[20%] origin-bottom z-0"></div>
								<img src={`/icons/household/household-icon-${String(household.iconIdx).padStart(2, '0')}.png`} alt="household icon" class="ml-auto w-[4rem] h-[4rem] z-10 relative"/>
							</div>
						</div>
					</button>
				{/each}
				
				<div class="flex justify-center mt-8">
					<PlusButton onClick={goCreateHousehold} />
				</div>
			</div>


		{/if}
	</div>

</div>