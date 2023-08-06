class RenderError extends Error {}
const BLOCK_SIZE = 40;
let DRAW_COUNT_DEBUG = 0;

function getFaceImage(points, closed = false) {
    if (points < 0 || points > 6) {
        throw RenderError(`No domino face with ${points} points`);
    }

    if (closed) {
        return document.getElementById("closed");
    }

    return document.getElementById("domino" + points);
}

function rotatePieceOffset(offset, rotation) {
    return {
        x: offset.x,
        y: offset.y,
        rotation: offset.rotation
    }
}

function getPieceOffsetDirection(parent, child) {
    if (parent.double) {
        const slot = parent.linked.indexOf(child);

        if (slot === 0) {
            return {
                x: 1.5,
                y: 0,
                rotation: 0
            }
        } else if (slot === 1) {
            return {
                x: -1.5,
                y: 0,
                rotation: 0
            }
        } else if (slot === 2) {
            return {
                x: 0,
                y: 1,
                rotation: 90
            }
        } else {
            return {
                x: 0,
                y: -1,
                rotation: -90
            }
        }
    } else {
        const direction = child.sides.includes(parent.sides[0]) ? -1 : 1;
        const multiplier = child.sides[0] === child.sides[1] ? 1.5 : 2;
        console.log(child.sides, direction, multiplier);
        return {
            x: direction * multiplier,
            y: 0,
            rotation: 0
        }
    }
}

function getPieceOffset(parent, child) {
    const offset = getPieceOffsetDirection(parent, child);
    offset.x *= BLOCK_SIZE
    offset.y *= BLOCK_SIZE
    return rotatePieceOffset(offset, parent.rotation);
}

class Piece {
    constructor(sides, closed, linked, x, y, rotation = 0) {
        this.sides = sides;
        this.closed = closed;
        this.linked = linked;
        this.double = sides[0] === sides[1];
        this.x = x;
        this.y = y;
        this.rotation = rotation;
    }

    render(ctx) {
        DRAW_COUNT_DEBUG++
        if (DRAW_COUNT_DEBUG > 15) {
            return;
        }

        // console.log(this.sides, this.x, this.y, this.rotation);

        ctx.save();

        ctx.translate(this.x, this.y);

        ctx.rotate(this.rotation / 180 * Math.PI);
        if (this.double) {
            ctx.rotate(90 / 180 * Math.PI);
        }

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(-BLOCK_SIZE, -0.5 * BLOCK_SIZE, 2 * BLOCK_SIZE, BLOCK_SIZE, 5);
        ctx.fill();

        // Faces
        ctx.drawImage(getFaceImage(this.sides[0], this.closed), -BLOCK_SIZE, -0.5 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        ctx.drawImage(getFaceImage(this.sides[1], this.closed), 0, -0.5 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);

        // Separator line
        ctx.beginPath();
        ctx.moveTo(0, -0.5 * BLOCK_SIZE);
        ctx.lineTo(0, -0.5 * BLOCK_SIZE);
        ctx.stroke();

        ctx.restore();

        for (let i = 0; i < this.linked.length; ++i) {
            const linkedPiece = this.linked[i];

            // Flip the linked Piece if the default side does not match
            if (this.rotation - linkedPiece.rotation === 180) {
                if (!this.sides.includes(linkedPiece.sides[1])) {
                    linkedPiece.sides = [linkedPiece.sides[1], linkedPiece.sides[0]];
                }
            } else {
                if (!this.sides.includes(linkedPiece.sides[0])) {
                    linkedPiece.sides = [linkedPiece.sides[1], linkedPiece.sides[0]];
                }
            }

            const offset = getPieceOffset(this, linkedPiece);
            const attachedPiece = new Piece(
                linkedPiece.sides,
                linkedPiece.closed,
                linkedPiece.linked,
                this.x + offset.x,
                this.y + offset.y,
                this.rotation + offset.rotation
            )

            /*if (attachedPiece.x >= window.innerWidth - BLOCK_SIZE || attachedPiece.x <= BLOCK_SIZE) {
                if (attachedPiece.y > window.innerHeight * 0.5) {
                    attachedPiece.rotation = -90;
                    attachedPiece.x -= 2 * BLOCK_SIZE;
                    attachedPiece.y -= BLOCK_SIZE;
                } else {
                    attachedPiece.rotation = 90;
                    attachedPiece.x -= 2 * BLOCK_SIZE;
                    attachedPiece.y += BLOCK_SIZE;
                }
            }*/

            attachedPiece.render(ctx);
        }
    }
}

function render() {
    renderBoard();
}

function renderBoard() {
    DRAW_COUNT_DEBUG = 0;

    const canvas = document.getElementById("board");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const ctx = document.getElementById("board").getContext("2d");
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

    if (state.round === null) {
        return
    }

    const data = state.round.board.origin;
    console.log(data);
    const piece = new Piece(data.sides, data.closed, data.linked, window.innerWidth * 0.5, window.innerHeight * 0.5);
    piece.render(ctx);
}