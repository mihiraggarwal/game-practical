<script lang="ts">
    export let children: Array<string>
    export let node_num: number

    let dialog: HTMLDialogElement;
    let action_counter: number = 0;
    
    const add_action = () => {
        dialog = document.getElementById(`action_modal-${node_num}`) as HTMLDialogElement;
        dialog.showModal();
    }

    const add_row = () => {
        action_counter++;
    }
    
    const enter = () => {
        children = Array.from(document.getElementsByClassName(`action_input ${node_num}`), x => (x as HTMLInputElement).value)
        dialog.close();
    }
</script>

<button type="button" class="action_btn" on:click={add_action}>Add Action</button>

<dialog class="action_modal" id="action_modal-{node_num}">
    <div class="modal_div">
        <div class="action_component">
            {#each {length: action_counter + 1} as _, i}
            <div class="indi_action">
                <div class="action_ntm">{i+1}.</div>
                <input type="text" class="action_input {node_num}">
            </div>
            {/each}
        </div>
        <div class="action_buttons">
            <button class="plus_btn" on:click={add_row}>
                <i class="fa fa-plus plus"></i>
            </button>
            <button class="enter_btn" on:click={enter}>Finish</button>
        </div>
    </div>
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

    .modal_div {
        display: flex;
        flex-direction: column;
        gap: 1vh;
    }

    .action_component {
        display: flex;
        flex-direction: column;
    }

    .indi_action {
        display: flex;
        flex-direction: row;
        gap: 1vw;
    }

    .action_buttons {
        display: flex;
        justify-content: center;
        gap: 0.5vw;
    }
</style>
