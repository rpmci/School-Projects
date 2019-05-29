#Reid McInroy
#ICS4U summative
#Mr. Foster
#June 6, 2016

#Solitaire

from random import *
import pygame
from pygame.locals import *
pygame.init()
pygame.mixer.init(44100, -16, 1, 1024)

class Card(pygame.sprite.Sprite):
    '''Models a Card. Contains a number and suit.'''
    def __init__(self, num, suit):
        '''Card(num, suit)
        Constructs a Card with the given number and suit.'''
        pygame.sprite.Sprite.__init__(self)
        self.__num = num
        self.__suit = suit
        self.image = pygame.image.load("Images/cardback.jpg").convert()
        self.rect = self.image.get_rect()
        if suit == "C" or suit == "S":
            self.__col = "B" #Black Card
        else:
            self.__col = "R" #Red Card
        self.__is_flipped = False #All cards start facedown
        
    def get_suit(self):
        '''C.get_suit() --> str
        Returns the suit of the Card.'''
        return self.__suit
    
    def get_col(self):
        '''C.get_col() --> str
        Returns the colour of the card.'''
        return self.__col
    
    def get_num(self):
        '''C.get_num() --> int
        Returns the number of the Card.'''
        return self.__num
    
    def is_flipped(self):
        '''C.is_flipped() --> bool
        Returns True if the Card has been flipped.'''
        return self.__is_flipped
    
    def flip(self):
        '''C.flip() --> None
        Flips the Card, changing between the card's back image and front image.'''
        if not self.__is_flipped:
            self.image = pygame.image.load("Images/{}{}.png".format(self.__suit, self.__num)).convert()
            self.__is_flipped = True
        else:
            self.image = pygame.image.load("Images/cardback.jpg").convert()
            self.__is_flipped = False

class Card_Stack(pygame.sprite.OrderedUpdates):
    '''Models a stack of Cards.'''
    def __init__(self):
        '''Card_Stack()
        Creates a stack to contain cards.'''
        pygame.sprite.OrderedUpdates.__init__(self)
        
    def get_top(self):
        '''C.get_top() --> Card
        If a card is contained, returns the top card.'''
        if len(self.sprites()) != 0:
            return self.sprites()[-1]
        
    def can_pick_up(self, card):
        '''C.can_pick_up(card) --> bool
        Returns True if the given card can be removed from the pile.'''
        if card in self.sprites():
            x = self.sprites().index(card)
            if x == len(self.sprites())-1 and card.is_flipped():
                return True
            else:
                if card.is_flipped() and self.sprites()[x+1].is_flipped():
                    return True
                else:
                    return False

    def stack(self, card): #problems while calling it "add()"
        '''C.stack(card) --> None
        Adds the given card(s) to the stack.'''
        pygame.sprite.OrderedUpdates.add(self, card)
        
    def lift_from(self, card):
        '''C.lift_from(card) --> Card
        if the Card is in the stack, it is returned.'''
        if card in self.sprites():
            return card
        
    def undo(self, last):
        '''C.undo(last) --> None
        Takes a tuple as an argument containing the last type of move,
        the column that card came from (itself), the column where cards went,
        and the list of cards moved.
        It moves the cards back to the earlier column.'''
        if last[0] == "cardflip":
            self.sprites()[-1].flip()
        elif last[0] == "score" or last[0] == "place":
            self.stack(last[3])
            last[2].remove(last[3])
            
