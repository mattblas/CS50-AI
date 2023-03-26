import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        #TODO - DONE
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count:
            mines = self.cells
        return mines

    def known_safes(self):
        #TODO DONE
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe = set()
        if self.count == 0:
            safe = self.cells
        return safe

    def mark_mine(self, cell):
        #TODO DONE
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        
        The mark_mine function should first check to see if cell is one of the cells included in the sentence.
            
            > If cell is in the sentence, the function should update the sentence so that cell is no longer 
            in the sentence, but still represents a logically correct sentence given that cell is known
            to be a mine.
            
            > If cell is not in the sentence, then no action is necessary.
        """
        if cell in self.cells:
            print(f"before: {self.cells}, {self.count}, {cell}")
            self.cells.remove(cell)
            self.count = self.count - 1
            print(f"after {self.cells}, {self.count}")

    def mark_safe(self, cell):
        #TODO DONE
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.

        The mark_safe function should first check to see if cell is one of the cells included in the sentence.
            
            >If cell is in the sentence, the function should update the sentence so that cell is no longer in
            the sentence, but still represents a logically correct sentence given that cell is known to be safe.
            
            >If cell is not in the sentence, then no action is necessary.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = [Sentence(cells=((1,1), (2,1), (2,2)), count=3), #(1,1)
                          Sentence(cells=((1,1), (1,3), (2,1), (2,2), (2,3)), count=4)] #(1,2)


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
         DONE 1) mark the cell as a move that has been made
         DONE 2) mark the cell as safe
         DONE 3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
        
         DONE 4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
        TODO
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1 DONE
        self.moves_made.add(cell)

        #2 DONE
        self.mark_safe(cell)

        #3 DONE

        cells = set()
        neighbors = self.neighbors(cell)
        for cell in neighbors:
            if cell not in self.safes and cell not in self.mines:
                cells.add(cell)
        self.knowledge.append(Sentence(cells, count))
        
        #4 TODO - ...
        """
        4) mark any additional cells as safe or as mines
        if it can be concluded based on the AI's knowledge base
        
        """
        safes = list()
        mines = list()
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                for cell in sentence.cells:
                    mines.append(cell)
            elif sentence.count == 0:
                for cell in sentence.cells:
                    safes.append(cell)
        if mines:
            for _ in mines:
                self.mark_mine(_)

        if safes:
            for _ in safes:
                self.mark_safe(_)
      
        """
        5) add any new sentences to the AI's knowledge base
            if they can be inferred from existing knowledge

        Consider just the two sentences our AI would know based on the top middle cell
        and the bottom middle cell. From the top middle cell, we have 
        {A, B, C} = 1. 
        From the bottom middle cell, we have 
        {A, B, C, D, E} = 2.
        Logically, we could then 
        infer a new piece of knowledge, that 
        {D, E} = 1. 
        After all, if two of A, B, C, D, and E are mines,
        and only one of A, B, and C are mines, then it stands to reason that exactly one of D and E must 
        be the other mine.

        More generally, any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset 
        of set2, then we can construct the new sentence set2 - set1 = count2 - count1. Consider the example 
        above to ensure you understand why that's true.

        So using this method of representing knowledge, we can write an AI agent that can gather knowledge about
        the Minesweeper board, and hopefully select cells it knows to be safe!"""
    
    def print_knowledge(self):
        for sentence in self.knowledge:
            print(sentence)

    def make_safe_move(self):
        #TODO
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_move = ...
        return safe_move

    def make_random_move(self):
        #TODO - DONE
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            w = random.randrange(1, self.width+1)
            h = random.randrange(1, self.height+1)
            cell = (w,h)
            if cell not in self.moves_made and cell not in self.mines:
                return cell

    def neighbors(self, cell):
        neighbors = set()
        w, h = cell
        for i in range(max(w-1, 0), w+2):
            for j in range(h-1, h+2):
                if (i,j) != cell and 0 < i < self.width+1 and 0 < j < self.height+1:
                    neighbors.add((i,j))
        return(neighbors)


class Tests():
    def test():
        MinesweeperAI().add_knowledge(cell=(5,3), count=1)

Tests.test()
