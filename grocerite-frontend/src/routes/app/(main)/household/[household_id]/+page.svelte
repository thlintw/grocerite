<script lang="ts">
    import { onMount } from "svelte";
    import { lc } from "$lib/stores/general";
    import { _ } from "svelte-i18n";
    import { page } from "$app/stores";
    import { authStore } from "$lib/stores/authStore";
    import { goto } from "$app/navigation";
    import type { RES } from "$lib/services/api";
    import { apiGetHousehold } from "$lib/api/household";
    import LoadingDotsOrange from "$lib/components/LoadingDotsOrange.svelte";
    import { toast } from "@zerodevx/svelte-toast";
    import { Household } from "$lib/models/household";
    import Button from "$lib/components/Button.svelte";
    import { fade } from "svelte/transition";
    import { cubicOut, cubicIn } from "svelte/easing";

    let householdId = $page.params.household_id;
    let apiLoading = true;
    let loadFailed = false;
    let householdData: Household | null = null;

    const loadApiHouseholdData = async () => {
        apiLoading = true;
        loadFailed = false;
        try {
            const res: RES = await apiGetHousehold(householdId);
            apiLoading = false;
            console.log(res);
            if (res.status === 'S') {
                householdData = Household.fromJson(res.data[0]);
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
        loadApiHouseholdData();
	});
</script>


<div class="flex flex-col w-full h-full gap-3 {$lc.text} relative">
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
                on:click={() => loadApiHouseholdData()}
                />
        </div>
    </div>
    {:else}

    <div in:fade={{ easing: cubicOut, duration: 200, delay: 200 }} out:fade={{ easing: cubicIn, duration: 200 }}   
        class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {householdData?.name}
        </span>
    </div>
    {/if}


</div>
