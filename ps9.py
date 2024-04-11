#SLR PARSING TECHNIQUE

from prettytable import PrettyTable
from collections import *
import copy

file=open("slr_parser_table.txt","r")

terminals=[]
non_terminals=[]
main_dict={}

accept_flag=False

for line in file:
  if "terminals" in line:
    splitted=line.split()
    rhs=splitted[1]
    rhs=rhs[1:-1]
    terminals=rhs.split(',')
    continue

  if "variables" in line:
    splitted=line.split()
    rhs=splitted[1]
    rhs=rhs[1:-1]
    non_terminals=rhs.split(',')
    header=terminals+non_terminals
    continue

  temp_dict={}
  splitted=line.split()
  lhs=splitted[0]
  rhs=splitted[1]
  rhs=rhs[1:-1]
  rhs_lis=rhs.split(',')

  i=0
  for h in header:
    temp_dict[h]=rhs_lis[i]
    i+=1

  main_dict[lhs]=temp_dict


print("Terminals:",terminals)
print("Non terminals:",non_terminals)

print("Parser table:")
for key in main_dict:
  print(key, main_dict[key])
print("\n\n")
table=PrettyTable(["Stack", "Action","Input_buffer"])
parse_inp=input("Enter the string to be parsed: ")

input_buffer=deque()
stack=[]

for c in parse_inp:
  input_buffer.append(c)
input_buffer.append('$')

stack.append('0')

print("INPUT STRING: ",parse_inp)
print("\n\n")
while(input_buffer):
  initial_stack=copy.deepcopy(stack)
  initial_buffer=copy.deepcopy(input_buffer)

  stack_top=stack[-1]
  curr_inp=input_buffer.popleft()

  curr_action=main_dict[stack_top][curr_inp]
  table.add_row([" ".join(initial_stack),curr_action," ".join(initial_buffer)])

  if(curr_action=='-'):
    print("STRING NOT ACCEPTED!")
    break

  if(curr_action=="accept"):
    accept_flag=True
    break

  if(curr_action[0]=='s'):
    state=curr_action[1]
    stack.append(curr_inp)
    stack.append(state)


  if(curr_action[0]=='r'):
    input_buffer.appendleft(curr_inp)
    string=curr_action[2:-1]
    splitted=string.split('->')
    lhs=splitted[0]
    rhs=splitted[1]
    rhs_reversed=rhs[::-1]
    j=len(stack)-1
    last_char=rhs[-1]
    last_ind=-1
    for j in range(len(stack)-1,-1,-1):
      if(stack[j]==last_char):
        last_ind=j
        break

    k=last_ind

    if(k!=-1):
      reverse_string=""
      num_chars=0
      while(k>-1):
        if(reverse_string==rhs_reversed):
          start_ind=k+1
          break

        if(stack[k] in header):
          reverse_string+=stack[k]

        num_chars+=1
        k-=1

      stack[last_ind+1]=main_dict[stack[start_ind-1]][lhs]
      stack[start_ind:last_ind+1]=lhs


if(accept_flag):
  print(table)




#SLR TABLE


from collections import defaultdict

prod=defaultdict(list)
start_symbol=""
terminals=[]
non_terminals=[]
aug_gram=""
states=defaultdict(list)
first_dict=defaultdict(list)
follow_dict=defaultdict(list)
goto_table=defaultdict(dict)
slr_table=defaultdict(dict)
first_episolon_flag=0
first_local_episolon_flag=0

def find_indirect_production(nonterm,prod_nonterm,visited):
  global first_episolon_flag
  global first_local_episolon_flag
  for production in prod[prod_nonterm]:
    if production[0] =="e":
       if production[0] not in first_dict[nonterm]:
          first_dict[nonterm].append(production[0])
       first_episolon_flag =1
       first_local_episolon_flag=1
       return
    if production[0] in terminals and production[0] not in first_dict[nonterm]:
          first_dict[nonterm].append(production[0])
    elif production[0] in non_terminals:
          if production[0] not in visited:
            visited.append(production[0])
            first_local_episolon_flag=0
            find_indirect_production(nonterm,production[0],visited)
            j=1
            while j<len(production) and first_local_episolon_flag==1:
                first_local_episolon_flag=0
                new_nonterm=production[j]
                j+=1
                while j<len(production) and production[j]=="d":
                  new_nonterm+=production[j]
                  j+=1
                visited.append(new_nonterm)
                find_indirect_production(nonterm,new_nonterm,visited)


