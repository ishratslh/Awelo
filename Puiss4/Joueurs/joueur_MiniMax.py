import sys
sys.path.append("../..")
import game
import random

#Idée: Choisir le coup avec la meilleure valeur de minimax = meilleure situation atteignable contre le meilleur coup

XC    = 0
POS   = 0
COIN  = 0
SCORE = 0

coefficients = [SCORE, COIN, XC, POS]

positions = [[ 120, -20, 20,  5,  5, 20, -20, 120],
             [ -20, -40, -5, -5, -5, -5, -40, -20],
             [  20,  -5, 15,  3,  3, 15,  -5,  20],
             [   5,  -5,  3,  3,  3,  3,  -5,   5],
             [   5,  -5,  3,  3,  3,  3,  -5,   5],
             [  20,  -5, 15,  3,  3, 15,  -5,  20],
             [ -20, -40, -5, -5, -5, -5, -40, -20],
             [ 120, -20, 20,  5,  5, 20, -20, 120]]

Pmax = 2
monJoueur = None

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global monJoueur
    monJoueur = game.getJoueur(jeu)

    return decision(jeu)

def decision(jeu):
    """retourne le meilleur coup"""
    coupMax=None
    valMax=None
    listeCoupsVal = game.getCoupsValides(jeu)

    for coup in listeCoupsVal:
        copie = game.getCopieJeu(jeu)
        game.joueCoup(copie, coup)

        val = estimationMin(copie)
        if valMax is None or val>valMax:
            valMax=val
            coupMax=coup

    return coupMax

def estimationMax(jeu, p=1):
    """retourne une estimation max à une certaine profondeur donnée"""
    if game.finJeu(jeu):
        gagnant = game.getGagnant(jeu)
        if gagnant == monJoueur:
            return 1000
        else:
            return -1000

    if p == Pmax:
        return evaluation(jeu)

    Vmax=float("-inf")
    listeCoupsVal = game.getCoupsValides(jeu)
    for coup in listeCoupsVal:
        copie = game.getCopieJeu(jeu)
        game.joueCoup(copie, coup)

        v = estimationMin(copie,p+1)
        if Vmax<v :
            Vmax = v

    return Vmax

def estimationMin(jeu, p=1):
    """retourne une estimation min à une certaine profondeur donnée"""
    Vmin=float("inf")
    if game.finJeu(jeu):
        gagnant = game.getGagnant(jeu)
        if gagnant == monJoueur :
            return 1000
        else :
            return -1000

    if p == Pmax:
        return evaluation(jeu)

    for coup in game.getCoupsValides(jeu):
        copie = game.getCopieJeu(jeu)
        game.joueCoup(copie, coup)

        v = estimationMax(copie,p+1)
        if  Vmin > v :
            Vmin = v

    return Vmin

def scores(jeu):
    """ jeu -> list
        retourne une liste des scores d'evaluation
    """
    return [evaluationScore(jeu), evaluationCoin(jeu), evaluationXC(jeu), evaluationPos(jeu)]

def dot(jeu, coeff):
    """ jeu, coeff(list) -> float
        produit scalaire de liste des evaluations et coefficients
    """
    evaluations = scores(jeu)
    if (len(evaluations) == len(coeff)):
        s=0
        for i in range(len(coeff)):
            s+=coeff[i]*evaluations[i]
    return s

def evaluation(jeu):
    return dot(jeu, coefficients)

def evaluationScore(jeu):
    """Attribue un score au coup : retourner le coup qui donne le meilleur resultat"""
    return game.getScore(jeu, monJoueur)-game.getScore(jeu, monJoueur%2+1)

def evaluationCoin(jeu):
    """Attribue un score au coup : le nombre de pions en coin de monJoueur"""
    comp=0
    for i in 0,7:
        for j in 0,7:
            if(jeu[0][i][j] == monJoueur):
                comp+=1
    return comp

def evaluationXC(jeu):
    """Attribue un score au coup : le nombre de pions autour du coin de monJoueur"""
    comp=0
    for i in 0,1,6,7:
        for j in 0,1,6,7:
            if((i,j) != (0,0) and (i,j) != (7,7) and (i,j) != (0,7) and (i,j) != (7,0)):
                if(jeu[0][i][j] == monJoueur):
                    comp+=1
    return comp

def evaluationPos(jeu):
    """Attribue un score au coup :  la somme des points selon la position dans le plateau de mon Joueur"""
    plateau=game.getPlateau(jeu)
    comp=0
    for i in range(8):
        for j in range(8):
            if(plateau[i][j]==monJoueur):
                comp+=positions[i][j]
    return comp
