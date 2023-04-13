import requests
import json

#get_lists() is used to get all the lists in the board.
def get_lists():
    data = authentication.copy()
    #url to the lists in the board with id as boardID
    board_url = url + '/boards/' + authentication["boardID"] + '/lists'
    #initiates the http request for the board_url and gets the lists data
    response = requests.get(url = board_url, data = data)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print("Request Failure code:", response.status_code)

#Choose_list() is used to choose the list in which you want to add the newly created card.
def choose_list():
    available_lists = get_lists()
    print('Which list you would like to add the card created? Please select the list numebr from the below lists. \n')
    for i in range(len(available_lists)):
        print(f'{i}. {available_lists[i]["name"]}')

    #takes user input for the list to which the card belongs to  
    reply = int(input())
    if reply not in range(len(available_lists)):
        print('Please choose the list from the available lists only.\n')
        return choose_list()
    else:
        return available_lists[reply]["id"]

#choose_CardColor() is for selecting the label/color for new card.
def choose_CardColor():
    reply = input('What label would you prefer for this card? Please choose a number. \n1. To Do\n2. Doing\n3. Done\n4. Not Started\n')
    if reply == '1':
        return 'green'
    elif reply == '2':
        return 'red'
    elif reply == '3':
        return 'blue'
    elif reply == '4':
        return 'yellow'
    else:
        print('Please choose the labels from the defined lables only.\n')
        return choose_CardColor()

#add_comment() will add the comment to the card with id as card_id.
def add_comment(card_id):
    reply = input('Would you like to add a comment to the card (Y/N)?\n')
    if reply.lower() == 'y':
        comment_text = input('Enter the text for the comment:\n')
        data = authentication.copy()
        data['text'] = comment_text
        #url to the cards in the board with id as card_id.
        comment_url = url + "/cards/" + card_id + "/actions/comments"
        #initiates the request for the card_url and gets the card data
        response = requests.post(url = comment_url, data = data)
        if response.status_code == 200:
            print('Successfuly added the comment to the card.\n')
        else:
            print("Error response code: ", response.status_code)
    if reply.lower() == 'n':
        print('Card has been successfully added to the board.\n')
        return
    else:
        return add_comment(card_id)

#create_card() takes user input for the card parameters and creates a new card and appends it to the list specified by the user.
def create_card():
    data = authentication.copy()
    data['idList'] = choose_list()
    card_name = input('What would you like to call the card?\n')
    card_url = url + "/cards"
    data['name'] = card_name
    data['labels'] = [choose_CardColor()]
    response = requests.post(url = card_url, data = data)
    if response.status_code == 200:
        add_comment(json.loads(response.text)["id"])
    else:
        print(response.status_code)


# program starts here. Parameters for account authentication is mentioned here.
# key, token and boardid are unique for different users.

# url is for the trello API call
url = "https://api.trello.com/1/"
# Key would have the trello API key value
key = "67e4381f8240a8be04bc0c224c364555"
# token is a unique value which will grant access permissions to the trello account.
token = "ATTAed2cf41d0c80cc1f8d8598c691f8262615fc352dbd5f48a31bb75eb946120792AC48A057"
# boardid would be the unique id for the board to which user wants to add the cards.
boardid = "642e04b1d680935e2fa5156a"
authentication = {'key': key, 'token': token, 'boardID': boardid}

# function call starts here.
create_card()
