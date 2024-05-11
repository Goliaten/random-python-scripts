from os import name as os_name, system as os_system
from shutil import get_terminal_size
from copy import deepcopy

def pause():
    input("Click enter to continue...")

def clear():              #used to clear terminal/shell screen
    if os_name == 'nt':           #on windows
        os_system('cls')
    else:                #on linux/macOS  (Posix)
        os_system('clear')

def lengthen(string, length=1, opt=0, char=' '):
    string = str(string)
    optimalIndentLeft = int(len(string) + (length - len(string)) / 2)
    
    while len(string) < length:
        if opt == 0:     #makes text go to the left
            string += char
        elif opt == 1:  #makes text go to middle
            if len(string) < optimalIndentLeft:
                string = char + string
            else:
                string += char
        elif opt == 2:   #makes text go to the right 
            string = char + string
            
    return string


def menu_print(menuMain, menuSecond=[], menuIndex=1, verticalPosition=0, horizontalPosition=0, columns=1):
    
    clear()
    MAX_WIDTH, LENGTH = get_terminal_size((80, 24))
    LENGTH -= 1 + len(menuSecond)      #making space for input/pause and seond menu
    
    #--------------some-failsafes-----------------
    if columns < 1:
        columns = 1
    elif columns > MAX_WIDTH:
        columns = MAX_WIDTH
    if verticalPosition not in range(0, 3):
        verticalPosition = 0
    if horizontalPosition not in range(0, 3):
        horizontalPosition = 0
    
    
    WIDTH = int(MAX_WIDTH / columns)
    
    
    #---------------------line-breaker----------------------------
    #checking if line is wider than screen
    for enum, line in enumerate(menuMain):
        
        if len(line) > WIDTH:
            for index in range(WIDTH, -1, -1):      #spliting line
                char = line[index]
                if char == " ":      #looking for closest space from the (length) character to first (i.e. looking for ' ' for nice split)
                    separator = index + 1      #if separator is at 0 index, infinite loop wil be created
                    break
            else:                    #or taking the (width) bit
                separator = WIDTH
            
            part1 = line[:separator].strip()   #separating line
            part2 = line[separator:]
            menuMain[enum] = part1                #and adding it to menu  (part1 to place on old line)
            menuMain.insert(enum+1, part2)       #(part 2 to next line)
    
    
    #-------------additional-footer-creator----------------
    #if menuMain is longer than length of terminal, reduces length and adds line of information
    pageFooter = []
    if len(menuMain) > LENGTH:
        LENGTH -= 1 #reducing length, so page footer can fit
        
        pageFooter.append('[back][next]')
        while len(pageFooter[0]) < MAX_WIDTH:           #insterting spaces so that [back] and [next] are on opposite side of screen
            pageFooter[0] = pageFooter[0][:6] + ' ' + pageFooter[0][6:]
    
    
    #--------------new-menu-creator------------------
    #adds new menu page each time the amount of lines in menu is bigger than length
    menus = {
        "menu1": deepcopy(menuMain)
    }
    
    if len(menus["menu1"]) > LENGTH:
        for x in range( 0, int( len(menus["menu1"]) / LENGTH) ):
            newKey = "menu" + str(x + 2)
            menus[newKey] = []
    
    
    #-----------------------menu-organiser---------------------
    #moves excess lines to next menu
    for enum, key in enumerate(menus, 1):
        next_key = key[:4] + str(enum + 1)      #choosing next key in dictionary
        while len(menus[key]) > LENGTH:         #moving lines untill len(menu) fits in length
            menus[next_key].append(menus[key][LENGTH])
                
            del menus[key][LENGTH]     #deleting excess line from old key
    
    
    #---------page-normaliser---------------------
    #makes sure m isn't bigger than number of menus
    if menuIndex > len(menus):
        menuIndex = len(menus)        #maximal m
    elif menuIndex <= 0:
        menuIndex = 1            #minimal m
        
    menu = menus[f"menu{menuIndex}"]
    
    
    #------------------- menu-extender---------------------------
    #extends menu until it is long enough to fill entire screen
    if verticalPosition == 0:   #top position
        while len(menu) < LENGTH: 
            menu.append("")
            
    elif verticalPosition == 1:   #middle position
        optimalIndex = int( len(menu) +  (LENGTH - len(menu)) / 2 )
        while len(menu) < optimalIndex: 
            menu.insert(0, "")
        while len(menu) < LENGTH: 
            menu.append("")
        
    elif verticalPosition == 2:   #bottom position
        while len(menu) < LENGTH: 
            menu.insert(0, "")
    
    menu += pageFooter + menuSecond
    
    
    #----------------additional-column-menus-----------------------
    #if there are more than 1 columns( range(1,1) does not return anything) then
    #add menus that will be displayed side by side in separate columns
    menuColumns = []
    for x in range(1, columns):
        newKey = f"menu{x+menuIndex}"
        if newKey in menus.keys():
            menuColumns.append( menus[newKey] )
    
    
    #---------------menu-aligner/printer--------------------
    #aligns vertically line and prints it
    for enum, line in enumerate(menu):
        
        lineColumns = []                   #gathering additional columns for current row
        for menuColumn in menuColumns:     #if menuColumns is empty, this will be ommited
            if enum < len(menuColumn):
                lineColumns.append(menuColumn[enum])
        
        if horizontalPosition == 0:                  #left position
            line = lengthen(line, WIDTH, 0)
            for lineColumn in lineColumns:
                line += lengthen(lineColumn, WIDTH, 0)
            
        elif horizontalPosition == 1:                #middle position
            line = lengthen(line, WIDTH, 1)
            for lineColumn in lineColumns:
                line += lengthen(lineColumn, WIDTH, 1)
            
        elif horizontalPosition == 2:                #right position
            line = lengthen(line, WIDTH, 2)
            for lineColumn in lineColumns:
                line += lengthen(lineColumn, WIDTH, 2)
            
        print(line)
    
    return menuIndex

