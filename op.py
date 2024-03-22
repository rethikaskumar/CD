import networkx as nx

stack=['']*20

top=-1
i=0
h_index=-1
'''
prec=[  ['>', '>','<','<','<','>'],
        ['>', '>','<','<','<','>'],
        ['>', '>','>','>','<','>'],
        ['>', '>','>','>','<','>'],
        ['>', '>','>','>','e','>'],
        ['<', '<','<','<','<','>']]

op=['+', '-', '*', '/', 'i', '$']
'''
prec=[['e', '>', '>', '>'],
      ['<', '>', '<', '>'],
      ['<', '>', '>', '>'],
      ['<', '<', '<', 'e']]

op=['i', '+', '*', '$']

handles=["E*E", "E+E", "i"]

def reduce():
    global top, h_index
    for i in range(len(handles)):
        hlen=len(handles[i])
        if stack[top]==handles[i][0] and top+1>=hlen:
            f=1
            t=1
            for ts in range(1, hlen):
                if stack[top-ts] != handles[i][ts]:
                    f=0
                    break
                t=t+1
            if f==1:
                stack[top-t+1]='E'
                top=top-t+1
                h_index=i
                return True
    return False

def check():
    if top!=2:
        return False
    if stack[0]=='$' and stack[1]=='E' and stack[2]=='$':
        return True
    return False

def parse():
    global top
    l=len(inp)
    top+=1
    #print(top)
    stack[top]='$'
    print("\nStack\t\t\tInput\t\t\tAction\n")
    while i<l:
        shift()
        print(''.join(stack), '\t\t\t', inp[i:], "\t\t\tShift")
        if top>=0 and i<l:
            m=op.index(stack[top])
            n=op.index(inp[i])
            if prec[m][n]=='>' :
                while reduce():
                    print(''.join(stack), '\t\t\t', inp[i:], '\t\t\tReduced: E->', handles[h_index])
    if check():
        print("\nAccepted\n")
    else:
        print("\nInvalid String\n")

def shift():
    global top, i
    top+=1
    stack[top]=inp[i]
    i+=1

inp=input("Enter expression to parse: ")
inp+='$'
parse()

def precedence_fn():
  def findMaxlength(edges, source, visited):
    len=0
    for edge in edges:
      if edge[0]==source and edge[1] not in visited:
        visited.append(edge[1])
        len=max(len, 1+findMaxlength(edges, edge[1], visited))
        visited.remove(edge[1])
    return len
  n=len(op)
  inc=4/n
  pos={}
  fNode=['f'+i for i in op]
  gNode=['g'+i for i in op]
  for i in range(len(op)):
    pos[fNode[i]]=[-1, -2+i*inc]
    pos[gNode[i]]=[1, -2+i*inc]
  edges=[]
  for i in range(len(op)):
    for j in range(len(op)):
      if prec[i][j]=='<':
        edges.append(('g'+op[j], 'f'+op[i]))
      elif prec[i][j]=='>':
        edges.append(('f'+op[i], 'g'+op[j]))
  G = nx.DiGraph()
  G.add_edges_from(edges)
  nx.draw_networkx(G, pos)
  for node in fNode+gNode:
    visited=[node]
    maxl=findMaxlength(edges, node, visited)
    print(node, '\t\t', maxl)

precedence_fn()
