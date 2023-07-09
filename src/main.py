'''
    File: main.py

    Authors:
        Carolina Mokarzel - 11932247
        Fernando Braghiroli - 11800500
        Guilherme Mafra - 11272015
        Ryan Viana - 11846690

    Date: 2023-06-09
'''

from constants.constants import P_ALPHABET, \
    transition_table, output_table, \
    state_to_class_dict, keyword_tokens_dict, \
    INPUT_FILE_PATH, OUTPUT_FILE_PATH
from classes.moore_machine import MooreMachine
from classes.lexical_analysis import LexicalAnalysis
from classes.parsing import Parser
from utils.utils import getValidTokens

moore_machine = MooreMachine( 
  P_ALPHABET, # input_alphabet
  [0,1,2,15,16,17,23], # states
  transition_table, 
  0, # initial_state
  state_to_class_dict.keys(), # final_states
  ['1','2','3'], # output_alphabet
  output_table 
)

lexical_analysis = LexicalAnalysis(
  moore_machine, 
  state_to_class_dict, 
  keyword_tokens_dict
)

with open(INPUT_FILE_PATH, 'r') as file:
    code = file.read()

lexical_analysis.runLexicalAnalysis(code)

tokens = ['TOKEN CLASS -- TOKEN\n']
tokens += lexical_analysis.getTokens()
output = '\n'.join(tokens)

with open(OUTPUT_FILE_PATH, 'w') as file:
    file.write(output)

# print(getValidTokens(tokens))
parsing = Parser(getValidTokens(tokens))
parsing.parse()