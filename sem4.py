'''
Exercise 1

1) Tree in the picture

2)  
    S.s
    A.s
    ID.s
    X.lexval
    Y.lexval
    Z.lexval
    K.lexval
    
3)
    S.s := A.s
    A.s := A1.s*10 + ID.lexval
    ID.s := X.lexval
    ID.s := Y.lexval
    ID.s := Z.lexval
    ID.s := K.lexval
    X.lexval := 1
    Y.lexval := 2
    Z.lexval := 3
    K.lexval := 4

Exercise 2

1) Tree in the picture

2)
    S.s
    A.s
    ID.s
    X.lexval
    Y.lexval
    Z.lexval
    K.lexval

3)
    S -> {A1.h := A2.s;}A 
    A -> {ID.h = A1.h*10}ID + {A2.h = ID.s}A
    ID -> {}X
        | Y
        | Z
        | K
    X.lexval -> 1
    Y.lexval -> 2
    Z.lexval -> 3
    K.lexval -> 4
'''