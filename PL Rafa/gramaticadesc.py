# entry -> line ';' entry 
#       -> Epsilon

# line -> definition 
#      -> instruction 

# defnition -> type aux

# aux  -> name aux_ 
# aux_ -> ',' name aux_
#      -> Epsilon

# name -> ID 
#      -> pointer ID 
#      -> ID dim

# type -> INT 
#      -> CHAR 
#      -> FLOAT  

# pointer -> '*' pointer 
#         -> '*'

# dim -> '[' NINT ']' dim 
#     -> '[' NINT ']'

# instruction -> assign 
#             -> var 
#             -> '&' ID

# assign -> var '=' expr

# var -> ID 
#     -> pointer ID 
#     -> ID vector

# vector -> '[' value ']' vector 
#        -> '[' value ']'

# value -> ID 
#        -> pointer ID 
#        -> num 
    
# num -> NINT 
#     -> NFLOAT
    
# expr -> sum '+' expr 
#      -> sum

# sum -> factor '*' sum 
#     -> factor 

# factor -> var 
#        -> num 
#        -> '(' expr ')'