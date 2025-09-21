from sly import Lexer, Parser

class PetNeeds():
    hunger = 1  # stores how hungry the pet is
    thirst = 1  # stores how thirsty the pet is
    energy = 1  # stores how much energy the pet has left


class PetLexer(Lexer):
    tokens = {NAME, NUMBERS, STRING}  # categorizes of each token that will be used
    ignore = '\t'  # tokens that are ignored by the program
    literals = {'=', '+', '-', '/', '%',
                '*', '(', ')', ',', ';',
                '{', '}', '[', ']'}  # simple tokens that will be required constantly

    # the format of NAME and STRING
    # first [] stores start with characters and second [] stores followed by characters
    NAME = r'[a-zA-Z][a-zA-Z_]'
    STRING = r'\".*?\"'  # strings must be double quote with anything in it

    # tokens for numbers
    @_(r'\d+')  # any digits
    def NUMBER(self, token):
        # makes value into python format
        token.value, = int(token.vlaue)
        return token

    # token for comments
    @_(r'#.*')
    def COMMENT(self, token):
        pass  # passes due to code not running from comments


class PetParser(Parser):
    # tokens being given from lexer to parser
    tokens = PetLexer.tokens

    # order of operations/processors in operations, math, and logic
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statment(self, parser):
        pass

    # used for variables and assigning variables
    # creating a variable with nothing assigned to it
    @_('var_assign')
    def statment(self, parser):
        return parser.var_assign

    # assigned an expression or operation to the variable
    @_('NAME' "=" 'EXPR')
    def var_assign(self, parser):
        return ('var_assign', parser.NAME, parser.EXPR)

    # assigned a string to the variable
    @_('NAME' "=" 'STRING')
    def var_assign(self, parser):
        return ('var_assign', parser.NAME, parser.STRING)

    # simply an expression or operation
    @_('EXPR')
    def statment(self, parser):
        return (parser.EXPR)

    # expressions and operations when dealing with math-based precedence
    # addition
    @_('EXPR' "+" 'EXPR')
    def EXPR(self, parser):
        return ('add', parser.EXPR0, parser.EXPR1)

    # subtraction
    @_('EXPR' "-" 'EXPR')
    def EXPR(self, parser):
        return ('sub', parser.EXPR0, parser.EXPR1)

    # multiplication
    @_('EXPR' "*" 'EXPR')
    def EXPR(self, parser):
        return ('mul', parser.EXPR0, parser.EXPR1)

    # division
    @_('EXPR' "/" 'EXPR')
    def EXPR(self, parser):
        return ('div', parser.EXPR0, parser.EXPR1)

    # remainder
    @_('EXPR' "%" 'EXPR')
    def EXPR(self, parser):
        return ('rem', parser.EXPR0, parser.EXPR1)

    # simply a name
    @_('NAME')
    def EXPR(self, parser):
        return ('var', parser.NAME)

    # simply a number
    @_('NUMBER')
    def EXPR(self, parser):
        return ('num', parser.NUMBER)




