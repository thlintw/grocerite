<script lang="ts">
    import { onMount } from "svelte";
    import { lc } from "$lib/stores/general";
    import { _ } from "svelte-i18n";
    import { page } from "$app/stores";

    let householdId = $page.params.household_id;

    onMount(async () => {
    });
</script>


<div class="flex flex-col w-full gap-3 {$lc.text}">


    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {householdId}
        </span>
    </div>

</div>
