<script lang="ts">
    import ActionBtn from "./ActionBtn.svelte";
    import PlusBtn from "./PlusBtn.svelte";

    import { onMount, afterUpdate } from 'svelte';

    import { global_node_num, profile, profile_index, current_imperfection } from "$lib/stores"

    export let node;
    export let Node_class;
    export let action = "";

    export let widt: number = 0;
    export let initial = false;

    export let colour = false;
    
    let imperfect = false;

    let node_wid: number;
    let doc_wid: number;

    let wid_arr: Array<number> = []

    let choice: number;
    let node_num = node.node_number

    let child_colour_num: number;
    let line_colour: boolean = colour;

    $: if ($current_imperfection.length == 0) imperfect = false

    $: pr = $profile
    $: for (let p of pr[$profile_index].flat(2)) {
        if (p.num == node_num) {
            line_colour = true;
            for (let a = 0; a < node.actions.length; a++) {
                if (node.actions[a] == p.action) {
                    child_colour_num = node.children[a].node_number
                    break;
                }
            }
        }
    }

    let playerNum: string;
    let payoffval: string;
    let children: Array<string> = [];

    onMount(() => {
        node_wid = document.getElementById(`initial-${node_num}`)!.clientWidth
        doc_wid = document.documentElement.clientWidth
    })

    afterUpdate(() => {
        node_wid = document.getElementById(`initial-${node_num}`)!.clientWidth
        doc_wid = document.documentElement.clientWidth
    })

    $: widt = (node_wid / doc_wid) * 100

    $: if (choice == 0) {
        node.player = parseInt(playerNum);
        node.payoffs = [];
    } else if (choice == 1) {
        node.payoffs = payoffval.split(",").map((x) => parseInt(x))
    }

    // the for loop was being run infinitely since node_num was being updated at every recursive backtrack
    // and then since it was being run again children was being updated again which meant that the
    // forward run was beginning again
    // thus, the node_num was going from 1 to 0 to 1 to 0 and so on.
    // soln: wrap in a function and only have the reactivity on children

    const update_children = (kids: Array<string>) => {
        const wlen = wid_arr.length
        if (kids.length > 0) {
            for (let i = 0; i < (kids.length - wlen); i++) {
                node.actions = children
                const new_node = new Node_class($global_node_num)
                global_node_num.update(n => n+1)
                node.children.push(new_node)

                wid_arr.push(0)
            }
        }
    }

    const set_width_hr = (kids: Array<string>, widths: Array<number>, width: number) => {
        if (kids.length > 0) {
            const wid_add = widths.reduce((x, y) => {return x+y}, 0)
            const n: number = kids.length

            const old_width = wid_add + 2*(n-1) - (wid_arr[0] / 2) - (wid_arr[wid_arr.length - 1] / 2)
            const new_width = width - (wid_arr[0] / 2) - (wid_arr[wid_arr.length - 1] / 2)
            const hr_width = old_width < new_width ? old_width : new_width

            const hr = document.getElementById(`hr-${node_num}`)
            hr!.style.display = "block"
            hr!.style.width = `${hr_width}vw`
            hr!.style.marginLeft = `${wid_arr[0]/2}vw`
            hr!.style.marginRight = `${wid_arr[wid_arr.length - 1]/2}vw`
        }
    }

    $: update_children(children)
    $: set_width_hr(children, wid_arr, widt)
    
</script>

<div class="initial" id="initial-{node_num}">
    {#if (action != "")}
        <div class="top_line">
            <div class="line top" class:colour={colour}></div>
            <div class="action" class:colour={colour}>{action}</div>
            <div class="line top" class:colour={colour}></div>
        </div>
    {/if}

    <div class="inner_initial">
        <div class="main_node">
        <PlusBtn bind:choice={choice} bind:playerNum={playerNum} bind:payoffval={payoffval} node_num={node.node_number} initial={initial} colour={colour} bind:imperfect={imperfect} node={node} />
        {#if (choice == 0)}
            <div class="action_div">
                <ActionBtn bind:children={children} node_num={node.node_number} initial={initial} colour={colour} />
            </div>
        {/if}
        </div>
    </div>

    {#if (children.length > 0)}
        <div class="line" class:colour={initial || colour || line_colour}></div>
    {/if}
        
    <hr id="hr-{node_num}"/>

    <div class="child_nodes">
        {#if (node.children.length != 0)}
            {#each node.children as n, i}
                <svelte:self node={n} Node_class={Node_class} bind:widt={wid_arr[i]} action={children[i]} profile={profile} colour={child_colour_num==n.node_number} />
            {/each}
        {/if}
    </div>
</div>

<style>
    .initial {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .main_node {
        display: flex;
        flex-direction: row;
        gap: 1vw;
    }

    .action {
        font-family: "Inter";
        font-size: 1em;
    }

    .inner_initial {
        display: flex;
        flex-direction: column;
    }

    .top_line {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .line {
        width: 0;
        height: 5vh;
        border: 1px solid #000;
    }

    .top {
        height: 2.5vh;
    }

    .colour {
        border-color: #16e16e;
        color: #16e16e;
    }

    hr {
        display: none;
        width: 0;
        color: #000;
        border: 1px solid #000;
        margin: 0;
    }

    .child_nodes {
        display: flex;
        flex-direction: row;
        gap: 2vw;
        justify-content: center;
    }
</style>