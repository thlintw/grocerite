<script lang="ts">
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  	import { faPlus } from '@fortawesome/free-solid-svg-icons';

    export let cls = '';
    export let onClick: () => void = () => {};
</script>


<button type="button" class="
    rounded-full bg-orange-200 text-orange-400 text-3xl w-10 h-10 flex items-center justify-center
    hover:bg-orange-300 hover:text-orange-500 active:bg-orange-200 active:text-orange-400
    {cls}
"
    on:click={onClick}>
    <FontAwesomeIcon icon={faPlus} />
</button>