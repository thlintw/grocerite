<script lang="ts">
    
    import { _, locale } from "svelte-i18n";
    import { lc } from "$lib/stores/general";
    import IconSelectionDialog from "$lib/components/IconSelectionDialog.svelte";
    import TextInputDialog from "$lib/components/TextInputDialog.svelte";
    import ListPropCardButton from "$lib/components/ListPropCardButton.svelte";
    import ContainerDialog from "$lib/components/ContainerDialog.svelte";
    import PlusButton from "$lib/components/PlusButton.svelte";
    import { faComment, faPen, faSun, faUser, faUserAltSlash } from "@fortawesome/free-solid-svg-icons";
    import type { Container } from "$lib/models/container";
    import { onMount } from "svelte";
    import { Household, Member } from "$lib/models/household";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import MemberDialog from "$lib/components/MemberDialog.svelte";
    import { set } from "date-fns";
    import Button from "$lib/components/Button.svelte";
    import { dialog } from "$lib/stores/dialogStore";
    import type { RES } from "$lib/services/api";
    import { apiCreateHousehold } from "$lib/api/household";
    import { goto } from "$app/navigation";
    import { toast } from "@zerodevx/svelte-toast";

    $: showIconDialog = false;
    $: showHousholdNameDialog = false;
    $: showContainerDialog = false;
    $: showMemberDialog = false;
    const setIconDialog = (value: boolean) => showIconDialog = value;
    const setHousholdNameDialog = (value: boolean) => showHousholdNameDialog = value;
    const setContainerDialog = (value: boolean) => {
        showContainerDialog = value;
        containerError = '';
    };
    const setMemberDialog = (value: boolean) => showMemberDialog = value;

    let householdName = '';
    let householdIconPath = '';
    let householdIconIdx = 0;
    let householdContainers: Container[] = [];
    let newHouseholdData: Household = new Household();
    let householdCreator: Member;
    let householdButtonLoading = false;
    
    let nameError = '';
    let iconError = '';
    let creatorError = '';
    let containerError = '';

    let currentEditContainer: Container | null;

    const editContainer = (container: Container) => {
        currentEditContainer = container;
        console.log(currentEditContainer);
        setContainerDialog(true);
    };
    
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
        setContainerDialog(false);
        if (currentEditContainer) {
            householdContainers = householdContainers.map((container) => {
                if (container.name === currentEditContainer!.name) {
                    return e.detail.container;
                }
                return container;
            });
        } else {
            householdContainers = [...householdContainers, e.detail.container];
        }
    };


    const checkName = () => {
        if (householdName === '') {
            nameError = 'Household name is required';
        } else {
            nameError = '';
        }
    };

    const checkIcon = () => {
        if (householdIconIdx === 0) {
            iconError = 'Household icon is required';
        } else {
            iconError = '';
        }
    };

    const checkCreator = () => {
        if (!householdCreator) {
            creatorError = 'Creator member is required';
        } else {
            creatorError = '';
        }
    };

    const checkContainers = () => {
        if (!householdContainers.length) {
            containerError = 'At least one container is required to create a household';
        } else {
            containerError = '';
        }
    };

    const makePostData = () => {
        return {
            name: householdName,
            iconIdx: householdIconIdx,
            containers: householdContainers.map((container) => {
                return {
                    type: container.type,
                    name: container.name,
                };
            }),
            creator: {
                name: householdCreator.name,
                pfpIdx: householdCreator.pfp.idx,
                pfpBgColor: householdCreator.pfp.bgColor,
                pfpPresenting: householdCreator.pfp.presenting,
            }
        };
    };

    const createHousehold = async () => {
        householdButtonLoading = true;
        checkName();
        checkIcon();
        checkCreator();
        checkContainers();
        if (!nameError && !iconError && !creatorError && !containerError) {
            console.log('Creating household');
            console.log(makePostData());
            const data = makePostData();
            try {
                const res: RES = await apiCreateHousehold(data);
                if (res.status === 'S') {
                    goto(`/app/household/${res.data[0].householdId}`);
                }
            } catch (e) {
                toast.push('Failed to create household');
                console.error(e);
            }
        }
        householdButtonLoading = false;
        // if (!)
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
        currentEditItem={currentEditContainer}
        currentContainerNames={householdContainers.map((container) => container.name)}
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
        current={householdCreator}
        on:click:barrierDismiss={(e) => {
            setMemberDialog(false);
        }}
        on:click:addItem={(e) => {
            console.log(e.detail);
            householdCreator = e.detail.member;
            creatorError = '';
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
            error={nameError}
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
            error={creatorError}
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
                    currentEditContainer = null;
                    setContainerDialog(true);
                }}
                />
            <div class="text-orange-500 text-base font-normal ml-2 {$lc.text}">
                {$_('household_addHouseholdContainers')}
            </div>
        </div>
    </div>

    <div class="
        flex flex-col
        w-full h-full gap-5
        pb-32 lg:pb-3
        mt-2
    ">
    {#if householdContainers.length > 0 }
        {#each householdContainers as container}
            <div class="w-full bg-orange-50 px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl shadow-grocerite-orange-200-sm">
                <div class="flex items-center text-neutral-700">
                    <img src={`/icons/container/container-icon-${container.type}.png`} alt="{`${container.type}'s icon`}" class="w-10 lg:w-14" />
                    <div class="flex flex-col gap-0.5 pl-2">
                        <div class="text-sm text-neutral-500 lg:text-sm overflow-hidden text-ellipsis text-nowrap pr-2 flex items-center">
                            <span class="">{$_(`common_containerType_${container.type}`)}</span>
                        </div>
                        <div class="font-bold text-orange-500 text-base lg:text-lg overflow-hidden text-ellipsis text-nowrap pr-2 flex items-center ml-1">
                            <span class="">{container.name}</span>
                        </div>
                    </div>
                    <button class="ml-auto"
                        on:click={() => editContainer(container)}>
                        <FontAwesomeIcon icon={faPen} class="text-orange-500 text-sm" />
                    </button>
                </div>
            </div>
        {/each}
    {/if}
    {#if containerError !== ''}
        <div class="w-full px-3 lg:px-5 py-3 flex flex-col gap-3 rounded-xl text-sm text-red-400 border-2 border-red-400">
            {containerError}
        </div>
    {/if}
    </div>


    <div class="flex justify-center mt-3">
        <Button
            text={$_('household_createNewHousehold')}
            disabled={householdButtonLoading}
            loading={householdButtonLoading}
            on:click={() => createHousehold()}
            />
    </div>

</div>
