<script lang="ts">

    import { any_imperfect, current_imperfection } from "$lib/stores";

    export let choice;

    export let playerNum;
    export let payoffval;

    export let node_num
    export let initial = false;

    export let node;

    export let colour: boolean = false;
    export let imperfect: boolean = false;

    let dialog: HTMLDialogElement;

    let selected: number;

    $: for (let n in $current_imperfection) {
        if ($current_imperfection[n].node_number == node.node_number) {
            imperfect = true
            break
        }
        else {
            imperfect = false
        }
    }

    const onClick = (event: any) => {
        if (event.target === dialog) {
            dialog.close()
        }
    }

    const btnClick = () => {
        dialog = document.getElementById(`dlg-${node_num}`) as HTMLDialogElement;
        dialog.addEventListener("click", onClick)
        dialog!.showModal()
    }

    const moveBtn = () => {
        selected = 0;
        const player_input = document.getElementById(`player_num_${node_num}`) as HTMLInputElement
        const payoff_input = document.getElementById(`payoff_${node_num}`) as HTMLInputElement
        payoff_input!.style.display = "none"
        player_input!.style.display = "flex"

        const input_box = document.getElementById(`player_input_${node_num}`)
        input_box!.focus()
    }
        
    const payoffBtn = () => {
        selected = 1;
        const payoff_input = document.getElementById(`payoff_${node_num}`) as HTMLInputElement
        const player_input = document.getElementById(`player_num_${node_num}`) as HTMLInputElement
        player_input!.style.display = "none"
        payoff_input!.style.display = "flex"

        const input_box = document.getElementById(`payoff_input_${node_num}`)
        input_box!.focus()
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
        new_val.style.fontSize = "1.25em"

        plus_btn!.appendChild(new_val)
        
        dialog!.close()
    }

    const playerEnter = (event: SubmitEvent & { currentTarget: EventTarget & HTMLFormElement; }) => {
        event.preventDefault()
        choice = 0;
        const btn = document.getElementById(`plus-btn-node-${node_num}`)
        btn!.style.borderRadius = "50%"
        btn!.style.borderWidth = "3px"
        btn!.style.padding = "0"
        playerNum = (document.getElementById(`player_input_${node_num}`) as HTMLInputElement).value
        enter(playerNum)
    }
        
    const payoffEnter = (event: SubmitEvent & { currentTarget: EventTarget & HTMLFormElement; }) => {
        event.preventDefault()
        choice = 1;
        const btn = document.getElementById(`plus-btn-node-${node_num}`)
        btn!.style.borderRadius = "5px"
        btn!.style.borderWidth = "3px"
        btn!.style.padding = "0 2vw"
        payoffval = (document.getElementById(`payoff_input_${node_num}`) as HTMLInputElement).value
        enter(`(${payoffval})`)
    }

    const getImperfections = (event: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement; }) => {
        event.preventDefault()
        imperfect = !imperfect

        if (imperfect) {
            current_imperfection.update(x => [...x, node])
            any_imperfect.update(i => true)
        }
        else {
            current_imperfection.update(x => x.filter(x => x != node))
            if ($current_imperfection.length == 0) any_imperfect.update(i => false)
        }     
    }
</script>

<div class="main">
    <button class="plus-btn" class:colour={initial || colour} class:imperfect={imperfect} id="plus-btn-node-{node_num}" on:click={btnClick} on:contextmenu={(event) => getImperfections(event)} data-testid="plus-node-{node_num}">
        <i class="fa fa-plus plus {node_num}" id="plus-node-{node_num}"></i>
    </button>
</div>

<dialog class="dlg" id="dlg-{node_num}">
    <div class="dialog">
        <div class="top_btns">
            <button class="optionBtn" class:selected={selected==0} on:click={moveBtn} data-testid="move-{node_num}">Move</button>
            <button class="optionBtn" class:selected={selected==1} on:click={payoffBtn} data-testid="payoff-{node_num}">Payoff</button>
        </div>

        <form class="player_num" id="player_num_{node_num}" on:submit={(event) => playerEnter(event)}>
            <input type="number" name="player_num" class="player_input" id="player_input_{node_num}" placeholder="Player Number" required data-testid="playernum-{node_num}" />
            <button class="optionBtn" data-testid="move_enter_{node_num}">Enter</button>
        </form>

        <form class="payoff" id="payoff_{node_num}" on:submit={(event) => payoffEnter(event)}>
            <input type="text" name="payoff" class="payoff_input" id="payoff_input_{node_num}" placeholder="Payoff (example: 1,2)" required pattern="^-?\d+(,-?\d+)*-?\d?$" data-testid="payoffval-{node_num}" />
            <button class="optionBtn" id="enterBtn" data-testid="payoff_enter_{node_num}">Enter</button>
        </form>
    </div>
</dialog>

<style>
    .plus-btn {
        border: 5px solid #000;
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        padding: 0.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fff;
    }

    .colour {
        border: 5px solid;
        background-color: #16e16e;
    }

    .imperfect {
        background-color: rgb(132, 176, 247);
    }

    .plus-btn:hover {
        cursor: pointer;
    }

    .plus {
        font-size: 2em;
    }

    input {
        border: 3px solid #000;
        border-radius: 5px;
        padding: 0.5vh 0.5vw;
        font-size: 1em;
    }

    .player_num {
        display: none;
        flex-direction: column;
        align-items: center;
        gap: 3vh;
    }

    .payoff {
        display: none;
        flex-direction: column;
        gap: 3vh;
        align-items: center;
    }

    dialog {
        border: 3px solid #000;
        border-radius: 5px;
        padding: 0;
    }

    .dialog {
        padding: 3vh 2vw;
        display: flex;
        flex-direction: column;
        gap: 2vh;
        justify-content: center;
    }

    .optionBtn {
        background-color: #fff;
        border: 3px solid #000;
        color: #000;
        border-radius: 5px;
        font-size: 1em;
        padding: 0.3em 1em
    }

    .selected {
        background-color: #000;
        color: #fff;
    }

    .optionBtn:hover {
        cursor: pointer;
    }

    #enterBtn {
        width: auto;
    }
</style>