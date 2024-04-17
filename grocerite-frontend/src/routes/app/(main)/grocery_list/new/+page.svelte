<script lang="ts">
    import DateDialog from "$lib/components/DateDialog.svelte";
import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import ListPropCardButton from "$lib/components/ListPropCardButton.svelte";
    import ScrollableSelectDialog from "$lib/components/ScrollableSelectDialog.svelte";
    import TextInputDialog from "$lib/components/TextInputDialog.svelte";
    import type { Member } from "$lib/models/household";
    import { lc } from "$lib/stores/general";
    import { faCalendar, faCalendarXmark, faComment, faSun, faUser, faUserAltSlash } from "@fortawesome/free-solid-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import { onMount } from "svelte";
    import { _, locale } from "svelte-i18n";

    let showIconDialog = false;
    const setIconDialog = (value: boolean) => showIconDialog = value;

    let showListNameDialog = false;
    const setListNameDialog = (value: boolean) => showListNameDialog = value;

    let showAssigneeDialog = false;
    const setAssigneeDialog = (value: boolean) => showAssigneeDialog = value;

    let showDeadlineDialog = false;
    const setDeadlineDialog = (value: boolean) => showDeadlineDialog = value;


    let listName: string = '';
    let listIconPath: string = '';
    let listIconIdx: number = -1;
    let listAssignee: Member | null = null;
    let listDeadline: Date | null = null;

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

    const getFormattedDeadline = (date: Date, locale: string) => {
        return date.toLocaleDateString(locale);
    };

    $: formattedDeadline = listDeadline && $locale ? getFormattedDeadline(listDeadline, $locale) : '';



    const tempMemberList = [
        {
            iconPath: '/icons/avatar/fp/avatar-fp-01.png',
            label: 'Alice',
            value: 'Alice'
        },
        {
            iconPath: '/icons/avatar/mp/avatar-mp-02.png',
            label: 'Bob',
            value: 'Bob'
        },
        {
            iconPath: '/icons/avatar/nb/avatar-nb-03.png',
            label: 'Charlie',
            value: 'Charlie'
        },
        {
            iconPath: '/icons/avatar/fp/avatar-fp-04.png',
            label: 'Diana',
            value: 'Diana'
        },
        {
            iconPath: '/icons/avatar/mp/avatar-mp-05.png',
            label: 'Eve',
            value: 'Eve'
        },
        {
            iconPath: '/icons/avatar/nb/avatar-nb-05.png',
            label: 'Frank',
            value: 'Frank'
        },
        {
            iconPath: '/icons/avatar/fp/avatar-fp-07.png',
            label: 'Grace',
            value: 'Grace'
        },
        {
            iconPath: '/icons/avatar/mp/avatar-mp-08.png',
            label: 'Hank',
            value: 'Hank'
        },
        {
            iconPath: '/icons/avatar/nb/avatar-nb-01.png',
            label: 'Ivy',
            value: 'Ivy'
        },
        {
            iconPath: '/icons/avatar/fp/avatar-fp-10.png',
            label: 'Jack',
            value: 'Jack'
        },
    ];

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

    <ScrollableSelectDialog
        showDialog={showAssigneeDialog}
        title="groceryList_placeholderSelectAsignee"
        on:click:barrierDismiss={(e) => {
            setAssigneeDialog(false);
        }}
        options={tempMemberList}
        on:click:selectOption={(e) => {
            listAssignee = e.detail.option.value;
            setAssigneeDialog(false);
        }}
        />

    <DateDialog
        showDialog={showDeadlineDialog}
        title="groceryList_placeholderSelectDeadline"
        on:click:barrierDismiss={(e) => {
            setDeadlineDialog(false);
        }}
        on:click:selectDate={(e) => {
            listDeadline = e.detail.date;
            setDeadlineDialog(false);
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
            onClick={() => setAssigneeDialog(true)}
            icon={faUser}
            headerText={$_('groceryList_labelListAsignee')}
            >
            {#if !listAssignee}
            <div class="text-neutral-300 text-base font-normal flex items-center gap-2">
                <div class="text-neutral-200">
                    <FontAwesomeIcon icon={faUserAltSlash} class="text-[3rem]" />
                </div>
            </div>
            {:else if listAssignee}
                <span>{listAssignee.label}</span>
            {/if}
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setDeadlineDialog(true)}
            icon={faCalendar}
            headerText={$_('groceryList_labelListDeadline')}
            >
            {#if !listDeadline}
            <div class="text-neutral-300 text-base font-normal flex items-center gap-2">
                <div class="text-neutral-200">
                    <FontAwesomeIcon icon={faCalendarXmark} class="text-[3rem]" />
                </div>
            </div>
            {:else if listDeadline}
                <span>{ formattedDeadline }</span>
            {/if}
        </ListPropCardButton>
    </div>
</div>
