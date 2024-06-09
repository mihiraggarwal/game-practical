<script lang="ts">
    import PlusBtn from "./PlusBtn.svelte";

    let node_counter = 0
    let next_branch_counter = 0

    let ind_action_counter = 0
    
    const add_action = () => {
        if (node_counter == 0) node_counter++
        const actions_div = document.getElementsByClassName("action_div")[node_counter-1]

        const action_elem = document.createElement("input")
        action_elem.setAttribute("type", "text")
        action_elem.className = "actions"
        
        actions_div?.appendChild(action_elem)
        next_branch_counter++
        ind_action_counter++
    }    
</script>

<div class="initial">
    <PlusBtn />
    <button type="button" class="action_btn" on:click={add_action}>Add action</button>
    <div class="action_div"></div>
</div>

<style>
    .initial {
        display: flex;
        flex-direction: row;
        gap: 10px
    }
    
    .action_div {
        display: flex;
        flex-direction: row;
        gap: 10px
    }
</style>