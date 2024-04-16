<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { _, locale } from "svelte-i18n";
    import { lc, showLoadingOverlay } from "$lib/stores/general";
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import FormInput from "$lib/components/FormInput.svelte";
    import Button from "$lib/components/Button.svelte";

    let showDialog = false;

    const openIconDialog = () => {
        showDialog = true;
    };

    const closeIconDialog = () => {
        showDialog = false;
    };


    let listName: string = '';
    let listIconPath: string = '';
    let listIconIdx: number = -1;

    onMount(() => {
        getLocalizedDefaultName();
        getRandomDefaultIconIdx();
    });


    const getLocalizedDefaultName = () => {
        let key = 'groceryList_newListDefaultName';
        let todayString = new Date().toLocaleDateString($locale!);
        listName = `${$_(key)} ${todayString}`;
    };

    const getRandomDefaultIconIdx = () => {
        const num = Math.floor(Math.random() * 8) + 1;
        listIconPath = `/icons/groceryList/groceryList-icon-${String(num).padStart(2, '0')}.png`;
        listIconIdx = num;
    };

    const getGroceryIcon = (iconPath: string) => {
        closeIconDialog();
        const regex = /groceryList-icon-(\d{2})\.png$/;
        const match = iconPath.match(regex);
        if (match && match[1]) {
            listIconPath = iconPath;
            listIconIdx = parseInt(match[1], 10);
        }
    };
    
</script>

<div class="flex flex-col w-full gap-3 {$lc.text}">

    <IconSelectionDialog 
        showDialog={showDialog}
        mode="groceryList"
        title="common_selectAnIcon"
        on:click:selectIcon={(e) => {
            getGroceryIcon(e.detail.iconPath);
        }}
        on:click:barrierDismiss={closeIconDialog}
    />

    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('newListForm_createNewList')}
        </span>
    </div>
    <div class="mt-2 flex flex-col gap-3">
        <FormInput 
            id="listName"
            label={$_('groceryList_labelListName')}
            placeholder={$_('groceryList_placeholderListName')}
            bind:value={listName}
        />

        <div class="w-full flex-col">
            <div class="{$lc.text} block text-lg text-neutral-700">
                {$_('groceryList_labelListIcon')}
            </div>
            <div class="w-full flex gap-3 items-center">
                <div class="flex items-center gap-3 p-3 bg-orange-50 rounded-lg">
                    <img src={listIconPath} alt="icon" class="w-20" />
                </div>
                <!-- <button type="button" on:click={openIconDialog}
                    class="p-2 bg-orange-500 rounded-lg text-white">
                    {$_('common_select')}
                </button> -->

                <Button
                    text={$_('common_select')}
                    on:click={openIconDialog}
                />
            </div>
        </div>
    </div>
</div>
