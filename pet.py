from scipy.special.cython_special import exprel
from sly import Lexer, Parser
from time import sleep
import random
import logging

########################################
# PET STATUS # PET STATUS # PET STATUS #
########################################

class PetStatus:
    # stores the data of each need and how they work
    class Need():
        def __init__(self, alive: bool, current: float = 1, action: str = '', minmax: tuple[float, float] = (0, 2), drain: float = 0.1, gain: float = 0.1, delay: float = 1):
            self._alive = alive  # a reference to the alive value in pet
            self._current = current  # how much of the need is fulfilled
            self._action = action  # the string that notifies the user what need is being worked with
            self._minmax = minmax  # the minimum amount of the need before the pet dies and the maximum amount a need can be satisfied
            self._drain = drain  # how much each token drains
            self._gain = gain  # how much satisfying the need gives back
            self._delay = delay  # the length of the delay when satisfying the need

        def check(self):
            # checks the current amount of the need
            return self._current

        def alive(self):
            # checks if the need has caused the pet to die or not
            return self._alive

        def death(self):
            # method happens once a pet dies do to a need going to zero
            print(f"< PET DEAD >")
            print(f"< CAUSE: Lack Of {self._action} >")  # displays what need caused the death
            self._alive = False

        def current_test(self):
            # test to see if current is within range of minmax
            # checks if needs are below the minimum. if below the minimum, then the pet dies
            if self._current < self._minmax[0]:
                if self._alive:
                    self.death()  # causes pet to die and stopping the program
            # checks if needs are above the maximum. if below the maximum, then cap
            elif self._current > self._minmax[1]:
                self._current = self._minmax[1]  # sets current back within the maximum limits

        def current_calculation(self, value: float = 0, severity: float = 1, offset: tuple[float, float] = (0, 0)):
            # calculations and alterations that can be done to give more power to how current is altered
            return (value * severity) + random.uniform(offset[0], offset[1])

        def delay(self, severity: float = 1, offset: tuple[float, float] = (0, 0)):
            # severity is how much more or less the delay effects the pet
            print(f"< Pet's Currently {self._action} >")  # displays that the need is being taken care of
            sleep(self.current_calculation(self._delay, severity, offset))  # the duration in seconds the delay will happen for the action
            print(f"< Pet's Finished {self._action} >")  # displays that the need is being taken care of

        def drain(self, severity: float = 1, offset: tuple[float, float] = (0, 0)):
            # severity is how much a token will drain a need
            # offset is how much it can randomly adjust the amount drained from the needs current
            self._current -= self.current_calculation(self._drain, severity, offset)
            # checks if needs are below the minimum
            self.current_test()

        def gain(self, severity: float = 1, offset: tuple[float, float] = (0, 0), instant: bool = False):
            # severity is how much a token will gain a need
            # offset is how much it can randomly adjust the amount given to the needs current
            self._current += self.current_calculation(self._gain, severity, offset)
            # checks if needs are above maximum
            self.current_test()
            if not instant:
                self.delay()  # adds a delay to make sure users cannot span giving there pet needs

    # generates a random name every time the program is ran, purly visual
    name = random.choice(["Luna", "Oliver", "Mittens", "Leo", "Bella", "Shadow", "Simba", "Whiskers", "Chloe", "Jasper", "Nala", "Smokey", "Oreo", "Pumpkin", "Milo", "Patches", "Tigger", "Cleo", "Cosmo", "Ginger", "Zelda", "Rocky", "Binx", "Pepper", "Waffles", "Sir Reginald Fluffington III", "Felix", "Salem", "Goose", "Garfield", "Bagheera", "Gizmo", "Cinder", "Willow", "Hazel", "Olive", "Penelope", "Zoe", "Midnight", "Onyx", "Sterling", "Orion", "Jinx", "Figaro", "Cheshire", "Artemis",
                          "Max", "Buddy", "Lucy", "Charlie", "Daisy", "Cooper", "Sadie", "Bear", "Molly", "Zeus", "Ruby", "Duke", "Penny", "Scout", "Jack", "Stella", "Winston", "Bandit", "Finn", "Mocha", "Gus", "Apollo", "Biscuit", "Marley", "Chewie", "Professor Wigglebottom", "Bailey", "Koda", "Riley", "Thor", "Loki", "Bruno", "Toby", "Murphy", "Otis", "Hank", "Harley", "Gunner", "Samson", "Beau", "Ace", "Buster", "Diesel", "Titan", "Roxy", "Sasha", "Kona", "Zara",
                          "Kiwi", "Sunny", "Pip", "Echo", "Skye", "Mango", "Percy", "Indigo", "Robin", "Zazu", "Jade", "Sparrow", "Chirpy", "Finch", "Iago", "Zephyr", "Polly", "Hedwig", "Pico", "Bluebell", "Oscar", "Nimbus", "Peanut", "Phoenix", "Tweetie", "Captain Feathers", "Rio", "Jewel", "Kiko", "Petey", "Cypress", "Lark", "Dove", "Merlin", "Griffin", "Comet", "Galaxy", "Starlight", "Quill", "Soren", "Gylfie",
                          "Squeaky", "Nibbles", "Cheddar", "Remy", "Stuart", "Fievel", "Algernon", "Splinter", "Pinky", "Brain", "Nugget", "Domino", "Barnaby", "Mortimer", "Gouda", "Mochi", "Rizzo", "Popcorn", "Einstein", "Marble", "Basil", "Despereaux", "Scabbers", "Crouton", "Pip-squeak", "Lord Squeakington", "Templeton", "Nicodemus", "Timothy", "Gadget", "Zipper", "Monterey", "Colby", "Provolone", "Feta", "Parsley", "Twitch", "Scamp", "Gus-Gus", "Jaq", "Ratthew"])
    alive = True  # this is used to check if the program should end
    # list of all the needs together
    hunger = Need(True, 100, "Eating", (0, 100), 0.5, 25, 10)  # drains when handling variables directly
    thirst = Need(True, 100, "Drinking", (0, 100), 1.5, 50, 2)  # drains when handing every single expr in the parser
    energy = Need(True, 100, "Resting", (0, 100), 0.1, 50, 30)  # drains slowly over time form any code ran
    # the dictionary here is only used for easier searching for the needs
    needs_list = {'hunger': hunger, 'thirst': thirst, 'energy': energy}  # PUT ALL NEEDS HERE

