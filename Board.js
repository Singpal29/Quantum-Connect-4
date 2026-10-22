var p1 = "R";
var p2 = "G";
var currPlayer = p1;

var gameOver = false;
var board;

var rows = 6;
var cols = 7;
var pieceType = "Normal";
var firstPiece = true;
var p1Count = 0;
var p2Count = 0;
var piecesPlaced;

window.onload = function() {
  setGame();
}

function setGame() {
  board = [];
  for (let r = 0; r < rows; r++) {
    let row = [];
    let types = [];
    for (let c = 0; c < cols; c++) {
      row.push(" ");
      let tile = document.createElement("div");
      tile.addEventListener("click", collapse);
      tile.id = r.toString() + "-" + c.toString();
      tile.classList.add("tile");
      document.getElementById("board").append(tile);

    }
    board.push(row);
  }
  for (let c = 0; c < cols; c++) {
    let placer = document.createElement("div");
    placer.id = c.toString() + " Button";
    placer.classList.add("placer");
    placer.addEventListener("click", setPiece);
    document.getElementById("buttons").append(placer);
  }
  let swapper = document.createElement("div");
  swapper.id = "swapper";
  swapper.classList.add("swapper");
  swapper.innerText = pieceType;

  swapper.addEventListener("click", swap);
  document.getElementById("piece-choice").append(swapper);
  
}
function setPiece() {
  if (gameOver) return;
  
  let col = parseInt(this.id.split(" ")[0]);
  let r = rows - 1;
  for (; r >= 0; r--) {
    if (board[r][col] == " ") break;
  }
  if (r < 0) return;
  
  let tile = document.getElementById(r + "-" + col);
  if (pieceType == "Normal") {
    board[r][col] = currPlayer;
    if (currPlayer == p1) {
      tile.classList.add("red-piece");
      
      
      
    }
    else {
      tile.classList.add("green-piece");
      
      

    }
    swap_player();
  }

  else {
    if (currPlayer == p1) {
      tile.classList.add("quantum-red-piece");
      tile.innerText = p1Count;
      board[r][col] = "P";
      
    }
    else {
      tile.classList.add("quantum-green-piece");
      tile.innerText = p2Count;
      board[r][col] = "Y";
      
    }
    if (firstPiece) firstPiece = false;
    else {
      if (currPlayer == p1) p1Count++;
      else p2Count++;
      swap_player();
      firstPiece = true;
      

      

    }
  }
  
  

  checkGame();
}