class Column_Stack(Card_Stack):
    '''Models a column of cards in Solitaire'''
    def __init__(self, pos):
        '''Column_Stack(pos)
        Constructs a Column_Stack with a position 
        for reference to other Column_Stacks.'''
        Card_Stack.__init__(self)
        self.__pos = pos
        
    def get_pos(self):
        '''C.get_pos() --> int
        Returns the position of the Column_Stack'''
        return self.__pos
        
    def can_add(self, cards):
        '''C.can_add(cards) --> bool
        Takes list of cards, and checks if the Column_Stack
        can add those cards to itself, based on the number and
        colour of the top card.'''
        x = cards[0] #Only look at top card of a stack
        if x.is_flipped():
            if self.get_top() == None: #Empty pile
                if x.get_num() == 13: #Can only place king on empty
                    return True
                else:
                    return False
            elif self.get_top().get_col() != x.get_col() and \
                self.get_top().get_num() - 1 == x.get_num(): #Dif colour and one less in number
                return True
            else:
                return False
        
    def can_flip(self, card):
        '''C.can_flip(card) --> bool
        Returns True if the given card is the top card of
        the stack and it has not already been flipped.'''
        if card in self.sprites():
            if self.sprites()[-1] == card and not card.is_flipped():
                return True
        
    def stack(self, card): #problems while calling it "add()"
        '''C.stack(card) --> None
        Adds the given list of cards to the stack and assigns their position.'''
        Card_Stack.stack(self, card)
        for i in card:
            i.rect.topleft = (31 + 98*self.get_pos(), 161 + 30*(len(self.sprites()) - len(card) + card.index(i)))
            
    def take_back(self, cards):
        '''C.take_back(cards) --> None
        Reassigns the position of the given list of cards.
        Sets it back to its position in the column.'''
        for i in cards:
            i.rect.topleft = (31 + 98*self.get_pos(), 161 + 30*(len(self.sprites()) - len(cards) + cards.index(i)))
            
    def lift_from(self, card):
        '''C.lift_from(card) --> list
        Takes a list with one card as an argument.
        Returns a list containing the card 
        and any cards below it on the Stack.'''
        x = self.sprites().index(card)
        if x == len(self.sprites())-1: 
            return card
        else:
            temp = self.sprites()[x:]
            return temp

class Score_Stack(Card_Stack):
    '''Models a scoring pile in Solitaire'''
    def __init__(self, pos, suit):
        '''Score_Stack(pos, suit)
        Constructs a Score_Stack with a suit and a
        position for reference to other Column_Stacks.'''
        Card_Stack.__init__(self)
        self.__pos = pos
        self.__suit = suit
        
    def get_pos(self):
        '''S.get_pos() --> int
        Returns the position of the Score_Stack'''
        return self.__pos
    
    def can_add(self, cards):
        '''S.can_add(cards) --> bool
        Takes a list containing a single card as an argument.
        Returns True if the given card can be added.'''
        if len(cards) == 1:
            temp = cards[0]
            if temp.is_flipped():
                if self.get_top() != None: #If the pile contains a card
                    if self.get_top().get_num() + 1 == temp.get_num() and \
                       self.__suit == temp.get_suit():
                        return True
                    else:
                        return False
                else: #If it is an Ace
                    if temp.get_num() == 1 and temp.get_suit() == self.__suit:
                        return True
                    else:
                        return False
                
    def stack(self, cards): #problems while calling it "add()"
        '''S.stack(cards) --> None
        Takes a list containing a single Card as an argument.
        Adds the given card to the stack and assigns their position.'''
        Card_Stack.stack(self, cards)
        cards[0].rect.topleft = (324 + 98*self.get_pos(), 31)
        
    def take_back(self, card):
        '''S.take_back(card) --> None
        Takes a list containing a single Card as an argument.
        Reassigns the position of the given card.'''      
        card[0].rect.topleft = (324 + 98*self.get_pos(), 31)
        
    def is_full(self):
        '''S.is_full() --> bool
        Returns True if all cards of its suit are in the stack.''' 
        if self.get_top() != None:
            if self.get_top().get_num() == 13:
                return True

class Stack_Set(list):
    '''A set of all Card_Stacks in a game of Solitaire'''
    def __init__(self):
        '''Stack_Set() -> new empty list
        Stack_Set(iterable) -> new list initialized from iterable's items
        Constructs a list to contain all Card_Stacks'''
        list.__init__(self)
        
    def card_collide(self, xy):
        '''S.card_collide(xy) ==> tuple
        Goes through all Card_Stacks contained within itself and
        if there is a collision, it returns the top card colliding
        with the point xy and the Stack that contains it.'''
        colliding = None
        
        for i in self: #Check each Card_Stack
            if len(i.sprites()) != 0: #Avoid checking if there are no cards
                if len(i.sprites()) == 1: #Avoid loop if only one card is there
                    if i.sprites()[0].rect.collidepoint(xy):
                        colliding = (i, i.sprites()[0])
                else:
                    for s in range(len(i.sprites())): #Check each Sprite in that Card_Stack
                        if s + 1 == len(i.sprites()) and i.sprites()[s].rect.collidepoint(xy) or \
                            i.sprites()[s].rect.collidepoint(xy) and not i.sprites()[s+1].rect.collidepoint(xy):
                            colliding = (i, i.sprites()[s])
        return colliding
        
    def clear(self, surf, bgd):
        '''S.clear(surf, b) --> None
        Erases the previous position of all Cards in all Card_Stacks.'''
        for i in self:
            i.clear(surf, bgd)
            
    def draw(self, surf):
        '''S.draw(surf) --> None
        Draws all Cards in all Card_Stacks onto the surface.'''
        for i in self:
            i.draw(surf)
            
    def game_over(self):
        '''S.game_over() --> bool
        Returns True if all Score_Stacks are full'''
        x = True
        for i in self:
            if type(i) == Score_Stack:
                if not i.is_full(): #If any stack is not full, it is not over
                    x = False
        return x
                
