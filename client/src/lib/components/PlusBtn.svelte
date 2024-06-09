<script lang="ts">

    export let choice;

    const btnClick = () => {
        const dialog = document.getElementById("dlg")
        dialog?.showModal()
    }

    const moveBtn = () => {
        const player_input = document.getElementById("player_num")
        const payoff_input = document.getElementById("payoff")
        payoff_input!.style.display = "none"
        player_input!.style.display = "block"
    }
    
    const payoffBtn = () => {
        const payoff_input = document.getElementById("payoff")
        const player_input = document.getElementById("player_num")
        player_input!.style.display = "none"
        payoff_input!.style.display = "block"
    }

    const enter = (val: string) => {
        const plus_btn = document.getElementsByClassName("plus-btn")[0]
        const plus_icos = document.getElementsByClassName("plus") as HTMLCollectionOf<HTMLElement>
        Array.from(plus_icos).forEach(plus_ico => {
            plus_ico.style.display = "none"
        });
        
        const new_val = document.createElement("div")
        new_val.className = "plus"
        new_val.innerHTML = val

        plus_btn.appendChild(new_val)
        
        const dialog = document.getElementById("dlg")
        dialog?.close()
    }

    const playerEnter = () => {
        choice = 0;
        const playerNum = (document.getElementById("player_input") as HTMLInputElement).value
        enter(playerNum)
    }
        
    const payoffEnter = () => {
        choice = 1;
        const payoffval = (document.getElementById("payoff_input") as HTMLInputElement).value
        enter(payoffval)
    }
</script>

<div class="main">
    <button class="plus-btn" on:click={btnClick}>
        <i class="fa fa-plus plus"></i>
    </button>
</div>

<dialog id="dlg">
    <button class="optionBtn" on:click={moveBtn}>Move</button>
    <button class="optionBtn" on:click={payoffBtn}>Payoff</button>

    <div id="player_num">
        <div>Player: </div>
        <input type="number" name="player_num" id="player_input" />
        <button class="optionBtn" on:click={playerEnter}>Enter</button>
    </div>

    <div id="payoff">
        <div>Payoff: </div>
        <input type="text" name="payoff" id="payoff_input" />
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

    #player_num {
        display: none
    }

    #payoff {
        display: none
    }
</style>