<script lang="ts">
    
    import { _, locale } from "svelte-i18n";
    import { lc } from "$lib/stores/general";
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import TextInputDialog from "$lib/components/TextInputDialog.svelte";
    import ListPropCardButton from "$lib/components/ListPropCardButton.svelte";
    import ContainerDialog from "$lib/components/ContainerDialog.svelte";
    import PlusButton from "$lib/components/PlusButton.svelte";
    import { faComment, faSun, faUser, faUserAltSlash } from "@fortawesome/free-solid-svg-icons";
    import type { Container } from "$lib/models/container";
    import { onMount } from "svelte";
    import { Household, Member } from "$lib/models/household";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import MemberDialog from "$lib/components/MemberDialog.svelte";

    $: showIconDialog = false;
    $: showHousholdNameDialog = false;
    $: showContainerDialog = false;
    $: showAvatarDialog = false;
    $: showMemberDialog = false;
    const setIconDialog = (value: boolean) => showIconDialog = value;
    const setHousholdNameDialog = (value: boolean) => showHousholdNameDialog = value;
    const setContainerDialog = (value: boolean) => showContainerDialog = value;
    const setAvatarDialog = (value: boolean) => showAvatarDialog = value;
    const setMemberDialog = (value: boolean) => showMemberDialog = value;

    let householdName = '';
    let householdIconPath = '';
    let householdIconIdx = 0;
    let householdContainers: Container[] = [];
    let newHouseholdData: Household = new Household();
    let householdCreator: Member;

    
    const getHouseholdIcon = (iconPath: string) => {
        setIconDialog(false);
        const regex = /household-icon-(\d{2})\.png$/;
        const match = iconPath.match(regex);
        if (match && match[1]) {
            householdIconPath = iconPath;
            householdIconIdx = parseInt(match[1], 10);
        }
    };

    const handleHouseholdNameKeyUp = (e: CustomEvent) => {
        if (e.detail.key === 'Enter') {
            setHousholdNameDialog(false);
        }
    };

    onMount(() => {
        householdName = $_('household_newHouseholdDefaultName');
        householdIconIdx = Math.floor(Math.random() * 9) + 1;
        householdIconPath = `/icons/household/household-icon-${String(householdIconIdx).padStart(2, '0')}.png`;
        newHouseholdData = new Household();
    });

    $: if (householdName !== '') {
        newHouseholdData.name = householdName;
    }

    $: if (householdIconIdx !== 0) {
        newHouseholdData.iconIdx = householdIconIdx;
    }

    $: if (householdContainers.length > 0) {
        newHouseholdData.containers = householdContainers;
    }

    const processContainerDialogData = (e: CustomEvent) => {
        console.log(e.detail.container);
    };

</script>


