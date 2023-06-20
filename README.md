# Sudoku
## Given puzzle board
* A number of puzzles have been made available in /sodoku
* An easy-difficulty puzzle: easy.txt
* Four medium-difficulty puzzles: medium1.txt, medium2.txt, medium3.txt, and medium4.txt
* Two hard-difficulty puzzles: hard1.txt and hard2.txt
## Sudoku.py
* Run Sudoku.py in Jupyter kernal
* Change the initial puzzle board path by calling read_board()
* Example command
```
import Sudoku as sodu
import importlib
importlib.reload(sodu)
b = sodu.read_board("sudoku/hard1.txt")
p = sodu.Sudoku(b)
p.infer_with_guessing()
print(p)
```
## SudokuGUI.py
* Run SudokuGUI.py in Jupyter kernal
* You could try different solvers to implement
* You could reset the puzzle using the text input. The text input allows for two different puzzle formats (empty block with '*' or '0'). 
* Example text input
```
821*****7
***8***6*
*6*93***5
**82*16**
***7**284
24*6*37**
6*5***1*3
*7**5****
912*****6
```
## 
