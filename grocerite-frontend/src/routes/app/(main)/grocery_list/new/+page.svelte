<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { _ } from "svelte-i18n";
    import { lc, showLoadingOverlay } from "$lib/stores/general";
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";

    let showDialog = false;

    const openIconDialog = () => {
        showDialog = true;
    };

    const closeIconDialog = () => {
        showDialog = false;
    };

    const getGroceryIcon = (iconPath: string) => {
        const regex = /groceryList-icon-(\d{2})\.png$/;
        const match = iconPath.match(regex);
        if (match && match[1]) {
            console.log(parseInt(match[1], 10));
            return parseInt(match[1], 10);
        }
        return null;
    };
</script>

<IconSelectionDialog 
    showDialog={showDialog}
    mode="groceryList"
    title="common_select"
    on:click:selectIcon={(e) => {
        getGroceryIcon(e.detail.iconPath);
    }}
    on:click:barrierDismiss={closeIconDialog}
    />
<div class="flex flex-col w-full gap-3">
    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('newListForm_createNewList')}
        </span>
    </div>
    <div class="w-full">
        <button type="button" on:click={openIconDialog}>
            test icon dialog
        </button>
    </div>
</div>
