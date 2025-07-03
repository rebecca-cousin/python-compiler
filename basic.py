# ERROR MESSAGES
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}:{self.details}  "
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += "\n\n" + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start , pos_end ,details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)

class IllegalSyntaxError(Error):
    def __init__(self, pos_start , pos_end ,details):
        super().__init__(pos_start, pos_end, "Illegal Syntax Error", details)

class RuntimeError(Error):
    def __init__(self, pos_start , pos_end ,details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context


#POSITIONING 
class Position:
    def __init__(self, idx, ln, col, fn, ftxt): #idx = index, ln = line number, col = column, fn = filename, ftxt = filetext
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1 #or otherwise move to the next character
        self.col += 1

        if current_char == "\n": #\n obviously representing a new line
            self.ln += 1 #meaning go to a new line
            self.col = 0 #column is set to 0 because its a new line

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#IMPORTS
from strings_with_arrows import *

import string

# INTEGERS
DIGITS = "0123456789"
LETTERS = string.ascii_letters + ">"
LETTERS_DIGITS = LETTERS + DIGITS

# TOKENS
# TT meaning token type


TT_INT = "INT"                  #integer
TT_FLOAT = "FLOAT"              #float
TT_IDENTIFIER = "IDENTIFIER"    #string for variableName
TT_EQ = "EQ"
TT_PLUS = "PLUS"                #plus(+)
TT_MINUS = "MINUS"              #minus(-)
TT_MUL = "MUL"                  #multipication(*)
TT_DIV = "DIV"                  #division(/)
TT_POW = "POW"                  #power operator(**) 
TT_LPAREN = "LPAREN"            #left parentheses or bracket('(')
TT_RPAREN = "RPAREN"            #right parentheses or bracket(')')
TT_EOF = "EOF"                  #end of file   
TT_KEYWORD = "KEYWORD"          #keywords in python
TT_PRINT = "PRINT"              #print statement  
TT_NEWLINE = "NEWLINE"          #newline 


KEYWORDS = ["VAR", ">", "LET", "PRINT", "print"]

class Token:      #A token just has a type and a value
    def __init__(self, type_,value=None, pos_start=None,pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_start.copy()

    def matches(self, type_, value=None):
        return self.type == type_ and self.value == value

    def __repr__(self):     #This function is for tokens which do not have values
        if self.value: return f'{self.type}:{self.value}' #If the token has a value then return both the type and the value
        return f'{self.type}'    #If the token doesnt have a value then just return the tokens type alone


# LEXICAL ANALYSER

class Lexer: #This is to create the lexical analyser 
    def __init__(self, fn, text):         #Ideally a scanner only needs the text in order to convert it into tokens but the filename was passed here for error handling
        self.fn = fn
        self.text = text                   #function to read in the text from source code
        self.pos = Position(-1, 0, -1, fn, text)    #function to monitor the current position of each character
        self.current_char = None          # function to know which character its currently on
        self.advance()                     #calls the function which tuns trhough the text


    def advance(self):        #This is to kind of iterate over the text
        self.pos.advance(self.current_char)    #increment the position object (index and column) by 1
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None #track the character its currently on but will stop when the lenght of the text is reached


    def make_tokens(self): #change this to generate tokens
        tokens = [] #all the tokens will be stored in this list
            
        while self.current_char != None:
                if self.current_char in " \t":
                    self.advance()
                elif self.current_char in LETTERS + ">":
                    tokens.append(self.make_identifier())
                elif self.current_char.isalpha():
                    tokens.append(self.make_identifier())
                elif self.current_char in DIGITS + ".": #a dot was added because it could be a floating point number
                    tokens.append(self.make_number())   # because a number can be more than one character, we call the make number function
                elif self.current_char == "=":
                    tokens.append(Token(TT_EQ, pos_start=self.pos))
                    self.advance()
                elif self.current_char == "+":
                    tokens.append(Token(TT_PLUS , pos_start=self.pos))
                    self.advance()
                elif self.current_char == "-":
                    tokens.append(Token(TT_MINUS, pos_start=self.pos))
                    self.advance()
                elif self.current_char == "*":
                    self.advance()
                    if self.current_char == "*":
                        tokens.append(Token(TT_POW, pos_start=self.pos))
                    else:
                        tokens.append(Token(TT_MUL, pos_start=self.pos))
                    self.advance()
                elif self.current_char == "/":
                    tokens.append(Token(TT_DIV, pos_start=self.pos))
                    self.advance()
                elif self.current_char == "(":
                    tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                    self.advance()
                elif self.current_char == ")":
                    tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                    self.advance()
                elif self.current_char == "\n":
                    tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                    self.advance()
                else:
                    print(self.current_char)
                    pos_start = self.pos.copy()
                    # char = self.current_char  
                    return [], IllegalCharError(pos_start, self.pos, "'" + str(self.current_char) + "'")
                    # self.advance() 


        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None #return the tokens list

        #Function to make numbers (because it can either be an integer or a floating point number)
        #The idea is to just iterate over the number and add every character to a string,, obv a loop would be needed
        #In the iteration of the number if a '.' is spotted, the number is taken to be a float and if not it is an Integer
    def make_number(self):
        num_str = ""   #This variable represents the number we want to return but in string format
        dot_count = 0  #This variable helps us differentiate floating point values from integers.
        pos_start = self.pos.copy()
       
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1: break #this line is basically for error handling as well. We normally increment the 
                #dot count by 1 when we see a . However if the dot count is already 1 then we just break.
                dot_count += 1 
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 1:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
        else:
            return Token(TT_INT, int(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = "" #variable to store the identifier
        pos_start = self.pos.copy()

        while self.current_char != None and (self.current_char.isalnum() or self.current_char in LETTERS_DIGITS + "_" + ">"):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)


#NODES
class NumberNode:  #NumberNode class declaration. basically a number
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self): # returns the number token as a string
        return f"{self.tok}"

class VarAccessNode: #this node is for variable access, meaning to access the value of the variable
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode: #this node is to allow for variable declaration and assignment
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class PrintNode:
    def __init__(self, value_node):
        self.value_node = value_node
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f'PRINT({self.value_node})'

class BinOpNode: #Create a binary operation node (2 + 3) is a binary operation 
    def __init__(self, left_node, op_tok, right_node): # in this now 2 is the leftnode, + is the op_tok, 3 is the right_node  
        #or in the example (2 * 3 + 4 / 5) - (2 * 3 is the left node), + is the op_tok and (4 / 5 is the right node)
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node


        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"



#PARSE RESULT
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self




##PARSER or SYNTAX ANALYSER
class Parser:   #Creating the parser class
    def __init__(self,tokens): #the parser just takes in the tokens and if all goes well, generates an ABS for the grammar
        self.tokens = tokens
        self.tok_idx = -1 #meaning token index 
        self.advance() #for the parser to iterate over the tokens
        self.variables = {}

    def advance(self): # i feel it should have self passed as an argument sha
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    #ParseFunction 
    def parse(self):  #parse function to return the expression
        res = self.expr()    
        # if res.error and self.current_tok != TT_EOF:  #There is supposed to be a not here. This line of code is to check whether or not we have reached the end of the file
            # return res.failure(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*' or '/'"))
        return res

    def factor(self):  # i feel it should have self passed as an argument sha
        res = ParseResult()
        tok = self.current_tok

        #functionality for unary operations (-2 or -13.4)
        if tok.type in (TT_PLUS, TT_MINUS):       #if the token is a plus or a minus
            res.register(self.advance())          #move to the next token
            factor = res.register(self.factor())  #get the factor meaning the number or numbers after the initial plus or minus
            if res.error: return res              #if there is an error return the error
            return res.success(UnaryOpNode(tok, factor)) #if there isn't an error, return the unary operation node

        #functionality for classic numbers
        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            return res.success(VarAccessNode(tok))

        #functionality for brackets and changing order of operation
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))

        elif tok.type == TT_KEYWORD and tok.value == 'PRINT' or tok.value == "print":
            # res.register_advancement()
            self.advance()
            if self.current_tok.type == TT_LPAREN:
                # res.register_advancement()
                self.advance()
                value = res.register(self.expr())
                if res.error: return res
                if self.current_tok.type == TT_RPAREN:
                    # res.register_advancement()
                    self.advance()
                    return res.success(PrintNode(value))
                else:
                    return res.failure(IllegalSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')'"
                    ))
            else:
                return res.failure(IllegalSyntaxError(
                    tok.pos_start, tok.pos_end,
                    "Expected '('"
                ))
    
        #This is the main error, it returns when an individual doesnt pass in an integer or a floating point number
        return res.failure(IllegalSyntaxError(tok.pos_start, tok.pos_end, "Expected integer or floating point number"))

    def term(self):  
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_POW))

    def expr(self):
        res = ParseResult()

        while self.current_tok.type == TT_NEWLINE:
            self.advance()

        if self.current_tok.matches(TT_KEYWORD, ">"):
            # res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier"))
        
            var_name = self.current_tok
        # res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))
        
        # res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))


        node = res.register(self.bin_op(self.term, (TT_PLUS, TT_MINUS)))

        if res.error:
            return res.failure(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'VAR', int , float, identifier, '+', '-', or ')' "))

        return res.success(node)


    def bin_op(self, func, ops): #the function bin_op is to make a general function that can make both terms and expressions
        res = ParseResult() #Creates a new parse result
        left = res.register(func())  #depending on the input passed, this left could return another binary expression (term)
        if res.error: return res #If theres an error in getting the factor or a nested bin_op, itll return the 'return res.failure(IllegalSyntaxError(tok.pos_start, tok.pos_end, "Expected integer or floating point number"))' error

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func()) #depending on the input passed, this right could return another binary expression (term)  
            if res.error: return res     #If theres an error in getting the factor or a nested bin_op, itll return the 'return res.failure(IllegalSyntaxError(tok.pos_start, tok.pos_end, "Expected integer or floating point number"))' error

            left = BinOpNode(left, op_tok, right)

        return res.success(left) #If finally there are no errors it will return the node successfully


