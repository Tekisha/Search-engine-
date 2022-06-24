def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    lps = [0]*M #cuva najduzi prefiks sufiks vrijednosti za pat
    j=0 #indeks za pat[]

    computeLPSArray(pat, M, lps)

    i = 0 #index za txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1
        
        if j== M:
            return i-j
        
        elif i<N and pat[j] != txt[i]:
            if j != 0:
                j= lps[j-1]
            else:
                i+=1
    
    return -1 #ako nema fraze vraca -1
        
def computeLPSArray(pat, M, lps):
    len = 0 # duzina najduzeg prefiksa sufiksa

    i=1 # prvi karakter uvijek jednak 0 u tabeli

    while i<M:
        if pat[i] == pat[len]:
            len +=1
            lps[i] = len
            i +=1
        else:
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i+=1
