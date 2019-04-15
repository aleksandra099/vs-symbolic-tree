from ply import lex as lex
from ply import yacc as yacc
import sys

tokens = [

	'LP',
	'RP',
	#'TRUE',
	'FALSE',
	'INT',
	'FLOAT',

	#'BIN',
	#'OCT',
	#'HEX',

	'EQUALITY',
	'NE',
	'LT',
	'LE',
	'GT',
	'GE',

	'NAME',
	'TYPE',

	'ADD',
	'SUB',
	'MUL',
	'DIV',
	'REM',

	'AND',
	'OR',
	'XOR',
	'SHL',
	#'ASHR',
	'LSHR',

	'REFN',
	'DOTS',
	'READ'
	
]

t_DOTS = r'\:'
t_LP = r'\('
t_RP = r'\)'
#t_TRUE = r'true'

t_ignore = r' '

def t_READ(t):
	r'Read(LSB|MSB)?'
	t.type = 'READ'
	return t

def t_REFN(t):
	r'N[0-9]+'
	t.type = 'REFN'
	return t
###
def t_ADD(t):
	r'Add'
	t.type = 'ADD'
	return t

def t_DIV(t):
	r'(UDiv|SDiv)'
	t.type = 'ADD'
	return t

def t_REM(t):
	r'(URem|SRem)'
	t.type = 'REM'
	return t

def t_SUB(t):
	r'Sub'
	t.type = 'SUB'
	return t

def t_MUL(t):
	r'Mul'
	t.type = 'MUL'
	return t
###
def t_TYPE(t):
	r'w[0-9]+'
	t.type = 'TYPE'
	return t

def t_FALSE(t):
	r'false'
	t.type = 'FALSE'
	return t

###
def t_EQUALITY(t):
	r'Eq'
	t.type = 'EQUALITY'
	return t

def t_NE(t):
	r'Ne'
	t.type = 'NE'
	return t

def t_LT(t):
	r'(Ult|Slt)'
	t.type = 'LT'
	return t

def t_LE(t):
	r'(Ule|Sle)'
	t.type = 'LE'
	return t

def t_GT(t):
	r'(Ugt|Sgt)'
	t.type = 'GT'
	return t

def t_GE(t):
	r'(Uge|Sge)'
	t.type = 'GE'
	return t
###

def t_AND(t):
	r'And'
	t.type = 'AND'
	return t

def t_OR(t):
	r'Or'
	t.type = 'OR'
	return t

def t_XOR(t):
	r'Xor'
	t.type = 'XOR'
	return t

def t_SHL(t):
	r'Shl'
	t.type = 'SHL'
	return t

def t_LSHR(t):
	r'(LShr|AShr)'
	t.type = 'LSHR'
	return t
###
'''
def t_BIN(t):
	r'[+-]?(0b)[01_]+'
	t.value = str(t.value)
	return t

def t_OCT(t):
	r'[+-]?(0o)[0-7_]+'
	t.value = str(t.value)
	return t

def t_HEX(t):
	r'[+-]?(0x)[0-9a-fA-F_]+'
	t.value = str(t.value)
	return t
'''
def t_FLOAT(t):
	r'[+-]?(fp)?\d+\.\d+'
	t.value = str(t.value)
	return t

def t_INT(t):
	r'(([+-]?(i)?[0-9]+)|true)'
	t.value = str(t.value)
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9._]*'
	#t.value = str(t.value)
	t.type = 'NAME'
	return t

def t_error(t):
	print("Illegal characters!")
	t.lexer.skip(1)

lexer = lex.lex() 

precedence = (
	#('left','ADD','SUB')
)

#testiramo pojedinacne tokene

lexer.input("N0")

while True:
	tok = lexer.token()
	if not tok:
		break
	print(tok)

def p_calc(p):
	'''
	calc : expression
		 | empty
	'''
	
	#print(p[1])
	print(run(p[1]))

