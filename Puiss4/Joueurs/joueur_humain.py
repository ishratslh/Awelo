import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    while True:
        try:
            y = int(input("Saisir le numero de la colonne : "))
            break
        except ValueError:
            print("Ceci n'est pas un chiffre\n")
    return (0,y)
