<script lang="ts">
    /*
    SOP for tree
    - ask for number of players
    - get initial node and get the player on it
    - get actions on initial node
    and so on
    - in the end, get payoffs
    */

    import PlusBtn from "../lib/components/PlusBtn.svelte";

    let nPlayers: number;
    let initial_player: number;

    let iActions: Array<string>;
    $: iActions

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
    
    const add_move = () => {
        node_counter++
        const old_action_btn = Array.from(document.getElementsByClassName("action_btn")).at(-1)
        old_action_btn?.setAttribute("disabled", "true")
        
        const old_inputs = Array.from(document.getElementsByClassName("player_input")).at(-1)
        old_inputs?.setAttribute("disabled", "true")
        
        const actions_input = Array.from(document.getElementsByClassName("actions"))
        actions_input.slice(actions_input.length - ind_action_counter)
        
        actions_input.forEach(x => {
            x.setAttribute("disabled", "true")
        });

        // const iLen = iActions.length
        // iActions.push(...Array.from(document.getElementsByClassName("actions") , x => (x as HTMLInputElement).value).slice(iLen))
        
        const further_div = document.getElementsByClassName("further")[0]

        const ind_div = document.createElement("div")
        ind_div.className = "ind_div"
        ind_div.style.display = "flex"
        ind_div.style.flexDirection = "row"

        further_div.appendChild(ind_div)

        const player_elem = document.createElement("input")
        player_elem.setAttribute("type", "number")
        player_elem.setAttribute("placeholder", "Player")
        player_elem.className = "player_input"

        ind_div.appendChild(player_elem)

        const action_btn = document.createElement("button")
        action_btn.textContent = "Add action"
        action_btn.className = "action_btn"
        action_btn.onclick = add_action

        ind_div.appendChild(action_btn)

        const action_div = document.createElement("div")
        action_div.className = "action_div"

        for (let i = 0; i < next_branch_counter; i++) {
            const action_elem = document.createElement("input")
            action_elem.setAttribute("type", "text")
            action_elem.className = "actions"
            
            action_div?.appendChild(action_elem)
        }

        ind_div.appendChild(action_div)
    }

</script>

<h1>game-practical</h1>
<div class="pre-tree">
    <label for="players">Number of players</label>
    <input type="number" id="players" name="players" bind:value={nPlayers} required />
</div>
<br /><br />

<div class="tree">
    <div class="initial">
        <PlusBtn />
        <!-- <input type="number" name="player_input" class="player_input" bind:value={initial_player} required placeholder="Player" /> -->
        <button type="button" class="action_btn" on:click={add_action}>Add action</button>
        <div class="action_div"></div>
    </div>

    <div class="further">
        {#if node_counter < 1}
            <button type="button" id="node_btn" on:click={add_move} disabled>Add move</button>
        {:else}
            <button type="button" id="node_btn" on:click={add_move}>Add move</button>
        {/if}
    </div>
</div>

<style>
    .pre-tree {
        display: flex;
        justify-content: center;
        gap: 1vw
    }

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

    .tree {
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    h1 {
        font-family: "Inter";
        text-align: center;
    }
</style>