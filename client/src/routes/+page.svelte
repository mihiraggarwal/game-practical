<script lang="ts">
    /*
    SOP for tree
    - ask for number of players
    - get initial node and get the player on it
    - get actions on initial node
    and so on
    - in the end, get payoffs
    */

    let nPlayers: number;
    let initial_player: number;

    let iActions: Array<string>;
    $: iActions

    let node_counter = 0
    
    const add_action = () => {
        if (node_counter == 0) node_counter++
        const actions_div = document.getElementsByClassName("action_div")[node_counter-1]

        const action_elem = document.createElement("input")
        action_elem.setAttribute("type", "text")
        action_elem.className = "actions"
        
        actions_div?.appendChild(action_elem)
    }
    
    const add_move = () => {
        node_counter++
        const old_action_btn = Array.from(document.getElementsByClassName("action_btn")).at(-1)
        old_action_btn?.setAttribute("disabled", "true")
        
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

        ind_div.appendChild(action_div)
    }

</script>

<h1>game-practical</h1>
<label for="players">Number of players</label>
<input type="number" id="players" name="players" bind:value={nPlayers} required />
<br /><br />

<div class="tree">
    <div class="initial">
        Initial node
        <input type="number" name="player_input" id="initial_player" bind:value={initial_player} required placeholder="Player" />
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