def first():
    global first_episolon_flag
    for nonterm in prod:
      for production in prod[nonterm]:
        if production[0] in terminals and production[0] not in first_dict[nonterm]:
          first_dict[nonterm].append(production[0])
        elif production[0] in non_terminals:
          visited=[production[0]]
          first_episolon_flag =0
          find_indirect_production(nonterm,production[0],visited)
          i=1
          while i<len(production) and first_episolon_flag==1:
            first_episolon_flag =0
            new_nonterm=production[i]
            i+=1
            while i<len(production) and production[i]=="d":
                new_nonterm+=production[i]
                i+=1
            visited.append(new_nonterm)
            find_indirect_production(nonterm,new_nonterm,visited)

def follow():
   append_at_last=[]
   follow_dict[start_symbol].append("$")
   for nonterm in prod:
      for production in prod[nonterm]:
          i=0
          while i<len(production):
            new_symbol=production[i]
            i+=1
            while i<len(production) and production[i]=="d":
                new_symbol+=production[i]
                i+=1
            if new_symbol in non_terminals:
               if i<len(production):
                if production[i] in terminals and production[i] not in follow_dict[new_symbol]:
                  follow_dict[new_symbol].append(production[i])
                else:
                  prev_i=i
                  new_nonterm=production[i]
                  i+=1
                  while i<len(production) and production[i]=="d":
                      new_nonterm+=production[i]
                      i+=1
                  i=prev_i
                  follow_i=first_dict[new_nonterm]
                  for first_term in follow_i:
                    if first_term !='e' and first_term not in follow_dict[new_symbol]:
                        follow_dict[new_symbol].append(first_term)
                    if first_term == "e":
                      append_at_last.append((new_symbol,nonterm))

               if i == len(production):
                append_at_last.append((new_symbol,nonterm))
   for new_symbol,nonterm in append_at_last:
        follow_nonterm=follow_dict[nonterm]
        for first_term in follow_nonterm:
            if first_term !='e' and first_term not in follow_dict[new_symbol]:
                follow_dict[new_symbol].append(first_term)

def closure(productions):
  set_i=[]
  for production in productions:
    set_i.append(production)
  i=0
  while i < len(set_i):
      production=set_i[i]
      i+=1
      splitted=production.split("->")
      rhs=splitted[1]
      if "." in rhs:
        dot_index=rhs.index(".")
        if production not in set_i:
          set_i.append(production)
        if dot_index+1 < len(rhs) and rhs[dot_index+1] in non_terminals:
          nonterm=rhs[dot_index+1]
          for prod_rhs in prod[nonterm]:
            prod_new=nonterm+"->."+prod_rhs
            if prod_new not in set_i:
              set_i.append(prod_new)

  return set_i

def goto(item,gram_symbol):
    productions=[]
    for production in item:
       splitted=production.split("->")
       rhs=splitted[1]
       if "." in rhs:
         dot_index=rhs.index(".")
         if dot_index+1 < len(rhs) and rhs[dot_index+1]==gram_symbol:
            new_production=production.replace("."+gram_symbol,gram_symbol+".")
            productions.append(new_production)
    if len(productions)>0:
      return closure(productions)
    return productions