<div class="flex flex-col w-full gap-3 {$lc.text}">

    <IconSelectionDialog
        showDialog={showIconDialog}
        mode="household"
        title="common_selectAnIcon"
        on:click:selectIcon={(e) => {
            getHouseholdIcon(e.detail.iconPath);
        }}
        on:click:barrierDismiss={(e) => {
            setIconDialog(false);
        }}
    />

    
    <IconSelectionDialog
        showDialog={showAvatarDialog}
        mode="avatar"
        title="common_selectAvatar"
        on:click:selectIcon={(e) => {
            getHouseholdIcon(e.detail.iconPath);
        }}
        on:click:barrierDismiss={(e) => {
            setAvatarDialog(false);
        }}
    />

    <TextInputDialog
        title="groceryList_listNameDialogTitle"
        showDialog={showHousholdNameDialog}
        bind:value={householdName}
        placeholder="groceryList_placeholderListName"
        showRefreshButton={true}
        on:click:barrierDismiss={(e) => {
            setHousholdNameDialog(false);
        }}
        on:keyup={handleHouseholdNameKeyUp}
        />

        
    <ContainerDialog
        showDialog={showContainerDialog}
        on:click:barrierDismiss={(e) => {
            setContainerDialog(false);
        }}
        on:click:selectOption={(e) => {
            console.log(e.detail.selected);
        }}
        title='common_addContainerCallToAction'
        on:click:addItem={processContainerDialogData}
        />

    <MemberDialog
        showDialog={showMemberDialog}
        title="household_selectYourMemberAvatar"
        on:click:barrierDismiss={(e) => {
            setMemberDialog(false);
        }}
        />


    <div class="{$lc.title} text-2xl text-orange-500 flex items-center">
        <span class="whitespace-nowrap overflow-hidden text-ellipsis">
            {$_('household_createNewHousehold')}
        </span>
    </div>
    <div class="grid gap-3 w-full grid-cols-2">
        <ListPropCardButton
            onClick={() => setHousholdNameDialog(true)}
            icon={faComment}
            headerText={$_('household_householdName')}
            >
            <span class="text-neutral-700 font-normal">{householdName}</span>
        </ListPropCardButton>

        <ListPropCardButton
            onClick={() => setIconDialog(true)}
            icon={faSun}
            headerText={$_('groceryList_labelListIcon')}
            >
            <img src={householdIconPath} alt="icon" class="w-20" />
        </ListPropCardButton>

    </div>
    <div class="grid gap-3 w-full grid-cols-1">
        <ListPropCardButton
            onClick={() => setMemberDialog(true)}
            icon={faUser}
            headerText={$_('household_createrAvatar')}
            >
            {#if !householdCreator}
                <div class="text-neutral-300 text-base font-normal flex items-center gap-2">
                    <div class="text-neutral-200">
                        <FontAwesomeIcon icon={faUserAltSlash} class="text-[3rem]" />
                    </div>
                </div>
            {:else if householdCreator !== null}
                <div class="flex items-center gap-2">
                    <div class="rounded-full"
                        style={`background-color: ${householdCreator.pfp.bgColor}`}>
                        <img src={`/icons/avatar/${householdCreator.pfp.presenting}/avatar-${householdCreator.pfp.presenting}-${householdCreator.pfp.idx.toString().padStart(2, '0')}.png`} alt="assignee" class="w-16 h-16 rounded-full" />
                    </div>
                    <span>{householdCreator.name}</span>
                </div>
            {/if}
        </ListPropCardButton>

    </div>
    <div class="flex-col w-full mt-5">
        <div class="w-full flex items-center justify-start">
            <PlusButton
                onClick={() => {
                    setContainerDialog(true);
                }}
                />
            <div class="text-orange-500 text-base font-normal ml-2 {$lc.text}">
                {$_('household_addHouseholdContainers')}
            </div>
        </div>
    </div>

    <!-- <div class="
        flex flex-col
        w-full h-full gap-5
        pb-32 lg:pb-3
        mt-2
    ">
    {#if Object.keys(groupedListItems).length > 0 }
        {#each Object.values(ItemCategory) as category}
            {#if groupedListItems[category]}
                <div class="w-full bg-orange-50 px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl shadow-grocerite-orange-200-sm">
                    <div class="flex items-center w-full gap-2 border-b-2 border-b-orange-100 pb-2">
                        <h3 class="text-xl lg:text-2xl text-orange-500 {$lc.title}">{$_(`common_category_${category}`)}</h3>
                        <img src={getItemCategoryIcon(category)} alt="{category}" class="ml-auto w-8 lg:w-10" />
                    </div>
                    <div class="flex flex-col gap-2 mb-2">
                        {#each groupedListItems[category] as item}
                            <div class="flex items-center text-neutral-700">
                                <div class="text-xl {$lc.text} font-mono text-center w-16 font-bold shrink-0">{item.quantity}</div>
                                <div class="{$lc.text} text-base lg:text-lg overflow-hidden text-ellipsis text-nowrap pr-2 flex items-center">
                                    <span class="">{item.name}</span>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
        {/each}
    {/if}
    </div> -->
</div>
