from random import shuffle

# global variables
all_ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
all_suits = ["♠", "♡", "♣", "♢"]
rank_order = {all_ranks[i]:i for i in range(len(all_ranks))}
   
    
class PlayingCard():
    '''represents a single card'''
    
    def __init__(self, rank, suit, facedown=True):
        '''init rank, suit, facedown, and color attributes'''
        self.rank = rank
        self.suit = suit
        self.facedown = facedown
        if suit in ["♠", "♣"]:
            self.color = "black"
        else:
            self.color = "red"
            
    def flip_faceup(self):
        '''set facedown to False'''
        self.facedown = False
        
    def flip_facedown(self):
        '''set facedown to True'''
        self.facedown = True
        
    def __repr__(self):
        '''print ? if facedown, else print card rank and suit'''
        if self.facedown:
            return "????"
        return f"{self.rank}{self.suit}"
    
    
class Deck():
    '''the deck of cards that is drawn from'''
    
    def __init__(self):
        '''init full deck if no argument passed in suit, len'''
        self.cards = []
        for s in all_suits:
            for r in all_ranks:
                self.cards.append(PlayingCard(r, s))
        self.shuffle_deck()
    
    def shuffle_deck(self):
        '''shuffle the deck using shuffle method'''
        shuffle(self.cards)
        
    def deal_card(self, card_count=1, flip=True):
        '''deal card from the "top" of the deck, which is index 0'''
        if card_count > len(self.cards):
            print(f"Cannot deal {card_count} cards. The deck only has {len(self.cards)} cards left!")
            return None
        else:
            dealt = self.cards[:card_count]
            # flip all dealt cards faceup if flip is True
            if flip == True:
                [card.flip_faceup() for card in dealt]
            self.cards = self.cards[card_count:]
            return dealt
    
    def top_off(self, cards):
        '''add cards to the "bottom" of the deck, which is the end of list'''
        for card in cards:
            card.flip_facedown()
            self.cards.append(card)
            
    def __repr__(self):
        '''print top card if not empty'''
        if len(self.cards) > 0:
            return self.cards[0].__repr__()
        return ""
        
    
class Cell():
    '''must fill all 4 cell in rank/suit order to win game'''
    
    def __init__(self):
        self.cards = []
        
    def move(self, rank, suit, destination):
        '''return boolean whether move was successful'''
        if len(self.cards) > 0:
            top = self.cards[-1]
            # check if target card matches top card
            if top.rank == rank and top.suit == suit and top.facedown == False and destination.accept(top):
                # add top card to destination, delete top card, flip new top card faceup just in case
                destination.cards += [top]
                self.cards = self.cards[:-1]
                top.flip_faceup()
                return True
        return False
    
    def accept(self, card):
        '''return boolean whether cell can accept card'''
        # cell is empty, needs to accept Ace first
        if len(self.cards) < 1:
            if card.rank == 'A':
                return True
            else:
                # we cannot accept any other card than Ace if cell empty
                return False
        # cell is not empty
        top = self.cards[-1]
        # check if target card can be placed on top of top card in cell
        if top.suit == card.suit and rank_order[top.rank] + 1 == rank_order[card.rank]:
            return True
        return False
    
    def __repr__(self):
        '''print top card if not empty'''
        if len(self.cards) > 0:
            return self.cards[-1].__repr__()
        return ""


class Column():
    '''must clear 7 columns to win game'''
    
    def __init__(self, cards):
        '''init cards and flip top one face up'''
        self.cards = cards
        self.cards[-1].flip_faceup()
        
    def move(self, rank, suit, destination):
        '''return boolean whether move was successful'''
        for i in range(len(self.cards)):
            c = self.cards[i]
            # check target card is faceup and is in column
            if not c.facedown and c.rank == rank and c.suit == suit:
                # check if destination accepts and destination type is not Cell, because cell cannot accept more than 1 card
                if destination.accept(c) and not (type(destination) == Cell and i < len(self.cards) - 1):
                    # move card(s) to destination, delete card(s) from column, flip top card faceup if not empty
                    destination.cards += self.cards[i:]
                    self.cards = self.cards[:i]
                    if len(self.cards) > 0:
                        self.cards[-1].flip_faceup()
                    return True
        return False
    
    def accept(self, card):
        '''return boolean whether column can accept card'''
        # column is empty, can accept a King
        if len(self.cards) < 1:
            if card.rank == 'K':
                return True
            else:
                # cannot accept any other card than King in empty column
                return False
        # column is not empty
        top = self.cards[-1]
        # check if target card is opposite color to top, and rank order
        if top.color != card.color and rank_order[top.rank] == rank_order[card.rank] + 1:
            return True
        return False
        
    def __repr__(self):
        '''print card(s) seperated by spaces (facedown will affect what cards appear as)'''
        ret = ""
        for s in [c.__repr__() for c in self.cards]:
            ret = ret + s + " "
        if ret == "":
            return "None"
        return ret[:-1]
        
    
