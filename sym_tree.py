import re
import os.path
from glob import glob
from graphviz import Digraph
from pyparsing import originalTextFor
from pyparsing import nestedExpr
from optparse import OptionParser
import itertools

from Parser.parser import *
from io import StringIO
import sys

paths = []
filesToInclude = []
maxDepth = None

op = OptionParser("usage: %prog maxDepth, default = MAX")
op.add_option('-d', '--depth', dest='depth', default=None)
op.add_option('-o', '--output', dest='pdfOutput', default=None)
opts,remainder = op.parse_args()

maxDepth = int(opts.depth)
pdfOutput = opts.pdfOutput

#print(maxDepth)

for filename in glob('klee-last/*.pc'):
    filesToInclude.append(os.path.splitext(filename)[0])


#parsiranje sym.path fajlova i konstruisanje razlicitih putanja
for filename in filesToInclude:
    with open(filename+'.sym.path') as file:
	#Jedna putanja se sastoji od n bitova (0,1) koji vode do lista. 0 oznacava da ulov nije ispunjen, 1 da jeste
        path = [int(line.rstrip()) for line in itertools.islice(file, 0, maxDepth)]
	#paths je matrica stabla
        paths.append(path)

#print(paths)

#parsiranje svih .pc fajlova redom i popunjavanje instrukcija
pathsInstructions = []
for instrFilename in filesToInclude:
    with open(instrFilename+'.pc') as instrFile:
        stuff = instrFile.read()
        st = re.sub(r'\s+', ' ', stuff)
	#izdvajanje uslova koji se nalazi u []
        st1 = re.search(r'query \[(.+)\]', st).group(1)
        scanner = originalTextFor(nestedExpr('(', ')'))
        instructions = []

        for match in scanner.searchString(st1):
            instructions.append(match[0])
        pathsInstructions.append(instructions)
        
#repl = re.search(r'\((Read.SB.+?)\)', st1).group(1).split()[-1]
#st2 = re.sub(r'\((Read.SB.+?)\)', repl, st1)


#Dodatni parametri numIt and parentNumIt, trebaju nam zbog crtanja u biblioteci graph
class TreeNode:
    def __init__(self, cond, numIt, parentNumIt, instruction):
        self.cond = cond	#da li se dolazi iz true ili false grane u cvor
        self.numIt = numIt	#redni broj cvora
        self.left = self.right = None
        self.parentNumIt = parentNumIt	#redni broj roditelja
        self.instruction = instruction	#instrukcija koja se upisuje
 

g = Digraph('g', filename=pdfOutput, node_attr={'shape': 'record', 'height': '.1'})
root = TreeNode("root", 0, None, None)
g.node('node0', '')
nodeNumIt = 1

#sve putanje mecovane sa instrukcijama
for path, pathInstruction in zip(paths, pathsInstructions):
    node = root

    #jedna putanje se mecuje sa njenom istrukcijom
    for branch, instruction in zip(path, pathInstruction):
        #repl = re.search(r'\((Read.SB.+?)\)', instruction).group(1).split()[-1]
        #readableInstruction = re.sub(r'\((Read.SB.+?)\)', repl, instruction)
        
        #parsiramo instrukcije, fja parser radi print pa preusmeravamo stdout stream
        readableInstructionTemp = instruction
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        readableInstruction = parser.parse(readableInstructionTemp)
        readableInstruction = mystdout.getvalue()
        sys.stdout = old_stdout
        #provera ispisuje parsiranje na stdout
        parser.parse(readableInstructionTemp)


        side = 'left' if branch else 'right'
        if getattr(node, side) is not None: #ako taj nod nema to dete
            node = getattr(node, side)
        else:
            newNode = TreeNode('t' if branch else 'f', nodeNumIt, node.numIt, readableInstruction)
            setattr(node, side, newNode)
            node = newNode
            nodeNumIt += 1
            

#for path in paths:
#    node = root
   #Go through all branches in one path and fill the tree for the missing nodes
#    for branch in path:
#        side = 'left' if branch else 'right'
#        if getattr(node, side) is not None:
#            node = getattr(node, side)
#        else:
#            newNode = TreeNode('t' if branch else 'f', nodeNumIt, node.numIt, '0')
#            setattr(node, side, newNode)
#            node = newNode
#            nodeNumIt += 1



def preorder(node, level=0):
    if node is None:
        return
    
    #Inicijalizacija
    if (node.left is None):
        node.instruction = 'end'
    else:
        node.instruction = node.left.instruction
    g.node('node' + str(node.numIt), node.instruction)

    #debugging print
    #print(" " * (level*4), node.cond, node.numIt, node.instruction)
    preorder(node.left, level+1)
    preorder(node.right, level+1)
    if(level != 0):
	#Povezivanje noda sa roditeljem
        #g.edge('node'+str(node.parentNumIt), 'node'+str(node.numIt), label =  node.cond + ': ' + node.instruction)
         g.edge('node'+str(node.parentNumIt), 'node'+str(node.numIt), label =  node.cond)

preorder(root)
#Print debugging
#print(g.source)
g.view()
