<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";

    let groceryListId = '';

    onMount(async () => {
        const { params } = $page;
        groceryListId = params.grocery_list_id;

        if (groceryListId) {
            
        }
    });
</script>

<div>
    <h1>Grocery List Edit</h1>
    <p>Grocery List ID: {groceryListId}</p>
</div>