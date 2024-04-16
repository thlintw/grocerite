<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { _, locale } from "svelte-i18n";
    import { lc, showLoadingOverlay } from "$lib/stores/general";
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import FormInput from "$lib/components/FormInput.svelte";
    import Button from "$lib/components/Button.svelte";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import { faComment, faPen, faSun, faUser } from "@fortawesome/free-solid-svg-icons";
    import TextInputDialog from "$lib/components/TextInputDialog.svelte";

    let showIconDialog = false;

    const setIconDialog = (value: boolean) => showIconDialog = value;

    let showListNameDialog = false;

    const setListNameDialog = (value: boolean) => showListNameDialog = value;


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
        setIconDialog(false);
        const regex = /groceryList-icon-(\d{2})\.png$/;
        const match = iconPath.match(regex);
        if (match && match[1]) {
            listIconPath = iconPath;
            listIconIdx = parseInt(match[1], 10);
        }
    };

    const handleListNameKeyUp = (e: CustomEvent) => {
        const key = e.detail.key;
        if (key === 'Enter' || key === 'Escape') {
            setListNameDialog(false);
        }
    };

</script>

<div class="flex flex-col w-full gap-3 {$lc.text}">

    <IconSelectionDialog 
        showDialog={showIconDialog}
        mode="groceryList"
        title="common_selectAnIcon"
        on:click:selectIcon={(e) => {
            getGroceryIcon(e.detail.iconPath);
        }}
        on:click:barrierDismiss={(e) => {
            setIconDialog(false);
        }}
    />

    <TextInputDialog
        title="groceryList_listNameDialogTitle"
        showDialog={showListNameDialog}
        bind:value={listName}
        placeholder="groceryList_placeholderListName"
        showRefreshButton={true}
        on:click:barrierDismiss={(e) => {
            setListNameDialog(false);
        }}
        on:keyup={handleListNameKeyUp}
        on:click:refresh={() => {
            getLocalizedDefaultName();
        }}
        />


    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('newListForm_createNewList')}
        </span>
    </div>
    <div class="grid gap-3 w-full grid-cols-2 2xl:grid-cols-3">
        <button class="flex flex-col rounded-xl bg-orange-50 p-2 shrink-0"
            on:click={() => setListNameDialog(true)}>
            <div class="flex items-center gap-2 text-lg w-full px-2">
                <FontAwesomeIcon
                    icon={faComment}
                    class="text-emerald-700"
                    />
                <span>{$_('groceryList_labelListName')}</span>
                <div class="ml-auto">
                    <FontAwesomeIcon
                        icon={faPen}
                        class="text-orange-500"
                        />
                </div>
            </div>
            <div class="flex grow font-bold px-3 py-1 justify-center items-center text-left">
                <span>{listName}</span>
            </div>
        </button>
        <button class="flex flex-col rounded-xl bg-orange-50 p-2 shrink-0" 
            on:click={() => setIconDialog(true)}>
            <div class="flex items-center gap-2 text-lg w-full">
                <FontAwesomeIcon
                    icon={faSun}
                    class="text-emerald-700"
                    />
                <span>{$_('groceryList_labelListIcon')}</span>
                <div class="ml-auto">
                    <FontAwesomeIcon
                        icon={faPen}
                        class="text-orange-500"
                        />
                </div>
            </div>
            <div class="flex font-bold px-3 py-1 items-center justify-center overflow-hidden w-full">
                <img src={listIconPath} alt="icon" class="w-20" />
            </div>
        </button>
    </div>
</div>