#####################################
# PET LEXER # PET LEXER # PET LEXER #
#####################################

class PetLexer(Lexer):
    tokens = {NAME, INT, FLOAT, STRING, BOOL, TYPE, CONDITION, ET, NE, LT, LE, GT, GE}  # categorizes of each token that will be used
    ignore = '\t '  # tokens that are ignored by the program
    literals = {'=', '+', '-', '*', '/', '%', '^',
                '(', ')', '[', ']', ',', ':', '{', '}'}  # simple tokens that will be required constantly

    # statement operation tokens
    ET = r'=='  # equal to
    NE = r'!='  # not equal to
    LT = r'<<'  # less than
    LE = r'<='  # less than or equal to
    GT = r'>>'  # greater than
    GE = r'>='  # greater than or equal to

    # tokens for float numbers
    @_(r'\d+\.\d+')  # any digits
    def FLOAT(self, token):
        # makes value into python format
        token.value = float(token.value)
        return token

    # tokens for integer numbers
    @_(r'\d+')  # any digits
    def INT(self, token):
        # makes value into python format
        token.value = int(token.value)
        return token

    # tokens for integer numbers
    @_(r'true|false')  # true or false
    def BOOL(self, token):
        # makes value into python format
        token.value = True if token.value == 'true' else False  # due to the weirdness of bool(), empty means false and anything means true
        return token

    # the format of NAME and STRING and all the possible variable types
    # first [] stores start with characters and second [] stores followed by characters
    CONDITION = r'if|while'
    TYPE = r'int|float|string|bool|list'
    NAME = r'[a-zA-Z][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'  # strings must be double quote with anything in it

    # token for comments
    @_(r'#.*')
    def COMMENT(self, token):
        pass  # passes due to code not running from comments

########################################
# PET PARSER # PET PARSER # PET PARSER #
########################################

