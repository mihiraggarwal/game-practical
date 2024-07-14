<script>
    import question from "$lib/icons/question-sign.png"
    import play from "$lib/icons/play-button-arrowhead.png"
    import github from "$lib/icons/github.png"
</script>

<div class="container">
    <h1>game-practical</h1>
    <div class="options">
        <a href="/help"><img src={question} alt="question" class="question"></a>
        <a href="/play"><img src={play} alt="play" class="play"></a>
        <a href="https://github.com/mihiraggarwal/game-practical" target="_blank"><img src={github} alt="github" class="github"></a>
    </div>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        box-sizing: border-box;
        justify-content: center;
        align-items: center;
        gap: 3vh;
    }

    h1 {
        font-family: "airbnb-bold";
        font-size: 2.5em;
        padding: 0;
        margin: 0;
    }

    .options {
        display: flex;
        gap: 2vw;
    }

    a {
        border: 3px solid #000;
        border-radius: 100%;
        width: 5vw;
        height: 5vw;
        padding: 0;
        background-color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    img {
        width: 2.6vw;
    }

    .play {
        margin-left: 0.5vw;
    }

    .github {
        width: 3.2vw;
    }
</style>