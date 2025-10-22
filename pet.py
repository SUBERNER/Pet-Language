from scipy.special.cython_special import exprel
from sly import Lexer, Parser
from time import sleep
import random

########################################
# PET STATUS # PET STATUS # PET STATUS #
########################################

class PetStatus:
    # stores the data of each need and how they work
    class Need():
        def __init__(self, alive: bool, current: float = 1, action: str = '', minmax: tuple[float, float] = tuple[0, 2], drain: float = 0.1, gain: float = 0.1, delay: float = 1):
            self._alive = alive  # a reference to the alive value in pet
            self._current = current  # how much of the need is fulfilled
            self._action = action  # the string that notifies the user what need is being worked with
            self._minmax = minmax  # the minimum amount of the need before the pet dies and the maximum amount a need can be satisfied
            self._drain = drain  # how much each token drains
            self._gain = gain  # how much satisfying the need gives back
            self._delay = delay  # the length of the delay when satisfying the need

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
                    death() # causes pet to die and stopping the program
            # checks if needs are above the maximum. if below the maximum, then cap
            elif self._current > self._minmax[1]:
                self._current = self._minmax[1]  # sets current back within the maximum limits

        def current_calculation(self, value: float = 0, severity: float = 1, offset: tuple[float, float] = tuple[0, 0]):
            # calculations and alterations that can be done to give more power to how current is altered
            return (value * severity) + random.uniform(offset[0], offset[1])

        def drain(self, severity: float = 1, offset: tuple[float, float] = tuple[0, 0]):
            # severity is how much a token will drain a need
            # offset is how much it can randomly adjust the amount drained from the needs current
            self._current -= current_calculation(self._drain, severity, offset)
            # checks if needs are below the minimum
            current_test()
            print(self._current)

        def gain(self, severity: float = 1, offset: tuple[float, float] = tuple[0, 0]):
            # severity is how much a token will gain a need
            # offset is how much it can randomly adjust the amount given to the needs current
            self._current -= current_calculation(self._gain, severity, offset)
            # checks if needs are above maximum
            current_test()

        def delay(self, severity: float = 1, offset: tuple[float, float] = tuple[0, 0]):
            # severity is how much more or less the delay effects the pet
            print(f"< Pet's {self._action} >")  # displays that the need is being taken care of
            time.sleep(current_calculation(self._delay, severity, offset))  # the duration in seconds the delay will happen for the action

    # generates a random name every time the program is ran, purly visual
    name = random.choice(["Luna", "Oliver", "Mittens", "Leo", "Bella", "Shadow", "Simba", "Whiskers", "Chloe", "Jasper", "Nala", "Smokey", "Oreo", "Pumpkin", "Milo", "Patches", "Tigger", "Cleo", "Cosmo", "Ginger", "Zelda", "Rocky", "Binx", "Pepper", "Waffles", "Sir Reginald Fluffington III", "Felix", "Salem", "Goose", "Garfield", "Bagheera", "Gizmo", "Cinder", "Willow", "Hazel", "Olive", "Penelope", "Zoe", "Midnight", "Onyx", "Sterling", "Orion", "Jinx", "Figaro", "Cheshire", "Artemis",
                          "Max", "Buddy", "Lucy", "Charlie", "Daisy", "Cooper", "Sadie", "Bear", "Molly", "Zeus", "Ruby", "Duke", "Penny", "Scout", "Jack", "Stella", "Winston", "Bandit", "Finn", "Mocha", "Gus", "Apollo", "Biscuit", "Marley", "Chewie", "Professor Wigglebottom", "Bailey", "Koda", "Riley", "Thor", "Loki", "Bruno", "Toby", "Murphy", "Otis", "Hank", "Harley", "Gunner", "Samson", "Beau", "Ace", "Buster", "Diesel", "Titan", "Roxy", "Sasha", "Kona", "Zara",
                          "Kiwi", "Sunny", "Pip", "Echo", "Skye", "Mango", "Percy", "Indigo", "Robin", "Zazu", "Jade", "Sparrow", "Chirpy", "Finch", "Iago", "Zephyr", "Polly", "Hedwig", "Pico", "Bluebell", "Oscar", "Nimbus", "Peanut", "Phoenix", "Tweetie", "Captain Feathers", "Rio", "Jewel", "Kiko", "Petey", "Cypress", "Lark", "Dove", "Merlin", "Griffin", "Comet", "Galaxy", "Starlight", "Quill", "Soren", "Gylfie",
                          "Squeaky", "Nibbles", "Cheddar", "Remy", "Stuart", "Fievel", "Algernon", "Splinter", "Pinky", "Brain", "Nugget", "Domino", "Barnaby", "Mortimer", "Gouda", "Mochi", "Rizzo", "Popcorn", "Einstein", "Marble", "Basil", "Despereaux", "Scabbers", "Crouton", "Pip-squeak", "Lord Squeakington", "Templeton", "Nicodemus", "Timothy", "Gadget", "Zipper", "Monterey", "Colby", "Provolone", "Feta", "Parsley", "Twitch", "Scamp", "Gus-Gus", "Jaq", "Ratthew"])
    alive = True  # notifies the program if the pet is alive and if the code should continue running
    # list of all the needs together
    hunger = Need(alive, 1, "Eating", (0, 1), 0.02, 0.25, 10)  # stores how hungry the pet is
    thirst = Need(alive, 1, "Drinking", (0, 1), 0.05, 0.5, 2)  # stores how thirsty the pet is
    energy = Need(alive, 1, "Resting", (0, 1), 0.01, 0.5, 30)  # stores how much energy the pet has left

