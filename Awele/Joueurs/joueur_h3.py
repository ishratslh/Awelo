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
    listeCoupsVal = game.getCoupsValides(jeu) #Recupere la liste des coups valides
    listeEstimation = []

    for coup in listeCoupsVal : #parcourt la liste des coups valides et joue coup horizon 1
        listeEstimation.append(estimation( jeu,coup, 2 , jeu[4][jeu[1]-1], 0)) #ajoute a la liste l'estimation du coup a horizon2
        """jeu[4][jeu[1]-1] = Score du joueur actuel"""


    listeMin = []

    for i in listeEstimation :
        """Recupere les minimums de listeEstimation (liste de liste de liste) Faire un truc recurzif"""
        temp = []
        if i == [] : temp.append(0)
        else :
            for j in i :
                if j == [] :
                    temp.append(0)
                else :
                    temp.append(min(j))
        listeMin.append(min(temp))

    #print(listeMin)

    return listeCoupsVal[listeMin.index(max(listeMin))]

"""
def estimation(jeu, coup, profondeur, Score, Min ):
    copie = game.getCopieJeu(jeu)

    if profondeur == 0 :
        Resultat = evaluation(copie, Score, coup)
        return Resultat

    game.joueCoup(copie, coup)
    listeCoupsVal = game.getCoupsValides(copie) #Recupere la liste des coups valides
    return [estimation(copie, coup, profondeur-1, Score, Min ) for coup in listeCoupsVal ]
"""

def estimation( jeu, coup, profondeur, Score, Min ):
    copie = game.getCopieJeu(jeu)
    game.joueCoup( copie, coup )
    listeCoupsValide = game.getCoupsValides(copie)
    Resultat = []

    if profondeur == 1 :
        for coupValide in listeCoupsValide :
            note = evaluation(copie, Score, coupValide)
            Resultat.append(note)
            if  note < Min :
                return  Resultat
        return Resultat

    return [estimation(copie, Coup, profondeur-1, Score, Min ) for Coup in listeCoupsValide ]

def evaluation(jeu, score, coup):
    """joue sur la copie du jeu (est) et attribue un score au coup"""
    game.joueCoup(jeu, coup)
    return jeu[4][jeu[1]-1]-score
