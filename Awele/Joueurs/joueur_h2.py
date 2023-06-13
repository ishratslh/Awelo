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
    listeCoupVal = game.getCoupsValides(jeu) #Recupere la liste des coups valides
    listeEstimation = []
    Min = 0
    for coup in listeCoupVal : #parcourt la liste des coups valides et joue coup horizon 1
        copie = game.getCopieJeu(jeu)
        listeEstimation.append(estimation(copie, coup, 2 , jeu[4][jeu[1]-1], Min)) #ajoute a la liste l'estimation du coup a horizon2
        """jeu[4][jeu[1]-1] = Score du joueur actuel"""
    return listeCoupVal[listeEstimation.index(max(listeEstimation))]

def estimation(jeu, coup, profondeur, Score, Min ):
    """prend une copie du jeu, et retourne une estimation à une certaine profondeur donnée"""
    game.joueCoup(jeu, coup)
    lVal=game.getCoupsValides(jeu)
    Resultat = Min
    for coup in lVal : #parcourt la liste des coups valides et joue coup horizon 2
        copie=game.getCopieJeu(jeu)
        Resultat = evaluation(copie, Score, coup)
        if Resultat < Min : break
        else : Min = Resultat
    return Min

def evaluation(jeu, score, coup):
    """joue sur la copie du jeu (est) et attribue un score au coup"""
    game.joueCoup(jeu, coup)
    return jeu[4][jeu[1]-1]-score
