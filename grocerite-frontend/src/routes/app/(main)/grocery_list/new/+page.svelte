<script lang="ts">
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import ListPropCardButton from "$lib/components/ListPropCardButton.svelte";
    import TextInputDialog from "$lib/components/TextInputDialog.svelte";
    import { lc } from "$lib/stores/general";
    import { faCalendar, faComment, faSun, faUser } from "@fortawesome/free-solid-svg-icons";
    import { onMount } from "svelte";
    import { _, locale } from "svelte-i18n";

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
    <div class="grid gap-3 w-full grid-cols-2">
        <ListPropCardButton
            onClick={() => setListNameDialog(true)}
            icon={faComment}
            headerText={$_('groceryList_labelListName')}
            >
            <span>{listName}</span>
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setIconDialog(true)}
            icon={faSun}
            headerText={$_('groceryList_labelListIcon')}
            >
            <img src={listIconPath} alt="icon" class="w-20" />
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setIconDialog(true)}
            icon={faCalendar}
            headerText={$_('groceryList_labelListDeadline')}
            >
            <img src={listIconPath} alt="icon" class="w-20" />
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setIconDialog(true)}
            icon={faUser}
            headerText={$_('groceryList_labelListAsignee')}
            >
            <img src={listIconPath} alt="icon" class="w-20" />
        </ListPropCardButton>
    </div>
</div>
