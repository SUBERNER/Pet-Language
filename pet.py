from sly import Lexer, Parser
from time import sleep
import random

########################################
# PET STATUS # PET STATUS # PET STATUS #
########################################

class PetStatus:
    # stores the data of each need and how they work
    class Need():
        def __init__(self, alive: bool, current: float = 1, action: str = '', minmax: tuple[float,float] = tuple[0,2], drain: float = 0.1, gain: float = 0.1, delay: float = 1):
            self._alive = alive # a reference to the alive value in pet
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
                self._current = self._minmax[1] # sets current back within the maximum limits

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
    tokens = {NAME, NUMBER, STRING, TYPE}  # categorizes of each token that will be used
    ignore = '\t '  # tokens that are ignored by the program
    literals = {'=', '+', '-', '/', '%',
                '*', '(', ')', ',', ';'}  # simple tokens that will be required constantly

    # the format of NAME and STRING
    # first [] stores start with characters and second [] stores followed by characters
    TYPE = r'int|string'
    NAME = r'[a-zA-Z][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'  # strings must be double quote with anything in it

    # tokens for integer numbers
    @_(r'\d+')  # any digits
    def NUMBER(self, token):
        # makes value into python format
        token.value = int(token.value)
        return token

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
        ('right', '^'), # exponents
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.environment = {}

    @_('')
    def statement(self, parse):
        pass

    # used for variables and declaring variables
    # creating a variable with nothing assigned to it
    @_('var_declare')
    def statement(self, parse):
        return parse.var_declare

    # assigned an expression or operation to the variable with the type if the var is new
    @_('TYPE NAME "=" EXPR')
    def var_declare(self, parse):
        return 'var_declare', parse.TYPE, parse.NAME, parse.EXPR

    # used for variables and assigning variables
    # variables with something assigned to it
    @_('var_assign')
    def statement(self, parse):
        return parse.var_assign

    # assigned an expression or operation to the variable
    @_('NAME "=" EXPR')
    def var_assign(self, parse):
        return 'var_assign', parse.NAME, parse.EXPR

    # simply an expression or operation
    @_('EXPR')
    def statement(self, parse):
        return parse.EXPR

    # expressions and operations when dealing with math-based precedence
    # addition
    @_('EXPR "+" EXPR')
    def EXPR(self, parse):
        return 'add', parse.EXPR0, parse.EXPR1

    # subtraction
    @_('EXPR "-" EXPR')
    def EXPR(self, parse):
        return 'sub', parse.EXPR0, parse.EXPR1

    # multiplication
    @_('EXPR "*" EXPR')
    def EXPR(self, parse):
        return 'mul', parse.EXPR0, parse.EXPR1

    # division
    @_('EXPR "/" EXPR')
    def EXPR(self, parse):
        return 'div', parse.EXPR0, parse.EXPR1

    # remainder
    @_('EXPR "%" EXPR')
    def EXPR(self, parse):
        return 'rem', parse.EXPR0, parse.EXPR1

    # exponents
    @_('EXPR "^" EXPR')
    def EXPR(self, parse):
        return 'pow', parse.EXPR0, parse.EXPR1

    # negatives
    @_('"-" EXPR %prec UMINUS')
    def EXPR(self, parse):
        return parse.EXPR

    # simply a name
    @_('NAME')
    def EXPR(self, parse):
        return 'var', parse.NAME

    # simply a number
    @_('NUMBER')
    def EXPR(self, parse):
        return 'num', parse.NUMBER

    # simply a string
    @_('STRING')
    def EXPR(self, parse):
        return 'str', parse.STRING

###########################################
# PET EXECUTE # PET EXECUTE # PET EXECUTE #
###########################################

class PetExecute:
    def __init__(self, tree, environment):  #
        self.environment = environment  # stores the variables
        result = self.walk(tree)  # returns the full abstract syntax tree holding the split statements form the parser
        # prints results after the tree has been walked and the results of the statements have been made
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':  # test if a result is a string
            print(result)


    def walk(self, node):
        # returns if node is already a Python-based value
        if isinstance(node, int) or isinstance(node, str):
            return node

        # returns if no nodes where found
        if node == None:
            return None

        # returns the value if the node is a simple number or string
        if node[0] == 'num' or node[0] == 'str':
            return node[1]

        # returns the nodes value it after doing simple math
        if node[0] == 'add':
            return self.walk(node[1]) + self.walk(node[2])
        elif node[0] == 'sub':
            return self.walk(node[1]) - self.walk(node[2])
        elif node[0] == 'mul':
            return self.walk(node[1]) * self.walk(node[2])
        elif node[0] == 'div':
            return self.walk(node[1]) / self.walk(node[2])
        elif node[0] == 'rem':
            return self.walk(node[1]) % self.walk(node[2])
        elif node[0] == 'pow':
            return self.walk(node[1]) ** self.walk(node[2])

        # stores data inside variables inside the environment when declared
        if node[0] == 'var_declare':
            environmental_variable = {'type': node[1], 'value': self.walk(node[3])}
            self.environment[node[2]] = environmental_variable
            return node[1]

        # returns and stores data inside variables that are stored in the environment
        # only works for variables that already exist
        if node[0] == 'var_assign':
            self.environment[node[1]]['value'] = self.walk(node[2])
            return node[1]

        # returns the value of the variable asked for
        if node[0] == 'var':
            try:
                return self.environment[node[1]]['value']  # tries to find variable and its data
            except LookupError:  # if no variable or data was found
                print(f"< '{node[1]}' Undefined >")  # only displays name of variable
                return 0


######################
# MAIN # MAIN # MAIN #
######################

# runs everything to collect user inputs, and output results from user inputs
if __name__ == '__main__':
    lexer = PetLexer()
    parser = PetParser()
    status = PetStatus()
    print(f"Take Care Of Your New Pet")
    print(f"{status.name} Is Your Pet's Name")
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
            print(list(lexer.tokenize(command)))  # DEBUGGING ONLY
            tree = parser.parse(lexer.tokenize(command))  # splits command between spaces
            PetExecute(tree, environment)  # runs the commands

    # makes user press something ENTER before the program fully closes
    input(f'< Press ENTER To Exit >')







