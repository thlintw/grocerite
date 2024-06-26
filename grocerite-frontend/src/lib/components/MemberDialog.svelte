<script lang="ts">
    import { Container, ContainerItem, ContainerType } from '$lib/models/container';
    import { lc } from '$lib/stores/general';
    import { scaleFade } from '$lib/transitions';
    import type { IconDefinition, icon } from '@fortawesome/fontawesome-svg-core';
    import { faTimes, faUserAltSlash, faXmark } from '@fortawesome/free-solid-svg-icons';
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import SearchableFormInput from './SearchableFormInput.svelte';
    import { createEventDispatcher, onMount } from 'svelte';
    import { _ } from 'svelte-i18n';
    import { fade } from 'svelte/transition';
    import type { SelectCandidate } from '$lib/types/general';
    import IconSelectionDialog from './IconSelectionDialog.svelte';
    import ScrollableSelectDialog from './ScrollableSelectDialog.svelte';
    import { ItemCategory } from '$lib/models/item';
    import Button from './Button.svelte';
    import QuantitySelectionDialog from './QuantitySelectionDialog.svelte';
    import type { GroceryListItem } from '$lib/models/groceryList';
    import FormInput from './FormInput.svelte';
    import PaletteDialog from './PaletteDialog.svelte';
    import { Member } from '$lib/models/household';

    const dispatch = createEventDispatcher();

    export let showDialog = false;
    export let title: string = '';
    export let availableContainers: Container[] = [];
    export let current: Member | null = null;

    let memberName = '';
    let pfpIdx: number;
    let pfpPresenting: 'mp' | 'fp' | 'nb';
    let pfpBgColor = '';
    let containerType: ContainerType = ContainerType.Refrigerator;
    let itemQuantity = 1;
    let itemContainer: Container | null = null;

    let showPaletteDialog = false;
    const setPaletteDialog = (value) => {
        showPaletteDialog = value;
    };

    let showAvatarDialog = false;
    const setAvatarDialog = (value: boolean) => {
        showAvatarDialog = value
    };

    let showContainerDialog = false;
    const setContainerDialog = (value) => {
        showContainerDialog = value;
    };

    const onAddItem = () => {
        // const item: GroceryListItem = {
        //     idx: -1,
        //     name: containerName,
        //     category: itemCategory,
        //     quantity: itemQuantity,
        //     targetContainerIdx: itemContainer!.idx,
        //     ticked: false,
        //     storeIdx: -1,
        // };
        const member = new Member({
            pfp: {
                idx: pfpIdx,
                presenting: pfpPresenting,
                bgColor: pfpBgColor,
            },
            name: memberName,
        });
        dispatch('click:addItem', { member });
    };

    const onBarrierDismiss = () => {
        dispatch('click:barrierDismiss');
    };

    const getContainerTypeOptions = () => {
        return Object.values(ContainerType).map((category) => {
            return {
                value: category,
                label: $_(`common_containerType_${category}`),
                iconPath: `/icons/container/container-icon-${category}.png`,
            };
        });
    };


    const itemQuantityControl = (mode: '--' | '-' | '+' | '++') => {
        switch (mode) {
            case '--':
                if (itemQuantity > 10) {
                    itemQuantity -= 10;
                } else {
                    itemQuantity = 1;
                }
                break;
            case '-':
                if (itemQuantity > 1) {
                    itemQuantity--;
                }
                break;
            case '+':
                itemQuantity++;
                break;
            case '++':
                itemQuantity += 10;
                break;
        }
    };

    const getContainerOptions = () => {
        return availableContainers.map((container) => {
            return {
                value: container.idx.toString(),
                label: container.name,
                iconPath: `/icons/container/container-icon-${container.type}.png`,
            };
        });
    };

    let buttonLoading = false;

    const reset = () => {
        memberName = '';
        containerType = ContainerType.Refrigerator;
        itemQuantity = 1;
        itemContainer = null;
        pfpBgColor = '';
        pfpIdx = 0;
        pfpPresenting = 'fp';
    };

    const setCurrent = () => {
        if (current) {
            memberName = current.name;
            pfpBgColor = current.pfp.bgColor;
            pfpIdx = current.pfp.idx;
            pfpPresenting = current.pfp.presenting;
        }
    };

    $: {
        if (!showDialog) {
            reset();
            setCurrent();
        }
    }

    const onSelectColor = (event) => {
        showPaletteDialog = false;
        pfpBgColor = event.detail.color;
    };

    const onSelectIcon = (event) => {
        const rpatt = /avatar-(\w{2})-(\d{2})\.png/;
        const match = event.detail.iconPath.match(rpatt);
        if (match && match[1] && match[2]) {
            pfpPresenting = match[1] as 'mp' | 'fp' | 'nb';
            pfpIdx = parseInt(match[2], 10);
        }
        setAvatarDialog(false);
    };
    
    