class Hand(pygame.sprite.OrderedUpdates):
    '''Models a hand to hold a group of Card'''
    def __init__(self):
        '''Hand()
        Constructs a Hand that can contain Cards.
        Contains a variable to keep track of where 
        cards were lifted from.'''
        pygame.sprite.OrderedUpdates.__init__(self)
        self.__col_from = None #variable to keep track of where cards are from
        
    def is_empty(self):
        '''H.is_empty() --> bool
        Returns True if it contains no Cards.'''
        if len(self.sprites()) == 0:
            return True
        else:
            return False
        
    def pick_up(self, col_cards):
        '''H.pick_up(col_cards) --> None
        Takes a tuple giving a stack and cards to pick up,
        and adds those cards to itself. 
        Keeps track of what stack it came from.'''
        pygame.sprite.OrderedUpdates.add(self, col_cards[1])
        self.__col_from = col_cards[0]
        
    def get_col_from(self):
        '''H.get_col_from() --> Card_Stack
        Returns the Card_Stack that the most recent Cards came from.'''
        return self.__col_from
    
    def move(self, xy):
        '''H.move(xy) --> None
        Sets the position of all Cards being held based on the given coordinates.'''
        for i in range(len(self.sprites())):
            self.sprites()[i].rect.center = (xy[0], 35+xy[1]+30*i)
    
class Deck_Stack(Card_Stack):
    '''Models the Deck and pile of flipped cards in a game of Solitaire'''
    def __init__(self, cards):
        '''Deck_Stack(cards)
        Constructs a deck with the given list of Cards.
        Constructs and adds a sprite for when the deck is empty.
        Contains a list of flipped and unflipped cards.'''
        Card_Stack.__init__(self)
        for i in cards:
            i.rect.topleft = (31, 31)
        self.__empty = pygame.sprite.Sprite() #Sprite for collisions with no cards left
        self.__empty.image = pygame.image.load("Images/greencard.png").convert()
        self.__empty.rect = pygame.rect.Rect(31, 31, 73, 98)
        self.add(self.__empty) #Set the empty deck sprite as the first so it's at the bottom
        self.add(cards)
        cards.insert(0, self.__empty) #Add it to the front of the list
        self.__unturned = cards
        self.__turned = []
    
    def is_empty(self):
        '''D.is_empty() --> bool
        Returns True if there are no unturned cards left in the Deck.'''
        if len(self.__unturned) == 1: #If only sprite left is self.__empty
            return True
        
    def turn(self):
        '''D.turn() --> None
        Flips the top card and places it face up on the turned pile.
        If the deck is empty, it returns all cards from the turned pile
        back to the deck and sets them face down.'''
        if not self.is_empty(): #If there is a card left
            self.__unturned[1].rect.topleft = (129, 31) #At 1 because of empty deck sprite
            self.__unturned[1].flip()
            self.__turned.append(self.__unturned.pop(1)) #Move it from unturned to turned
            
        else: #Flipped cards go back into deck     
            for i in range(len(self.__turned)):
                self.__turned[i].rect.topleft = (31, 31)
                self.__turned[i].flip()
                self.__unturned.append(self.__turned[i])
            self.__turned = []
                
    def can_pick_up(self, card):
        '''D.can_pick_up(card) --> bool
        Returns True if the given card is in the turned pile and can be picked up.'''
        if len(self.__turned) != 0:
            if card in self.__turned:
                return True
    
    def take_back(self, card):
        '''D.take_back(card) --> None
        Takes a list containing a single card as an argument.
        Reassigns the position of the card.
        Sets it back to the position of the turned pile.'''
        if card[0] in self.__unturned:
            card[0].rect.topleft = (31, 31)
        else:
            card[0].rect.topleft = (129, 31)
            
    def remove(self, card):
        '''D.remove(card) --> None
        Takes a list of containing a single card as an argument.
        Removes the card from the deck.'''
        if type(card) == list:
            temp = card[0]
        else:
            temp = card
        Card_Stack.remove(self, temp) #Remove from Card_stack
        self.__turned.remove(temp) #Remove from list keeping track of cards
    
    def undo(self, last):
        '''D.undo(last) --> None
        Takes a tuple as an argument containing the last type of move,
        the set that card came from (itself), the column where cards went,
        and the list of cards moved.
        It moves the cards back to the earlier column.'''
        if last[0] == "deckflip":
            if len(self.__turned) == 0 and not self.is_empty():
                while not self.is_empty():
                    self.turn()
            else:
                self.__unturned.insert(1, self.__turned.pop(-1))
                self.__unturned[1].flip()
                self.take_back([self.__unturned[1]])
        elif last[0] == "place" or last[0] == "score":
            last[2].remove(last[3])
            self.empty() #Remove all sprites
            self.__turned += last[3] #Insert moved cards
            new_sprites = self.__unturned[:1] + self.__turned + self.__unturned[1:]
            self.add(new_sprites) #Add them back in order
            self.take_back(last[3])
        
