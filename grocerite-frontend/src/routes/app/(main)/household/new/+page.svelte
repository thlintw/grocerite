<script lang="ts">
    
    import { _, locale } from "svelte-i18n";
    import { lc } from "$lib/stores/general";
</script>


<div class="{$lc.title} text-2xl text-orange-500 flex items-center">
    <span class="whitespace-nowrap overflow-hidden text-ellipsis">
        {$_('newListForm_createNewList')}
    </span>
</div>