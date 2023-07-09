'''
    File: lexical_analysis.py

    Authors:
        Carolina Mokarzel - 11932247
        Fernando Braghiroli - 11800500
        Guilherme Mafra - 11272015
        Ryan Viana - 11846690

    Date: 2023-06-09
'''

from classes.moore_machine import MooreMachine
from constants.constants import TOKEN_CHAR_FLAG
from typing import List, Dict

class LexicalAnalysis():
  '''
    LexicalAnalysis class performs tokenization on input code using a MooreMachine.
      It classifies tokens based on the final state of the Moore Machine and assigns 
        output values to determine their size and valid character positions.
      The analyzer iterates through the code token by token, generates tokens with their
         respective classes, and stores them in a list.
      The class provides methods to retrieve the generated tokens.
  '''


  def __init__(
      self, 
      moore_machine: MooreMachine, 
      state_to_class_dict: (Dict[int, str]), 
      keyword_tokens_dict: (Dict[str, str])
    ):
    """
      Initialize a LexicalAnalysis object.

      Args:
          moore_machine (MooreMachine): Object of the MooreMachine class that performs tokenization.
          state_to_class_dict (Dict[int, str]): Dictionary that maps the final states of the Moore Machine to their respective classes.
          keyword_tokens_dict (Dict[str, str]): Dictionary that maps the keywords to their respective tokens.
    """
    self.moore_machine =  moore_machine
    self.tokens = []
    self.state_to_class_dict = state_to_class_dict
    self.keyword_tokens_dict = keyword_tokens_dict
  


  def getTokenClass(self, token: str, current_state: int):
    """
      Retrieves the class of a token based on the current state.

      Args:
          token (str): The token to classify.
          current_state (int): The current state of the machine.

      Returns:
          str: The class of the token.
    """
    token_class = self.state_to_class_dict[current_state] 
    if token_class != 'token':
      return token_class
    else:
      if token in self.keyword_tokens_dict.keys():
        return self.keyword_tokens_dict[token] 
      else:
        return self.keyword_tokens_dict['ident']



  def getTokenSize(self, string: str):
    """
      Calculates the size of the token.

      Args:
          string (str): The input string.

      Returns:
          int: The size of the token.
    """
    size = len(string) 
    for char in reversed(string):
      
      if char == '1':
        return size 
      size-= 1
      
    return size



  def getCurrentCode(self, code: str, moore_output: str):
    """
      Retrieves the remaining code after tokenization.

      Args:
          code (str): The input code.
          moore_output (str): The output from the Moore Machine.

      Returns:
          str: The remaining code after tokenization.
    """
    size = self.getTokenSize(moore_output)
    return code[size:]



  def mooreOutputTokenizer(self, string, moore_output):
    """
      Tokenizes the output from the Moore Machine.

      Args:
          string (str): The input string.
          moore_output (str): The output from the Moore Machine.

      Returns:
          str: The tokenized output.
    """
    token = ''.join([char for char, output_value in zip(string[:len(moore_output)], moore_output) if output_value == TOKEN_CHAR_FLAG])
    return token



  def runLexicalAnalysis(self, code: str):
    """
      Runs the lexical analysis on the given code.

      Args:
          code (str): The input code to be analyzed.
    """
    
    code += ' '

    # Iterates through the code token by token.
    while code:
      
      # Get the output and the current state
      current_state, output = self.moore_machine.runMooreMachine(code)

      # If no errors occurs 
      if current_state != -1:
        
        # If the string reaches the end
        if (output or current_state) is None:
          break
        
        # Get token and token class
        token = self.mooreOutputTokenizer(code, output)
        if token is not None:
          token_class = self.getTokenClass(token, current_state)
          self.tokens.append(f'{token_class} -- "{token}"')

        # If the code reaches the end, it is terminated. 
        if (code) is None: 
          break
        
        # Otherwise, the code is obtained by excluding the token that was defined.
        code = self.getCurrentCode(code, output)

      # If erros occurs
      else: 

        token = code[0]
        self.tokens.append(f'{output}')
        code = code[1:]
        current_state = 0



  def getTokens(self):
    """
      Retrieves the tokens and your respectivies classes generated by the lexical analysis.

      Returns:
          list: List of tokens.
    """
    return self.tokens
