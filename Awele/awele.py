import copy
import sys
sys.path.append("..")
sys.path.append("./Joueurs")
import game

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups valides None, liste des coups joues vide, scores a 0 et joueur = 1)
    """
    plateau = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
    joueur = 1
    listeDesCoupsValides = None
    listeDesCoupsJoues = []
    score = [0, 0]

    return [ plateau, joueur,  listeDesCoupsValides, listeDesCoupsJoues, score ]

def affiche(jeu):
    plateau = jeu[0]
    print ( "        |  0  |  1  |  2  |  3  |  4  |  5  |")
    print ( "--------------------------------------------")
    for i in range (len (plateau)) :
        s = "|"
        for j in plateau[i] :
            s +="  "+str(j)+"  |"
        print("  ",i,"  ",s)
        print ( "--------------------------------------------")

def estAffame(jeu,joueur):                    #vérifie si le joueur en parametre est affame
    return ( sum(jeu[0][joueur-1])==0 )

def estValide(jeu,coup,checkNourri=False):    #verifie si le coup est valide
    if ( not ( coup[0] == (jeu[1]-1) ) ) :
        return False
    g=jeu[0][coup[0]][coup[1]]
    if ( g==0 ):
        return False
    if (checkNourri) :
        if ( coup[0]==0 ) :
            return ( g > (5-coup[1]) )
    return True

def getCoupsValides(jeu):
    affame=estAffame(jeu, jeu[1]%2+1)         #jeu[1]%2+1 donne le joueur adversaire
    return [ (jeu[1]-1, c) for c in range(0,6) if estValide(jeu, ((jeu[1]-1),c), affame) ]

def getCopieJeu(jeu) :                        #copie = copie du jeu dont les instances
    return [copy.deepcopy(i) for i in jeu]

def deplacer( case , antihoraire=True) :
    if antihoraire :
        if case[0] == 0 :
            if case[1]>0:
                case[1]-= 1
            else :
                case[0] = 1

        elif case[0] == 1 :
            if case[1]<5:
                case[1]+= 1
            else :
                case[0] = 0
    else :                                    #deplacement dans le sens antihoraire
        if case[0] == 0 :
            if case[1]<5:
                case[1]+= 1
            else :
                case[0] = 1
        elif case[0] == 1 :
            if case[1]>0:
                case[1]-= 1
            else :
                case[0] = 0

def egrainer(jeu, case) :
    caseDepart = case
    Case = [case[0],case[1]]
    nbGraines = jeu[0][case[0]][case[1]] #contenu de la case choisie...
    jeu[0][case[0]][case[1]] = 0         #...vidé
    #EGRAINER (dans le sens anti-horaire)
    while nbGraines > 0 :
        deplacer(Case)
        if ( (Case[0] == case[0] and Case[1] == case[1])) : #on ne remplit pas la case où l'on vient de prendre les graines
            continue
        nbGraines -= 1
        jeu[0][Case[0]][Case[1]] += 1
    #MANGER
    copie = getCopieJeu(jeu)
    score=0
    while not (estAffame(jeu,jeu[1])) :                                               #on ne peut pas manger si le coup qui affame l’adversaire

        if Case[0] == (jeu[1] - 1) :                                                  #Si la dernière graine tombe dans un trou de son camp
            break
        elif (( jeu[0][Case[0]][Case[1]] < 4 ) and ( jeu[0][Case[0]][Case[1]] > 1 )): #s'il y a deux ou trois graines dans ce trou
            score+= jeu[0][Case[0]][Case[1]]                                          #on capture ces deux ou trois graines et les met de côté
            jeu[0][Case[0]][Case[1]] = 0
            deplacer(Case,False)                                                      #pour manger éventuellement dans le sens horaire
        else :
            break

    #Joueur Adverse Affame
    if (estAffame(jeu,(jeu[1]%2+1))) :
        jeu[0]=copie[0]
        jeu[2]=None


    #Ajout des points au score du joueur
    jeu[4][jeu[1]-1]+=score

    jeu[1]= jeu[1]%2+1                #changer de joueur
    jeu[3].append(caseDepart)         #ajouter le coup à la liste de coups joues

def joueCoup(jeu,coup):
    egrainer(jeu,coup)
    jeu[2]=listeCoupsValides(jeu)

def finJeu(jeu):
    if jeu[2] == None :
        return ( len(jeu[3])>=100)
    return ( len(jeu[3])>=100 or len(jeu[2]) == 0)

def listeCoupsValides(jeu) :
    return getCoupsValides(jeu)

def finalisePartie(jeu):
    game.changeJoueur(jeu)
