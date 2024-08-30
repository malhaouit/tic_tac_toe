import React, { useState } from 'react';
import axios from 'axios';
import './StartGame.css'; // Import the new CSS file

const StartGame = ({ onStartGame }) => {
  const [player1Name, setPlayer1Name] = useState('');
  const [player2Name, setPlayer2Name] = useState('');

  const handleStart = async () => {
    try {
      const player1 = await axios.post('http://localhost:5000/players', { name: player1Name });
      const player2 = await axios.post('http://localhost:5000/players', { name: player2Name });

      const game = await axios.post('http://localhost:5000/games', {
        first_player_id: player1.data.id,
        second_player_id: player2.data.id,
      });

      onStartGame(game.data);
    } catch (error) {
      console.error('Error creating players or game:', error);
      alert('Error creating players. Please check the console for more details.');
    }
  };

  return (
    <div className="start-game-container">
      <h1>Start a New Game</h1>
      <input
        type="text"
        placeholder="Player 1 Name"
        value={player1Name}
        onChange={(e) => setPlayer1Name(e.target.value)}
        className="player-input"
      />
      <input
        type="text"
        placeholder="Player 2 Name"
        value={player2Name}
        onChange={(e) => setPlayer2Name(e.target.value)}
        className="player-input"
      />
      <button onClick={handleStart} className="start-button">Start Game</button>
    </div>
  );
};

export default StartGame;
