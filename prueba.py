def main():
    oracion = 'Mary entiende muy bien Python'
    frases = oracion.split() # convierte a una lista cada palabra
    print ("La oración analizada es:", oracion, ".\n")
    for palabra in range(len(frases)):
        print ("Palabra: {0}, en la frase su posición es: {1}".format(frases[palabra], palabra))
if __name__ == "__main__":
    main()