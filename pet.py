from sly import Lexer, Parser

class PetNeeds:
    hunger = 1  # stores how hungry the pet is
    thirst = 1  # stores how thirsty the pet is
    energy = 1  # stores how much energy the pet has left


class PetLexer(Lexer):
    tokens = {NAME, NUMBER, STRING}  # categorizes of each token that will be used
    ignore = '\t '  # tokens that are ignored by the program
    literals = {'=', '+', '-', '/', '%',
                '*', '(', ')', ',', ';'}  # simple tokens that will be required constantly

    # the format of NAME and STRING
    # first [] stores start with characters and second [] stores followed by characters
    NAME = r'[a-zA-Z][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'  # strings must be double quote with anything in it

    # tokens for numbers
    @_(r'\d+')  # any digits
    def NUMBER(self, token):
        # makes value into python format
        token.value = int(token.value)
        return token

    # token for comments
    @_(r'#.*')
    def COMMENT(self, token):
        pass  # passes due to code not running from comments

    # ADD TOKEN FOR COMMENT BLOCKS


class PetParser(Parser):
    # tokens being given from lexer to parser
    tokens = PetLexer.tokens

    # order of operations/processors in operations, math, and logic
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', '^'),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.environment = {}

    @_('')
    def statement(self, parse):
        pass

    # used for variables and assigning variables
    # creating a variable with nothing assigned to it
    @_('var_assign')
    def statement(self, parse):
        return parse.var_assign

    # assigned an expression or operation to the variable
    @_('NAME "=" EXPR')
    def var_assign(self, parse):
        return 'var_assign', parse.NAME, parse.EXPR

    # assigned a string to the variable
    @_('NAME "=" STRING')
    def var_assign(self, parse):
        return 'var_assign', parse.NAME, parse.STRING

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
            print(self.walk(node[1]) / self.walk(node[2]))
            return self.walk(node[1]) / self.walk(node[2])
        elif node[0] == 'rem':
            return self.walk(node[1]) % self.walk(node[2])
        elif node[0] == 'pow':
            return self.walk(node[1]) ** self.walk(node[2])

        # returns and stores data inside variables that are stored in the environment
        if node[0] == 'var_assign':
            self.environment[node[1]] = self.walk(node[2])
            return node[1]

        # returns the value of the variable asked for
        if node[0] == 'var':
            try:
                return self.environment[node[1]]  # tries to find variable and its data
            except LookupError:  # if no variable or data was found
                print(f"< '{node[1]}' Undefined >")
                return 0


# runs everything to collect user inputs and output results from user inputs
if __name__ == '__main__':
    lexer = PetLexer()
    parser = PetParser()
    print("Take Care Of Your Pet")
    environment = {}  # all variables that are kept between each command a user makes

    # continues until an error occurs or user end process
    while True:
        try:
            command = input('Pet Language: ')

        except EOFError:
            break

        # if commands form user was received
        if command:
            tree = parser.parse(lexer.tokenize(command))  # splits command between spaces
            PetExecute(tree, environment)  # runs the commands







