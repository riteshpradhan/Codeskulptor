########
# author: Ritesh Pradhan
# Codeskulptor project
# Memory-pic
########



###
# Input arguments and flags:
# Ouput:
# Assumptions: 
#   1. 
# Known issues:
#   1.
###Functions:
# 0. main                   : Control the program's flow
###Helper functions:
# 1. did_ball_touch_paddle  : Tells if ball has indeed hit a paddle
#### Event Handlers:
# 1.
###
###Change History:
# DATE    PRG  REASON
############################################################################################
# 20130522 YM   First release
#
############################################################################################
# Imported/external modules:
import simplegui
import random
###GlobalVariables
DRAW_AREA_WIDTH=500
DRAW_AREA_HEIGHT=500
#
CARDS_PER_ROW=4
CARDS_PER_COLUMN=4
FRAME_SIDE_AREA=30
FRAME_TOP_AREA=50
TOP_TEXT_AREA=50
#
FRAME_WIDTH=DRAW_AREA_WIDTH+FRAME_SIDE_AREA*2
FRAME_HEIGHT=DRAW_AREA_HEIGHT+FRAME_TOP_AREA + TOP_TEXT_AREA
#
CARD_HEIGHT=100
CARD_WIDTH=DRAW_AREA_WIDTH/CARDS_PER_COLUMN
HIDDEN=0
SHOWN=1
PREV=0
CURR=1
#
iMatchesFound=0
#
CardNumbers=[]
CardImagesLocation=[
 "http://upload.wikimedia.org/wikipedia/en/d/d4/Mickey_Mouse.png"
,"http://upload.wikimedia.org/wikipedia/en/6/67/Minnie_Mouse.png"
####,"http://upload.wikimedia.org/wikipedia/commons/a/a8/Donald_Duck_-_The_Spirit_of_%2743_%28cropped_version%29.jpg" ### You cannot see background in JPG-avoid
 ,"http://images.wikia.com/disney/images/6/6b/Donald_Duck_transparent.png"
,"http://upload.wikimedia.org/wikipedia/en/2/21/DaisyDuck.png"
,"http://images.wikia.com/epicmickey/images/1/17/Pluto_disneycharacter.png"
,"http://upload.wikimedia.org/wikipedia/en/a/a6/Goofy.svg"
,"http://images2.wikia.nocookie.net/__cb20060317230553/candh/images/e/e8/Calvin1.gif"
,"http://www.cooperativeindividualism.org/calvin-claims-earth.gif"
]
CardImages=[]

CardsExposed=[]
CardsPositions=[]
#
INVALID_VALUE=-99999
PreviousAndCurrentCard=[INVALID_VALUE,INVALID_VALUE]
WrongMatch=[INVALID_VALUE,INVALID_VALUE]
#
iClicks=-1
state=0  #0: Begin, 1: One card, 2: Two cards
GAME_BEGAN=0
ONE_CARD=1
TWO_CARDS=2
#
lblMoves=None
frmMemory=None
iTimerInterval=1000
iIncrement=1
iTime=-1
fGameIsOn=False
strMessage=""
#
###
def init():
############################################################################################
# helper function to initialize globals
############################################################################################
    global state, iClicks, fGameIsOn, strMessage, iTime, CardImages,iMatchesFound
    global CardsPositions, CardsExposed, CardNumbers, PreviousAndCurrentCard, WrongMatch
    state = GAME_BEGAN
    iClicks=0
    iTime=0
    iMatchesFound=0
    fGameIsOn=True
    strMessage=""
    PreviousAndCurrentCard=[INVALID_VALUE,INVALID_VALUE]
    WrongMatch=[INVALID_VALUE,INVALID_VALUE]
#
    CardImages=[]
    CardsPositions=[]
    CardsExposed=[]
    CardNumbers = range (1,9)
    CardNumbers = CardNumbers + range (1,9)
    random.shuffle(CardNumbers)