</script>

{#if showDialog}

    <PaletteDialog
        showDialog={showPaletteDialog}
        on:click:barrierDismiss={() => setPaletteDialog(false)}
        title={$_('household_selectPfpColor')}
        on:click:selectColor={onSelectColor}
        />

        
    <IconSelectionDialog
        showDialog={showAvatarDialog}
        mode="avatar"
        title="common_selectAvatar"
        on:click:selectIcon={(e) => {
            onSelectIcon(e);
        }}
        on:click:barrierDismiss={(e) => {
            setAvatarDialog(false);
        }}
    />



    <button transition:fade on:click={onBarrierDismiss} 
        class="fixed inset-0 left-0 top-0 w-full h-full z-[10008] bg-neutral-700/20"></button>
    <div transition:scaleFade
        class="fixed top-0 right-0 bottom-0 left-0 z-[10009] pointer-events-none 
            flex items-center justify-center">
        <div class="pointer-events-auto z-[10010] flex flex-col lg:w-[40rem] 2xl:w-[55rem] w-11/12
            ">
            <div class="ml-1 text-2xl text-orange-500 flex-grow {$lc.title} 
                relative drop-shadow-grocerite-orange-100-lg top-4 left-1">
                <div class="drop-shadow-title">{ $_(title) }</div>
            </div>
            <div class="bg-orange-50 rounded-2xl flex gap-3 py-7 px-5
                shadow-grocerite-orange-200-sm {$lc.text} flex-col items-center">

                <div class="relative flex w-full">

                    <FormInput 
                        label={$_('groceryList_addListItemsName')}
                        placeholder={$_('household_enterYourMemberName')}
                        bind:value={memberName}
                        on:select={(e) => {
                            memberName = e.detail[0].label;
                        }}
                    />
                </div>
                <div class="w-full grid grid-cols-1 lg:grid-cols-2 gap-3">
                
                    <div class="flex w-full flex-col">
                        <div class="text-lg text-emerald-700 font-bold">
                            {$_('household_avatarBackground')}
                        </div>
                        <div class="px-3">
                            <button type="button" 
                                class="flex items-center gap-2 rounded-xl px-3 py-2 bg-orange-100"
                                on:click={() => setPaletteDialog(true)}>
                                {#if !pfpBgColor}
                                    <div class="w-16 h-14 rounded-full bg-neutral-300 items-center flex justify-center">
                                        <FontAwesomeIcon icon={faTimes} class="text-neutral-100 text-4xl" />
                                    </div>
                                {:else}
                                    <div class="w-16 h-14 rounded-full" 
                                        style="background-color: {pfpBgColor}">
                                    </div>
                                {/if}
                            </button>
                        </div>
                    </div>
                
                    <div class="flex w-full flex-col">
                        <div class="text-lg text-emerald-700 font-bold">
                            {$_('household_avatarIcon')}
                        </div>
                        <div class="px-3">
                            <button type="button" 
                                class="flex items-center gap-2 rounded-xl px-3 py-2 bg-orange-100"
                                on:click={() => {setAvatarDialog(true)}}>
                                {#if !pfpIdx}
                                    <div class="w-16 h-16 rounded-full items-center flex justify-center">
                                        <FontAwesomeIcon icon={faUserAltSlash} class="text-neutral-300 text-4xl" />
                                    </div>
                                {:else}
                                    <div>
                                        <img src={`/icons/avatar/${pfpPresenting}/avatar-${pfpPresenting}-${String(pfpIdx).padStart(2,'0')}.png`} 
                                            alt="category icon" class="w-16" />
                                    </div>
                                {/if}
                            </button>
                        </div>
                    </div>



                </div>
                
                <div>
                    <Button 
                        loading={buttonLoading}
                        text={$_('household_confirmAvatar')}
                        on:click={onAddItem}
                    />
                </div>
                
            </div>
        </div>
    </div>
{/if}