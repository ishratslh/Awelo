import sys
sys.path.append("..")
sys.path.append("./Joueurs")
import game
import copy

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups valides None, liste des coups joues vide, scores a 0 et joueur = 1)
    """#Haut 6 larg 7
    plateau = [[0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0]]
    joueur = 1
    listeDesCoupsValides = None
    listeDesCoupsJoues = []
    score = [0, 0]

    return [ plateau, joueur,  listeDesCoupsValides, listeDesCoupsJoues, score ]

def affiche(jeu):
    plateau = jeu[0]
    print ( "        |  0  |  1  |  2  |  3  |  4  |  5  |  6  |")
    print ( "--------------------------------------------------")
    for i in range (len (plateau)) :
        s = "|"
        for j in plateau[i] :
            s +="  "+str(j)+"  |"
        print("  ",i,"  ",s)
        print ( "--------------------------------------------------")

def getScore(jeu):
    scoreJ1=0
    scoreJ2=0
    for i in range(0,6):
        for j in range(0,7):
            if ( jeu[0][i][j]==1 ):
                scoreJ1+=1
            if ( jeu[0][i][j]==2 ):
                scoreJ2+=1
    return (scoreJ1,scoreJ2)

def estValide(jeu,coup) :                                             #verifie si le coup est valide
    if ( (coup[1]>6) or (coup[1]<0) ) :                  #si on saisit un chiffre negatif ou sup à 6
        return False
    if (jeu[0][coup[0]][coup[1]] != 0) and (coup[0]==0) : return False            #si la case d'une colonne est remplie tout en haut
    return True

def getCoupsValides(jeu):
    return [ (x,y) for x in range (0,6) for y in range (0,7) if estValide(jeu,(x,y))]

def getCopieJeu(jeu) :
    return [copy.deepcopy(i) for i in jeu]

def deplacer(case, haut=True, bas=True, gauche=True, droite=True):
    if (haut and case[0]>0):
        case[0]-=1
    if (bas and case[0]<7):
        case[0]+=1
    if (gauche and case[1]>0):
        case[1]-=1
    if (droite and case[1]<7):
        case[1]+=1

def prise(jeu, colonne):
    #placer le pion
    for i in range (0,5) : #lignes
        if (jeu[0][i][colonne]==0) and (jeu[0][i+1][colonne]!=0) and (i<4) :
            case[0]=i
            case[1]=colonne
            jeu[0][case[0]][colonne]=jeu[1]
        if (jeu[0][i][colonne]==0) and (i==5) :
            case[0]=i
            case[1]=colonne
            jeu[0][case[0]][colonne]=jeu[1]

    win=False
    #LIGNES
    #droite
    Case = [case[0],case[1]] #Case = la case mouvante
    comp=0
    if ( Case[1]<6 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]][Case[1]+1] == jeu[1]) and (Case[1]+1<6) and (comp<4)):  #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, False, False, False, True)                        #on déplace la case à droite
        if (comp==4) : win=True

    #gauche
    Case = [case[0],case[1]]
    comp=0
    if ( Case[1]>0 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]][Case[1]-1] == jeu[1]) and (Case[1]-1>0) and (comp<4)):  #tant que la case suivante est une case de notre couleur ET qu'on n'est pas à l'avant-derniere case de la ligne
            comp+=1
            deplacer(Case, False, False, True, False)                            #on déplace la case à gauche
        if (comp==4) : win=True

    #haut
    Case = [case[0],case[1]]
    comp=0
    if ( Case[0]>0 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]-1][Case[1]] == jeu[1]) and (Case[0]-1>0) and (comp<4)): #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, True, False, False, False)                            #on déplace la case en haut
        if (comp==4) : win=True

    #bas
    Case = [case[0],case[1]]
    comp=0
    if ( Case[0]<5 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]+1][Case[1]] == jeu[1]) and (Case[0]+1<5) and (comp<4)):  #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, False, True, False, False)                            #on déplace la case en bas
        if (comp==4) : win=True

    #DIAGONALES
    #bas/droit
    Case = [case[0],case[1]]
    comp=0
    if ( (Case[0]<5) and (Case[1]<6) ): #Pour les cases du bord
        while ( (jeu[0][Case[0]+1][Case[1]+1] == jeu[1]) and (Case[0]+1<5) and (Case[1]+1<6) and (comp<4)):   #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, False, True, False, True)                                                  #on déplace la case en bas à droite
        if (comp==4) : win=True

    #bas/gauche
    Case = [case[0],case[1]]
    comp=0
    if ( (Case[0]<5) and (Case[1]>0) ): #Pour les cases du bord
        while ( jeu[0][Case[0]+1][Case[1]-1] == jeu[1] and (Case[0]+1<5) and (Case[1]-1>0) and (comp<4) ):  #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, False, True, True, False)                                                  #on déplace la case en bas à gauche
        if (comp==4) : win=True

    #haut/gauche
    Case = [case[0],case[1]]
    comp=0
    if ( (Case[0]>0) and (Case[1]>0) ): #Pour les cases du bord
        while ( jeu[0][Case[0]-1][Case[1]-1] == jeu[1] and (Case[0]-1>0) and (Case[1]-1>0) and (comp<4)):  #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, True, False, True, False)                                                  #on déplace la case en haut à gauche
        if (comp==4) : win=True

    #haut/droit
    Case = [case[0],case[1]]
    comp=0
    if ( (Case[0]>0) and (Case[1]<6) ): #Pour les cases du bord
        while ( jeu[0][Case[0]-1][Case[1]+1] == jeu[1] and (Case[0]-1>0) and (Case[1]+1<6) and (comp<4) ):  #tant que la case suivante est une case de notre couleur
            comp+=1
            deplacer(Case, True, False, False, True)                                                   #on déplace la case en haut à droite
        if (comp==4) : win=True


    Score = getScore(jeu)
    jeu[4][0]=Score[0]
    jeu[4][1]=Score[1]

    game.changeJoueur(jeu)                                        #changer de joueur
    jeu[3].append(case)                                           #ajouter le coup à la liste de coups joues

    if (win) : jeu[2] = None
    else: jeu[2]=listeCoupsValides(jeu)

def joueCoup(jeu,coup):
    prise(jeu,coup)

def finJeu(jeu):
    if jeu[2] == None :
        return ( len(jeu[3])>=100)
    return ( len(jeu[3])>=100 or len(jeu[2]) == 0)

def listeCoupsValides(jeu) :
    return getCoupsValides(jeu)

def finalisePartie(jeu) :
    return
