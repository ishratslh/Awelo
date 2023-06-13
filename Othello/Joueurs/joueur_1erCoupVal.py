import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer qui est le premier coup valide
    """
    return game.getCoupsValides(jeu)[0]