#
    for iCounter in range (0, len(CardImagesLocation)):
        CardImages.append(simplegui.load_image(CardImagesLocation[iCounter]))
    ####print "========================= N E W  G A M E ==========================================="
    for iCounter in range (0, 16):
        CardsPositions.append([FRAME_SIDE_AREA+(iCounter%CARDS_PER_COLUMN)*CARD_WIDTH,FRAME_TOP_AREA+TOP_TEXT_AREA+(iCounter//CARDS_PER_ROW)*CARD_HEIGHT])
        CardsExposed.append(HIDDEN)
        ####print  iCounter+1 , CardNumbers[iCounter], CardsPositions[iCounter]        
#####
    return
###     
def TheRectangle(LeftTop):
############################################################################################
# 
############################################################################################
    Rectangle=[]
    Rectangle.append( [LeftTop[0], LeftTop[1]] )
    Rectangle.append( [LeftTop[0] + CARD_WIDTH, LeftTop[1]] )
    Rectangle.append( [LeftTop[0] + CARD_WIDTH,LeftTop[1] + CARD_HEIGHT] )
    Rectangle.append( [LeftTop[0] , LeftTop[1] + CARD_HEIGHT] )
#
    return Rectangle    
###
def PointIsInsideBox(Point, Box):
############################################################################################
# 
############################################################################################
    if ( ( ( Point[0] > Box[0] ) and Point[0] < Box[0] + CARD_WIDTH )  
       and ( Point[1] > Box[1] ) and Point[1] < Box[1] + CARD_HEIGHT ):
        return True
    else: 
       return False
###     
def DrawImage(iNumber, Location, canvas):
############################################################################################
# 
############################################################################################
    iNumber=iNumber-1
    ImageHeight=CardImages[iNumber].get_height()
    ImageWidth=CardImages[iNumber].get_width()
    canvas.draw_image(  CardImages[iNumber],
                      ( ImageWidth/2, ImageHeight/2 ), (ImageWidth,ImageHeight), 
                      ( Location[0]+CARD_WIDTH/2, Location[1]+CARD_HEIGHT/2 ),(CARD_HEIGHT,CARD_WIDTH)
                    )
                       
#
    return;
###
def WhichCardWasClicked(MousePosition):
############################################################################################
# Returns the number of card which was clicked
############################################################################################
    iCardNumber=-1
    for iCounter in range (0, 16):
        if ( PointIsInsideBox(MousePosition, CardsPositions[iCounter])):
            iCardNumber=iCounter
            break
#
    return iCardNumber
###     
def HasGameFinished():
############################################################################################
# Returns the status of game T / F
############################################################################################
    for iCounter in range (0, len(CardsExposed) ):
        if ( CardsExposed[iCounter] == HIDDEN ):
            return False
#
    return True
###     

# define event handlers
def mouseclick(pos):
############################################################################################
# 1. Get which card was clicked upon
# 2. If invalid range (e.g. clicked on blank space, borders etc.) - ignore.
# 3. If already exposed card - ignore.
# 4. All'z well - show card
# 5. 
############################################################################################
    global state, iClicks, fGameIsOn, iMatchesFound
#
    iCurrentCard=WhichCardWasClicked(pos)
###    print "===========>>" + str(iCurrentCard) + " = = =" + str(PreviousAndCurrentCard)
#Validations:
    if ( iCurrentCard < 0 or iCurrentCard >= 16):
       return
    if ( iCurrentCard == PreviousAndCurrentCard[CURR] ):
        return
    if ( CardsExposed[iCurrentCard] == SHOWN):
       return
#
    if (fGameIsOn): 
        iClicks=iClicks + 1
###Update current / previsous card's track
    if (not CardsExposed[iCurrentCard] == SHOWN):
        PreviousAndCurrentCard[PREV]=PreviousAndCurrentCard[CURR]
        PreviousAndCurrentCard[CURR]=iCurrentCard
#
####Expose the current card
    CardsExposed[PreviousAndCurrentCard[CURR]]=SHOWN
    if state == GAME_BEGAN:
        state = ONE_CARD
    elif state == ONE_CARD:
        state = TWO_CARDS
        if (CardNumbers[PreviousAndCurrentCard[PREV]] == CardNumbers[PreviousAndCurrentCard[CURR]]):
            CardsExposed[PreviousAndCurrentCard[PREV]]=SHOWN
            iMatchesFound=iMatchesFound+1
###Nothing to hide...all went well!
            WrongMatch[PREV]=INVALID_VALUE
            WrongMatch[CURR]=INVALID_VALUE
        else:
            WrongMatch[PREV]=PreviousAndCurrentCard[PREV]
            WrongMatch[CURR]=PreviousAndCurrentCard[CURR]
#
        if ( HasGameFinished() ):
           fGameIsOn=False
    else:
        state = ONE_CARD
        if (not WrongMatch[PREV] == INVALID_VALUE ):
            CardsExposed[WrongMatch[PREV]]=HIDDEN
        if (not WrongMatch[CURR] == INVALID_VALUE ):
            CardsExposed[WrongMatch[CURR]]=HIDDEN

    return
###                         
def draw(canvas):
############################################################################################
# add game state logic here
############################################################################################
    global lblMoves, strMessage
    if (fGameIsOn): 
       strMessage = str(iTime) + " seconds, and " + str(iClicks) + " clicks, found " + str (iMatchesFound) + " of " + str(len(CardNumbers)/2) + "!"
    else:
       strMessage = "Wow! Solved in " + str(iTime) + " seconds, and " + str(iClicks) + " clicks!"
#
    canvas.draw_polygon([[FRAME_SIDE_AREA,10],[FRAME_WIDTH-FRAME_SIDE_AREA,10],[FRAME_WIDTH-FRAME_SIDE_AREA, TOP_TEXT_AREA],[FRAME_SIDE_AREA, TOP_TEXT_AREA]], 1, "Red","Yellow")
    canvas.draw_text("Memory Game", [150, 40], 40, "Blue")
    for iCounter in range (0, 16):
       canvas.draw_polygon(TheRectangle(CardsPositions[iCounter]), 1, "Blue","Green")
       if ( CardsExposed[iCounter]==SHOWN ):
           canvas.draw_text(str(CardNumbers[iCounter]),[CardsPositions[iCounter][0]+CARD_WIDTH/2,CardsPositions[iCounter][1]+CARD_HEIGHT/2],10, "Red")
           DrawImage(CardNumbers[iCounter],CardsPositions[iCounter],canvas)
#
    canvas.draw_text(strMessage, [100, CARDS_PER_COLUMN*CARD_HEIGHT + 2*FRAME_TOP_AREA + TOP_TEXT_AREA], 24, "White")
#
    if ( not lblMoves == None ): 
         lblMoves.set_text("Moves = " + str (iClicks))
    elif (not frmMemory == None):
         lblMoves=frmMemory.add_lable("Moves = " + str (iClicks))        
###
    return
###
def timer_tick():
############################################################################################
#
############################################################################################
    global iTime
    if (fGameIsOn):
        iTime = iTime + iIncrement

    return
###

def main():
############################################################################################
#Control the program-flow
#1. Create frame
#2. Add/register controls
#3. Start the frame
############################################################################################
    """main - control the program flow
    """
    global bPause, lblMoves
# initialize global variables
    init()
#
# create frame and add a button and labels
    frmMemory = simplegui.create_frame("Memory", FRAME_WIDTH, FRAME_HEIGHT)
    frmMemory.add_button("Restart", init)
    lblMoves = frmMemory.add_label("Moves=x")
    tTimer= simplegui.create_timer(iTimerInterval, timer_tick)
# register event handlers
    frmMemory.set_mouseclick_handler(mouseclick)
    frmMemory.set_draw_handler(draw)
# get things rolling
    tTimer.start()
    frmMemory.start()
###
###Finally - don't run if this program is 'imported''
if __name__ == "__main__":
     main()
#
###End Of Program