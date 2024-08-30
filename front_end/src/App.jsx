import React, { useState } from 'react';
import StartGame from './components/StartGame';
import GameBoard from './components/GameBoard';
import GameOver from './components/GameOver';

const App = () => {
  const [gameId, setGameId] = useState(null);
  const [player1Id, setPlayer1Id] = useState(null);
  const [player2Id, setPlayer2Id] = useState(null);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);

  const handleStartGame = (gameData) => {
    setGameId(gameData.id);
    setPlayer1Id(gameData.first_player_id);
    setPlayer2Id(gameData.second_player_id);
  };

  const handleGameOver = (winner) => {
    setGameOver(true);
    setWinner(winner);
  };

  const handleRestart = () => {
    setGameOver(false);
    setWinner(null);
    setGameId(null);
    setPlayer1Id(null);
    setPlayer2Id(null);
  };

  return (
    <div className="app">
      {!gameId && !gameOver && (
        <StartGame onStartGame={handleStartGame} />
      )}
      {gameId && !gameOver && (
        <GameBoard
          gameId={gameId}
          player1Id={player1Id}
          player2Id={player2Id}
          onGameOver={handleGameOver}
        />
      )}
      {gameOver && (
        <GameOver winner={winner} onRestart={handleRestart} />
      )}
    </div>
  );
};

export default App;
