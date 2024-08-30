import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cell from './Cell';
import './GameBoard.css'; // Import the new CSS file

const GameBoard = ({ gameId, player1Id, player2Id, onGameOver }) => {
  const [cells, setCells] = useState(Array(9).fill(''));
  const [currentPlayer, setCurrentPlayer] = useState('X');
  const [gameOver, setGameOver] = useState(false);
  const [player1Name, setPlayer1Name] = useState('Player 1');
  const [player2Name, setPlayer2Name] = useState('Player 2');

  useEffect(() => {
    const fetchGame = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/games/${gameId}`);
        setCells(response.data.board);
      } catch (error) {
        console.error('Error fetching game:', error);
      }
    };

    const fetchPlayerNames = async () => {
      try {
        const player1Response = await axios.get(`http://localhost:5000/players/${player1Id}`);
        const player2Response = await axios.get(`http://localhost:5000/players/${player2Id}`);
        setPlayer1Name(player1Response.data.name);
        setPlayer2Name(player2Response.data.name);
      } catch (error) {
        console.error('Error fetching player names:', error);
      }
    };

    fetchGame();
    fetchPlayerNames();
  }, [gameId, player1Id, player2Id]);

  const handleCellClick = async (index) => {
    if (cells[index] === '' && !gameOver) {
      try {
        const response = await axios.put(`http://localhost:5000/games/${gameId}/move`, {
          index,
          player: currentPlayer,
        });

        setCells(response.data.board);
        if (response.data.winner) {
          setGameOver(true);
          onGameOver(response.data.winner);
        } else {
          setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X');
        }
      } catch (error) {
        console.error('Error making move:', error);
        alert('Error making move. Please try again.');
      }
    }
  };

  return (
    <div className="game-board-container">
      <h2>Current Player: {currentPlayer === 'X' ? player1Name : player2Name}</h2>
      <div className="board">
        {cells.map((cell, index) => (
          <Cell key={index} value={cell} onClick={() => handleCellClick(index)} />
        ))}
      </div>
    </div>
  );
};

export default GameBoard;

