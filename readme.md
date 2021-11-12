# Raspberry Pi tetris game
## Manual

### Game rules
The objective is to keep the board clear as long as possible
random tetromino pieces will fall from the top, and you can move
them left-right or rotate to fit in place.
If an entire row is filled, it is cleared, and the board moves down.
Do this as long as possible

### Controls
- **Up**    -Rotates a piece
- **Down**  -Moves a piece down faster
- **Left**  -Moves a piece left
- **Left**  -Moves a piece left
- **Middle**  -Restarts the game

### Development
It is created using a Raspberry pi, python, sense hat, numpy
The board is one big numpy array, and every piece that falls is it's own tiny numpy array. Every step it's moved or falls, it is checking for collissions between the walls or other pieces to determine if a move is possible. And if there is a collission while going downwards, the piece is burned in place on the main game-board, and the process starts anew

