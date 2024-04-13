
<svelte:head>
	<title>{$_('household_pageTitle')}</title>
	<meta name="description" content="household" />
</svelte:head>

<script lang="ts">
	import { _, locale, locales } from 'svelte-i18n';

</script>

<div class="bg-red-200">
    12345
	{$_('common_signIn')}


<select bind:value={$locale}>
	{#each $locales as locale}
	  <option value={locale}>{locale}</option>
	{/each}
  </select>
</div>