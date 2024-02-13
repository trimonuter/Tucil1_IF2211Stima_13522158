from time import time, sleep
from random import randint
from termcolor import colored
from datetime import datetime
import os.path
import sys


def slowprint(str):
    for char in str:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.01)
    sleep(0.5)

class Game:
    def __init__(self):
        
        self.maxPoints = 0
        self.maxSequence = ''
        self.path = []
    
    def formatSequence(self, seq):
        seqStr = ''
        for i in range(len(seq)):
            if not i % 2 and i:
                seqStr += ' '
            seqStr += seq[i]
        return seqStr
    
    def traverse(self, x, y, path, visited, isVertical):
        if len(path) / 2 == self.MAX_BUFFER:
            points = 0
            for seq in self.seq:
                if seq in path:
                    points += self.seq[seq]
                    
            if points > self.maxPoints:
                self.maxPoints = points
                self.maxSequence = path
                self.originalPath = visited
                self.path = [(x + 1, y + 1) for (y, x) in visited]
        elif isVertical:
            for i in range(self.ROW):
                if (i, x) not in visited:
                    newVisited = [x for x in visited] + [(i, x)]
                    self.traverse(x, i, path + self.grid[i][x], newVisited, False)
        else:
            for j in range(self.COL):
                if (y, j) not in visited:
                    newVisited = [x for x in visited] + [(y, j)]
                    self.traverse(j, y, path + self.grid[y][j], newVisited, True)
                
    
    def findMax(self):
        start = time()
        for j in range(self.COL):
            self.traverse(j, 0, self.grid[0][j], [(0, j)], True)
            
        totalTime = round(time() - start, 3) * 1000
        # Print results
        slowprint(colored('\nSolve finished!\n\n', 'green'))
        
        if self.maxPoints == 0:
            slowprint(colored('\nMaximum Points     : ', 'yellow') + str(self.maxPoints))
            slowprint('\nNo path with points greater than 0 found.\n')
            
            slowprint(colored('\n\nTime taken: ', 'green') + colored(str(totalTime) + ' ms\n\n', 'yellow'))
        else: 
            for y in range(self.ROW):
                for x in range(self.COL):
                    node = self.grid[y][x]
                    
                    if (y, x) in self.originalPath:
                        print(colored(node + ' ', 'yellow'), end='')
                    else:
                        print(node + ' ', end='')
                        
                    sys.stdout.flush()
                    sleep(0.001)
                sleep(0.01)
                print()
            
            slowprint(colored('\nMaximum Points     : ', 'yellow') + str(self.maxPoints))
            slowprint(colored('\nPath               : ', 'yellow') + str(self.formatSequence(self.maxSequence)))
            slowprint(colored('\nPath Coordinates   : ', 'yellow') + str(self.path))
            
            slowprint(colored('\n\nTime taken: ', 'green') + colored(str(totalTime) + ' ms\n\n', 'yellow'))
            
            # Save results
            choice = False
            while not choice:
                slowprint('Do you want to save the results to a .txt file? (Y/N): ')
                save = input()
                
                if save == 'Y':
                    choice = True
                    
                    filename = 'test/' + self.filename
                    slowprint(colored('\nSaving to ', 'green') + colored(filename, 'yellow') + colored('...', 'green'))
                    sleep(1)
                    
                    with open(filename, 'w') as file:
                        file.write(str(self.maxPoints) + '\n')
                        file.write(self.formatSequence(self.maxSequence) + '\n')
                        for node in self.path:
                            file.write(str(node) + '\n')
                        file.write('\n' + f'{totalTime} ms')
                        
                    slowprint(colored('\nFile has been successfully saved!\n', 'green'))
                elif save == 'N':
                    choice = True
                else:
                    slowprint('Choice not recognized!\n')
        
        slowprint(colored('\nThanks for playing!\n', 'yellow'))
    
    def readFile(self):
        slowprint('\nPlease input a ' + colored('file name (including the .txt extension) ', 'yellow') + 'for input.')
        slowprint('\nPlease make sure the file exists and is ' + colored('located in the "input" folder', 'yellow') +  ' as a .txt file.\n\n')
        
        found = False
        while not found:
            slowprint('File name: ')
            name = input()
            filename = 'input/' + name
            
            if os.path.isfile(filename):
                slowprint(colored('\nReading from file...', 'green'))
                found = True
            else:
                slowprint('\nFile not found! Please make sure ' + colored('you have inputted the correct file name ', 'yellow') + 'and ' + colored('it is located in the correct directory ', 'yellow') + '(/input)!\n')
        
        self.filename = name
        with open(filename) as file:
            # Buffer length
            bufferLength = int(file.readline())
            
            # Matrix size
            matrixSize = [int(x) for x in file.readline().split()]
            matCol = matrixSize[0]
            matRow = matrixSize[1]
            
            # Matrix
            matrix = []
            for i in range(matRow):
                matrix.append(file.readline().split())
                
            # Sequences
            totalSeq = int(file.readline())
            seq = {}
            for i in range(totalSeq):
                sequence = file.readline().replace(' ', '').replace('\n', '')
                seq[sequence] = int(file.readline())
                
        # Set variables
        self.MAX_BUFFER = bufferLength
        self.ROW = matRow
        self.COL = matCol
        
        self.grid = matrix
        self.seq = seq
        
        # Solve
        self.findMax()
        
    def randomize(self):
        slowprint('\nPlease provide the following parameters to aide the randomization process:\n')
        
        # Token amount
        tokenAmountValid = False
        
        while not tokenAmountValid:
            slowprint(colored('\nToken amount: ', 'green'))
            tokenAmount = input()
            
            try:
                tokenAmount = int(tokenAmount)
                if tokenAmount <= 0:
                    raise ValueError("Positive numbers only!")
                
                tokenAmountValid = True
            except:
                slowprint(colored('Invalid token amount!', 'red'))
                
        # Tokens
        tokensValid = False
        
        while not tokensValid:
            slowprint(colored('\nTokens (seperated by spaces ; each token consist of two characters): ', 'green'))
            tokens = input().split()
            
            if len(tokens) != tokenAmount:
                slowprint(colored('Invalid token amount!', 'red'))
            else:
                tokensValid = True
    
        # Buffer size
        bufferSizeValid = False
        
        while not bufferSizeValid:
            slowprint(colored('\nBuffer size: ', 'green'))
            bufferSize = input()
            
            try:
                bufferSize = int(bufferSize)
                
                if bufferSize <= 0:
                    raise ValueError("Positive numbers only!")
                
                bufferSizeValid = True
            except:
                slowprint(colored('Invalid buffer size!', 'red'))
                
        # Matrix size
        matrixSizeValid = False
        
        while not matrixSizeValid:
            slowprint(colored('\nMatrix size (cols rows): ', 'green'))
            matrixSize = input().split()
            
            if len(matrixSize) != 2:
                slowprint(colored('Invalid matrix size!', 'red'))
            else:
                try:
                    cols = int(matrixSize[0])
                    rows = int(matrixSize[1])
                    
                    if cols <= 0 or rows <= 0:
                        raise ValueError("Positive numbers only!")
                    
                    matrixSizeValid = True
                except:
                    slowprint(colored('Invalid matrix size!', 'red'))
                    
        # Sequence amount
        sequenceAmountValid = False
        
        while not sequenceAmountValid:
            slowprint(colored('\nSequence amount: ', 'green'))
            sequenceAmount = input()
            
            try:
                sequenceAmount = int(sequenceAmount)
                if sequenceAmount <= 0:
                    raise ValueError("Positive numbers only!")
                
                sequenceAmountValid = True
            except:
                slowprint(colored('Invalid sequence amount!', 'red'))
                
        # Max sequence length
        maxSequenceLengthValid = False
        
        while not maxSequenceLengthValid:
            slowprint(colored('\nMaximum sequence length (>= 2): ', 'green'))
            maxSequenceLength = input()
            
            try:
                maxSequenceLength = int(maxSequenceLength)
                if maxSequenceLength <= 1:
                    raise ValueError("Positive numbers only!")
                
                maxSequenceLengthValid = True
            except:
                slowprint(colored('Invalid maximum sequence length!', 'red'))
                
        # Generate matrix
        matrix = [[tokens[randint(0, tokenAmount - 1)] for j in range(cols)] for i in range(rows)]
        
        # Generate sequences
        seqs = {}
        for i in range(sequenceAmount):
            seqValid = False
            
            while not seqValid:
                seq = ''
                length = randint(2, maxSequenceLength)
                
                for j in range(length):
                    token = tokens[randint(0, tokenAmount - 1)]
                    seq += token
                    
                if seq not in seqs:
                    seqValid = True
                    
            points = randint(0, 50)
            seqs[seq] = points
            
        timestamp = str(datetime.now().time())[:8].replace(':', '_')
        self.filename = 'random_' + timestamp
        
        # Set variables
        self.grid = matrix
        self.seq = seqs
        
        self.ROW = rows
        self.COL = cols
        self.MAX_BUFFER = bufferSize
        
        # Show matrix and sequences
        slowprint(colored('\nGeneration finished!', 'green'))
        slowprint(colored('\nMatrix:\n', 'yellow'))
        for y in range(self.ROW):
            for x in range(self.COL):
                node = self.grid[y][x]
                print(node + ' ', end='')
                    
                sys.stdout.flush()
                sleep(0.001)
            sleep(0.01)
            print()
            
        slowprint(colored('\nSequences:', 'yellow'))
        for seq in self.seq:
            slowprint('\n' + str(self.formatSequence(seq)) + ': ' + str(self.seq[seq]))
            
        sleep(1)
            
        # Generate solve
        slowprint(colored('\n\nGenerating solve...', 'green'))
        self.findMax()
    
    def interface(self):
        slowprint('Welcome to ' + colored('Cyberpunk 2077 Breach Protocol!', 'green') + '\n')
        slowprint('Please choose your input method:\n\n')
        slowprint(colored('1. ', 'yellow') + 'Input from file\n')
        slowprint(colored('2. ', 'yellow') + 'Randomly generate puzzle\n')
        
        
        choiceValid = False
        while not choiceValid:
            slowprint('\nYour choice: ')
            choice = input()
            
            if choice == '1':
                choiceValid = True
                self.readFile()
            elif choice == '2':
                choiceValid = True
                self.randomize()
            else:
                slowprint('\nChoice not recognized!')
        
game = Game()
game.interface()