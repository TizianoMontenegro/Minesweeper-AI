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
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
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
        self.knowledge = []

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
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark cell as one of the moves made
        self.moves_made.add(cell)

        # Mark cell as safe cell
        self.mark_safe(cell)

        # Add knowledge
        # Looping around the given cell
        # And adding the neighbors cell into a set
        cells_set = set()
        for row in range(cell[0]-1, cell[0]+2):
            for col in range(cell[1]-1, cell[1]+2):
                # If cell is into the limit cells of board 8x8
                if (row,col) != cell and 0 <= row < self.height and 0 <= col < self.width:
                    # If cell is not a clicked one, not neither a safe and a mine
                    if (row,col) not in self.moves_made and (row,col) not in self.safes and (row,col) not in self.mines:
                        cells_set.add((row,col))

                    # If cell is a mine susbtract one to the count because wo wont add it to the K.B.
                    elif (row,col) in self.mines:
                        count -= 1
        # Create a new Sentence
        new_sentence = Sentence(cells=cells_set, count=count)
        # Add that part of knowledge in the knowledge base
        self.knowledge.append(new_sentence)

        # # If a cell in cells is know to be mine or safe in a sentence, 
        # # Then mark that cell as mine or safe                                                        
        # for cell in cells_set:
        #     for sentence in self.knowledge:
        #         if sentence.known_mines():
        #             if cell in sentence.known_mines():
        #                 self.mark_mine(cell)

        #         if sentence.known_safes():
        #             if cell in sentence.known_safes():
        #                 self.mark_safe(cell)

        # # If cells_set is a subset of one sentence in ai knowledge
        # # Then infer new information from it and add it to the ai knowledge base
        # for sentence in self.knowledge:
        #     if cells_set.issubset(sentence.cells) and cells_set != sentence.cells:
        #         # Get the difference between both sets
        #         remaining_cells = sentence.cells.difference(cells_set)
                
        #         # Get the difference of counts
        #         remaining_count = sentence.count - count
                
        #         # If remaining_cells has cells
        #         if remaining_cells:
        #             # Create a new sentence with new knowledge
        #             new_sentence = Sentence(cells=remaining_cells, count=remaining_count)
                    
        #             # Add sentence if it's already not in the K.B.
        #             if new_sentence not in self.knowledge:
        #                 self.knowledge.append(new_sentence)

        while True:
            loop_stop = False

            # If a cell in sentence is known to be mine or safe in a sentence,
            # But it does not recognized as safe or mine cell 
            # Then mark that cell as mine or safe       
            for sentence in self.knowledge.copy():
                safe_cells = sentence.known_safes()
                if safe_cells:
                    for safe_cell in safe_cells.copy():
                        if safe_cell not in self.safes:
                            self.mark_safe(safe_cell)
                            loop_stop = True
                
                mine_cells = sentence.known_mines()
                if mine_cells:
                    for mine_cell in mine_cells.copy():
                        if mine_cell not in self.mines:
                            self.mark_mine(mine_cell)
                            loop_stop = True
                
            # If cells_set is a subset of one sentence in ai knowledge
            # Then infer new information from it and add it to the ai knowledge base
            for index1, sentence1 in enumerate(self.knowledge):
                for index2, sentence2 in enumerate(self.knowledge):
                    if index1 == index2:
                        continue

                    if sentence1.cells.issubset(sentence2.cells):
                        cells_based = sentence2.cells.difference(sentence1.cells)
                        count_based = sentence2.count - sentence1.count
                        
                        if len(cells_based) != 0:
                            sentence_based = Sentence(cells=cells_based, count=count_based)

                            if sentence_based not in self.knowledge:
                                self.knowledge.append(sentence_based)
                                loop_stop = True

            if not loop_stop:
                break


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_random_cells = []
        for row in range(self.width):
            for col in range(self.height):
                if (row,col) not in self.moves_made and (row,col) not in self.mines:
                    possible_random_cells.append((row,col))

        if len(possible_random_cells) == 0:
            return None
        else:
            random.shuffle(possible_random_cells)  
            return possible_random_cells[0]
