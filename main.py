import sys
import random
from functools import partial
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load('form.ui')
        self.game = [[None for i in range(3)] for j in range(3)]

        self.game[0][0] = self.ui.btn_11
        self.game[0][1] = self.ui.btn_12
        self.game[0][2] = self.ui.btn_13
        self.game[1][0] = self.ui.btn_21
        self.game[1][1] = self.ui.btn_22
        self.game[1][2] = self.ui.btn_23
        self.game[2][0] = self.ui.btn_31
        self.game[2][1] = self.ui.btn_32
        self.game[2][2] = self.ui.btn_33

        self.player = 1
        self.player1_wins = 0
        self.player2_wins = 0
        self.draw = 0

        self.status = []
        self.remain_empty = []
        self.win = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

        self.ui.show()

        for i in range(3):
            for j in range(3):
                self.game[i][j].clicked.connect(partial(self.play, i, j))

    def play(self, i, j):

        if self.game[i][j].text() == "":
            if self.player == 1:
                self.game[i][j].setText('x')
                self.game[i][j].setStyleSheet('color: blue; background-color: #CCFFFF')
                self.player = 2

                if self.ui.rb_p_vs_pc.isChecked():
                    self.remain_empty = []
                    for i in range(3):
                        for j in range(3):
                            self.remain_empty.append(self.game[i][j].text())
                    try:
                        self.empty_index = ({value: [i for i, v in enumerate(self.remain_empty) if v == value] \
                                             for value in set(self.remain_empty)})['']
                        self.random_position = random.choice(self.empty_index)
                        self.game[self.random_position // 3][self.random_position % 3].setText('O')
                        self.game[self.random_position // 3][self.random_position % 3].setStyleSheet('color: red; background-color: #FFFFCC')
                        self.player = 1
                    except:
                        pass

            elif self.player == 2:
                if self.ui.rb_p_vs_p.isChecked():
                    self.game[i][j].setText('O')
                    self.game[i][j].setStyleSheet('color: red; background-color: #FFFFCC')
                    self.player = 1

        self.check()

    def clean_board(self):
        for i in range(3):
            for j in range(3):
                self.game[i][j].setText('')
                self.game[i][j].setStyleSheet('')
        self.status = []
        self.player = 1

    def check(self):

        self.status = []
        for i in range(3):
            for j in range(3):
                self.status.append(self.game[i][j].text())
        # print(self.status)

        indices = {value: [i for i, v in enumerate(self.status) if v == value] for value in set(self.status)}
        for z in range(len(self.win)):
            if all(item in indices['x'] for item in self.win[z]):
                msg_box = QMessageBox()
                msg_box.setText("P1 winned")
                self.player1_wins += 1
                self.ui.lbl_player1.setText(str(self.player1_wins))
                msg_box.exec()
                self.clean_board()

            elif 'O' in indices.keys() and len(self.status)>0:
                if all(item in indices['O'] for item in self.win[z]):
                    msg_box = QMessageBox()
                    msg_box.setText("P2 winned")
                    self.player2_wins += 1
                    self.ui.lbl_player2.setText(str(self.player2_wins))
                    msg_box.exec()
                    self.clean_board()
                else:
                    if (len(indices['x']) + len(indices['O'])) == 9 and z == len(self.win) - 1:          # BUG ************
                        msg_box = QMessageBox()
                        msg_box.setText("DRAW")
                        self.draw += 1
                        self.ui.lbl_draw.setText(str(self.draw))
                        msg_box.exec()
                        self.clean_board()
                        break

        '''
        if all(self.game[0][i].text() == 'x' for i in range(3)):
            msg_box = QMessageBox()
            msg_box.setText("P1 winned")
            self.player1_wins += 1
            self.ui.lbl_player1.setText(str(self.player1_wins))
            msg_box.exec()
        '''





if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