class PetParser(Parser):
    # tokens being given from lexer to parser
    tokens = PetLexer.tokens

    # order of operations/processors in operations, math, and logic
    precedence = (
        ('left', 'ET', 'NE'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', '^'),  # exponents
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.environment = {}

    # default statements
    @_('')
    def statement(self, parse):
        pass

    # used for variables and declaring variables
    # creating a variable with nothing assigned to it
    @_('var_declare')
    def statement(self, parse):
        status.hunger.drain()  # drains food from pet
        return parse.var_declare

    # assigned an expression or operation to the variable with the type if the var is new
    @_('TYPE NAME "=" expr')
    def var_declare(self, parse):
        status.hunger.drain()  # drains food from pet
        return 'var_declare', parse.TYPE, parse.NAME, parse.expr

    # used for variables and assigning variables
    # variables with something assigned to it
    @_('var_assign')
    def statement(self, parse):
        status.hunger.drain()  # drains food from pet
        return parse.var_assign

    # assigned an expression or operation to the variable
    @_('NAME "=" expr')
    def var_assign(self, parse):
        status.hunger.drain()  # drains food from pet
        return 'var_assign', parse.NAME, parse.expr

    # assigned an expression or operation to the variable in a list
    @_('NAME "[" expr "]" "=" expr')
    def var_assign(self, parse):
        status.hunger.drain()  # drains food from pet
        return 'var_assign', parse.NAME, parse.expr0, parse.expr1

    # simply an expression or operation
    @_('expr')
    def statement(self, parse):
        status.thirst.drain()  # drains food from pet
        return parse.expr

    # used when there is more code to be executed after the value is true or false,
    # this is used when you want to run code with this, usually with run()
    @_('CONDITION "(" expr ")" ":" statement')
    def statement(self, parse):
        return parse.CONDITION, parse.expr, parse.statement

    # changing variable types
    @_('TYPE "(" expr ")"')
    def expr(self, parse):
        return 'call', parse.TYPE, parse.expr

    # functions
    @_('NAME "(" ")"')
    def expr(self, parse):
        return 'call', parse.NAME

    # functions
    # groups allow me to have dynamic argument sizes for calls
    @_('NAME "(" group ")"')
    def expr(self, parse):
        return 'call', parse.NAME, parse.group

    # expressions and operations when dealing with math-based precedence
    # addition
    @_('expr "+" expr')
    def expr(self, parse):
        return 'add', parse.expr0, parse.expr1

    # subtraction
    @_('expr "-" expr')
    def expr(self, parse):
        return 'sub', parse.expr0, parse.expr1

    # multiplication
    @_('expr "*" expr')
    def expr(self, parse):
        return 'mul', parse.expr0, parse.expr1

    # division
    @_('expr "/" expr')
    def expr(self, parse):
        return 'div', parse.expr0, parse.expr1

    # remainder
    @_('expr "%" expr')
    def expr(self, parse):
        return 'rem', parse.expr0, parse.expr1

    # exponents
    @_('expr "^" expr')
    def expr(self, parse):
        return 'pow', parse.expr0, parse.expr1

    # negatives
    @_('"-" expr %prec UMINUS')
    def expr(self, parse):
        return parse.expr

    # groups of math or operations within ()
    @_('"(" expr ")"')
    def expr(self, parse):
        return parse.expr

    # equal to statement operations
    @_('expr ET expr')
    def expr(self, parse):
        return 'eqt', parse.expr0, parse.expr1

    # not equal to statement operations
    @_('expr NE expr')
    def expr(self, parse):
        return 'not', parse.expr0, parse.expr1

    # less than statement operations
    @_('expr LT expr')
    def expr(self, parse):
        return 'les', parse.expr0, parse.expr1

    # less than or equal to statement operations
    @_('expr LE expr')
    def expr(self, parse):
        return 'leq', parse.expr0, parse.expr1

    # greater than statement operations
    @_('expr GT expr')
    def expr(self, parse):
        return 'gre', parse.expr0, parse.expr1

    # greater than or equal to statement operations
    @_('expr GE expr')
    def expr(self, parse):
        return 'geq', parse.expr0, parse.expr1

    # simply a name
    @_('NAME')
    def expr(self, parse):
        status.hunger.drain(0.25)  # drains food from pet
        return 'var', parse.NAME

    # searching data from list
    @_('NAME "[" expr "]"')
    def expr(self, parse):
        status.hunger.drain()  # drains food from pet
        return 'var', parse.NAME, parse.expr

    # simply a float number
    @_('FLOAT')
    def expr(self, parse):
        return 'num', parse.FLOAT

    # simply an int number
    @_('INT')
    def expr(self, parse):
        return 'num', parse.INT

    # simply a string
    @_('STRING')
    def expr(self, parse):
        return 'str', parse.STRING[1:-1]  # removes quotation marks for the string

    # simply a bool
    @_('BOOL')
    def expr(self, parse):
        return 'bool', parse.BOOL

    # everything below this is for handling lists and arrays of values or operations
    # goes though each group or expr in that are back to back between ','
    # determining if groups exist, the length of the groups, and then putting all the items in a group together
    @_('expr')
    def group(self, parse):
        status.hunger.drain(0.25)  # drains food from pet
        return [parse.expr]  # creates a new list that will added over time with the below method

    @_('group "," expr')
    def group(self, parse):
        parse.group.append(parse.expr)  # adds the new item the existing list
        return parse.group

    # empty lists
    @_('"[" "]"')
    def expr(self, parse):
        status.hunger.drain()  # drains food from pet
        return 'list', []  # returns an empty list

    # non-empty list
    @_('"[" group "]"')
    def expr(self, parse):
        status.hunger.drain()  # drains food from pet
        return 'list', parse.group  # returns


###########################################
# PET EXECUTE # PET EXECUTE # PET EXECUTE #
###########################################

class PetExecute:
    def __init__(self, tree, environment, status):  #
        self.environment = environment  # stores the variables
        result = self.walk(tree)  # returns the full abstract syntax tree holding the split statements form the parser
        #print(result)  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING

    # used for displaying error or warning messages and will affect your pet differently
    def error_message(self, message: str):  # error messages will display red and instantly kill the animal
        print(f"\033[31m< {message} >\033[0m")
        status.alive = False

    def warning_message(self, message: str):  # warning messages will display yellow and will slightly drain all needs from the pet
        print(f"\033[33m< {message} >\033[0m")
        status.thirst.drain(3)
        status.hunger.drain(3)
        status.energy.drain(3)

    def walk(self, node):

        # everytime the program walks it uses energy
        status.energy.drain()
        # additionally, all actions will also drain thirst and hunger, but much slower with each action draining some more thn others
        status.hunger.drain(0.1)
        status.thirst.drain(0.1)

        # returns if no nodes where found
        if node == None:
            return None

        # condition statements and loops
        if node[0] == 'if':  # if statement
            if self.walk(node[1]):  # test if the test statement is true or false
                self.walk(node[2])  # runs the code if the if statement worked
        elif node[0] == 'while':  # while loop
            while self.walk(node[1]):  # test if the test statement is true or false
                self.walk(node[2])  # runs code until the while statement is not true

        #print(node)  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING
        # returns if node is already a Python-based value
        if isinstance(node, (int, float, str, bool, list)):
            return node

        # returns the value if the node is a simple number, string, bool, or list
        if node[0] == 'num' or node[0] == 'str' or node[0] == 'bool':
            return node[1]

        # turns values into normal values, then reconverts them into what the parser wants to work on
        # does this everytime a list is used
        if node[0] == 'list':
            node_list = []  # empty list to deconvert and reconvert the values into what the parser wants
            # creates a normal list
            for node_item in node[1]:
                node_list.append(self.walk(node_item))  # converts the value parser form to a normal value
            return node_list

        # returns the nodes value it after doing simple math
        if node[0] == 'add':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if type(node0) == type(node1):  # ints, floats, and strings
                return node0 + node1
            else:  # if there was a type mismatch
                self.error_message(f"'{node0}' & '{node1}' Uncombatable")  # displays if variables are uncombatable
        elif node[0] == 'sub':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if type(node0) == type(node1):  # ints, floats, and strings
                return node0 - node1
            else:  # if there was a type mismatch
                self.error_message(f"'{node0}' & '{node1}' Uncombatable")  # displays if variables are uncombatable
        elif node[0] == 'mul':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if (isinstance(node0, (int, float)) and type(node0) == type(node1)) or ((isinstance(node0, int) and isinstance(node1, str)) or (isinstance(node0, str) and isinstance(node1, int))):  # ints and floats, or one string and one int
                return node0 * node1
            else:  # if there was a type mismatch
                self.error_message(f"'{node0}' & '{node1}' Uncombatable")  # displays if variables are uncombatable
        elif node[0] == 'div':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if isinstance(node0, (int, float)) and type(node0) == type(node1):  # ints and floats
                return node0 / node1
            else:  # if there was a type mismatch
                self.error_message(f"'{node0}' & '{node1}' Uncombatable")  # displays if variables are uncombatable
        elif node[0] == 'rem':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if isinstance(node0, (int, float)) and type(node0) == type(node1):  # ints and floats
                return node0 % node1
            else:  # if there was a type mismatch
                self.error_message(f"'{node0}' & '{node1}' Uncombatable")  # displays if variables are uncombatable

        elif node[0] == 'pow':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if isinstance(node0, (int, float)) and type(node0) == type(node1):  # ints and floats
                return node0 ** node1
            else:  # if there was a type mismatch
                self.error_message(f"'{node0}' & '{node1}' Uncombatable")  # displays if variables are uncombatable

        # returns if statement is true after doing operations
        if node[0] == 'eqt':  # equal to
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            return node0 == node1
        if node[0] == 'not':  # not equal to
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            return node0 != node1
        if node[0] == 'les':  # less than
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            return node0 < node1
        if node[0] == 'leq':  # less than or equal to
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            return node0 <= node1
        if node[0] == 'gre':  # greater than
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            return node0 > node1
        if node[0] == 'geq':  # greater than or equal to
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            return node0 >= node1

        # stores data inside variables inside the environment when declared
        if node[0] == 'var_declare':
            # type casting
            node_value = self.walk(node[3])  # gets the value for testing and storing in environment
            #print(f"NODE: {node_value}")  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING
            try:
                # makes sure types are correct
                if node[1] == 'int':
                    if isinstance(node_value, float):
                        self.warning_message(f"'Converted '{node_value}' To '{int(node_value)}'")  # notifies that float was changed to int
                    node_value = int(node_value)  # changes to int
                if node[1] == 'float':
                    if isinstance(node_value, int):
                        self.warning_message(f"'Converted '{node_value}' To '{float(node_value)}'")  # notifies that int was changed to float
                    node_value = float(node_value)  # changes to float
                elif node[1] == 'string':
                    node_value = str(node_value)   # changes to string
                elif node[1] == 'bool':
                    if isinstance(node_value, (int, float, str)):  # notifies how the other value was converted if converted into a bool
                        self.warning_message(f"'Converted '{node_value}' To '{bool(node_value)}'")  # notifies that anything was changed to bool
                    node_value = bool(node_value)   # changes to bool
                elif node[1] == 'list':
                    if isinstance(node_value, (int, float, str, bool)):  # notifies how the other value was entered in a list
                        self.warning_message(f"'Converted '{node_value}' To '{[node_value]}'") # notifies that anything was put into a list
                        node_value = [node_value]  # changes node variable into a list
                # stores value
                environmental_variable = {'type': node[1], 'value': node_value}
                self.environment[node[2]] = environmental_variable
                return node[2]
            except (ValueError, TypeError):  # happens if the value that has operations preformed on it is the wrong type or if the value is invalid
                self.warning_message(f"'{node_value}' To '{type(node_value)}' Uncombatable")  # notifies that float was changed to int

        # returns and stores data inside variables that are stored in the environment
        # only works for variables that already exist
        if node[0] == 'var_assign':
            # checks if variable is stored in a list or not
            # type casting is not done within changing values within the list, as lists do not care what type of value ios being stored
            if len(node) == 4:  # works if the variable is part of a list
                node_index = self.walk(node[2])  # gets the index for list searching
                node_variable = self.environment[node[1]]  # gets list form environment to extract the data from within the list
                node_value = self.walk(node[3])  # gets the value for testing and storing in environment

                # stores value
                node_variable['value'][node_index] = node_value  # stores the new value within the list
                return node_value

            else:  # if not a list
                node_variable = node[1]  # the variable itself
                node_value = self.walk(node[2])  # gets the value for testing and storing in environment

                # type casting
                # also displays if the value changed in anyway when changing its type
                if self.environment[node_variable]['type'] == 'int':  # searches for the variable's type in the environment
                    if isinstance(node_value, float):  # notifies how the other value was converted if converted into a bool
                        self.warning_message(f"Converted '{node_value}' To '{int(node_value)}'")  # notifies that float was changed to int
                    node_value = int(node_value)  # changes to int
                elif self.environment[node_variable]['type'] == 'float':  # searches for the variable's type in the environment
                    if isinstance(node_value, int):
                        self.warning_message(f"Converted '{node_value}' To '{float(node_value)}'")  # notifies that int was changed to float
                    node_value = float(node_value)  # changes int to float
                elif self.environment[node_variable]['type'] == 'string':  # searches for the variable's type in the environment
                    node_value = str(node_value)  # changes to string
                elif self.environment[node_variable]['type'] == 'bool':  # searches for the variable's type in the environment
                    if isinstance(node_value, (int, float, str)):  # notifies how the other value was converted if converted into a bool
                        self.warning_message(f"Converted '{node_value}' To '{bool(node_value)}'")  # notifies that types were changed to bool
                    node_value = str(node_value)  # changes to bool
                elif self.environment[node_variable]['type'] == 'list':  # searches for the variable's type in the environment
                    if isinstance(node_value, (int, float, str, bool)):  # notifies how the other value was entered in a list
                        self.warning_message(f"'Converted '{node_value}' To '{[node_value]}'")  # notifies that anything was put into a list
                        node_value = [node_value]  # changes node variable into a list

                # stores value
                self.environment[node_variable]['value'] = node_value
                return node_variable

        # returns the value of the variable asked for
        if node[0] == 'var':
            try:
                try:  # will attempt to check if the var is a list instead of a single variable
                    return self.environment[node[1]]['value'][self.walk(node[2])]  # takes data from that index
                except IndexError:  # if variable is not part of a list
                    return self.environment[node[1]]['value']  # tries to find variable and its data
            except LookupError:  # if no variable or data was found
                self.error_message(f"'{node[1]}' Undefined")  # only displays name of variable
                return 0

        # returns results for functions and all things functions
        if node[0] == 'call':  # only functions

            # extracting the values from all of the arguments that were put in a group list
            node_list = []  # will store reach argument in this list and will pull how far as needed for each call method
            if isinstance(node[2], list):  # checks if the node[2] is a group of expr or a single expr
                for node_argument in node[2]:
                    node_list.append(self.walk(node_argument))  # store and sets up argument to be used by the calls
            else:  # if it is a single expr statement and nor a group
                node_list.append(self.walk(node[2]))

            # only uses one argument
            if node[1] == 'print':  # functions for displaying text or data
                print(node_list[0])  # prints out the exact same as print in python
            # only uses one argument
            elif node[1] == 'input':  # functions for asking and receiving user data or input
                return input(node_list[0])  # gets the argument inside the input method for displaying and returns a user's response
            # only uses one argument
            elif node[1] == 'run':  # functions for running many lines of code together
                node_file = node_list[0]  # gets the file path given that has all the code to run
                try:
                    if isinstance(node_file, str):
                        with open(node_file, 'r') as file:  # opens the file after removing the double quotation marks at the beginning and end
                            node_texts = str.split(file.read(), '\n')  # splits each statement in the text file into its own statement
                            for node_text in node_texts:  # goes through each statement
                                # tests if pet program is not alive
                                # goes through each need in the dictionary and tests if they are dead
                                for need in status.needs_list.values():
                                    if not need.alive():
                                        status.alive = False  # pet is labeled as dead
                                        break
                                if status.alive == False:
                                    break

                                node_tree = parser.parse(lexer.tokenize(node_text))  # splits command between spaces
                                PetExecute(node_tree, self.environment, status)  # runs the commands with existing environment, parser, lexer, and everything else
                    else:
                        self.error_message(f"'{node_file}' Type Uncombatable")  # notifies that file must be a string
                except FileNotFoundError:
                    self.warning_message(f"'{node_file}' Unfound")  # notifies if the file was not found

            # only uses one argument
            elif node[1] == 'len':  # checks the length of lists
                return len(node_list[0])
            # only uses one argument
            elif node[1] == 'clear':  # clears the data from inside a list
                return node_list[0].clear()
            # requires two argument, the list variable, and the data being added to the end of the list
            elif node[1] == 'append':  # adds data to the end of a list
                return node_list[0].append(node_list[1])
            # requires three argument, the list variable, the position in the list the data will go in, and the data being added tothe list
            elif node[1] == 'insert':  # adds data anywhere to the list
                return node_list[0].insert(node_list[1], node_list[2])
            # requires two argument, the list variable, and the location of the data being removed
            elif node[1] == 'pop':  # removes data form anywhere in the list
                return node_list[0].pop(node_list[1])
            # requires two argument, the list variable, and the data being removed
            elif node[1] == 'remove':  # removes specified data from the list
                return node_list[0].remove(node_list[1])
            # requires two argument, the list variable, and the data being counted
            elif node[1] == 'count':  # counts the amount of that data inside a list
                return node_list[0].count(node_list[1])
            # only uses one argument
            elif node[1] == 'sort':  # sorts the data alphabetically
                return node_list[0].sort()

            # only uses one argument
            elif node[1] == 'replenish':  # used to replenish stats for the pet
                node_need = node_list[0]  # finds the need that will be replenished
                try:
                    # recovers what was drained during replenishing
                    status.hunger.gain(0.08, instant=True)
                    status.thirst.gain(0.13, instant=True)
                    status.energy.gain(0.010, instant=True)

                    status.needs_list[node_need].gain()  # replenishes the pets needs by giving pets more of the need, allowing users to run code for longer
                except KeyError:  # if the need does no
                    self.warning_message(f"'{node_need}' Need Nonexistent")  # notifies that file must be a string
            # only uses one argument
            elif node[1] == 'check':  # used to check the stats for the pet
                node_need = node_list[0]  # finds the need that will be checked
                try:
                    return status.needs_list[node_need].check()  # replenishes the pets needs by giving pets more of the need, allowing users to run code for longer
                except KeyError:  # if the need does not exist:
                    self.warning_message(f"'{node_need}' Need Nonexistent")  # notifies that file must be a string
            # all below are used to change the variable type, only uses one argument
            elif node[1] == 'int':  # functions for changed variable types to int
                return int(node_list[0])  # gets the argument inside and converts the variable into an integer
            elif node[1] == 'float':  # functions for changed variable types to float
                return float(node_list[0])  # gets the argument inside and converts the variable into a float
            elif node[1] == 'string':  # functions for changed variable types to string
                return str(node_list[0])  # gets the argument inside and converts the variable into a string
            elif node[1] == 'bool':  # functions for changed variable types to bool
                return bool(node_list[0])  # gets the argument inside and converts the variable into a bool
            elif node[1] == 'type':  # functions to see what kind of type a variable is
                return type(node_list[0]).__name__  # gets the argument inside and returns what type the value is

        # if nothing came form the walk method
        return None

######################
# MAIN # MAIN # MAIN #
######################

# runs everything to collect user inputs, and output results from user inputs
if __name__ == '__main__':

    lexer = PetLexer()
    parser = PetParser()
    status = PetStatus()
    print(f"Take Care Of Your New Pet")
    print(f"'{status.name}' Is Your Pet's Name")
    environment = {}  # all variables that are kept between each command a user makes
    # environment stores static variables as a dictionary, so it will store the variable type and the value inside the variable

    # continues until an error occurs or user end process
    while True:
        try:
            # tests if pet program is not alive
            # goes through each need in the dictionary and tests if they are dead
            for need in status.needs_list.values():
                if not need.alive():
                    status.alive = False  # pet is labeled as dead
                    break
            if status.alive == False:
                break

            command = input(f'{status.name}: ')  # the name of the programming languages changes everytime, based on your pets name

        except EOFError:
            break  # ends programming language

        # if commands form user was received
        if command:
            #print(list(lexer.tokenize(command)))  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING
            tree = parser.parse(lexer.tokenize(command))  # splits command between spaces
            PetExecute(tree, environment, status)  # runs the commands

        print(f"HUNGER: {status.hunger.check()}")
        print(f"THIRST: {status.thirst.check()}")
        print(f"ENERGY: {status.energy.check()}")

    # makes user press something ENTER before the program fully closes
    input(f'\033[32m< Press ENTER To Exit >\033[0m')