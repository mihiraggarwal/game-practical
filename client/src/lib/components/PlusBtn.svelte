<script lang="ts">
    const btnClick = () => {
        const dialog = document.getElementById("dlg")
        dialog?.showModal()
    }

    const moveBtn = () => {
        const dialog = document.getElementById("dlg")
        dialog?.close()
    }

    const payoffBtn = () => {
        const dialog = document.getElementById("dlg")
        dialog?.close()
    }
</script>

<button class="plus-btn" on:click={btnClick}>
    <i class="fa fa-plus"></i>
</button>

<dialog id="dlg">
    <button class="optionBtn" on:click={moveBtn}>Move</button>
    <button class="optionBtn" on:click={payoffBtn}>Payoff</button>
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

    i {
        font-size: 2em;
    }
</style>