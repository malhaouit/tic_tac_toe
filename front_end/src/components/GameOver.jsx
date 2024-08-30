import React from 'react';

const GameOver = ({ winner, onRestart }) => {
  return (
    <div>
      <h1>Game Over!</h1>
      <h2>Winner: {winner}</h2>
      <button onClick={onRestart}>Play Again</button>
    </div>
  );
};

export default GameOver;
