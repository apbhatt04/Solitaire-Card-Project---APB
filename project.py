    ###########################################################

    #  Computer Project #10

    #  Solitaire card game

    #  Use function to initialize solitaire data structures

    #  Use functions to change cards between data structures

    #  Use function to display the board

    #  Use function if winning state has been reached

    #  Parse and error check the string inputted

    #  Use function to execute commands

    #  Close program if prompted

    ###########################################################

from cards import Card, Deck

MENU ='''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
def initialize():
    '''This function initializes the game of Solitaire.
       parameters: Nothing
       returns: tableau: a list of 7 lists, with cards dealt to each column
       foundation: an empty list of 4 lists
       stock: a list of cards not added to tableau
       waste: a list of the top card from the stock'''

    player_deck = Deck()
    cards = Card()

    
    tableau = [[] for i in range(7)] #Create 7 columns
        
    for i in range(7): #Append a card to all columns
        tableau[i].append(player_deck.deal())
        
    for i in range(1, 7): 
        tableau[i].append(player_deck.deal())
    
    for i in range(2, 7):
        tableau[i].append(player_deck.deal())
        
    for i in range(3, 7):
        tableau[i].append(player_deck.deal())
    
    for i in range(4, 7):
        tableau[i].append(player_deck.deal())
        
    for i in range(5, 7):
        tableau[i].append(player_deck.deal())
        
    for i in range(6, 7):
        tableau[i].append(player_deck.deal())
        
    for i in tableau: #Flip the last card
        for values in i:
            values.flip_card()

    for i in tableau:
        last_card = i[-1]
        last_card.flip_card()

    foundation = [[] for i in range(4)] #Create a foundation for the four card classes

    stock = player_deck
    stock.shuffle()
    
    for i in range(1): #Return the last card in the stock to the waste
        waste = []
        card = player_deck.deal()
        waste.append(card)
        
    return tableau, stock, foundation, waste

    
def display(tableau, stock, foundation, waste):
    """ This function displays the 4 data structures created in initialize().
       parameters: tableau: a list of 7 lists, with cards dealt to each column
       foundation: an empty list of 4 lists
       stock: a list of cards not added to tableau
       waste: a list of the top card from the stock
       returns: Nothing
       """
    stock_top_card = "empty"
    found_top_cards = ["empty","empty","empty","empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1] 
    if len(stock):
        stock_top_card = "XX" #stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock","waste","foundation"))
    print("\t\t\t\t     ",end = '')
    for i in range(4):
        print(" {:5d} ".format(i+1),end = '')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), str(waste_top_card)), end = "")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end = "")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end = '')
    for i in range(7):
        print(" {:5d} ".format(i+1),end = '')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ",end = '')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end = '')
            except IndexError:
                print(" {:5s} ".format(''), end = '')
        print()
    print()
    

def stock_to_waste( stock, waste ):
    '''This function transfer a card from the stock to the waste, if valid.
       parameters: stock: a list of all cards not in the tableau nor the waste
       waste: a list of cards from the stock
       returns: Boolean: True if the move is valid, False otherwise'''

    player_deck = stock

    card = player_deck.deal()

    if card == None: #No card to append
        return False
    if card != None: 
        waste.append(card)
        return True
    
       
def waste_to_tableau( waste, tableau, t_num ):
    '''This function moves a card from the waste pile to the tableau, if valid.
       parameters: waste: a list of cards
       tableau: a list of lists containing cards in play
       t_num: an integer representing the column number in the tableau
       returns: Boolean: True if valid, False otherwise.'''

    waste_card = waste.pop(-1) #Last value in waste
    waste_rank = waste_card.rank()
    waste_suit = waste_card.suit()
    

    compare_list = tableau[t_num] #t_num list in tableau

    if compare_list != []:
        compare_card = compare_list[-1] #Returns last values in tableau list
        compare_rank = compare_card.rank()
        compare_suit = compare_card.suit()

    if compare_list == []:
        compare_rank = 14 #14 so that you can place a king card
        compare_suit = 14 #Can be anything

    suit_colors = 0 #Initalize color
    if waste_suit == 2 and compare_suit == 3 or waste_suit == 3 and compare_suit == 2:
        suit_colors == 0 #Red suits
    elif waste_suit == 1 and compare_suit == 4 or waste_suit == 4 and compare_suit == 1:
        suit_colors += 1 #Black suits
    else:
        suit_colors += 2 #Opposite color suits

    if waste_suit != compare_suit and suit_colors == 2 and waste_rank == compare_rank - 1: #If suit colors are opp. and card is 1 rank down..
        tableau[t_num].append(waste_card)
        return True
    else:
        waste.append(waste_card) #Put card back into waste
        return False

def waste_to_foundation( waste, foundation, f_num ):
    '''This function transfers a card from the waste to the foundation pile.
       parameters: waste: a list of cards
       foundation: a list of lists containing cards that are stacked in rank order
       f_num: an integer representing the index of the foundation list of lists
       returns: Boolean: True if valid, False otherwise.'''
    
    card = waste.pop(-1)
    rank = card.rank()
    suit = card.suit()

    compare_rank = 0 #Initialize values
    compare_suit = 0

    if foundation[f_num] != []:
        for values in foundation[f_num]:
            compare_rank = values.rank()
            compare_suit = values.suit()



    if rank == compare_rank + 1 and suit == compare_suit or rank == 1:
        foundation[f_num].append(card)
        return True
    else:
        waste.append(card)
        return False

def tableau_to_foundation( tableau, foundation, t_num, f_num ):
    '''This function transfers a card from the tableau to the foundation pile.
       parameters: tableau: a list of lists containing the cards in play.
       foundation: a list of lists containing cards stacked in rank order.
       t_num: an integer representing the index of the tableau list
       f_num: an integer representing the index of the foundation list
       returns: Boolean: True if valid, False if otherwise.'''

    card_list = tableau[t_num]
    card = card_list.pop(-1)

    suit = card.suit()
    rank = card.rank()

    foundation_list = foundation[f_num] 
    if foundation_list != []:
        compare = foundation_list[-1]
        compare_suit = compare.suit()
        compare_rank = compare.rank()
    elif foundation_list == []:
        compare_suit = suit
        compare_rank = 0

    if suit == compare_suit and rank == compare_rank + 1:
        foundation[f_num].append(card)
        if len(card_list) >= 1: #If the list is not empty...
            last_card = card_list[-1]
            if last_card.is_face_up() != True:
                last_card.flip_card()
        return True

    elif suit == compare_suit + 1 and rank == 1:
        foundation[f_num].append(card)
        if len(card_list) >= 1:
            last_card = card_list[-1]
            if last_card.is_face_up() != True:
                last_card.flip_card()
        return True
    else:
        tableau[t_num].append(card)
        return False

def tableau_to_tableau( tableau, t_num1, t_num2 ):
    '''This function transfer a card from 1 column in the tableau to another column
    parameters: tableau: a list of lists containing the cards in play
    t_num1: an integer representing the index of the source column in the tableau
    t_num2: an integer representing the index of the destination column in the tableau
    returns: Boolean: True if the move is valid, False if otherwise.'''

    card_list = tableau[t_num1]
    card = card_list.pop(-1)

    rank = card.rank()
    suit = card.suit()

    compare_card_list = tableau[t_num2]
    if compare_card_list != []:
        compare_card = compare_card_list[-1]
        compare_suit = compare_card.suit()
        compare_rank = compare_card.rank()
    elif compare_card_list == []: 
        compare_suit = suit #King of any suits can be appended
        compare_rank = 14 #14 so you can append a king card (rank 13)

    suit_colors = 0 #Initalize color
    if suit == 2 and compare_suit == 3 or suit == 3 and compare_suit == 2:
        suit_colors == 0 #Red suits
    elif suit == 1 and compare_suit == 4 or suit == 4 and compare_suit == 1:
        suit_colors += 1 #Black suits
    else:
        suit_colors += 2 #Opposite color suits

    if suit_colors == 2 and rank == compare_rank - 1:
        tableau[t_num2].append(card)
        if len(card_list) >= 1:
            last_card = card_list[-1]
            if last_card.is_face_up() != True:
                last_card.flip_card()
        return True
    else:
        card_list.append(card)
        return False

    
def check_win (stock, waste, foundation, tableau):
    '''This function checks if the game is in a winning state.
       parameters: stock: a list containing cards not in the tableau
       waste: a list of cards not in the tableau nor in the stock
       foundation: a list of lists containing cards stacked in rank order
       tableau: a list of lists containing cards in play
       returns: Boolean: True if game is in winning state, False if it is not.'''

    tableau_blank = [[] for i in range(7)]

    stock_len = len(stock)
    waste_len = len(waste)

    if stock_len == 0 and waste_len == 0 and tableau == tableau_blank: #Implicitly test if foundation list has all cards
        return True
    else:
        return False
    

def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the 
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game        
        '''
    option_list = in_str.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]
    
    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']
    
    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1] 
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str,dest]
                               
    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT','TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT','TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            #elif opt_str == 'MFT' and (source < 0 or source > 3):
                #print("Error in Source.")
                #return None
            # source values are valid
            # check for valid destination values
            if (opt_str =='TT' and (dest < 1 or dest > 7)) \
                or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str,source,dest]

    print("\nError in option:", in_str)
    return None   # none of the above


