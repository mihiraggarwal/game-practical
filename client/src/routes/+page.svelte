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
    
    const add_action = () => {
        const actions_div = document.getElementsByClassName("all_initial_actions")[0]

        const action_elem = document.createElement("input")
        action_elem.setAttribute("type", "text")
        action_elem.setAttribute("class", "initial_action")
        action_elem.className = "initial_actions"

        actions_div?.appendChild(action_elem)
    }

    const add_move = () => {
        const first_action_btn = document.getElementById("initial_action_btn")
        first_action_btn?.setAttribute("disabled", "true")

        iActions = Array.from(document.getElementsByClassName("initial_actions") , x => (x as HTMLInputElement).value);
        console.log(iActions)
    }

</script>

<h1>game-practical</h1>
<label for="players">Number of players</label>
<input type="number" id="players" name="players" bind:value={nPlayers} required />
<br /><br />

<div class="tree">
    <div class="initial">
        Initial node
        <input type="number" name="initial_player" id="initial_player" bind:value={initial_player} required placeholder="Player" />
        <button type="button" id="initial_action_btn" on:click={add_action}>Add action</button>
        <div class="all_initial_actions"></div>
    </div>
    <div class="further">
        <button type="button" id="node_btn" on:click={add_move}>Add move</button>
    </div>
</div>

<style>
    .initial {
        display: flex;
        flex-direction: row;
        gap: 10px
    }
    
    .all_initial_actions {
        display: flex;
        flex-direction: row;
        gap: 10px
    }
</style>