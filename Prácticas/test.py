if __name__ == "__main__":
    v = []
    v.insert(0, 3)
    v.insert(0, 2)
    v.insert(0, 1)
    s = "Hola %d %d %d"
    aux = s.replace("%d", str(v.pop()), 1)
    while aux.find("%d") > -1:
        aux = aux.replace("%d", str(v.pop()),1)
    print(aux)
