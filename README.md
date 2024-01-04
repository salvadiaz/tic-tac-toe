# Tic-Tac-Toe
The goal of the project is to develop an API that lets you play the tic-tac-toe game.

## Assigment
The goal of this exercise is to develop an API that lets you play the tic-tac-toe game,
validate the board and return the winner.

## Features
<ul>
<li>
  Provide an endpoint that will receive the information of two players, such as their
names. The API will return an object with the game ID, player information, and which
player has to play next. <br>
Endpoint: POST /games <br>
Body (e.g.): {
  "players": [{"name": "pepe", "symbol": "X"}, {"name": "juan", "symbol": "O"}],
  "starting_player": "pepe"
}
  </li>
<li>
  When a game is created, the player who goes next should be able to submit a move.<br>
  In order to do that, another endpoint expects the game id, player name, row, and column. <br>
  The returned data should be the board state after the current play.<br>
  If the last move causes the game to end, the name of the winner should be on the "winner" field.<br>
    Endpoint: PUT /games <body>
    Body(e.g.): {
  "game_id":1,
  "player": "pepe",
  "row": 0,
  "column": 0
}
  </li>
<li>
  Provide an endpoint to list all the games. Finished games should also specify the winner.  
  </li>
<li>
  The API should let the user retrieve a single game by its ID.
  </li>
<li>
  Provide a way to delete a game by ID.
  </li>

<li>
ALL ENDPOINTS ARE LISTED AND READY TO TRY THEM OUT IN OPEN API (/docs)
</li>
</ul>

### Technologies / Frameworks
<ul>
<li>Python</li>
<li>fastAPI</li>
<li>SQLAlchemy</li>
<li>MySQL</li>
<li>pydantic</li>
</ul>

### Installation 
This app requires Docker and Docker Compose to run
<ul>
<li>
Git Clone: <br>
<code>$ git clone https://github.com/salvadiaz/tic-tac-toe.git</code>
</li>

<li>
Run in your terminal: <br>
<code> docker compose up -d </code><br>
</li> 
</ul>

### Running the app

<code>Open browser to http://localhost:8000/docs</code>