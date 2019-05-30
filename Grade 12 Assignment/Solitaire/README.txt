This was my final project in my high school cs course.
We were asked to create a game using Python and Pygame, and I chose to recreate Solitaire.


--- How Solitaire Works ---
The game of solitaire starts with 7 columns with an increasing number of cards which are randomly distributed, and the rest of the cards are left in the deck to be flipped. There are 4 places for cards to be scored.
The goal of solitaire is to score all cards in a pile of other cards with the same suit. An ace must be the first card scored, and to score a card, the card must be one number higher than the top card of the pile.
To play solitaire, the images of the cards, card back, empty deck, background, mouse cursor, fireworks, as well as multiple sound files are needed.


--- Features I have included ---
If a card is right clicked and can be scored, it is instantly scored.
Cards are flipped and moved by left clicks. A card can be flipped in a column if it is the top card of the column. When a card is clicked, if it can be moved, it and all cards below it are moved. If they are placed on a column where the top card has a different suit and is one number higher than the top card of the cards being moved, they are added to the column. If it is placed on a scoring pile and it can be added, it is scored.
If the spacebar is pressed, the deck is flipped.
If backspace is pressed, the last move is undone. Consecutive undos without other moves in between are not allowed.


--- Features that could be added ---
I could add a feature of being able to choose between easy and hard difficulties. For hard, I would not allow cycling through the deck more than 3 times, and I would flip 3 cards at once and not allow undos. The hardest part about that would have been setting up the 3 cards being flipped, and if a card was moved away and then taken back, I would have to keep track of if it to ensure it goes back to exactly the right spot.
I had hoped to add another end animation involving moving the cards, but I would have to figure out a good animation.
The sound files were not very high quality. They are not instant and they are not all at equal volume levels.
A menu allowing a choice of difficulty, as well as an option to start a new game without closing the window would be the next step in improving the game. A feature that would keep track of numeric score could also be added.
