'''
    File: utils.py

    Authors:
        Carolina Mokarzel - 11932247
        Fernando Braghiroli - 11800500
        Guilherme Mafra - 11272015
        Ryan Viana - 11846690

    Date: 2023-06-09
'''

from typing import List, Dict

def createParsingTokens(tokens):
    tokens = [token.split(' -- ')[0] for token in tokens[1:]]
    return tokens

def handleError(current_state: int, char: str, input_alphabet: List[str]):

  """
  Handles error cases in the Moore Machine.
  
  Args:
      current_state (int): Current state of the machine.
      char (str): Current character being processed.
      input_alphabet (List[str]): List of valid input characters.

  Returns:
      str: Error message if the character is invalid, otherwise None.
  """
  
  DIGITS = [str(i) for i in range(10)]
  WHITE_SPACES = tuple([' ','\t','\n','\v','\f','\r',None])
  
  # Invalid characters found error
  if (current_state in [0,1,2,8,9,12,17]) and (char not in input_alphabet):
    return f"Invalid character: {char}"
    
  # Invalid number error
  elif (current_state in [17]) and (char not in [*WHITE_SPACES,*DIGITS]):
    return f"Invalid number: {char}"
  return None