def lritems():
  aug_gram_start=aug_gram.replace("->","->.")
  c=closure([aug_gram_start])
  states["0"]=c
  i=0
  while i < len(states.keys()):
      item = states[str(i)]
      for nonterm in non_terminals:
        goto_list=goto(item,nonterm)
        goto_table[str(i)][nonterm]="-"
        if len(goto_list)>0 and  goto_list not in list(states.values()):
          state_no=len(states.keys())
          states[str(state_no)]=goto_list
        if len(goto_list)>0:
          state_no_goto_list=str(list(states.values()).index(goto_list))
          print("goto(",str(i),",",nonterm,")  ---------  ",state_no_goto_list," ----- ",goto_list)
          goto_table[str(i)][nonterm]=state_no_goto_list
      for term in terminals:
        goto_list=goto(item,term)
        goto_table[str(i)][term]="-"
        if len(goto_list)>0 and  goto_list not in list(states.values()):
          state_no=len(states.keys())
          states[str(state_no)]=goto_list
        if len(goto_list)>0:
          state_no_goto_list=str(list(states.values()).index(goto_list))
          print("goto(",str(i),",",term,")  ---------  ",state_no_goto_list," ----- ",goto_list)
          goto_table[str(i)][term]=state_no_goto_list
      i+=1
  print("\n\n\n\n")
  for state in states:
    print(state,"---------",states[state])

def find_slr_table():
    for state in states:
      for i in terminals:
        slr_table[state][i]="-"
      slr_table[state]["$"]="-"
      for i in non_terminals:
        slr_table[state][i]="-"
      for item in states[state]:
          splitted=item.split("->")
          lhs=splitted[0]
          rhs=splitted[1]
          if "." in rhs:
            dot_index=rhs.index(".")
            if dot_index+1 < len(rhs):
               if rhs[dot_index+1] in non_terminals:
                  nonterm=rhs[dot_index+1]
                  slr_table[state][nonterm] = goto_table[state][nonterm]
               elif rhs[dot_index+1] in terminals:
                  term=rhs[dot_index+1]
                  if goto_table[state][term]:
                    slr_table[state][term] ="Shift:"+goto_table[state][term]
                  else:
                    slr_table[state][term]=goto_table[state][term]
            if dot_index+1==len(rhs):
              if item == aug_gram+".":
                slr_table[state]["$"]="ACCEPT"
              else:
                for follow in follow_dict[lhs]:
                  slr_table[state][follow]="Reduce:"+item.replace(".","")

file = open("grammar3.txt","r")

for line in file:
  stripped=line.strip()
  if "start" in stripped:
     splitted=stripped.split()
     start_symbol=splitted[1]
     start_dash=start_symbol+"d"
     while start_dash in prod:
        start_dash=start_dash+"d"
     prod[start_dash]=start_symbol
     aug_gram=start_dash+"->"+start_symbol
     continue
  if "terminals" in stripped:
    splitted=stripped.split()
    terminals=splitted[1:]
    continue
  splitted=stripped.split("->")
  prod[splitted[0]].append(splitted[1])
  if splitted[0] not in non_terminals:
    non_terminals.append(splitted[0])

print(terminals)
print(non_terminals)
print(prod)
print("\n\n\n\n")
lritems()
first()
print("\n\n\n\n")
print("First")
for nonterm in first_dict:
  print(nonterm," --------- ",first_dict[nonterm])
follow()
print("\n\n\n\n")
print("Follow")
for nonterm in follow_dict:
  print(nonterm," --------- ",follow_dict[nonterm])
print("\n\n\n\n")
find_slr_table()
print("states",end=" ")
for i in terminals:
    print(i,end=" ")
print("$",end=" ")
for i in non_terminals:
  print(i,end=" ")
print("\n")
for state in slr_table:
  print(state,end="  ")
  for action in slr_table[state]:
    print(slr_table[state][action],end=" ")
  print("\n")


#QUADRUPLES AND TRIPLES


from collections import *
from prettytable import PrettyTable

class Node:
  def __init__(self, value=None, left=None, right=None, next=None):
    self.value=value
    self.left=left
    self.right=right
    self.next=next