#####################################
# PET LEXER # PET LEXER # PET LEXER #
#####################################

class PetLexer(Lexer):
    tokens = {NAME, INT, FLOAT, STRING, BOOL, TYPE}  # categorizes of each token that will be used
    ignore = '\t '  # tokens that are ignored by the program
    literals = {'=', '+', '-', '*', '/', '%', '^',
                '(', ')', '[', ']', ',', ';'}  # simple tokens that will be required constantly

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
        return parse.var_declare

    # assigned an expression or operation to the variable with the type if the var is new
    @_('TYPE NAME "=" expr')
    def var_declare(self, parse):
        return 'var_declare', parse.TYPE, parse.NAME, parse.expr

    # used for variables and assigning variables
    # variables with something assigned to it
    @_('var_assign')
    def statement(self, parse):
        return parse.var_assign

    # assigned an expression or operation to the variable
    @_('NAME "=" expr')
    def var_assign(self, parse):
        return 'var_assign', parse.NAME, parse.expr

    # simply an expression or operation
    @_('expr')
    def statement(self, parse):
        return parse.expr

    # changing variable types
    @_('TYPE "(" expr ")"')
    def expr(self, parse):
        return 'call', parse.TYPE, parse.expr

    # functions
    @_('NAME "(" expr ")"')
    def expr(self, parse):
        return 'call', parse.NAME, parse.expr

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

    # simply a name
    @_('NAME')
    def expr(self, parse):
        return 'var', parse.NAME

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
        return [parse.expr]  # creates a new list that will added over time with the below method

    @_('group "," expr')
    def group(self, parse):
        parse.group.append(parse.expr)  # adds the new item the existing list
        return parse.group

    # empty lists
    @_('"[" "]"')
    def expr(self, parse):
        return 'list', []  # returns an empty list

    # non-empty list
    @_('"[" group "]"')
    def expr(self, parse):
        return 'list', parse.group  # returns

    # getting data from list
    @_('NAME "[" INT "]"')
    def expr(self, parse):
        return 'list_stuff'  # returns


###########################################
# PET EXECUTE # PET EXECUTE # PET EXECUTE #
###########################################

