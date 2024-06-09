<script lang="ts">
    import ActionBtn from "./ActionBtn.svelte";
    import PlusBtn from "./PlusBtn.svelte";

    let choice = 1;
</script>

<div class="initial">
    <PlusBtn bind:choice={choice} />
    {#if (choice == 0)}
        <div class="action_div">
            <ActionBtn />
        </div>
    {/if}
    <!-- <div class="action_div"></div> -->
</div>

<style>
    .initial {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
    }
    
    /* .action_div {
        display: flex;
        flex-direction: row;
        gap: 10px
    } */
</style>