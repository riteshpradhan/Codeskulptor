########
# author: Ritesh Pradhan
# Codeskulptor project
# Blackjack
########


###
# Input arguments and flags:
# Ouput:
# Assumptions: 
#   1. 
# Known issues:
#   1.
###Helper functions:
# 0. main                   : Control the program's flow
# 1. show_message           : Shows message in bottom pane
#### Event Handlers:
# 1. click_deal             : The "Deal" button
# 2. click_hit              : The "Hit" button
# 3. click_stand            : The "Stand" button ...ain't it informative??
#### Classes:
#    Card:
#    Deck: A colletion of Cards.
#    Hand: Can be Dealer or Player
###
###Change History:
# DATE     PRG  REASON
############################################################################################
# 20130601 YM   First release
#
############################################################################################
import simplegui
import random
import math
#Global constants / variables
# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (73, 98)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
#
CARD_BACK_SIZE = (71, 96)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    
#
TOP_MARGIN=50
BOTTOM_MARGIN=50
RIGHT_MARGIN=50
LEFT_MARGIN=50
DRAW_AREA_WIDTH=400
DRAW_AREA_HEIGHT=300
#
CANVAS_HEIGHT=TOP_MARGIN+DRAW_AREA_HEIGHT+BOTTOM_MARGIN
CANVAS_WIDTH=LEFT_MARGIN+DRAW_AREA_WIDTH+RIGHT_MARGIN
#
CARD_AT_HAND=0
CARD_STATUS=1
################deck = []
deck = None
Player=None
Dealer=None
flgGameInProgress = False
outcome = ""
strMessage=""
# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
FACED_UP=1
FACED_DOWN=2
DEALER=1
PLAYER=2

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, side,rotation):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        if  ( side == FACED_UP ) :
            canvas.draw_image( card_images, 
                               card_loc, CARD_SIZE, 
                               [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE, float(rotation))
        else:  
            canvas.draw_image( card_back,  
                               [card_back.get_width()/2,card_back.get_height()/2], CARD_BACK_SIZE,
                               [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE, float(rotation))
        return
# define hand class
class Hand:
    def __init__(self, iPlayerType):
#########################################################################################################
#   Constructor
#########################################################################################################
        self.CardsList=[]
        self.iPlayerType = iPlayerType
        self.iScore=0
        if ( self.iPlayerType == PLAYER ):
            self.LIMIT = 21
        else:
            self.LIMIT=17
        return
###
    def __str__(self):
        strCards=""
        for eachCard in self.CardsList: 
            strCards=strCards + " " + str(eachCard[CARD_AT_HAND])
        return strCards
###
    def give_me_points(self, points):
#########################################################################################################
#
#########################################################################################################
        self.iScore+=int(points)
        return
###
    def show_hole_card(self):
#########################################################################################################
#
#########################################################################################################
        if (self.iPlayerType == DEALER and len(self.CardsList) >= 2 and self.CardsList[1][CARD_STATUS]==FACED_DOWN):
             self.CardsList[1][CARD_STATUS]=FACED_UP
             return True
        else:
            return False
###

    def add_card(self, card):
#########################################################################################################
#
#########################################################################################################
        if ( self.iPlayerType == DEALER and len(self.CardsList) == 1 ):
            self.CardsList.append([card, FACED_DOWN])
        else:
            self.CardsList.append([card, FACED_UP])
        return
###
    def give_cards_back(self):
#########################################################################################################
#
#########################################################################################################
        returnList=[]
        while (len(self.CardsList)>0):
              card=self.CardsList.pop()
              returnList.append(card[CARD_AT_HAND])
        return returnList
###
    def get_value(self):
#########################################################################################################
# count aces as 1,
#    if the hand has an ace,
#     then add 10 to hand value if don't bust
#########################################################################################################
        iTotalValue=0
        iAces=0
        for each_card in self.CardsList:
            if (each_card[CARD_STATUS] == FACED_UP ):
                iCardValue = VALUES[each_card[CARD_AT_HAND].rank]
                iTotalValue += iCardValue
                if (iCardValue == 1):
                    iAces += 1
                    iTotalValue += 10
#
        while ( self.iPlayerType == PLAYER and iAces > 0 and ( self.busted(iTotalValue)) ):
                iTotalValue -= 10
                iAces -=1
        return iTotalValue
###
    def busted(self,iTotalValue):
#########################################################################################################
#
#########################################################################################################
        if ( iTotalValue >= self.LIMIT ):
            return True
        else:
            return False
    
    def draw(self, canvas, position, angle):
#########################################################################################################
#
#########################################################################################################
        iCount = 0
        CardX=LEFT_MARGIN +position[0]
        for each_card in self.CardsList:
          CardY=position[1]+TOP_MARGIN+CARD_SIZE[1]*iCount*1/4
          each_card[CARD_AT_HAND].draw(canvas,[CardX,CardY],each_card[CARD_STATUS],float(angle))
          iCount += 1
        return
 
        
# define deck class
class Deck:
    def __init__(self):
#########################################################################################################
#   Constructor
#########################################################################################################
        self.CardsInTheDeck=[]
        for each_suit in SUITS:
            for each_card_name in RANKS:
                NewCard=Card(each_suit, each_card_name)
                self.CardsInTheDeck.append(NewCard)
        self.shuffle()
        return
###
    def shuffle(self):
#########################################################################################################
# 1. Add cards back to deck
# 2. Shuffle
#########################################################################################################
        random.shuffle(self.CardsInTheDeck)
        return
###
    def deal_card(self):
#########################################################################################################
# Remove one card from the deck
#########################################################################################################
        if (len(self.CardsInTheDeck) > 0) :
            return (self.CardsInTheDeck.pop())
        else:
            show_message(" Wooopse-doopsie...you finished the whole deck! End Of Game!")
        return None
###
    def collect_cards_from_players(self,cards):
#########################################################################################################
# Remove one card from the deck
#########################################################################################################
        while (len(cards)>0):
           self.CardsInTheDeck.append(cards.pop())
        return
###
    def __str__(self):
        strX=""
#       show_message("Number of cards in this deck: " + str(len(self.CardsInTheDeck)))
        for eachCard in self.CardsInTheDeck:
            strX = strX + eachCard.suit + eachCard.rank + " "
        return strX
#define helper functions
###
def show_message(message):
#########################################################################################################
##########################################################################################################
    global strMessage
    #print "Player:" + str(Player.get_value()) + ":" + str(Player) + ", Score:" + str(Player.iScore)
    #print "Dealer:" + str(Dealer.get_value()) + ":" + str(Dealer) + ", Score:" + str(Dealer.iScore)
    #print message
    strMessage=message
    return
#
#define callbacks for buttons
def click_deal():
#########################################################################################################
#1. Give two card to Player and dealer, alternatively
#2. Just do it once??
#########################################################################################################
    global outcome, flgGameInProgress
    if (flgGameInProgress == False):
        flgGameInProgress = True
        show_message("New game: Hit, Stand, or ask for another deal to loose!!")
        deck.collect_cards_from_players(Player.give_cards_back())
        deck.collect_cards_from_players(Dealer.give_cards_back())
        deck.shuffle()
#
        Player.add_card(deck.deal_card())
        Dealer.add_card(deck.deal_card())
        Player.add_card(deck.deal_card())
        Dealer.add_card(deck.deal_card())
###     show_message(deck)
    else: 
        Dealer. give_me_points(1)
        show_message ("Game interrupted midway - Player lost!")
        flgGameInProgress = False
        Dealer.show_hole_card()
#
    outcome = ""
    return
###
def click_hit():
#########################################################################################################
# if the hand is in play, hit the player
# if busted, assign an message to outcome, update flgGameInProgress and score
#########################################################################################################
    global flgGameInProgress, outcome
    show_message("The game is on: Hit, Stand, or ask for another deal to loose!!")
    if ( not flgGameInProgress):
      show_message( outcome + "Cannot hit, please deal again to start")
      return
#
    Player.add_card(deck.deal_card())
    #print "Player:" + str(Player.get_value()) + ",Cards:" + str(Player) 
    if Player.busted(Player.get_value()):
       show_message("O-Oh! Player lost!")
       flgGameInProgress = False
       Dealer.show_hole_card()
       outcome = "Dealer won. "
       Dealer. give_me_points(1)
    return
### 
def click_stand():
#########################################################################################################
# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
# assign a message to outcome, update flgGameInProgress and score
#########################################################################################################
   global flgGameInProgress, outcome
   if (not flgGameInProgress):
      show_message(outcome + "No stand please, please deal again!")
      return
#
   if Player.busted(Player.get_value()):
       show_message("Sorry mate, but you are already busted, please deal again!")
       return
   #print "Dealer:" + str(Dealer.get_value()) + ", Cards:" +  str (Dealer)
#   
   while( not Dealer.busted(Dealer.get_value())):
   ##if(True):
        Dealer.show_hole_card()
        if (Dealer.busted(Dealer.get_value())):
            show_message("Dealer busted! Player won!")
            flgGameInProgress = False
            outcome = "Dealer got busted!"
            Player. give_me_points(1)
            return

        Dealer.add_card(deck.deal_card())
        #print Dealer
        if (Dealer.busted(Dealer.get_value())):
            show_message("Sorry, Dealer Sir, this time you are busted!")
            flgGameInProgress = False
            outcome = "Dealer got busted!"
            Player. give_me_points(1)
            return
#
        if ( Player.get_value() <= Dealer.get_value()):
            show_message("Yey! Dealer wins!")
            flgGameInProgress = False
            outcome = "Dealer won the game. "
            Dealer.give_me_points(1)
            return
        else:
            show_message("Yey! Player wins!")
            flgGameInProgress = False
            outcome = "Player won the game. "
            Player.give_me_points(1)
            return
#
   return
###
def draw_main_canvas(canvas):
#########################################################################################################
#
#########################################################################################################
    canvas.draw_polygon([[0,0],[CANVAS_WIDTH,0],[CANVAS_WIDTH,TOP_MARGIN],[0,TOP_MARGIN]]
                        , 1, "Red","Grey")
    canvas.draw_polygon([[0,CANVAS_HEIGHT],[CANVAS_WIDTH,CANVAS_HEIGHT],[CANVAS_WIDTH,CANVAS_HEIGHT - BOTTOM_MARGIN],[0,CANVAS_HEIGHT - BOTTOM_MARGIN]]
                        , 1, "Red","Blue")
    canvas.draw_polygon([[0,TOP_MARGIN],[LEFT_MARGIN,TOP_MARGIN],[LEFT_MARGIN,CANVAS_HEIGHT-BOTTOM_MARGIN],[0,CANVAS_HEIGHT-BOTTOM_MARGIN]]
                        , 1, "Red","Maroon")
    canvas.draw_polygon([[CANVAS_WIDTH-RIGHT_MARGIN,TOP_MARGIN],[CANVAS_WIDTH,TOP_MARGIN],[CANVAS_WIDTH,CANVAS_HEIGHT - BOTTOM_MARGIN],[CANVAS_WIDTH-RIGHT_MARGIN,CANVAS_HEIGHT - BOTTOM_MARGIN]]
                        , 1, "Red","Maroon")
#
    canvas.draw_text("Blackjack!", [CANVAS_WIDTH/2-100, 30], 30, "#00ffff ","sans-serif")
    canvas.draw_text("Player:" + str(Player.iScore), [LEFT_MARGIN, TOP_MARGIN/2], 20, "#110000")
    canvas.draw_text("Dealer:" + str(Dealer.iScore), [CANVAS_WIDTH-2*RIGHT_MARGIN, TOP_MARGIN/2], 20, "#110000")
    canvas.draw_text(str(strMessage) ,[LEFT_MARGIN/2, CANVAS_HEIGHT-30], 18, "#FFDDEE", "sans-serif")
    if (Player.get_value() > 0 or Dealer.get_value()>0):    
        canvas.draw_text("[Dealer:" + str(Dealer.get_value()) + "/Player:" +str(Player.get_value()) +"]"  ,[2*LEFT_MARGIN+30, CANVAS_HEIGHT-10], 14, "#FFDDEE", "monospace")
#   
    canvas.draw_text("Dealer",[LEFT_MARGIN+CARD_SIZE[0]*0.75,TOP_MARGIN*1.5], 20, "#00ffff ","sans-serif")
    Dealer.draw(canvas,[LEFT_MARGIN, TOP_MARGIN],math.pi-0.5)
#    
    canvas.draw_text("Player",[LEFT_MARGIN+2.8*CARD_SIZE[0],TOP_MARGIN*1.5], 20, "#00ffff ","sans-serif")
    Player.draw(canvas,[LEFT_MARGIN+2*CARD_SIZE[0], TOP_MARGIN],0.5)
    return
def main():
############################################################################################
#Control the program-flow
#1. Create frame
#2. Add/register controls
#3. Start the frame
############################################################################################
# initialization frame
    global Player, Dealer, deck,strMessage
    strMessage=""
    frame = simplegui.create_frame("Blackjack", CANVAS_WIDTH, CANVAS_HEIGHT)
    frame.set_canvas_background("Green")

    #create buttons and canvas callback
    frame.add_button("Deal",    click_deal   , 200)
    frame.add_button("Hit",     click_hit    , 200)
    frame.add_button("Stand",   click_stand  , 200)
    frame.set_draw_handler(draw_main_canvas)

    # deal an initial hand
    deck=Deck()
    Player=Hand(PLAYER)
    Dealer=Hand(DEALER)

    #####show_message(deck)
    # get things rolling
    frame.start()
    click_deal()
###
###Finally - don't run if this program is 'imported''
if __name__ == "__main__":
     main()
#
###End Of Program