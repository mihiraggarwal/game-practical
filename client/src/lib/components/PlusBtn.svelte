<script lang="ts">

    export let choice;

    export let playerNum;
    export let payoffval;

    export let node_num
    
    let dialog: HTMLDialogElement;

    const btnClick = () => {
        dialog = document.getElementById(`dlg-${node_num}`) as HTMLDialogElement;
        dialog!.showModal()
    }

    const moveBtn = () => {
        const player_input = document.getElementById(`player_num_${node_num}`) as HTMLInputElement
        const payoff_input = document.getElementById(`payoff_${node_num}`) as HTMLInputElement
        payoff_input!.style.display = "none"
        player_input!.style.display = "block"
    }
        
    const payoffBtn = () => {
        const payoff_input = document.getElementById(`payoff_${node_num}`) as HTMLInputElement
        const player_input = document.getElementById(`player_num_${node_num}`) as HTMLInputElement
        player_input!.style.display = "none"
        payoff_input!.style.display = "block"
    }

    const enter = (val: string) => {
        const plus_btn = document.getElementById(`plus-btn-node-${node_num}`)
        const plus_icos = document.getElementsByClassName(`plus ${node_num}`) as HTMLCollectionOf<HTMLElement>
        Array.from(plus_icos).forEach(plus_ico => {
            plus_ico.style.display = "none"
        });

        const new_val = document.createElement("div")
        new_val.className = `plus ${node_num}`
        new_val.innerHTML = val

        plus_btn!.appendChild(new_val)
        
        dialog!.close()
    }

    const playerEnter = () => {
        choice = 0;
        const btn = document.getElementById(`plus-btn-node-${node_num}`)
        btn!.style.borderRadius = "50%"
        playerNum = (document.getElementById(`player_input_${node_num}`) as HTMLInputElement).value
        enter(playerNum)
    }
        
    const payoffEnter = () => {
        choice = 1;
        const btn = document.getElementById(`plus-btn-node-${node_num}`)
        btn!.style.borderRadius = "0"
        payoffval = (document.getElementById(`payoff_input_${node_num}`) as HTMLInputElement).value
        enter(payoffval)
    }
</script>

<div class="main">
    <button class="plus-btn" id="plus-btn-node-{node_num}" on:click={btnClick}>
        <i class="fa fa-plus plus {node_num}" id="plus-node-{node_num}"></i>
    </button>
</div>

<dialog class="dlg" id="dlg-{node_num}">
    <button class="optionBtn" on:click={moveBtn}>Move</button>
    <button class="optionBtn" on:click={payoffBtn}>Payoff</button>

    <div class="player_num" id="player_num_{node_num}">
        <div>Player: </div>
        <input type="number" name="player_num" class="player_input" id="player_input_{node_num}" />
        <button class="optionBtn" on:click={playerEnter}>Enter</button>
    </div>

    <div class="payoff" id="payoff_{node_num}">
        <div>Payoff: </div>
        <input type="text" name="payoff" class="payoff_input" id="payoff_input_{node_num}" />
        <button class="optionBtn" on:click={payoffEnter}>Enter</button>
    </div>
</dialog>

<style>
    .plus-btn {
        border: 5px solid #000;
        border-radius: 50%;
        width: 3vw;
        height: 3vw;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fff;
    }

    .plus-btn:hover {
        cursor: pointer;
    }

    .plus {
        font-size: 2em;
    }

    .player_num {
        display: none
    }

    .payoff {
        display: none
    }
</style>