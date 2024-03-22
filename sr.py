gram = {
	"E":["E+E","E-E","i"]
}
startS= "E"
inp = input("Enter expression to parse: ")
inp+='$'

stack = "$"
print("Stack\t\t\tInput\t\t\tAction\n")

while True:
  action = True
  i = 0
  while i<len(gram[startS]):
    if gram[startS][i] in stack:
      stack = stack.replace(gram[startS][i],startS)
      print(stack, "\t\t\t", inp, '\t\t\tReduced: ', startS, '->', gram[startS][i])
      i=-1
      action = False
    i+=1
  if len(inp)>1:
    stack+=inp[0]
    inp=inp[1:]
    print(stack, '\t\t\t', inp, '\t\t\t', "Shift")
    action = False

  if inp == "$" and stack == ("$"+startS):
    print(stack, '\t\t\t', inp, '\t\t\t', 'Accepted')
    break

  if action:
    print(stack, '\t\t\t', inp, '\t\t\t', 'Invalid String')
    break
