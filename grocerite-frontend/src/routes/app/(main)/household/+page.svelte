
<svelte:head>
	<title>{$_('household_pageTitle')} - {$_('common_appName')}</title>
	<meta name="description" content="household" />
</svelte:head>

<script lang="ts">
	import { _, locale, locales } from 'svelte-i18n';
	import { lc } from '$lib/stores/general';
    import PlusButton from '$lib/components/PlusButton.svelte';

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
		<div class="text-center flex flex-col gap-4 text-neutral-500">
			<span class="font-bold text-2xl">You don't have any household yet</span>
			<span>Create one to start sharing your grocery lists with your family members</span>
		</div>
		<div class="flex justify-center mt-3">
			<PlusButton />
		</div>
    </div>
</div>