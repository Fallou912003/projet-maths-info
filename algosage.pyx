import time
#congruence sur les entiers
def inverse(a, p=7) :
    b = 0
    while (a*b != 1) :     
        b=b+1   
    return b

#addition et multiplication sur polynomes
def addition(f, g) :
    ring = f.parent()
    df = f.degree() ; cf = f.list()
    dg = g.degree() ; cg = g.list()
    dmin = min(df, dg)

    res = [0]*(dmin+1)
    for i in range(0, dmin+1):
        res[i] = cf[i]+cg[i]
    
    #ajout des derniers coefficients
    if dmin==df :
        res.extend(cg[dmin+1:])
    else :
        res.extend(cf[dmin+1:])
    return ring(res)

def soustraction(f, g) :
    ring = f.parent()
    df = f.degree() ; cf = f.list()
    dg = g.degree() ; cg = g.list()
    dmin = min(df, dg)

    res = [0]*(dmin+1)
    for i in range(0, dmin+1):
        res[i] = cf[i]-cg[i]
    
    #ajout des derniers coefficients
    if dmin==df :
        for e in cg[dmin:] :
            res.append(-e)
    else :
        res.extend(cf[dmin+1:])
    return ring(res)


def mult_naive(f, g) :
    ring = f.parent()
    df = f.degree() ; cf = f.list()
    dg = g.degree() ; cg = g.list()
    
    res = [0]*(df+dg+1) 
    
    for i in range(0, df+1):
        for j in range(0, dg+1):
            res[i+j] += cf[i]*cg[j]

    return ring(res) 
    
def karatsuba(f, g) :
    ring = f.parent()
    t = ring.gen()
    if f.is_zero() : return f
    if g.is_zero() : return g
    
    df = f.degree(); dg = g.degree()
    if (df == 0 or dg == 0) : #on considère que le thresold est 0 (à modifier ?) 
        return mult_naive(f, g)

    cf = f.list(); cg = g.list()
    k = max(df, dg).ceil()

    f0 = ring(cf[:k]); f1 = ring(cf[k:])
    g0 = ring(cg[:k]); g1 = ring(cg[k:])

    h1 = karatsuba(f0, g0)
    h2 = karatsuba(f1, g1)
    h5 = karatsuba(addition(f0,f1), addition(g0,g1))
    h7 = h5 - h1 - h2

    #h = h1 + h7.shift(k) + h2.shift(2*k) 
    #to shift a function = "déplacer le graphe de la fonction"
    #h7.shift(k) va remplacer l'indet par t^k donc élever le degré de k ?

    h = h1 + mult_naive(h7, t**k) + mult_naive(h2, t**(2*k))

    return h

#division euclidienne polynomes
def division(f, g) :
    t = f.parent().gen()    

    r = f
    cr = f.coefficients(); cg = g.list()
    if f.is_zero() : return f

    while (r.degree() >= g.degree()) :
        q = cr[-1]*inverse(cg[g.degree()])*t**(r.degree()-g.degree()) #cr[-1] n'est pas bon, l'algorithme ne fonctionne pas si à la fin de la boucle r a un coeff dominant nul
        r = r - q*g
    return r

#algorithmes du calcul de g(a) mod f
def eval_naive(g, a, f) :
    ring = g.parent()
    cg = g.list()
    res = 0
    for i in range(g.degree()+1) :
        res += g[i]*a**i
    return division(res, f)
    
#def eval_variante(g, a, f) :
#    ring = g.parent()
#    res = [0]*g.degree()
#    cg = g.list()

#    for i in range(g.degree()) :
#        res[i] = g[i]*(division(a**i, f))
    
#    return ring(res)

#def brentkung(g, a, f) :
#    r = ceil(g.degree()**(1/2))
#    s = ceil(g.degree()/r)

#    ac = [0]*a.degree()
#    ac[0] = 1

#    for i in range(1,r+1) :
 #       ac[i] = division(a*ac[i-1], f) 
    
 #   ma = 
