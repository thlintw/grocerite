<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { _ } from "svelte-i18n";
    import { lc, showLoadingOverlay } from "$lib/stores/general";
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import FormInput from "$lib/components/FormInput.svelte";

    let showDialog = false;

    const openIconDialog = () => {
        showDialog = true;
    };

    const closeIconDialog = () => {
        showDialog = false;
    };

    let selectedIconPath: string = "";
    let selectedIconIdx: number = -1;

    const getGroceryIcon = (iconPath: string) => {
        closeIconDialog();
        const regex = /groceryList-icon-(\d{2})\.png$/;
        const match = iconPath.match(regex);
        if (match && match[1]) {
            selectedIconPath = iconPath;
            selectedIconIdx = parseInt(match[1], 10);
        }
    };
</script>

<IconSelectionDialog 
    showDialog={showDialog}
    mode="groceryList"
    title="common_selectAnIcon"
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
        {#if selectedIconIdx !== -1}
        <div class="flex items-center gap-3">
            <img src={`/icons/groceryList/groceryList-icon-${String(selectedIconIdx).padStart(2, '0')}.png`} alt="icon" class="w-20" />
            <span>selected idx: {selectedIconIdx}</span>
        </div>
        {/if}
        <button type="button" on:click={openIconDialog}>
            test icon dialog
        </button>
    </div>
    <FormInput 
        id="test"
        label="This is label"
        placeholder="This is placeholder"
    />
</div>