#RUNTIME RESULT
class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self,res):
        if res.error: self.error = res.error
        return res.value

    def success(self,value):
        self.value = value
        return self

    def failure(self,error):
        self.error = error
        return error
        
    
#VALUES
class Number:
    def __init__(self,value):
        self.value = value
        self.set_pos()
        self.set_context()


    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if  isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtraced_by(self, other):
        if  isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        if  isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def raised_to(self,other):
        if isinstance(other,Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def divided_by(self, other):
        if  isinstance(other, Number):
        ############################################################################################
        #    if other.value == 0:                                                                  #
        #        return None, RuntimeError(other.pos_start, other.pos_end, "Cannot Divide by Zero")#
        ############################################################################################
            return Number(self.value / other.value).set_context(self.context), None
	
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

#CONTEXT
class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None


#SYMBOL TABLE
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self,name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self,name):
        del self.symbols[name]



#INTERPRETER
class Interpreter:
    def visit(self,node, context):
        method_name = f'visit_{type(node).__name__}' #this will return the className of the node. So for (1 + 2) it will return BinOpNode (but in actuality - visit_BinOpNode)
        # print(method_name)
        method = getattr(self, method_name, self.no_visit_method) #this will return the attributes of the class that was returned
        # print(method) 
        return method(node,context) #this will evaluate the method, for example: 

    def no_visit_method(self, node,context):
        raise Exception(f'No visit_{type(node).__name__} method defined') #this is the default method, for when no class is returned

    def visit_VarAccessNode(self,node,context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if value is None:
            res.failure(RuntimeError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))

        # value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node,context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        # print(value)
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_PrintNode(self, node, context):
        res = RTResult()
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        # print(value)
        return res.success(value)


    def visit_NumberNode(self,node,context):
        # print("Number Node Found")
        return RTResult().success(
        Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end) 
        )

    def visit_BinOpNode(self,node, context):
        # print("Found binary operator node")
        res = RTResult()
        left = res.register(self.visit(node.left_node, context)) #this returns a NumberNode which would eventually return a number - the left number
        if res.error: return res
        right = res.register(self.visit(node.right_node, context)) #this returns a NumberNode which would eventually return a number - the left number
        if res.error: return res


        if node.op_tok.type == TT_PLUS: #if the operator token is plus(+)
            result, error = left.added_to(right) #call the add function on the two numbers (generated through left and right)
        if node.op_tok.type == TT_MINUS: #if the operator token is plus(-)
            result, error = left.subtraced_by(right) #call the subtract function on the two numbers (generated through left and right)
        if node.op_tok.type == TT_MUL: #if the operator token is multiply(*)
            result, error = left.multiplied_by(right) #call the multiplication function on the two numbers (generated through left and right)
        if node.op_tok.type == TT_DIV: #if the operator token is divide(/)
            result, error = left.divided_by(right) #call the division function on the two numbers (generated through left and right)
        if node.op_tok.type == TT_POW: #if the operator is exponent(**)
            result,error = left.raised_to(right) #call the power function on the two numbers (generated through left and right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self,node,context):
        # print("Found Unary Operator Node")
        res = RTResult()
        number = res.register(self.visit(node.node, context)) #this checks the unary operation (e.g -5), so it would get 5 and put it in the number variable
        if res.error: return res

        error = None

        if node.op_tok.type == TT_MINUS: #so if the operation type is a minus 
            number,error = number.multiplied_by(Number(-1)) #then it would multiply the number by minus 1 making it a negative number
        
        if error:
            return res.failure(error) 
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))


#Function to run the code

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))


def run(fn, text):
    #Generate Tokens
    lexer = Lexer(fn, text) #create a new lexer object that uses the text inputted by the user
    tokens, error = lexer.make_tokens() #get the tokens and the error
    if error: return None, error 
    # return tokens,error

    #Generate Abstract Syntax Tree
    parser = Parser(tokens) #create a new parser object
    parser.TT_KEYWORD = TT_KEYWORD
    parser.TT_PRINT = TT_PRINT
    # print(tokens)
    ast = parser.parse() #this would return the abstract syntax tree
    if ast.error: return None, ast.error
    # return ast.node, ast.error

    #Run Program with Interpreter
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node,context)
    
    # return result, None
    return result.value, result.error





















