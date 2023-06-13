import sys
sys.path.append("../.")
sys.path.append("../../.")
sys.path.append("../Joueurs")
import game
import othello
import joueur_humain
import tkinter as tk

game.game=othello
game.joueur1=joueur_humain
game.joueur2=joueur_humain

TailleLinux   = [181,127, 20, 7, 4] #Ordinateur de la ppti
TailleWindows = [109, 80, 15, 5, 7] #Ordinateur personelle

Taille = TailleWindows

fenetre = tk.Tk()

pionsNoir  = tk.PhotoImage ( file = "Images/pionNoir.png")
pionsBlanc = tk.PhotoImage ( file = "Images/pionBlanc.png")

pionsNoir  = pionsNoir.subsample(Taille[4])
pionsBlanc = pionsBlanc.subsample(Taille[4])

l = [] #liste contenant les boutons tk.Button
jeu = game.initialiseJeu()


#Creation des Tk.Button qui forment le plateau de
for ligne in range(8):
    l.append([])
    for colonne in range(8):
        #Les 2 pions noirs du centre
        if (ligne == 4 and colonne == 3 ) or (ligne == 3 and colonne == 4 ) :
            b = tk.Button(fenetre,height = Taille[1],width = Taille[0] ,image = pionsNoir , borderwidth=1,bg="#ccedd4")

        #Les 2 pions blancs du centre
        elif (ligne == 4 and colonne == 4 ) or (ligne == 3 and colonne == 3 ) :
            b = tk.Button(fenetre,height = Taille[1] ,width = Taille[0] ,image = pionsBlanc , borderwidth=1,bg="#ccedd4")

        #le reste des pions
        else :
            b = tk.Button(fenetre,height = Taille[3] ,command= lambda ligne = ligne, colonne = colonne : saisieCoup((ligne,colonne)),width = Taille[2],  borderwidth=1,bg="#ccedd4")

        b.grid(row=ligne, column=colonne)
        l[ligne].append( b )


#Fonction permettant le deroulement de la partie
def changerPions(ligne, colonne ,joueur):
    button = l[ligne][colonne]
    button['image']  = pionsBlanc
    if joueur== 2 :
        button['image']  = pionsNoir
    button['width']  = Taille[0]
    button['height'] = Taille[1]

def saisieCoup(Coup):
    copieJeu=game.getCopieJeu(jeu)
    if game.getCoupsValides(jeu) == [] :
        if game.getGagnant(jeu) == 1 :
            print("Les blancs ont gagné la partie")
        else :
            print("Les noirs ont gagné la partie")
        fenetre.destroy() #permet de ferme la fenetre tkinter

    elif ( not game.coupValide(jeu,Coup)) :
        print("Coup non valide, réessayez !")

    else :
        game.joueCoup(jeu,Coup)
        print(game.getCoupsValides(jeu))
        actualiseJeu(jeu)

def actualiseJeu(jeu) :
    """
        Modifie les tk.Button en fonction du joueur qui possede la case
    """
    for i in range(8) :
        for j in range(8) :
            if   jeu[0][i][j] == 1 : changerPions(i,j,1)
            elif jeu[0][i][j] == 2 : changerPions(i,j,2)

fenetre.mainloop()
