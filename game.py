#!/usr/bin/env python
# -*- coding: utf-8 -*-

# plateau: List[List[nat]]
# liste de listes (lignes du plateau) d'entiers correspondant aux contenus des cases du plateau de jeu

# coup:[nat nat]
# Numero de ligne et numero de colonne de la case correspondante a un coup d'un joueur

# Jeu
# jeu:[plateau nat List[coup] List[coup] List[nat nat]]
# Structure de jeu comportant :
#           - le plateau de jeu
#           - Le joueur a qui c'est le tour de jouer (1 ou 2)
#           - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#           - La liste des coups joues jusqu'a present dans le jeu
#           - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2

game=None #Contient le module du jeu specifique: awele ou othello
joueur1=None #Contient le module du joueur 1
joueur2=None #Contient le module du joueur 2
import joueur_aleatoire
import joueur_h1


def unePartie(afficher=False,alea = True):
    jeu=game.initialiseJeu()
    it=0
    while ( not game.finJeu(jeu) ) :
        if (afficher) :
            affiche(jeu)
            print(getCoupsValides(jeu))
        if (alea and it<4) :                            #alea à initialiser : 4 premiers coups aléatoires (2 pour chaque joueur)
            coup=joueur_aleatoire.saisieCoup(jeu)
            game.joueCoup(jeu,coup)
        else :
            coup=saisieCoup(jeu)
            game.joueCoup(jeu,coup)
        it+=1

    if(afficher):
        if getGagnant(jeu)==0: print("Egalité \nScore du joueur 1 : ",getScores(jeu)[0],"\nScore du joueur 2 : ",getScores(jeu)[1])
        else: print("Le joueur ",getGagnant(jeu),"a gagné la partie \nScore du joueur 1 : ",getScores(jeu)[0],"\nScore du joueur 2 : ",getScores(jeu)[1])
    return getGagnant(jeu)


#Fonctions minimales

def getCopieJeu(jeu):
    """ jeu->jeu
        Retourne une copie du jeu passe en parametre
        Quand on copie un jeu on en calcule forcement les coups valides avant
    """
    return game.getCopieJeu(jeu)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu
    """
    return game.finJeu(jeu)

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
        On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
        et qu'elle retourne obligatoirement un coup valide
    """
    copieJeu=game.getCopieJeu(jeu)
    joueur=joueur1
    if (jeu[1]==2) :
        joueur=joueur2
    coup=joueur.saisieCoup(copieJeu)
    while ( not coupValide(jeu, coup)) :
        print("Coup non valide, réessayez !")
        coup = joueur.saisieCoup(copieJeu)
    return coup

def getCoupsValides(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups valides dans le jeu passe en parametre
        Si None, alors on met � jour la liste des coups valides
    """
    if jeu[2] is None:
        jeu[2]=game.listeCoupsValides(jeu)
    return jeu[2]

def coupValide(jeu,coup):
    """jeu*coup->bool
        Retourne vrai si le coup appartient a la liste de coups valides du jeu
    """
    listeCoupsValides=getCoupsValides(jeu)
    for c in listeCoupsValides :
        if (coup==c) :
            return True
    return False

def joueCoup(jeu,coup):
    """jeu*coup->void
        Joue un coup a l'aide de la fonction joueCoup defini dans le module game
        Hypothese:le coup est valide
        Met tous les champs de jeu à jour (sauf coups valides qui est fixée à None)
    """
    game.joueCoup(jeu,coup)

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    return game.initialiseJeu()

def getGagnant(jeu):
    """jeu->nat
    Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    game.finalisePartie(jeu)
    g=0
    if jeu[4][0]<jeu[4][1]:
        g=2
    if jeu[4][0]>jeu[4][1]:
        g=1
    return g

def affiche(jeu):
    """ jeu->void
        Affiche l'etat du jeu de la maniere suivante :
                 Coup joue = <dernier coup>
                 Scores = <score 1>, <score 2>
                 Plateau :

                         |       0     |     1       |      2     |      ...
                    ------------------------------------------------
                      0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                    ------------------------------------------------
                      1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                    ------------------------------------------------
                    ...       ...          ...            ...
                 Joueur <joueur>, a vous de jouer

         Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
    #listeCoup = getCoupsJoues(jeu)
    score = getScores(jeu)
    #print("Coup joue = " , listeCoup[len(listeCoup) -  1])
    print("Score = " , score[0] , " , " , score[1] )
    print("Plateau :")
    game.affiche(jeu)
    print("Joueur " , getJoueur(jeu) , ", a vous de jouer")

# Fonctions utiles

def getPlateau(jeu):
    """ jeu  -> plateau
        Retourne le plateau du jeu passe en parametre
    """
    return jeu[0]

def getCoupsJoues(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups joues dans le jeu passe en parametre
    """
    return jeu[3]

def getScores(jeu):
    """ jeu  -> Pair[nat nat]
        Retourne les scores du jeu passe en parametre
    """
    return jeu[4]

def getJoueur(jeu):
    """ jeu  -> nat
        Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
    """
    return jeu[1]

def changeJoueur(jeu):
    """ jeu  -> void
        Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
    """
    jeu[1]=jeu[1]%2+1

def getScore(jeu,joueur):
    """ jeu*nat->int
        Retourne le score du joueur
        Hypothese: le joueur est 1 ou 2
    """
    if joueur==1 :
        return jeu[4][0]
    else:
        return jeu[4][1]

def getCaseVal(jeu, ligne, colonne):
    """ jeu*nat*nat -> nat
        Retourne le contenu de la case ligne,colonne du jeu
        Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
    """
    return jeu[0][ligne][colonne]
