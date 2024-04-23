<script lang="ts">
    import DateDialog from "$lib/components/DateDialog.svelte";
import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import ListPropCardButton from "$lib/components/ListPropCardButton.svelte";
    import NewGroceryListItemDialog from "$lib/components/NewGroceryListItemDialog.svelte";
    import PlusButton from "$lib/components/PlusButton.svelte";
    import ScrollableSelectDialog from "$lib/components/ScrollableSelectDialog.svelte";
    import TextInputDialog from "$lib/components/TextInputDialog.svelte";
    import { Container, ContainerItem, ContainerType } from "$lib/models/container";
    import { GroceryListItem } from "$lib/models/groceryList";
    import { Member } from "$lib/models/household";
    import { ItemCategory } from "$lib/models/item";
    import { Store } from "$lib/models/store";
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

    let showNewItemDialog = false;
    const setNewItemDialog = (value: boolean) => showNewItemDialog = value;


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

    const tempHouseholdMembers = [
        new Member({
            userIdx: 0,
            pfp: {
                presenting: 'fp',
                idx: 1,
                bgColor: '#FFD700'
            },
            name: 'Alice',
        }),
        new Member({
            userIdx: 1,
            pfp: {
                presenting: 'mp',
                idx: 2,
                bgColor: '#FF6347'
            },
            name: 'Bob',
        }),
        new Member({
            userIdx: 2,
            pfp: {
                presenting: 'nb',
                idx: 3,
                bgColor: '#FF69B4'
            },
            name: 'Charlie',
        }),
        new Member({
            userIdx: 3,
            pfp: {
                presenting: 'fp',
                idx: 4,
                bgColor: '#FFD700'
            },
            name: 'Diana',
        }),
    ]

    const tempMemberList = tempHouseholdMembers.map((member) => {
        return {
            iconPath: `/icons/avatar/${member.pfp.presenting}/avatar-${member.pfp.presenting}-${member.pfp.idx.toString().padStart(2, '0')}.png`,
            iconBg: member.pfp.bgColor,
            value: member.userIdx.toString(),
            label: member.name,
        };
    })

    const tempMemberListWithNull = [
        {
            iconPath: 'x',
            iconBg: '',
            value: '-1',
            label: 'groceryList_cancelAsigneeSelection',
        },
        ...tempMemberList
    ];

    const getMemberFromIdx = (idx: number) => {
        return tempHouseholdMembers.find((member) => member.userIdx === idx);
    };

    const tempAvailableItems = [
        new ContainerItem({
            idx: 0,
            name: 'Apple',
            quantity: 0,
            category: ItemCategory.Fruits
        }),
        new ContainerItem({
            idx: 1,
            name: 'Banana',
            quantity: 3,
            category: ItemCategory.Fruits
        }),
        new ContainerItem({
            idx: 2,
            name: 'Carrot',
            quantity: 3,
            category: ItemCategory.Vegetables
        }),
        new ContainerItem({
            idx: 3,
            name: 'Milk',
            quantity: 1,
            category: ItemCategory.DairyAndEggs
        }),
        new ContainerItem({
            idx: 4,
            name: 'Eggs',
            quantity: 6,
            category: ItemCategory.DairyAndEggs
        }),
        new ContainerItem({
            idx: 5,
            name: 'Bread',
            quantity: 0,
            category: ItemCategory.BakeryAndBread
        }),
    ]

    const tempAvailableStores = [
        new Store({
            name: 'Walmart',
            idx: 0,
            location: '1234 Main St, Springfield, IL 62701'
        })
    ]

    const tempAvailableContainers = [
        new Container({
            name: 'Fridge',
            idx: 0,
            iconIdx: 1,
            type: ContainerType.Refridgerator
        }),
        new Container({
            name: 'Pantry',
            idx: 1,
            iconIdx: 2,
            type: ContainerType.Pantry
        }),
    ]

    $: availableMembers = tempMemberListWithNull;
    $: availableItems = tempAvailableItems.map((item) => {
        return {
            value: item.idx.toString(),
            label: item.name,
        };
    });
    $: availableStores = tempAvailableStores;

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
        options={availableMembers}
        on:click:selectOption={(e) => {
            if (e.detail.option.value !== '-1') {
                let ass = getMemberFromIdx(parseInt(e.detail.option.value, 10));
                if (ass) listAssignee = ass;
            } else {
                listAssignee = null;
            }
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

    <NewGroceryListItemDialog
        showDialog={showNewItemDialog}
        availableItems={availableItems}
        availableContainers={tempAvailableContainers}
        on:click:barrierDismiss={(e) => {
            setNewItemDialog(false);
        }}
        on:click:selectOption={(e) => {
            console.log(e.detail.selected);
        }}
        title='groceryList_addListItemsDialogTitle'
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
            <span class="text-neutral-700 font-normal">{listName}</span>
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setIconDialog(true)}
            icon={faSun}
            headerText={$_('groceryList_labelListIcon')}
            >
            <img src={listIconPath} alt="icon" class="w-20" />
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setDeadlineDialog(true)}
            icon={faCalendar}
            headerText={$_('groceryList_labelListDeadline')}
            optional={true}
            >
            {#if !listDeadline}
            <div class="text-neutral-300 text-base font-normal flex items-center gap-2">
                <div class="text-neutral-200">
                    <FontAwesomeIcon icon={faCalendarXmark} class="text-[3rem]" />
                </div>
            </div>
            {:else if listDeadline}
                <span class="text-neutral-700 font-normal">{ formattedDeadline }</span>
            {/if}
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setAssigneeDialog(true)}
            icon={faUser}
            headerText={$_('groceryList_labelListAsignee')}
            optional={true}
            >
            {#if !listAssignee}
            <div class="text-neutral-300 text-base font-normal flex items-center gap-2">
                <div class="text-neutral-200">
                    <FontAwesomeIcon icon={faUserAltSlash} class="text-[3rem]" />
                </div>
            </div>
            {:else if listAssignee}
                <div class="flex items-center gap-2">
                    <div class="rounded-full"
                        style={`background-color: ${listAssignee.pfp.bgColor}`}>
                        <img src={`/icons/avatar/${listAssignee.pfp.presenting}/avatar-${listAssignee.pfp.presenting}-${listAssignee.pfp.idx.toString().padStart(2, '0')}.png`} alt="assignee" class="w-16 h-16 rounded-full" />
                    </div>
                    <span>{listAssignee.name}</span>
                </div>
            {/if}
        </ListPropCardButton>

    </div>
    <div class="flex-col w-full mt-5">
        <div class="w-full flex items-center justify-start">
            <PlusButton
                onClick={() => {
                    setNewItemDialog(true);
                }}
                />
            <div class="text-orange-500 text-base font-normal ml-2 {$lc.text}">
                {$_('groceryList_addListItems')}
            </div>
        </div>
    </div>
</div>