class Fireworks(pygame.sprite.Sprite):
    '''Models fireworks'''
    def __init__(self):
        '''Fireworks()
        Constructs a sprite that represents fireworks.
        There are multiple images for the different stages.
        It is assigned a random starting image and random starting position.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        for i in range(8):
            temp_image = pygame.image.load("Images/firework_red{}.png".format(i)).convert_alpha()
            self.images.append(temp_image)
            
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = randint(0, screen.get_width()) #Random position
        self.rect.top = randint(0, screen.get_height())
        self.counter = randint(0, 16) #Start at a random image
        
    def update(self):
        '''F.update() --> None
        Cycles through the images.
        If the cycle has been completed, it is moved to a random place.'''
        if self.counter % 4 == 0:
            if self.counter == 32:
                self.counter = 0
                self.rect.left = randint(0, screen.get_width())
                self.rect.top = randint(0, screen.get_height())          
    
            else:
                self.counter += 1
                self.image = self.images[(self.counter//4)%len(self.images)]
        else:
            self.counter += 1
            
class Cursor(pygame.sprite.Sprite):
    '''Models a hand cursor that can be open or closed'''
    def __init__(self):
        '''Cursor()
        Constructs a cursor sprite. It has an open and closed image.'''
        pygame.sprite.Sprite.__init__(self)
        self.__open = True
        self.image = pygame.image.load("Images/openhand.png").convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()

    def update(self, xy, down):
        '''C.update() --> None
        Takes a coordinate and sets it as the center of the cursor.
        Takes an argument that states if the mouse is being pressed,
        and changes the image accordingly.'''
        self.rect.center = xy
        if down == 1 and self.__open == True or down == 0 and self.__open == False:
            if self.__open == True:
                self.image = pygame.image.load("Images/closedhand.png").convert()
                self.image.set_colorkey(self.image.get_at((0,0)))
                self.__open = False
            else:
                self.image = pygame.image.load("Images/openhand.png").convert()
                self.image.set_colorkey(self.image.get_at((0,0)))            
                self.__open = True
            
        
#Pygame setup
clock = pygame.time.Clock()
size = (725, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Solitaire")
bg = pygame.image.load("Images/Background.png").convert()

#Putting together the deck
ordered_deck = []
deck = []
suits = ["D","C","H","S"]

for x in range(1, 14):
    for y in range(4):
        ordered_deck.append(Card(x, suits[y]))
        
while len(ordered_deck) != 0:
    a = randrange(len(ordered_deck))
    deck.append(ordered_deck.pop(a))
    #ordered_deck.pop(a)

columns = [] #Column rects for detecting collisions
allcard = Stack_Set()
for i in range(7): #Setting up Columns, Column_Stacks
    columns.append(pygame.rect.Rect(66+98*i, 178, 3, 540))
    allcard.append(Column_Stack(i))
    for x in range(i+1): #Add number of cards based on what column it is
        allcard[i].stack([deck[0]]) #Methods take list of the single card
        deck.pop(0)
    allcard[-1].sprites()[-1].flip() #Flip last card of each Column_Stack
for i in range(4): #Setting up Score_Stacks
    allcard.append(Score_Stack(i, suits[i]))
    columns.append(pygame.rect.Rect(360+98*i, 31, 3, 49))
allcard.append(Deck_Stack(deck)) #The rest of the cards are the deck

hand = Hand()

#Sound Files
flip = pygame.mixer.Sound("Sounds/soundflip.wav")
pickup = pygame.mixer.Sound("Sounds/soundpickup.wav")
dropoff = pygame.mixer.Sound("Sounds/soundplace.wav")
no = pygame.mixer.Sound("Sounds/soundno.wav")
applause = pygame.mixer.Sound("Sounds/soundapplause.wav")
undo = pygame.mixer.Sound("Sounds/soundundo.wav")

last_move = None

#Endgame extras
font = pygame.font.SysFont("arial", 80)
endlabel = font.render("YOU WIN!", True, (165, 53, 198))

win = False
fire = pygame.sprite.Group()
for i in range(10):
    fire.add(Fireworks())

#Mouse cursor
cursor = Cursor()
cur = pygame.sprite.Group(cursor)

keep_going = True
while keep_going:
    clock.tick(45)
    for ev in pygame.event.get():
        if ev.type == QUIT: #Close the window
            keep_going = False
            
        elif ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                c = allcard.card_collide(ev.pos)
                if c!= None:
                    if c[0].can_pick_up(c[1]):
                        hand.pick_up((c[0], c[0].lift_from(c[1])))
                        pickup.play()
                        hand.move(ev.pos)
                    elif type(c[0]) == Deck_Stack: #If deck was clicked
                        c[0].turn()
                        flip.play()
                        last_move = ("deckflip", c[0])
                    else:
                        if c[0].can_flip(c[1]): #Flip top card in a column
                            c[1].flip()
                            flip.play()
                            last_move = ("cardflip", c[0])
            elif ev.button == 3: #Direct scoring if possible
                c = allcard.card_collide(ev.pos)
                if c!= None:
                    if type(c[1]) == Card: #If it is not the empty deck sprite
                        if type(c[0]) == Column_Stack and c[0].sprites()[-1] == c[1] \
                           and allcard[suits.index(c[1].get_suit()) + 7].can_add([c[1]]) \
                           or type(c[0]) != Column_Stack: #IF the card is in a stack, it must be the top card
                            if allcard[suits.index(c[1].get_suit()) + 7].can_add([c[1]]):
                                c[0].remove(c[1])
                                allcard[suits.index(c[1].get_suit()) + 7].stack([c[1]])
                                flip.play()
                                last_move = ("score", c[0], allcard[suits.index(c[1].get_suit()) + 7], [c[1]])
                
        elif ev.type == MOUSEBUTTONUP:
            if ev.button == 1 and not hand.is_empty(): #Left mouse button and cards are being held
                x = hand.sprites()[0].rect.collidelistall(columns)
                if x!= []:
                    x = x[0]
                    if allcard[x].can_add(hand.sprites()): #Add them to the stack
                        last_move = ("place", hand.get_col_from(), allcard[x], hand.sprites())
                        allcard[x].stack(hand.sprites())
                        hand.get_col_from().remove(hand.sprites())
                        hand.empty()
                        dropoff.play()
                    else: #Can't add them to the stack -> Return them to their stack
                        hand.get_col_from().take_back(hand.sprites())
                        hand.empty()
                        no.play()
                else: #No collision -> Return them to their stack
                    hand.get_col_from().take_back(hand.sprites())
                    hand.empty()
                    no.play()
                        
        elif ev.type == MOUSEMOTION:
            mousepos = ev.pos #Used for the cursor
            if pygame.mouse.get_pressed()[0] == 1: #If cards are being held, move them
                hand.move(ev.pos)
                
        elif ev.type == KEYDOWN: #Flip the deck
            if ev.key == K_SPACE:
                allcard[-1].turn()
                flip.play()
                last_move = ("deckflip", allcard[-1])
            elif ev.key == K_BACKSPACE:
                if last_move != None:
                    undo.play()
                    last_move[1].undo(last_move)
                    last_move = None #Only allow a single undo
                else:
                    no.play()
                
    screen.blit(bg, (0, 0))
    
    allcard.clear(screen, bg)
    allcard.draw(screen)
    hand.clear(screen, bg)
    hand.draw(screen)
    cur.update(mousepos, pygame.mouse.get_pressed()[0])
    cur.draw(screen)    

    if allcard.game_over() == True and win != True: #Will only occur once
        win = True
        applause.play()
        
    if win == True: #Keep the "You Win" and fireworks there even if cards are moved from the score stacks
        screen.blit(endlabel, (362 - endlabel.get_rect()[2]/2, 350 - endlabel.get_rect()[3]/2))
        fire.update()
        fire.draw(screen)
       
    pygame.display.flip()