def input_error_check(inputted, menuIndex, lengthMin, lengthMax, disableWrongInputCheck=False):
    #checks, if inputted is: string, in range of lengthMin and lengthMax, "ex", "next" or "back" in inputted
    #also manages setting menuIndex to 1 once errorCode for loop break/all good was set
    
    
    try:
        inputted = int(inputted)
        
    except: 
        if inputted == "ex":   #2 - loop break (exit or go back)
            menuIndex = 1
            errorCode = 2
            
        elif inputted == "back":    #3 - previous page
            menuIndex -= 1
            errorCode = 3             #There is no real need to return error code 3 and 4 But they
                                      #may be used in the future, and I am returning codes either way.
        elif inputted == "next":    #4 - next page
            menuIndex += 1
            errorCode = 4
            
        else:
            if disableWrongInputCheck == False:
                menu_print(["Wrong input"], [], 1, 2)
                pause()
            errorCode = 1     #1 - loop continue (wrong input)
            
    else: 
        if not (lengthMin <= inputted <= lengthMax):
            if disableWrongInputCheck == False:
                menu_print(["Choice out of allowed range"], [], 1, 2)
                pause()
            errorCode = 1     #1 - loop continue (wrong input)
        else: 
            menuIndex = 1
            errorCode = 0     #0 - all is good
    
    
    return inputted, errorCode, menuIndex


tuple_with_menus = (
    (
        0,                              # id
        "1\\0th menu",   # main menu text "{height},{width}\\{text}" or "{height width}\\{text}"
        "Possible nodes:",           # second menu text
        "Choose: ",                   # input label // text that's right before input() // write "" for ": " label
        "1\\Go to menu 1\\",   # option to select "{link}\\{text}\\{condition}"
        "2\\Go to menu 2\\",
    ),
    (
        1,
        "1\\2\\Welcome to menu 1",
        "",
        "",
        "null",
    ),
    (
        1,
        "2\\1\\Welcome to menu 2",
        "",
        "",
        "null",
    ),
)



# nople - collection of nodes or node tuple
# node - a 

DEFAULT_INPUT_LABEL = ": "


# what if there is only 1 option to choose from?
# what if that sole option is just "click to continue"?
#this function does not have menuIndex option from menu_print enabled
def use_node(node):
    
    #unpack values of the node
    id = node[0]
    *mainMenuOptions, menuMain = node[1].split("\\")
    menuMain = [menuMain]
    secondMenuText = node[2]
    inputLabel = node[3] if node[3] else DEFAULT_INPUT_LABEL
    optionSelect = []
    
    
    for x in node[4:]:
        x = x.split("\\")
        optionSelect.append(x)
    
    print(optionSelect)
    
    #make secondary menu
    menuSecond = [secondMenuText]
    if optionSelect:
        if optionSelect[0][0] != "null":
            menuSecond += [f"{y}. {x[1]}" for y, x in enumerate(optionSelect, 1)]
        else:
            pass
    
    #handle option conditions
    
    
    #determine if information about vertical and horizontal position were passed
    if mainMenuOptions:
        if len(mainMenuOptions) == 2:
            verticalPosition, horizontalPosition = mainMenuOptions
        else:
            verticalPosition = mainMenuOptions[0]
            horizontalPosition = verticalPosition
    else:
        verticalPosition, horizontalPosition = 0, 0
    
    #print menu
    
    #print menu and handle user input
    if optionSelect:
        while True:
            menu_print(menuMain, menuSecond, 1, verticalPosition, horizontalPosition, 1)
            userInput = input(inputLabel)
            userInput, errorCode, _ = input_error_check(userInput, 1, 1, len(optionSelect))
            
            if errorCode: # if it's not 0 // if error code is 1,2,3,4
                continue
            else:
                break
        
    else:
        pass
    
    #decide on the next node id
    outputNodeId = userInput
    
    #return next node id
    return outputNodeId
    

def rpg_menu_framework(nople, start):
    
    nodeId = start
    
    while True:
        nodeId = use_node(nople[nodeId])
    





from traceback import format_exc

try:
    rpg_menu_framework(tuple_with_menus, 0)
except Exception as a:
    print(format_exc())
    input()






































