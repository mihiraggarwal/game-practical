<script lang="ts">
    import ActionBtn from "./ActionBtn.svelte";
    import PlusBtn from "./PlusBtn.svelte";

    import { global_node_num } from "$lib/stores"

    export let node;
    export let Node_class;

    let choice = 1;
    let action_counter = 0;
    let node_num = node.node_number

    let playerNum: string;
    let payoffval: string;
    let children: Array<string> = [];

    $: if (choice == 0) {
        node.player = playerNum;
    }

    // the for loop was being run infinitely since node_num was being updated at every recursive backtrack
    // and then since it was being run again children was being updated again which meant that the
    // forward run was beginning again
    // thus, the node_num was going from 1 to 0 to 1 to 0 and so on.
    // soln: wrap in a function and only have the reactivity on children

    const update_children = (kids: Array<string>) => {
        for (let i = 0; i < kids.length; i++) {
            const new_node = new Node_class($global_node_num)
            global_node_num.update(n => n+1)
            node.children.push(new_node)
        }
    }

    $: update_children(children)
    
</script>

<div class="initial">
    <PlusBtn bind:choice={choice} bind:playerNum={playerNum} bind:payoffval={payoffval} node_num={node.node_number} />
    {#if (choice == 0)}
        <div class="action_div">
            <ActionBtn bind:action_counter={action_counter} bind:children={children} node_num={node.node_number} />
        </div>
    {/if}
    
    {#if (node.children.length != 0)}
        {#each node.children as n}
            <!-- since recursion, index everything in the id -->
            <svelte:self node={n} Node_class={Node_class} />
        {/each}
    {/if}
</div>

<style>
    .initial {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
    }
</style>