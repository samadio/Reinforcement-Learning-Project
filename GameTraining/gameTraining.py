from typing import List
from Game.board import Board
from Players.player import Player


class GameTraining:
    boardsize: int
    board: Board
    numBoxes: int
    players: List[Player]
    learning_model_step: int
    update_target_step: int

    def __init__(self, players: List[Player], boardsize: int = 4, learning_model_step: int =1,update_target_step: int = 1):
        self.boardsize = boardsize
        self.board = Board(self.boardsize)
        self.numBoxes = 0
        self.players = players

    def is_valid(self, idx: int) -> bool:
        return not self.board.vectorBoard[idx]  # (1==True gives False, 0 == False gives True)

    def play(self, train: bool):

        currentPlayer = self.players[0]
        currentPlayer.state = self.board.vectorBoard.copy()
        otherPlayer = self.players[1]
        turn = 0
        PlayerTurn = 0
        N = self.board.size
        while turn < (2 * N + 2) * N:

            action = currentPlayer.get_move(self.board.vectorBoard)

            if not self.is_valid(action):
                currentPlayer.invalidMove()
                return 1

            self.board.set_board(action)

            newNumBoxes = self.board.count_boxes()

            if newNumBoxes - self.numBoxes == 0:
                if turn > 0:
                    currentPlayer.no_score_move()
                    otherPlayer.add_record(self.board.vectorBoard, False)
                    if train:
                        otherPlayer.train_model_network()

                PlayerTurn += 1
                currentPlayer = self.players[PlayerTurn % 2]
                otherPlayer = self.players[(PlayerTurn + 1) % 2]
            else:
                currentPlayer.scored(newNumBoxes - self.numBoxes)
                self.numBoxes = newNumBoxes
                otherPlayer.opponentScored(newNumBoxes - self.numBoxes)

            turn += 1

        currentPlayer.endGameReward(currentPlayer.score > otherPlayer.score)
        currentPlayer.add_record(self.board.vectorBoard, True)
        otherPlayer.endGameReward(otherPlayer.score > currentPlayer.score)
        otherPlayer.add_record(self.board.vectorBoard, True)
        if train:
            currentPlayer.train_model_network()
        if train:
            otherPlayer.train_model_network()
        return 0

    def reset(self):
        self.board = Board(self.boardsize)
        self.numBoxes = 0
        for player in self.players:
            player.score = 0

