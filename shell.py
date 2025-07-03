import basic
    

while True:
    text = input('basic-')
    # print(text)
    # result is gotten from the run function, the run function returns tokens gotten from the make_tokens function 
    # or the abstract syntax tree from the parse.parse function
    # or the interpreter.visit method
    #   ^
    #   |
    result,error = basic.run("<stdin>", text)

    if error: print(error.as_string())
    
    else: print(result)

