import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    return decision(jeu)

def decision(jeu):
    """retourne le meilleur coup"""
    lVal=game.getCoupsValides(jeu)
    est=[]
    for coup in lVal:
        est.append(estimation(jeu, coup, 1))
    return lVal[est.index(max(est))]

def estimation(jeu, coup, profondeur=1):
    """prend une copie du jeu, et retourne une estimation à une certaine profondeur donnée"""
    copie=game.getCopieJeu(jeu)
    return evaluation(copie, copie[4][jeu[1]-1], coup)

def evaluation(jeu, score, coup):
    """joue sur la copie du jeu (est) et attribue un score au coup"""
    game.joueCoup(jeu, coup)
    return jeu[4][jeu[1]-1]-score
