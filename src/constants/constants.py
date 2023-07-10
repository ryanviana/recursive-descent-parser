'''
    File: constants.py

    Authors:
        Carolina Mokarzel - 11932247
        Fernando Braghiroli - 11800500
        Guilherme Mafra - 11272015
        Ryan Viana - 11846690

    Date: 2023-06-09
'''

import string


INPUT_FILE_PATH = '../input/input.txt'
OUTPUT_FILE_PATH = '../output/output.txt'

# Definition of the P-- alphabet.

DIGITS = [str(i) for i in range(10)]
ALPHABET_LETTERS  = [*list(string.ascii_lowercase),*list(string.ascii_uppercase)]
WHITE_SPACES = [' ','\t','\n','\v','\f','\r',None]
DIGITS = [str(i) for i in range(10)]
WHITE_SPACES = tuple([' ','\t','\n','\v','\f','\r',None])
OTHERS = ['}','{','(',')','.',':','>',';',',','<','/','*','-','+','=']

P_ALPHABET = tuple([*DIGITS, *ALPHABET_LETTERS, *WHITE_SPACES, *OTHERS])
WHITE_SPACES = tuple(WHITE_SPACES)
CHARS = tuple([*DIGITS, *ALPHABET_LETTERS])
ALPHABET_LETTERS = tuple([*ALPHABET_LETTERS])
DIGITS = tuple(DIGITS)
POINT = tuple('.')

# Definition of the transition table
transition_table = {

  0:{ 
      DIGITS:1,
      ALPHABET_LETTERS:2,
      tuple(['}']):3,
      tuple(['{']):4,
      tuple(['(']):5,
      tuple([')']):6,
      tuple(['.']):7,
      tuple([':']):8,
      tuple(['>']):9,
      tuple([';']):10,
      tuple([',']):11,
      tuple(['<']):12,
      tuple(['/']):13,
      tuple(['*']):14,
      tuple(['-']):15,
      tuple(['+']):16,
      WHITE_SPACES:0 
     },
  1:{
      DIGITS:1,
      POINT:17,
      WHITE_SPACES:18
  },
  2:{
      CHARS:2,
      WHITE_SPACES:19
  },
  8:{
      tuple(['=']):20,
      WHITE_SPACES:21
  },
  9:{
      tuple(['=']):22,
      WHITE_SPACES:23
  },
  12:{
      tuple(['=']):24,
      tuple(['>']):25,
      WHITE_SPACES:26
  },
  17:{
      DIGITS:17,
      WHITE_SPACES:27
  }
}



WHITE_SPACE_CHAR_FLAG = '0'
TOKEN_CHAR_FLAG = '1'
NON_TOKEN_CHAR_FLAG = '2'



# Definition of the relationship between the states and their respective
#outputs in the Moore Machine. 
output_table = {
      tuple([0]):WHITE_SPACE_CHAR_FLAG,
      tuple([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,20,22,24,25]):TOKEN_CHAR_FLAG,
      tuple([18,19,21,23,26,27]):NON_TOKEN_CHAR_FLAG
}



# Definition of the relationship between the final states and their 
#respective token class.
state_to_class_dict = {
    3: 'closing_braces_symbol',
    4: 'opening_braces_symbol',
    5: 'opening_parenthesis_symbol',
    6: 'closing_parenthesis_symbol',
    7: 'period_symbol',
    10: 'semicolon_symbol',
    11: 'comma_symbol',
    13: 'division_symbol',
    14: 'multiplication_symbol',
    15: 'subtraction_symbol',
    16: 'addition_symbol',
    18: 'integer_number',
    19: 'token',
    20: 'assignment_symbol',
    21: 'colon_symbol',
    22: 'greater_than_or_equal_symbol',
    23: 'greater_than_symbol',
    24: 'less_than_or_equal_symbol',
    25: 'not_equal_symbol',
    26: 'less_than_symbol',
    27: 'floating_point_number'
}


keyword_tokens_dict = {
    'program': 'simb_start',
    'ident': 'simb_identifier',
    'begin': 'simb_start',
    'end': 'simb_end',
    'const': 'simb_constant',
    'var': 'simb_variable',
    'real': 'simb_type_real',
    'integer': 'simb_type_integer',
    'procedure': 'simb_procedure',
    'read': 'simb_input',
    'write': 'simb_output',
    'while': 'simb_while',
    'do': 'simb_do',
    'if': 'simb_if',
    'then': 'simb_then',
    'else': 'simb_else',
    'for': 'simb_for',
    'to': 'simb_to'
}

user_friendly_dict = {
    'closing_braces_symbol': 'closing braces',
    'opening_braces_symbol': 'opening braces',
    'opening_parenthesis_symbol': 'opening parenthesis',
    'closing_parenthesis_symbol': 'closing parenthesis',
    'period_symbol': 'period',
    'semicolon_symbol': 'semicolon',
    'comma_symbol': 'comma',
    'division_symbol': 'division',
    'multiplication_symbol': 'multiplication',
    'subtraction_symbol': 'subtraction',
    'addition_symbol': 'addition',
    'integer_number': 'integer number',
    'token': 'token',
    'assignment_symbol': 'assignment',
    'colon_symbol': 'colon',
    'greater_than_or_equal_symbol': 'greater than or equal',
    'greater_than_symbol': 'greater than',
    'less_than_or_equal_symbol': 'less than or equal',
    'not_equal_symbol': 'not equal',
    'less_than_symbol': 'less than',
    'floating_point_number': 'floating point number',
    'simb_start': 'keyword program',
    'simb_identifier': 'keyword ident',
    'simb_start': 'keyword begin',
    'simb_end': 'keyword end',
    'simb_constant': 'keyword const',
    'simb_variable': 'keyword var',
    'simb_type_real': 'keyword real',
    'simb_type_integer': 'keyword integer',
    'simb_procedure': 'keyword procedure',
    'simb_input': 'keyword read',
    'simb_output': 'keyword write',
    'simb_while': 'keyword while',
    'simb_do': 'keyword do',
    'simb_if': 'keyword if',
    'simb_then': 'keyword then',
    'simb_else': 'keyword else',
    'simb_for': 'keyword for',
    'simb_to': 'keyword to'
}
