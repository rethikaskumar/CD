import os

#Left Recursion
n=int(input("Enter Number of productions "))
Sym=[]
V=[]
T=[]
P=[]
for i in range(n):
    prod=input("Enter production of the form V->(V U T) ")
    v=prod[0]
    if v not in V:
        V.append(v)
        P.append([])
    ind=V.index(v)
    for j in range(3,len(prod)):
        if(prod[j] not in Sym):
            Sym.append(prod[j])
    lst=prod[3:].split('|')
    for z in lst:
        P[ind].append(z)
for j in Sym:
    if j not in V:
        T.append(j)
l=len(V)
for i in range(l):
    for j in range(i):
        for p in P[i]:
            if(p[0]==V[j]):
                for k in P[j]:
                    P[i].append(k+p[1:])
                P[i].remove(p)
for i in range(len(V)):
    res=V[i]+'->'+P[i][0]
    for j in range(1,len(P[i])):
        res+='|'+P[i][j]
    print(res)
for i in range(l):
    flag=0
    for j in P[i]:
        if(j[0]==V[i]):
            flag=1
            break
    if(flag==1):
        V.append(V[i]+'\'')
        P.append([])
        j=0
        l=len(P[i])
        while(j<l):
            if(P[i][j][0]==V[i]):
                P[len(P)-1].append(P[i][j][1:]+V[i]+'\'')
            else:
                if(P[i]=='e'):
                    P[i].append(V[i]+'\'')
                else:
                    P[i].append(P[i][j]+V[i]+'\'')
            P[i].remove(P[i][j])
            l-=1
        P[len(P)-1].append('e')

#Left rec 2
def solveNonImmediateLR(self, A, B) :
        nameA = A.getName()
        nameB = B.getName()
 
        rulesA = []
        rulesB = []
        newRulesA = []
        rulesA = A.getRules()
        rulesB = B.getRules()
 
        for rule in rulesA :
            if rule[0 : len(nameB)] == nameB :
                for rule1 in rulesB :
                    newRulesA.append(rule1 + rule[len(nameB) : ])
            else :
                newRulesA.append(rule)
        A.setRules(newRulesA)
 
    def solveImmediateLR(self, A) :
        name = A.getName()
        newName = name + "'"
 
        alphas = []
        betas = []
        rules = A.getRules()
        newRulesA = []
        newRulesA1 = []
 
        rules = A.getRules()
 
        # Checks if there is left recursion or not
        for rule in rules :
            if rule[0 : len(name)] == name :
                alphas.append(rule[len(name) : ])
            else :
                betas.append(rule)
 
        # If no left recursion, exit
        if len(alphas) == 0 :
            return
 
        if len(betas) == 0 :
            newRulesA.append(newName)
 
        for beta in betas :
            newRulesA.append(beta + newName)
 
        for alpha in alphas :
            newRulesA1.append(alpha + newName)
 
        # Amends the original rule
 
        A.setRules(newRulesA)
        newRulesA1.append("\u03B5")
 
        # Adds new production rule
        newNonTerminal = NonTerminal(newName)
        newNonTerminal.setRules(newRulesA1)
        self.nonTerminals.append(newNonTerminal)
 
    def applyAlgorithm(self) :
        size = len(self.nonTerminals)
        for i in range(size) :
            for j in range(i) :
                self.solveNonImmediateLR(self.nonTerminals[i], self.nonTerminals[j])
            self.solveImmediateLR(self.nonTerminals[i])
#Left Factoring
for v in range(len(V)):
    pref=[]
    for i in range(2, len(P[v])+1):
        pref.append(os.path.commonprefix(P[v][:i]))
    for p in pref:
        if p!='':
            newv=V[v]+"'"
            V.append(newv)
            ind=V.index(newv)
            P.append([])
            for prod in range(len(P[v])):
                if P[v][prod].startswith(p):
                    P[ind].append(P[v][prod][len(p):])
                    P[v][prod]=p+newv
            P[ind].append('e')
            P[ind]=list(set([pr for pr in P[ind] if pr !='']))
            P[v]=list(set(P[v]))

print(V)
print(P)

result={}
for i in range(len(V)):
    result[V[i]]=P[i]