class PetExecute:
    def __init__(self, tree, environment):  #
        self.environment = environment  # stores the variables
        result = self.walk(tree)  # returns the full abstract syntax tree holding the split statements form the parser
        '''
        REMOVING FOR NOW AS THIS WAS MENT BEFORE THE PRINT AND RUN METHODS
        # prints results after the tree has been walked and the results of the statements have been made
        if result is not None and (isinstance(result, int) or isinstance(result, float)):
            print(result)
        if isinstance(result, str):  # test if a result is a string
            print(result)
        '''
        print(result)  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING

    def walk(self, node):
        if node and node[0] == 'program':
            self.walk(node[1])
            if node[2]:
                self.walk(node[2])
            return

        print(node)  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING
        # returns if node is already a Python-based value
        if isinstance(node, (int, float, str, bool)):
            return node

        # returns if no nodes where found
        if node == None:
            return None

        # returns the value if the node is a simple number, string, or bool
        if node[0] == 'num' or node[0] == 'str' or node[0] == 'bool':
            return node[1]

        # returns the nodes value it after doing simple math
        if node[0] == 'add':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if type(node0) == type(node1):  # ints, floats, and strings
                return self.walk(node[1]) + self.walk(node[2])
            else:  # if there was a type mismatch
                print(f"\033[31m< '{node[1][1]}' & '{node[2][1]}' Uncombatable >\033[0m")  # displays if variables are uncombatable
        elif node[0] == 'sub':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if type(node0) == type(node1):  # ints, floats, and strings
                return self.walk(node[1]) - self.walk(node[2])
            else:  # if there was a type mismatch
                print(f"\033[31m< '{node[1][1]}' & '{node[2][1]}' Uncombatable >\033[0m")  # displays if variables are uncombatable
        elif node[0] == 'mul':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if (isinstance(node0, (int, float)) and type(node0) == type(node1)) or ((isinstance(node0, int) and isinstance(node1, str)) or (isinstance(node0, str) and isinstance(node1, int))):  # ints and floats, or one string and one int
                return self.walk(node[1]) * self.walk(node[2])
            else:  # if there was a type mismatch
                print(f"\033[31m< '{node[1][1]}' & '{node[2][1]}' Uncombatable >\033[0m")  # displays if variables are uncombatable
        elif node[0] == 'div':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if isinstance(node0, (int, float)) and type(node0) == type(node1):  # ints and floats
                return self.walk(node[1]) / self.walk(node[2])
            else:  # if there was a type mismatch
                print(f"\033[31m< '{node[1][1]}' & '{node[2][1]}' Uncombatable >\033[0m")  # displays if variables are uncombatable
        elif node[0] == 'rem':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if isinstance(node0, (int, float)) and type(node0) == type(node1):  # ints and floats
                return self.walk(node[1]) % self.walk(node[2])
            else:  # if there was a type mismatch
                print(f"\033[31m< '{node[1][1]}' & '{node[2][1]}' Uncombatable >\033[0m")  # displays if variables are uncombatable
        elif node[0] == 'pow':
            node0 = self.walk(node[1])
            node1 = self.walk(node[2])
            if isinstance(node0, (int, float)) and type(node0) == type(node1):  # ints and floats
                return self.walk(node[1]) ** self.walk(node[2])
            else:  # if there was a type mismatch
                print(f"\033[31m< '{node[1][1]}' & '{node[2][1]}' Uncombatable >\033[0m")  # displays if variables are uncombatable

        # stores data inside variables inside the environment when declared
        if node[0] == 'var_declare':
            # type casting
            node_variable = self.walk(node[3])  # gets the value for testing and storing in environment
            print(f"NODE: {node_variable}")  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING
            try:
                # makes sure types are correct
                if node[1] == 'int':
                    if isinstance(node_variable, float):
                        print(f"\033[33m< 'Converted '{node_variable}' To '{int(node_variable)}' >\033[0m")  # notifies that float was changed to int
                    node_variable = int(node_variable)  # changes to int
                if node[1] == 'float':
                    if isinstance(node_variable, int):
                        print(f"\033[33m< 'Converted '{node_variable}' To '{float(node_variable)}' >\033[0m")  # notifies that int was changed to float
                    node_variable = float(node_variable)  # changes to float
                elif node[1] == 'string':
                    node_variable = str(node_variable)   # changes to string
                elif node[1] == 'bool':
                    if isinstance(node_variable, (int, float, str)):  # notifies how the other value was converted if converted into a bool
                        print(f"\033[33m< 'Converted '{node_variable}' To '{bool(node_variable)}' >\033[0m")  # notifies that anything was changed to bool
                    node_variable = bool(node_variable)   # changes to bool
                elif node[1] == 'list':
                    if isinstance(node_variable, (int, float, str, bool)):  # notifies how the other value was entered in a list
                        print(f"\033[33m< 'Converted '{node_variable}' To '{[node_variable]}' >\033[0m")  # notifies that anything was put into a list
                        node_variable = [node_variable]  # changes node variable into a list
                # stores value
                environmental_variable = {'type': node[1], 'value': node_variable}
                self.environment[node[2]] = environmental_variable
                return node[2]
            except (ValueError, TypeError):  # happens if the value that has operations preformed on it is the wrong type or if the value is invalid
                print(f"\033[33m< {node_variable}' To '{type(node_variable)}' Uncombatable >\033[0m")  # notifies that float was changed to int

        # returns and stores data inside variables that are stored in the environment
        # only works for variables that already exist
        if node[0] == 'var_assign':
            # type casting
            # also displays if the value changed in anyway when changing its type
            node_variable = self.walk(node[2])  # gets the value for testing and storing in environment
            if self.environment[node[1]]['type'] == 'int':  # searches for the variable's type in the environment
                if isinstance(node_variable, float):  # notifies how the other value was converted if converted into a bool
                    print(f"\033[33m< 'Converted '{node_variable}' To '{int(node_variable)}' >\033[0m")  # notifies that float was changed to int
                node_variable = int(node_variable)  # changes to int
            elif self.environment[node[1]]['type'] == 'float':  # searches for the variable's type in the environment
                if isinstance(node_variable, int):
                    print(f"\033[33m< 'Converted '{node_variable}' To '{float(node_variable)}' >\033[0m")  # notifies that int was changed to float
                node_variable = float(node_variable)  # changes int to float
            elif self.environment[node[1]]['type'] == 'string':  # searches for the variable's type in the environment
                node_variable = str(node_variable)  # changes to string
            elif self.environment[node[1]]['type'] == 'bool':  # searches for the variable's type in the environment
                if isinstance(node_variable, (int, float, str)):  # notifies how the other value was converted if converted into a bool
                    print(f"\033[33m< 'Converted '{node_variable}' To '{bool(node_variable)}' >\033[0m")  # notifies that types were changed to bool
                node_variable = str(node_variable)  # changes to bool
            elif self.environment[node[1]]['type'] == 'list':  # searches for the variable's type in the environment
                if isinstance(node_variable, (int, float, str, bool)):  # notifies how the other value was entered in a list
                    print(f"\033[33m< 'Converted '{node_variable}' To '{[node_variable]}' >\033[0m")  # notifies that anything was put into a list
                    node_variable = [node_variable]  # changes node variable into a list
            # stores value
            self.environment[node[1]]['value'] = node_variable
            return node[1]

        # returns the value of the variable asked for
        if node[0] == 'var':
            try:
                return self.environment[node[1]]['value']  # tries to find variable and its data
            except LookupError:  # if no variable or data was found
                print(f"\033[31m< '{node[1]}' Undefined >\033[0m")  # only displays name of variable
                return 0

        # returns results for functions and all things functions
        if node[0] == 'call':  # only functions
            if node[1] == 'print':  # functions for displaying text or data
                print(self.walk(node[2]))  # prints out the exact same as print in python
            elif node[1] == 'input':  # functions for asking and receiving user data or input
                return input(self.walk(node[2]))  # gets the argument inside the input method for displaying and returns a users response
            elif node[1] == 'run':  # functions for running many lines of code together
                node_file = self.walk(node[2])  # gets the file path given that has all the code to run
                try:
                    if isinstance(node_file, str):
                        with open(node_file, 'r') as file:  # opens the file after removing the double quotation marks at the beginning and end
                            node_texts = str.split(file.read(), '\n')  # splits each statement in the text file into its own statement
                            for node_text in node_texts:  # goes through each statement
                                node_tree = parser.parse(lexer.tokenize(node_text))  # splits command between spaces
                                PetExecute(node_tree, self.environment)  # runs the commands with existing environment, parser, lexer, and everything else
                    else:
                        print(f"\033[31m< '{node_file}' Type Uncombatable >\033[0m")  # notifies that file must be a string
                except FileNotFoundError:
                    print(f"< '{node_file}' Unfound >")  # notifies if the file was not found
            # all below are used to change the variable type
            elif node[1] == 'int':  # functions for changed variable types to int
                return int(self.walk(node[2]))  # gets the argument inside and converts the variable into an integer
            elif node[1] == 'float':  # functions for changed variable types to float
                return float(self.walk(node[2]))  # gets the argument inside and converts the variable into a float
            elif node[1] == 'string':  # functions for changed variable types to string
                return str(self.walk(node[2]))  # gets the argument inside and converts the variable into a string
            elif node[1] == 'bool':  # functions for changed variable types to bool
                return bool(self.walk(node[2]))  # gets the argument inside and converts the variable into a bool
            elif node[1] == 'type':  # functions to see what kind of type a variable is
                return type(self.walk((node[2]))).__name__  # gets the argument inside and returns what type the value is

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
            command = input(f'{status.name}: ')  # the name of the programming languages changes everytime, based on your pets name

            # tests if pet program is not alive
            if status.alive == False:
                break  # ends programming language

        except EOFError:
            break  # ends programming language

        # if commands form user was received
        if command:
            print(list(lexer.tokenize(command)))  # DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING DEBUGGING
            tree = parser.parse(lexer.tokenize(command))  # splits command between spaces
            PetExecute(tree, environment)  # runs the commands

    # makes user press something ENTER before the program fully closes
    input(f'\033[31< Press ENTER To Exit >\033[0m')







