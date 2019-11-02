if __name__ == "__main__":
    s = "Hola %d "
    a = 2
    aux = ""
    for char in s:
        if char == "%":
            aux = aux + str(a)
            char = char + 1 
        else:
            aux = aux + char

    print(aux)