function checkGame() {
  let draw = true;
  let winner1 = false;
  let winner2 = false;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols - 3; c++) {
      if (board[r][c] != " " && board[r][c] != "Y" && board[r][c] != "P") {
        if (board[r][c] == board[r][c + 1] && 
            board[r][c] == board[r][c + 2] && 
            board[r][c] == board[r][c + 3] 
        ) {
          if (board[r][c] == "R") winner1 = true;
          else winner2 = true;
        }
      }
      else {
        draw = false;
      }
    }
  }
  for (let c = 0; c < cols; c++) {
    for (let r = 0; r < rows - 3; r++) {
      if (board[r][c] != " " && board[r][c] != "Y" && board[r][c] != "P") {
        if (board[r][c] == board[r + 1][c] && 
            board[r][c] == board[r + 2][c] && 
            board[r][c] == board[r + 3][c] 
        ) {
          if (board[r][c] == "R") winner1 = true;
          else winner2 = true;
        }
      }
    }
  }
  for (let c = 0; c < cols - 3; c++) {
    for (let r = 0; r < rows - 3; r++) {
      if (board[r][c] != " " && board[r][c] != "Y" && board[r][c] != "P") {
        if (board[r][c] == board[r + 1][c + 1] && 
            board[r][c] == board[r + 2][c + 2] && 
            board[r][c] == board[r + 3][c + 3] 
        ) {
          if (board[r][c] == "R") winner1 = true;
          else winner2 = true;
        }
      }
    }
  }
  for (let c = 3; c < cols; c++) {
    for (let r = 0; r < rows - 3; r++) {
      if (board[r][c] != " " && board[r][c] != "Y" && board[r][c] != "P") {
        if (board[r][c] == board[r + 1][c - 1] && 
            board[r][c] == board[r + 2][c - 2] && 
            board[r][c] == board[r + 3][c - 3] 
        ) {
          if (board[r][c] == "R") winner1 = true;
          else winner2 = true;
        }
      }
    }
  }
  setWinner(winner1, winner2, draw);
}
function setWinner(winner1, winner2, draw) {
  if (!winner1 && !winner2 && !draw) return;
  gameOver = true;
  
  if ((winner1 && winner2) || draw) {
    
    document.getElementById("winner").innerText = "DRAW";
    document.getElementById("winner").style.color = "brown";
  }
  else {
    if (winner2) {
      document.getElementById("winner").innerText = "GREEN WINS";
      document.getElementById("winner").style.color = "green";
    }
    else {
      document.getElementById("winner").innerText = "RED WINS";
      document.getElementById("winner").style.color = "red";
    }
    
  }
}
function swap() {
  if (!firstPiece) return;
  if (gameOver) return;
  if (pieceType == "Normal") {
    
    pieceType = "Quantum";
    
    if (currPlayer == p1) {
      
      document.getElementById("swapper").style.backgroundColor = "pink";
    }
    else {
      document.getElementById("swapper").style.backgroundColor = "yellow";
    }
  }
  else {
    pieceType = "Normal";
    
    if (currPlayer == p1) {
      document.getElementById("swapper").style.backgroundColor = "red";
    }
    else {
      document.getElementById("swapper").style.backgroundColor = "green";
    }
  }
  document.getElementById("swapper").innerText = pieceType;
}
function collapse() {
  if (gameOver) return;
  if (!firstPiece) return;
  if (!this.classList.contains("quantum-red-piece") &&
      !this.classList.contains("quantum-green-piece")) return;

  let target = this.innerText;
  let cls = this.className; // the partner has the same color class
  let [cr, cc] = this.id.split("-").map(Number);

  if (this.classList.contains("quantum-red-piece")) {
    this.className = "tile red-piece";
    board[cr][cc] = p1;
  } else {
    this.className = "tile green-piece";
    board[cr][cc] = p2;
  }
  this.innerText = "";

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      let tile = document.getElementById(r + "-" + c);
      if (tile.className == cls && tile.innerText == target) {
        for (let row = r; row > 0; row--) {
          board[row][c] = board[row - 1][c];
          let below = document.getElementById(row + "-" + c);
          let above = document.getElementById((row - 1) + "-" + c);
          below.className = above.className;
          below.innerText = above.innerText;
        }
        board[0][c] = " ";
        let top = document.getElementById("0-" + c);
        top.className = "tile";
        top.innerText = "";

        checkGame();
        if (!gameOver) swap_player();
        return;
      }
    }
  }

  checkGame();
  if (!gameOver) swap_player();
}
function swap_player() {
  if (currPlayer == p1) {
    currPlayer = p2;
    if (pieceType == "Normal") {
      document.getElementById("swapper").style.backgroundColor = "green";
    }
    else {
      document.getElementById("swapper").style.backgroundColor = "yellow";
    }
    for (let c = 0; c < cols; c++) {
      document.getElementById(c.toString() + " Button").style.backgroundColor = "green";
    }

  }
  else {
    currPlayer = p1;
    if (pieceType == "Normal") {
      document.getElementById("swapper").style.backgroundColor = "red";
    }
    else {
      document.getElementById("swapper").style.backgroundColor = "pink";
    }
    for (let c = 0; c < cols; c++) {
      document.getElementById(c.toString() + " Button").style.backgroundColor = "red";
    }
  }
}