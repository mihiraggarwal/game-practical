<script lang="ts">
	import { PUBLIC_SERVER_URL } from "$env/static/public";

    import Subtree from "$lib/components/Subtree.svelte";
    import { global_node_num, profile, profile_index, any_imperfect, current_imperfection, all_imperfections } from "$lib/stores";

    let payoffs: Array<number>;

    let nSolns = 0;
    let selected = 0;
    let imperfect_selected = -1;

    let loading_spne = false;
    let loading_nash = false;

    let data_spne = false;
    let data_nash = false;

    class Node {
        public node_number: number
        public player: number
        public children: Array<Node>
        public actions: Array<string>
        public imperfect_to: Array<Node>
        public payoffs: Array<number>

        constructor(
            node_number: number,
            player: number = 0,
            children: Array<Node> = [],
            actions: Array<string> = [],
            imperfect_to: Array<Node> = [],
            payoffs: Array<number> = [],
        ) {
            this.node_number = node_number;
            this.player = player;
            this.children = children;
            this.actions = actions;
            this.imperfect_to = imperfect_to;
            this.payoffs = payoffs;
        }
    }

    const node = new Node($global_node_num)
    global_node_num.update(n => n+1)

    const solve = (type: string) => {
        let FETCH_URL: string;
        if (type == "spne") { loading_spne = true; FETCH_URL = `${PUBLIC_SERVER_URL}/spne` }
        else { loading_nash = true; FETCH_URL = `${PUBLIC_SERVER_URL}/nash` }

        fetch(FETCH_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(node)
        }).then(resp => {
            resp.json().then(data => {
                payoffs = data.payoffs
                profile.update(n => data.profile)
                nSolns = data.profile.length

                if (type == "spne") { loading_spne = false; data_spne = true; data_nash = false }
                else { loading_nash = false; data_nash = true; data_spne = false }
            })
        })
    }

    const select = (i: number) => {
        selected = i
        profile_index.update(n => i)
    }

    const show_imperfect = (imperfection: Node[], i: number) => {
        if (imperfect_selected == i) {
            current_imperfection.update(x => [])
            imperfect_selected = -1
        }
        else {
            current_imperfection.update(x => imperfection)
            imperfect_selected = i
        }
    }

    const saveImperfections = () => {
        all_imperfections.update(x => [...x, $current_imperfection])

        $current_imperfection.forEach(node => {
            const temp_arr = $current_imperfection.filter(x => x != node)
            node.imperfect_to = temp_arr
        })

        any_imperfect.update(i => false)
        current_imperfection.update(x => [])
    }
</script>

<div class="container">
    <div class="top">
        <h1>game-practical</h1>
        {#if (payoffs)}
            <div class="payoff">Payoff: ({payoffs[$profile_index]})</div>
        {:else if ($all_imperfections.length > 0)}
            <div class="info_sets">
                <div class="payoff">Imperfect Info Sets:</div>
                {#each $all_imperfections as imperfection, i}
                    <button class="soln_index" class:imperfect_selected={imperfect_selected==i} on:click={() => show_imperfect(imperfection, i)}></button>
                {/each}
            </div>
        {/if}
    </div>

    <div class="tree">

        <Subtree node={node} Node_class={Node} initial={nSolns > 0 ? true : false} />

    </div>

    <div class="answer-container">
        <div class="index_container">
            {#each Array.from({ length: nSolns }) as _, i}
                <button class="soln_index" class:selected={selected==i} on:click={() => select(i)}></button>
            {/each}
        </div>

        {#if ($any_imperfect)}
            <button on:click={saveImperfections}>Add Imperfect Info Set</button>
        {/if}

        <div class="buttons">
            <button on:click={() => solve("nash")} class:loading={loading_nash} class:selected={data_nash} disabled={loading_nash}>{loading_nash ? "Loading" : "Nash"}</button>
            <button on:click={() => solve("spne")} class:loading={loading_spne} class:selected={data_spne} disabled={loading_spne}>{loading_spne ? "Loading" : "SPNE"}</button>
        </div>
    </div>
</div>

<style>
    .container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 5vh 5vw;
        box-sizing: border-box;
        gap: 7.5vh;
    }

    .top {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2vh;
    }

    .payoff {
        font-family: "Inter";
        font-size: 1.5em;
    }

    .info_sets {
        display: flex;
        flex-direction: row;
        gap: 1vw;
    }

    h1 {
        font-family: "airbnb-bold";
        text-align: center;
        font-size: 2.25em;
        margin: 0;
    }

    .tree {
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .answer-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2vh;
    }

    button {
        background-color: #fff;
        border: 3px solid #000;
        color: #000;
        /* font-weight: bold; */
        border-radius: 7px;
        height: 100%;
        padding: 0.5vw 1vw;
        font-size: 1em;
    }

    button:hover {
        cursor: pointer;
    }

    .soln_index {
        border: 3px solid #000;
        border-radius: 100%;
        width: 2vw;
        height: 2vw;
        padding: 0;
    }

    .index_container {
        display: flex;
        gap: 1vw;
        flex-direction: row;
    }

    .selected {
        background-color: #16e16e;
    }
    
    .imperfect_selected {
        background-color: rgb(132, 176, 247);
    }

    .loading {
        background-color: gray;
    }

    .loading:hover {
        cursor: not-allowed;
    }

    .buttons {
        display: flex;
        gap: 1vw;
    }
</style>