class Stack:
  def __init__(self):
    self.top=None

  def push(self, node):
    if not self.top : #stack is empty
      self.top=node

    else:
      node.next=self.top
      self.top=node

  def pop(self):

    if not self.top: #stack is empty
      print("stack is empty!")

    else:
      popped=self.top
      self.top=self.top.next
      return popped

class SyntaxTree:
  def inorder(self, p):
    if (not p):
      return
    self.inorder(p.left)
    print(p.value,end="\t")
    self.inorder(p.right)

#expr = input("Enter the arithmetic expression with brackets: ")
expr="((a+b)*(a-b))"
print("INPUT EXPRESSION: ", expr)
print("\n\n")

stack = []
postfix = []

precedence={'*':2,"/":2,"+":1,"-":1}


#infix to postfix conversion:

for i in range(len(expr)):
    if (expr[i] == '('):
        stack.append(expr[i])

    elif (expr[i].isalpha()):
        postfix.append(expr[i])

    elif ((expr[i] in list(precedence.keys())) and stack[-1] == '('):
        stack.append(expr[i])

    elif (expr[i] in list(precedence.keys()) and stack[-1] in list(precedence.keys())):
        if (precedence[expr[i]] > precedence[stack[-1]]):
            stack.append(expr[i])
        else:
            while (len(stack) and stack[-1] != '(' and stack[-1] != ')' and precedence[expr[i]] <= precedence[stack[-1]]):
                postfix += stack.pop()
            stack.append(expr[i])

    elif (expr[i] == ')'):
        if len(stack) != 0:
            while (True):
                elt = stack.pop()
                if (elt == '('):
                    break
                else:
                    postfix += elt

print("POSTFIX NOTATION: ", postfix)

operators=['+','*','/','-']

#Syntax tree construction:
tree_stack=Stack()
syntax_tree=SyntaxTree()

for c in postfix:
  if c in operators:
    operator=Node(c)
    op2=tree_stack.pop()
    op1=tree_stack.pop()
    operator.left=op1
    operator.right=op2
    tree_stack.push(operator)

  elif c.isalpha():
    new_node=Node(c)
    tree_stack.push(new_node)

root=tree_stack.pop()

print("\n\nSYNTAX TREE -> Inorder traversal:")
syntax_tree.inorder(root)


#intermediate code generation:

for i in range(len(postfix)):
  postfix[i]=str(postfix[i])

temp_num=0
code=defaultdict(list)
i=0
while(i<len(postfix)):
  if(postfix[i] in operators):
    left=postfix[i-2]
    right=postfix[i-1]

    lhs='T'+str(temp_num)
    code[lhs].append(left)
    code[lhs].append(postfix[i])
    code[lhs].append(right)

    temp_num+=1
    postfix[i-2:i+1]="$"
    i-=2
    postfix[i]=lhs

  i+=1

print("\n\nIntermediate code: \n")
for key in code:
  print(key+" = "+" ".join(code[key]))
  print("\n")


#Quadruples:

quadruple=PrettyTable(["Operator", "Argument 1", "Argument 2", "Result"])


print("Quadruples: \n")
for key in code:
  rhs=code[key]
  for i in range(len(rhs)):
    if(rhs[i] in operators):
      op1=rhs[i-1]
      op2=rhs[i+1]

      quadruple.add_row([rhs[i],op1,op2,key])

print(quadruple)

#Triples:

triple = PrettyTable(["S_No","Operator", "Argument 1", "Argument 2"])
print("\n\n")
count=1
serial_nos={}
for c in list(code.keys()):
  serial_nos[c]=count
  count+=1

print("Triples\n")

count_str="1"
for key in code:
  rhs=code[key]
  for i in range(len(rhs)):
    if(rhs[i] in operators):
      op1=rhs[i-1]
      op2=rhs[i+1]

      if(op1 in list(serial_nos.keys())):
        op1=serial_nos[op1]

      if(op2 in list(serial_nos.keys())):
        op2=serial_nos[op2]

      triple.add_row([count_str,rhs[i],op1,op2])
      count_str=str(int(count_str)+1)


print(triple)