def p_expression_eq(p):
	'''
	expression : LP EQUALITY expression expression RP
			| LP NE expression expression RP
			| LP LT expression expression RP
			| LP LE expression expression RP
			| LP GT expression expression RP
			| LP GE expression expression RP
	'''
	p[0] = (p[2],p[4],p[3])

def p_expression_eq_false(p):
	'''
	expression : LP EQUALITY FALSE expression RP
	'''
	p[0] = (p[2],p[3],p[4])

def p_expression_refn(p):
	'''
	expression : REFN DOTS LP READ TYPE INT NAME RP
	'''
	p[0] = ('ref',p[1],p[7])

def p_expression_refn_var(p):
	'''
	expression : REFN	
	'''
	p[0] = ('refn',p[1])

def p_expression_add(p):
	'''
	expression : LP ADD expression expression RP
			| LP SUB expression expression RP
			| LP MUL expression expression RP
			| LP DIV expression expression RP
			| LP REM expression expression RP
	'''
	p[0] = (p[2],p[3],p[4])

def p_expression_and(p):
	'''
	expression : LP AND expression expression RP
			| LP OR expression expression RP
			| LP XOR expression expression RP
			| LP SHL expression expression RP
			| LP LSHR expression expression RP
			
	'''
	p[0] = (p[2],p[3],p[4])

def p_expression_int_float(p):
	'''
	expression : INT
		| FLOAT	
	'''
	p[0] = p[1]

def p_expression_var(p):
	'''
	expression : TYPE NAME
	'''
	p[0] = ('var',p[2])

def p_error(p):
	print("Syntax error found!")

def p_empty(p):
	'''
	empty :
	'''
	p[0] = None

parser = yacc.yacc()
env = {}
def run(p):
	global env
	if type(p) == tuple:
		if p[0] == 'Eq' and p[1] == 'false':
			return '!(' + run(p[2]) + ')'
		elif p[0] == 'Eq':
			return run(p[1]) + ' == ' + run(p[2])
		elif p[0] == 'Ne':
			return run(p[1]) + ' != ' + run(p[2])
		elif p[0] == 'Ult' or p[0] == 'Slt':
			return run(p[1]) + ' < ' + run(p[2])
		elif p[0] == 'Ule' or p[0] == 'Sle':
			return run(p[1]) + ' <= ' + run(p[2])
		elif p[0] == 'Ugt' or p[0] == 'Sgt':
			return run(p[1]) + ' > ' + run(p[2])
		elif p[0] == 'Uge' or p[0] == 'Sge':
			return run(p[1]) + ' >= ' + run(p[2])
		elif p[0] == 'var':
		 	return p[1]
		elif p[0] == 'Add':
		 	return run(p[1]) + ' + ' + run(p[2])
		elif p[0] == 'Sub':
		 	return run(p[1]) + ' - ' + run(p[2])
		elif p[0] == 'Mul':
		 	return run(p[1]) + ' * ' + run(p[2])
		elif p[0] == 'UDiv' or p[0] == 'SDiv':
		 	return run(p[1]) + ' / ' + run(p[2])
		elif p[0] == 'URem' or p[0] == 'SRem':
		 	return run(p[1]) + ' % ' + run(p[2])
		elif p[0] == 'And':
		 	return run(p[1]) + ' /\ ' + run(p[2])
		elif p[0] == 'Or':
		 	return run(p[1]) + ' \/ ' + run(p[2])
		elif p[0] == 'Xor':
		 	return run(p[1]) + ' ^ ' + run(p[2])
		elif p[0] == 'Shl':
		 	return run(p[1]) + ' << ' + run(p[2])
		elif p[0] == 'LShr' or p[0] == 'AShr':
		 	return run(p[1]) + ' >> ' + run(p[2])
		elif p[0] == 'ref':
			env[p[1]] = run(p[2])
			return p[2]
		elif p[0] == 'refn':
			if p[1] not in env:
				return 'Undeclared variable found!'
			else:
		  		return env[p[1]]
	else:
		return p

while True:
	try:
		s = input('>>')
	except EOFError:
		break
	parser.parse(s)
















		
