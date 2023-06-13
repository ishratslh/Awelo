import sys
sys.path.append("..")
sys.path.append("./Joueurs")
import game
import awele
game.game=awele
import joueur_h1
import joueur_h2
import joueur_AB
import joueur_humain
import joueur_MiniMax
import joueur_aleatoire
import joueur_1erCoupVal
#import joueur_h3
#import joueur_ABfix
#import joueur_apprenti

def jouerNparties( J1, J2, n=1, affiche = False ):
    """ Permet de lancer un nombre n de parties et d'afficher ou non les parties
    """
    gagnant = 0
    matchNull = 0
    VictoireJ1 = 0
    VictoireJ2 = 0

    game.joueur1= J1
    game.joueur2= J2

    for i in range (n) :
        gagnant = game.unePartie(affiche)
        if    (gagnant == 1) : VictoireJ1 += 1
        elif  (gagnant == 2) : VictoireJ2 += 1
        else : matchNull += 1

    print("Nombre de victoire de Joueur1 : " , VictoireJ1 , " , " ,( 100 * VictoireJ1 /n ) ,"% des parties  " )
    print("Nombre de victoire de Joueur2 : " , VictoireJ2 , " , " ,( 100 * VictoireJ2 /n ) ,"% des parties\n" )

jouerNparties( joueur_aleatoire, joueur_MiniMax, 1,True)
