import os
import html

# Global variables
files = [] # Holds file names
games = [] # Holds all games
ranking = [] # Holds games within a category like [["Everyone", [game_1, game_2]], ["3 Friends", [game_3, game_4]]]
friends_counter = 0 # Counts how many files must be processed
friends_total = 0 # Number of files present in the working directory

# Get all 'steam'-files in the folder and store them to be examined (actually HTML files lol)
for x in os.listdir():
    if x.endswith(".steam"):
        files.append(x)
        friends_counter += 1

friends_total = friends_counter # Maximum amount of friends

# Parse all html files from the working directory
for file in files:

    html_file = open(file, "r", encoding='utf-8').read() # Read one file at a time into a string
    html_file = html.unescape(html_file) # Replace '&amp;' with '&' (unescape HTML characters)

    # Loop over every character in the current file serially
    for character in range(len(html_file)):

        # Next game starts where the HTML tag is 'gameListRowItemName ellipsis', however this is a non-solid solution because it would break the code if Steam decideds to change the HTML tag
        if html_file[character - len("gameListRowItemName ellipsis"):character] == "gameListRowItemName ellipsis":

            # Get name of the game
            game_name = html_file[character + 3:html_file.find("</div>",character)]

            # Add game to list
            games.append(game_name)

# Loop trough all games: First off, find games that everyone has, then friends - 1, friends - 2 etc.
while friends_counter != 0:

    inner_ranking = [] # will contain all games for a specific friend count

    # Examine the list containing all games for multiple occurances
    for game in games:

        # Check for games that match counter, like if everyone has a particular game or n - 1 etc.
        if games.count(game) == friends_counter:
            
            # Check if it is alreay in list
            if not game in inner_ranking:
                inner_ranking.append(game)

    column_title = "" # This will hold the title like "3 Friends"

    # Everyone has the game
    if friends_counter == friends_total:
        column_title = "Everyone"
    elif friends_counter == 1:
        column_title = "No Friend"
    else:
        column_title = str(friends_counter) + " Friends"

    ranking.append([(column_title),inner_ranking])
    friends_counter -= 1

output_string = "" # This will hold the .csv-formatted string which is then wrote to the output file

# Create .csv category names
for category_counter in range(len(ranking)):
    output_string += ranking[category_counter][0] + ";"

output_string = output_string[:-1] + "\n" # Remove the last ';' (.csv convention)

# Create .csv-formatted game list, loop over every single game
loop_counter = 0
while loop_counter < len(ranking[-1][1]):

    one_line = "" # Holds one .csv-line (elements are seperated with a ';' and a line break '\n' at the end)
    for category_counter in range(len(ranking)):
        
        # Check if there is a game; if yes, add the game name and ';', if there is no game because the category has already ended, only append ';'
        if loop_counter < len(ranking[category_counter][1]):
            one_line += ranking[category_counter][1][loop_counter]
        one_line += ";"
            
    one_line = one_line[:-1] + "\n" # Remove the last ';' (.csv convention)
    output_string += one_line
    loop_counter += 1

# Write to .csv-formatted file named 'common_games'. This can easily be imported into Excel
file = open("common_games.csv", "w", encoding='utf-8')
file.write(output_string)