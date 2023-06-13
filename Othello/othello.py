import sys
sys.path.append("..")
sys.path.append("./Joueurs")
import game
import copy

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups valides None, liste des coups joues vide, scores a 0 et joueur = 1)
    """
    plateau = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,1,2,0,0,0],
               [0,0,0,2,1,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]
    joueur = 1
    listeDesCoupsValides = None
    listeDesCoupsJoues = []
    score = [0, 0]

    return [ plateau, joueur,  listeDesCoupsValides, listeDesCoupsJoues, score ]

def affiche(jeu):
    plateau = jeu[0]
    print ( "        |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |")
    print ( "---------------------------------------------------------")
    for i in range (len (plateau)) :
        s = "|"
        for j in plateau[i] :
            s +="  "+str(j)+"  |"
        print("  ",i,"  ",s)
        print ( "---------------------------------------------------------")

def getScore(jeu):
    scoreJ1=0
    scoreJ2=0
    for i in range(0,8):
        for j in range(0,8):
            if ( jeu[0][i][j]==1 ):
                scoreJ1+=1
            if ( jeu[0][i][j]==2 ):
                scoreJ2+=1
    return (scoreJ1,scoreJ2)

def estValide(jeu,coup) :                                             #verifie si le coup est valide
    if ( (coup[0]>7) or (coup[1]>7) or (coup[0]<0) or (coup[1]<0) ) : #si on saisit un chiffre negatif ou sup à 7
        return False
    if jeu[0][coup[0]][coup[1]] != 0 : return False
    for i in [-1,0,1] :
        for j in [-1,0,1] :
            if ( i == 0 and j== 0) or coup[0]+i < 0 or coup[1]+j< 0 or coup[0]+i > 7 or coup[1]+j > 7 : continue
            if jeu[0][coup[0]+i][coup[1]+j] == (jeu[1]%2+1) :
                copy = getCopieJeu(jeu)
                prise(copy,(coup[0],coup[1]))
                if getScore(jeu)[jeu[1]-1]+1 < getScore(copy)[jeu[1]-1] :
                    return True

    return False

def getCoupsValides(jeu):
    return [ (x,y) for x in range (0,8) for y in range (0,8) if estValide(jeu,(x,y))]

def getCopieJeu(jeu) :
    return [copy.deepcopy(i) for i in jeu]

    #case(x,y)

def deplacer(case, haut=True, bas=True, gauche=True, droite=True):
    if (haut and case[0]>0):
        case[0]-=1
    if (bas and case[0]<7):
        case[0]+=1
    if (gauche and case[1]>0):
        case[1]-=1
    if (droite and case[1]<7):
        case[1]+=1

def prise(jeu, case) :
    jeu[0][case[0]][case[1]]=jeu[1]                               #on place notre pion

    #droite
    Case = [case[0],case[1]] #Case = la case mouvante
    encadre=False
    if ( Case[1]<7 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]][Case[1]+1] == jeu[1]%2+1) and (Case[1]+1<7) ):  #tant que la case de droite est du chiffre adverse
            deplacer(Case, False, False, False, True)                            #on déplace la case à droite
        if (jeu[0][Case[0]][Case[1]+1] == jeu[1]) :                              #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise à droite")                                                  #print à retirer quand il n'y aura plus aucun probleme
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]][Case[1]+1] == jeu[1]%2+1 ):
            deplacer(Case, False, False, False, True)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                    #on encadre


    #gauche
    Case = [case[0],case[1]]
    encadre=False
    if ( Case[1]>0 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]][Case[1]-1] == jeu[1]%2+1) and (Case[1]-1>0) ):  #tant que la case de gauche est du chiffre adverse ET qu'on n'est pas à l'avant-derniere case de la ligne
            deplacer(Case, False, False, True, False)                            #on déplace la case à hauche
        if (jeu[0][Case[0]][Case[1]-1] == jeu[1]) :                              #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise à gauche")
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]][Case[1]-1] == jeu[1]%2+1 ):
            deplacer(Case, False, False, True, False)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                    #on encadre

    #haut
    Case = [case[0],case[1]]
    encadre=False
    if ( Case[0]>0 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]-1][Case[1]] == jeu[1]%2+1) and (Case[0]-1>0) ):  #tant que la case du haut est du chiffre adverse
            deplacer(Case, True, False, False, False)                            #on déplace la case en haut
        if (jeu[0][Case[0]-1][Case[1]] == jeu[1]) :                              #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise en haut")
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]-1][Case[1]] == jeu[1]%2+1 ):
            deplacer(Case, True, False, False, False)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                    #on encadre

    #bas
    Case = [case[0],case[1]]
    encadre=False
    if ( Case[0]<7 ): #Pour les cases du bord
        while ( (jeu[0][Case[0]+1][Case[1]] == jeu[1]%2+1) and (Case[0]+1<7) ):  #tant que la case du bas est du chiffre adverse
            deplacer(Case, False, True, False, False)                            #on déplace la case en bas
        if (jeu[0][Case[0]+1][Case[1]] == jeu[1]) :                              #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise en bas")
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]+1][Case[1]] == jeu[1]%2+1 ):
            deplacer(Case, False, True, False, False)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                    #on encadre

    #DIAGONALES
    #bas/droit
    Case = [case[0],case[1]]
    encadre=False
    if ( (Case[0]<7) and (Case[1]<7) ): #Pour les cases du bord
        while ( (jeu[0][Case[0]+1][Case[1]+1] == jeu[1]%2+1) and (Case[0]+1<7) and (Case[1]+1<7) ):   #tant que la case du bas/droit est du chiffre adverse
            deplacer(Case, False, True, False, True)                                                  #on déplace la case en bas à droite
        if (jeu[0][Case[0]+1][Case[1]+1] == jeu[1]) :                                                 #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise en diagonale bas/droit")
        Case = [case[0],case[1]]
        while jeu[0][Case[0]+1][Case[1]+1] == jeu[1]%2+1 :
            deplacer(Case, False, True, False, True)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                                         #on encadre

    #bas/gauche
    Case = [case[0],case[1]]
    encadre=False
    if ( (Case[0]<7) and (Case[1]>0) ): #Pour les cases du bord
        while ( jeu[0][Case[0]+1][Case[1]-1] == jeu[1]%2+1 and (Case[0]+1<7) and (Case[1]-1>0) ):     #tant que la case du bas/gauche est du chiffre adverse
            deplacer(Case, False, True, True, False)                                                  #on déplace la case en bas à gauche
        if (jeu[0][Case[0]+1][Case[1]-1] == jeu[1]) :                                                 #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise en diagonale bas/gauche")
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]+1][Case[1]-1] == jeu[1]%2+1 ):
            deplacer(Case, False, True, True, False)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                                         #on encadre

    #haut/gauche
    Case = [case[0],case[1]]
    encadre=False
    if ( (Case[0]>0) and (Case[1]>0) ): #Pour les cases du bord
        while ( jeu[0][Case[0]-1][Case[1]-1] == jeu[1]%2+1 and (Case[0]-1>0) and (Case[1]-1>0) ):     #tant que la case du haut/gauche est du chiffre adverse
            deplacer(Case, True, False, True, False)                                                  #on déplace la case en haut à gauche
        if ( jeu[0][Case[0]-1][Case[1]-1] == jeu[1] ) :                                               #si la case suivante est une case de notre couleur
            encadre = True
    if  encadre :
        #print("prise en diagonale haut/gauche")
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]-1][Case[1]-1] == jeu[1]%2+1 ):
            deplacer(Case, True, False, True, False)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                                         #on encadre

    #haut/droit
    Case = [case[0],case[1]]
    encadre=False
    if ( (Case[0]>0) and (Case[1]<7) ): #Pour les cases du bord
        while ( jeu[0][Case[0]-1][Case[1]+1] == jeu[1]%2+1 and (Case[0]-1>0) and (Case[1]+1<7)  ):     #tant que la case du haut/droit est du chiffre adverse
            deplacer(Case, True, False, False, True)                                                   #on déplace la case en haut à droite
        if ( jeu[0][Case[0]-1][Case[1]+1] == jeu[1] ) :                                                #si la case suivante est une case de notre couleur
            encadre = True
    if encadre :
        #print("prise en diagonale haut/droit")
        Case = [case[0],case[1]]
        while ( jeu[0][Case[0]-1][Case[1]+1] == jeu[1]%2+1 ):
            deplacer(Case, True, False, False, True)
            jeu[0][Case[0]][Case[1]] = jeu[1]                                                          #on encadre


    Score = getScore(jeu)
    jeu[4][0]=Score[0]
    jeu[4][1]=Score[1]

    game.changeJoueur(jeu)                                        #changer de joueur
    jeu[3].append(case)                                           #ajouter le coup à la liste de coups joues

def joueCoup(jeu,coup):
    prise(jeu,coup)
    jeu[2]=listeCoupsValides(jeu)

def finJeu(jeu):
    if jeu[2] == None :
        return ( len(jeu[3])>=100)
    return ( len(jeu[3])>=100 or len(jeu[2]) == 0)

def listeCoupsValides(jeu) :
    return getCoupsValides(jeu)

def finalisePartie(jeu) :
    return
