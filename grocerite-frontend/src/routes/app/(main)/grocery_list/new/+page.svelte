<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { _ } from "svelte-i18n";
    import { lc } from "$lib/stores/general";
</script>

<div class="flex flex-col w-full gap-3">
    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('newListForm_createNewList')}
        </span>
    </div>
</div>
