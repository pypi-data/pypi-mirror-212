let state;

const refreshState = () => {
    fetch("/status")
        .then(newState => state = newState);
}

const startGame = () => {
    fetch("/start")
        .then(refreshState);
}