<script lang="ts">
    import { goto } from '$app/navigation';
    import Button from '$lib/components/Button.svelte';
    import { AuthService } from '$lib/services/auth';

    const signOut = async () => {
        await AuthService.getInstance().signOutUser();
        goto('/app/login');
    };
</script>



<div>

    <Button
        text="Sign Out"
        color="orange"
        size="md"
        on:click={signOut}
        />
</div>