class Solitaire():
    '''implement game mechanics'''
    
    def __init__(self):
        '''init num moves, cells, flipped (from deck), deck, columns'''
        self.moves = 0
        # initialize 4 empty cells, s1 through s4
        self.cells = [Cell() for i in range(4)]
        self.flipped = []
        self.deck = Deck()
        self.deck.shuffle_deck()
        # initialize 4 columns, c1 through c7
        self.columns = [Column(self.deck.deal_card(i+1, False)) for i in range(7)]
        self.play()
        
    def end(self):
        '''return boolean on whether win condition achieved'''
        # check if all cells are filled
        sum_cell = 0
        for cell in self.cells:
            sum_cell += len(cell.cards)
        if sum_cell == 52:
            # print end message
            print("***********************************************")
            print("*** CONGRATULATIONS! YOU HAVE WON THE GAME! ***")
            print("***********************************************")
            return True
        return False
    
    def play(self):
        '''function that runs the game until end condition'''
        # print start message
        print()
        print("*****************************")
        print("*** Let's play solitaire! ***")
        print("*****************************")
        
        # print start instructions
        print()
        print('Follow this link for the rules of Solitaire: https://www.ducksters.com/games/solitaire_rules.php')
        print('When prompted on what to do, you can type')
        print('1. quit, to quit the game.')
        print('2. draw, to draw a card from the Deck and place it in Flipped/')
        print('3. move rank suit destination, which would \nmove a card with {rank} of {suit} to the destination of choice (c1 through c7 or s1 through s4). For example, to move the Ace of Hearts to Foundation S1, you would type "move A H S1".')
        print()
        
        # keep track of translation from s1: cell[0] and c1: column[0], etc
        col_cel_dict = {'C{0}'.format(i+1):self.columns[i] for i in range(7)}
        for i in range(4):
            col_cel_dict['S{0}'.format(i+1)] = self.cells[i]
        translate_suit = {"S":"♠", "H":"♡", "C":"♣", "D":"♢"}

        # run game until end condition achieved
        while not self.end():
            # print game state
            print(self)
            user = input('What do you want to do? ').upper()
            print()
            
            # if user types quit, end game
            if 'QUIT' in user:
                break
                
            # if draw, deal one card from deck into flipped
            elif 'DRAW' in user:
                if len(self.flipped) < 1 and len(self.deck.cards) < 1:
                        print("No cards left to draw.")
                elif len(self.deck.cards) < 1:
                    self.deck.top_off(self.flipped)
                    self.flipped = []
                self.flipped += self.deck.deal_card()
                self.moves += 1
                
            # if move, iterate through flipped/cols/cells and call move(card, destination)
            elif 'MOVE' in user and len(user.split()) == 4:
                # parse user input
                user = user.split()
                rank = user[1]
                suit = user[2]
                dest_key = user[3]
                # early breaking condition
                move_success = False
                
                # error checking
                if (len(rank) == 1 or rank == '10') and len(suit) == 1 and len(dest_key) == 2 and rank in all_ranks \
                and suit in translate_suit.keys() and dest_key in col_cel_dict.keys():
                
                    # check top card of flipped
                    if len(self.flipped) > 0:
                        card = self.flipped[-1]
                        # check if card matches
                        if not card.facedown and card.rank == rank and card.suit == translate_suit[suit]:
                            # check if destination accepts card
                            if col_cel_dict[user[3]].accept(card):
                                # update break condition, add cards to destination, delete card from flipped
                                move_success = True
                                col_cel_dict[user[3]].cards += [card]
                                self.flipped = self.flipped[:-1]
                                self.moves += 1

                    # check column for card
                    if move_success == False:
                        for stack in self.columns:
                            # attempt move (will return False if card not found)
                            if stack.move(user[1], translate_suit[user[2]], col_cel_dict[user[3]]):
                                # update break condition
                                move_success = True
                                self.moves += 1
                                break

                    # check cell for card
                    if move_success == False:
                        for stack in self.cells:
                            # attempt move (will return False if card not found)
                            if stack.move(user[1], translate_suit[user[2]], col_cel_dict[user[3]]):
                                # update break condition
                                move_success = True
                                self.moves += 1
                                break

                    if move_success == False:
                        print('Invalid move: card was not found or cannot be moved to location.')
                
                else:
                    print('Invalid command: The format of move is "move rank suit destination".')
             
            else:
                print('Invalid command. \nExamples: quit, draw, move A C C4 (to move Ace of Clubs to Column 4)')
            print()
            
    
    def __repr__(self):
        '''print out UI'''
        # keep track if column has reached its last card. 1 signifies it reached its end, 2 signifies bottom of card has printed
        col_end_reached = {i:0 for i in range(7)}
        
        # print moves
        print(f"Moves: {self.moves}")
        
        # print deck and cells
        print("Deck  Flipped      S1    S2    S3    S4")
        print("╔════╗╔════╗     ╔════╗╔════╗╔════╗╔════╗")
        if len(self.flipped) > 0:
            print(f"║{self.deck.__repr__().center(4)}║║{self.flipped[-1].__repr__().center(4)}║     ", end="")
        else:
            print(f"║{self.deck.__repr__().center(4)}║║    ║     ", end="")
        print(f"║{self.cells[0].__repr__().center(4)}║║{self.cells[1].__repr__().center(4)}║║{self.cells[2].__repr__().center(4)}║║{self.cells[3].__repr__().center(4)}║")
        print("║    ║║    ║     ║    ║║    ║║    ║║    ║")
        print("╚════╝╚════╝     ╚════╝╚════╝╚════╝╚════╝")
        print()
        
        # print columns
        print("  C1    C2    C3    C4    C5    C6    C7")
        rows = max([len(self.columns[i].cards) for i in range(7)])+2
        for row in range(rows):
            for col in range(7):
                if len(self.columns[col].cards) > row and col_end_reached[col] == 0:
                    print("╔════╗", end="")
                elif col_end_reached[col] == 1:
                    print("║    ║", end="")
                else:
                    print("      ", end="")
            print()
            
            for col in range(7):
                if col_end_reached[col] == 1:
                    print("╚════╝", end="")
                    col_end_reached[col] += 1
                elif len(self.columns[col].cards) > row:
                    print(f"║{self.columns[col].cards[row].__repr__().center(4)}║", end="")
                    if len(self.columns[col].cards) == row + 1:
                        col_end_reached[col] += 1
                else:
                    print("      ", end="")
            print()

        return ''
    

Solitaire()