def main(): 
    print(MENU)  

    tableau, stock, foundation, waste = initialize()

    display(tableau, stock, foundation, waste)

    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

    
    while user_input != "Q" and user_input != "q":

       
        valid = parse_option(user_input)

        if valid == None: #Incorrect input
            display(tableau, stock, foundation, waste)
            user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

        if valid != None:
            if valid[0] == "SW" or valid[0] == "sw":
                sw = stock_to_waste(stock, waste)
                if sw == True:
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
                elif sw == False:
                    print("\nInvalid move!\n")
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

            if valid[0] == "WF" or valid[0] == "wf":
                f_num = valid[1] - 1
                wf = waste_to_foundation(waste, foundation, f_num)

                if wf == True:
                    if check_win(stock, waste, foundation, tableau) == True:
                        print("You won!")
                        display(tableau, stock, foundation, waste)
                    else:
                        display(tableau, stock, foundation, waste)
                        user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
                elif wf == False:
                    print("\nInvalid move!\n")
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

            
            if valid[0] == "WT" or valid[0] == "wt":
                t_num = valid[1] - 1
                wt = waste_to_tableau(waste, tableau, t_num)
                if wt == True:
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
                elif wt == False:
                    print("\nInvalid move!\n")
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")


            if valid[0] == "TF" or valid[0] == "tf":
                t_num = valid[1] - 1
                f_num = valid[2] - 1
                tf = tableau_to_foundation(tableau, foundation, t_num, f_num)
                if tf == True:
                    if check_win(stock, waste, foundation, tableau) == True:
                        print("You won!")
                        display(tableau, stock, foundation, waste)
                    else:
                        display(tableau, stock, foundation, waste)
                        user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
                elif tf == False:
                    print("\nInvalid move!\n")
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

            if valid[0] == "TT" or valid[0] == "tt":
                t_num1 = valid[1] - 1
                t_num2 = valid[2] - 1
                tt = tableau_to_tableau(tableau, t_num1, t_num2)
                if tt == True:
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
                elif tt == False:
                    print("\nInvalid move!\n")
                    display(tableau, stock, foundation, waste)
                    user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

        if user_input == "H": #Print options
            print(MENU)
            user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")

        if user_input == "R": #Display the board
            print(MENU) 
            tableau, stock, foundation, waste = initialize()
            display(tableau, stock, foundation, waste)
            user_input = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")


    
    

if __name__ == '__main__':
     main()
