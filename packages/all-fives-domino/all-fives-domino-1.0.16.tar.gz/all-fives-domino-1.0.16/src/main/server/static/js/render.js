class RenderError extends Error {}

function getFaceImage(points, closed = false) {
    if (points < 0 || points > 6) {
        throw RenderError(`No domino face with ${points} points`);
    }

    if (closed) {
        return "static/img/closed.png";
    }

    return `static/img/d${points}.png`;
}

class Piece {
    constructor(sides, closed) {
        this.sides = sides
        this.closed = closed
        this.double = sides[0] === sides[1]
    }

    render() {
        const piece = document.createElement("div");

        const pieceDisplay = document.createElement("div");
        pieceDisplay.classList.add("piece-display");
        const attachedPieces = document.createElement("div");
        attachedPieces.classList.add("attached-pieces")
        piece.append(pieceDisplay, attachedPieces);

        piece.classList.add("piece")
        if (this.double) {
            piece.classList.add("double")
        }

        for (const side of this.sides) {
            const face = document.createElement("img")
            face.classList.add("face")
            face.src = getFaceImage(side, this.closed)
            pieceDisplay.append(face)
        }

        return piece
    }
}

function render() {
    renderBoard();
}

function renderBoard() {
    document.getElementById("board").innerHTML = "";

    if (state.round === null) {
        return
    }

    const origin = state.round.board.origin;
    renderPiece(origin);
}

function renderPiece(data) {
    const piece = new Piece(data.sides, data.closed, data.double);
    document.getElementById("board").append(piece.render())
}