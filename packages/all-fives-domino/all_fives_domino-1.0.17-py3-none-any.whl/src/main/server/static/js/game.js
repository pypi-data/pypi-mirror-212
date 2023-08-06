let state;

const refreshState = () => {
    fetch("/status")
        .then(r => r.json())
        .then(newState => {
            state = newState;
            render();
        });
}

const startGame = () => {
    fetch("/start");
}

setTimeout(refreshState, 1000)
