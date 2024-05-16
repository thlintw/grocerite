<script lang="ts">
    export let size: 'sm' | 'md' | 'lg' = 'md';

    const sizes = {
        sm: 'w-3',
        md: 'w-4',
        lg: 'w-6'
    }
</script>

<span class="flex gap-2">
    <img src="/image/leaf.png" alt="jump-leaf" class="{sizes[size]} h-auto animate-b0"/>
    <img src="/image/leaf.png" alt="jump-leaf" class="{sizes[size]} h-auto animate-b1"/>
    <img src="/image/leaf.png" alt="jump-leaf" class="{sizes[size]} h-auto animate-b2"/>
</span>