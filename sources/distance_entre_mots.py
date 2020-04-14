import numpy as np

# Cette fonction retourne la distance qu'il existe entre deux mots
# rentrés en argument de la fonction ici appelés mot1 et mot2.
def CalculDistanceMots(mot1, mot2):

    # Nous utilisons le package NumPy pour faciliter l'écriture
    # de la matrice d.
    d = np.zeros((len(mot1)+1,len(mot2)+1))
    d[:,0] = np.arange(0,len(mot1)+1)
    d[0] = np.arange(0, len(mot2)+1)
    #print(d)

    cout = 0
    for i in range(1,len(mot1)+1):
        #print(i)
        for j in range(1,len(mot2)+1):
            if mot1[i-1] == mot2[j-1]:
                cout = 0
            else:
                cout = 1

            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cout)

            if i > 1 and j > 1 and mot1[i-1] == mot2[j-2] and mot1[i-2] == mot2[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2]+1)

    #print(d)
    return int(d[len(mot1)][len(mot2)])

