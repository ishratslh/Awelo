import sys
sys.path.append("../..")
import game
import random

#Idée: Certaines branches de l'arbre peuvent etre evitees parce qu'elles sont inutiles

SCORE= 0.2
LIGNE = -0.2
DIFF = 0.1
LIGNEADV = -0.1

coefficients = [SCORE, LIGNE, DIFF, LIGNEADV]

Pmax = 3
monJoueur = None
nbNoeuds = 0

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global monJoueur
    monJoueur = game.getJoueur(jeu)

    return decision(jeu)

def decision(jeu):
    """retourne le meilleur coup"""
    alpha = float("-inf") #Valeur du meilleur coup trouve (La plus grande valeur) jusqu'a Max
    beta  = float("inf")  #Valeur du Pire coup trouve (La plus grande valeur) jusqu'a Min
    valMax=None
    coupMax=None

    listeCoupsVal = game.getCoupsValides(jeu)
    for coup in listeCoupsVal:
        copie = game.getCopieJeu(jeu)
        game.joueCoup(copie, coup)

        val = estimationBetaMin(copie, alpha, beta)
        global nbNoeuds
        nbNoeuds+=1
        if valMax is None or val>valMax:
            valMax=val
            coupMax=coup

        alpha = max(alpha, val)

    return coupMax

def estimationAlphaMax(jeu, alpha, beta, p=1):
    """retourne une estimation Amax à une certaine profondeur donnée"""
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
        v = estimationBetaMin(copie, alpha, beta, p+1)
        global nbNoeuds
        nbNoeuds+=1
        if Vmax<v :
            Vmax = v
        if Vmax >= beta:  #Si Val > Beta  la branche est evitee
            return Vmax
        alpha = max(alpha, Vmax)
    return Vmax

def estimationBetaMin(jeu, alpha, beta, p=1):
    """retourne une estimation Bmin à une certaine profondeur donnée"""
    if game.finJeu(jeu):
        gagnant = game.getGagnant(jeu)
        if gagnant == monJoueur:
            return 1000
        else:
            return -1000
    if p == Pmax: return evaluation(jeu)
    Vmin=float("inf")
    listeCoupsVal = game.getCoupsValides(jeu)
    for coup in listeCoupsVal:
        copie = game.getCopieJeu(jeu)
        game.joueCoup(copie, coup)
        v = estimationAlphaMax(copie,alpha, beta, p+1)
        global nbNoeuds
        nbNoeuds+=1
        if Vmin>v :
            Vmin = v
        if Vmin <= alpha: #Si Val < Alpha la branche est evitee
            return Vmin
        beta = min(beta, Vmin)
    return Vmin

def scores(jeu):
    """ jeu -> list
        retourne une liste des scores d'evaluation
    """
    return [evaluationScore(jeu), evaluationLigne(jeu), evaluationDifference(jeu), evaluationLigneAdv(jeu)]

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
    """Attribue un score au coup : retourner le coup qui donne le meilleur resultat en faisant une difference de scores"""
    return game.getScore(jeu, monJoueur)-game.getScore(jeu, monJoueur%2+1)

def evaluationDifference(jeu):
    """Attribue un score au coup : retourne la difference des graines entre notre camp et le camp adverse"""
    adv = monJoueur % 2 + 1
    if(monJoueur == 1):
        mesCases = jeu[0][0]
        casesAdv = jeu[0][1]
    else:
        mesCases = jeu[0][1]
        casesAdv = jeu[0][0]

    return sum(mesCases)-sum(casesAdv)

def evaluationLigne(jeu):
    """Attribue un score au coup : Ne pas avoir de cases avec des 1 et 2 graines dans notre camp sinon malus"""
    if(monJoueur == 1):
        mesCases = jeu[0][0]
    else:
        mesCases = jeu[0][1]

    comp=6
    for i in mesCases:
        if(i in [1,2]):
            comp-=1

    return comp

def evaluationLigneAdv(jeu):
    """Attribue un score au coup : Avoir des cases avec des 1 et 2 graines dans le camp de l'adversaire"""
    if(monJoueur == 1):
        casesAdv = jeu[0][1]
    else:
        casesAdv = jeu[0][0]
    comp=0
    for i in casesAdv:
        if(i in [1,2]):
            comp+=1

    return comp
