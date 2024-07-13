<script lang="ts">

    import { profile, profile_index } from "$lib/stores"

    export let children: Array<string>
    export let node_num: number
    
    let colour: boolean = false

    let dialog: HTMLDialogElement;
    let action_counter: number = 0;

    $: pr = $profile
    $: for (let p of pr[$profile_index].flat(2)) {
        if ((p.num == node_num) || (p.destination == node_num)) {
            colour = true;
            break;
        }
        else {
            colour = false;
        }
    }
    
    const add_action = () => {
        dialog = document.getElementById(`action_modal-${node_num}`) as HTMLDialogElement;
        dialog.showModal();
    }

    const add_row = () => {
        action_counter++;
    }
    
    const enter = (event: SubmitEvent & { currentTarget: EventTarget & HTMLFormElement; }) => {
        event.preventDefault();
        children = Array.from(document.getElementsByClassName(`action_input ${node_num}`), x => (x as HTMLInputElement).value)
        dialog.close();
    }
</script>

<button type="button" class="action_btn" class:colour={colour} on:click={add_action}>Add Action</button>

<dialog class="action_modal" id="action_modal-{node_num}">
    <form class="modal_div" on:submit={(event) => {enter(event)}}>
        <div class="action_component">
            {#each {length: action_counter + 1} as _, i}
            <div class="indi_action">
                <div class="action_ntm">{i+1}.</div>
                <input type="text" class="action_input {node_num}" required>
            </div>
            {/each}
        </div>
        <div class="action_buttons">
            <button type="button" class="plus_btn" on:click={add_row}>
                <i class="fa fa-plus plus"></i>
            </button>
            <button type="submit" class="enter_btn">Finish</button>
        </div>
    </form>
</dialog>

<style>
    .action_btn {
        background-color: #fff;
        border: 3px solid #000;
        color: #000;
        border-radius: 5px;
        height: 100%;
        width: 8vw;
        font-size: 1em;
    }

    .action_btn:hover {
        cursor: pointer;
    }

    dialog {
        border: 3px solid #000;
        border-radius: 5px;
        padding: 3vh 2vw;
    }

    .modal_div {
        display: flex;
        flex-direction: column;
        gap: 2vh;
        justify-content: center;
    }

    input {
        border: 3px solid #000;
        border-radius: 5px;
        padding: 0.5vh 0.5vw;
        font-size: 1em;
    }

    .action_component {
        display: flex;
        flex-direction: column;
        gap: 0.5vh;
        align-items: flex-start;
    }

    .action_ntm {
        font-family: "Inter";
        font-size: 1em;
        width: 2vw;
    }

    .indi_action {
        display: flex;
        flex-direction: row;
        /* gap: 1vw; */
        align-items: center;
    }

    button {
        background-color: #fff;
        border: 3px solid #000;
        color: #000;
        border-radius: 5px;
        font-size: 1em;
        padding: 0.3em 1em
    }

    button:hover {
        cursor: pointer;
    }

    .action_buttons {
        display: flex;
        justify-content: center;
        gap: 0.5vw;
    }

    .colour {
        background-color: #16e16e;
    }
</style>
