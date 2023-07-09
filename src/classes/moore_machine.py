'''
    File: moore_machine.py

    Authors:
        Carolina Mokarzel - 11932247
        Fernando Braghiroli - 11800500
        Guilherme Mafra - 11272015
        Ryan Viana - 11846690

    Date: 2023-06-09
'''

from typing import List, Dict
from utils.utils import handleError

class MooreMachine():
  """
    Represents a Moore Machine, which is a finite-state machine with output.
    The machine transitions between states based on the current state and input
    characters, and produces output based on the current state.
  """
  


  def __init__(
      self, 
      input_alphabet: List[str], 
      states: List[int], 
      transition_table: (Dict[int, Dict[List[str], int]]), 
      initial_state: (int), 
      final_states: (List[int]), 
      output_alphabet: (List[str]), 
      output_table: (Dict[List[int], str])
    ):
    """
      Initializes a Moore Machine.

      Args:
          input_alphabet: List of valid input characters.
          states: List of possible states.
          transition_table: Transition table defining state transitions based on input characters.
          initial_state : Initial state of the machine.
          final_states : List of final/accepting states.
          output_alphabet : List of valid output characters.
          output_table : Output table defining outputs 
            based on states.
    """

    self.input_alphabet = input_alphabet
    self.states = states
    self.transition_table = transition_table
    self.initial_state = initial_state
    self.final_states = final_states
    self.output_alphabet = output_alphabet
    self.output_table = output_table
    self.DIGITS = tuple([str(i) for i in range(10)])



  def transition_function(self, state_in: int, char: str):
    """
      Computes the next state based on the current state and input character.

      Args:
          state_in (int): Current state of the machine.
          char (str): Current input character.

      Returns:
          int: Next state based on the transition table.
    """

    if state_in not in self.transition_table.keys():
      return None

    for input, state_out in self.transition_table[state_in].items():  
      
      if char in input:
        return state_out
     
      elif None in input:
        return state_out

    return None

  

  def output_function(self, current_state: int):
    """
      Computes the output based on the current state and output table.

      Args:
          current_state (int): Current state of the machine.

      Returns:
          str: Output corresponding to the current state.
    """

    for states, output in self.output_table.items():  
      
      if current_state in states:   
        return output 
    
    return None
  
    

  def runMooreMachine(self, string: str):
    """
        Runs the Moore Machine on the given string.

        Args:
            string (str): Input string to be processed by the machine.

        Returns:
            Tuple[int, str]: Tuple containing the final state and output if 
                a final state is reached, otherwise (None, None). 
              If an error occurs, it returns (-1, error_message).
    """

    current_state = self.initial_state
    output =  ''

    # Iterates character by character until an error is encountered in a character 
    #or the final accepting state of the automaton is reached.
    while string:
      char = string[0]

      try:
        # Incrementing an output based on the execution of the transition table 
        current_state = self.transition_function(current_state, char)
        error = handleError(current_state, char, self.input_alphabet)
        
        # If no error occurs, the output is incremented according to the output table.
        if error is None:
          
          output += self.output_function(current_state)
          if current_state in self.final_states:
            return current_state, output 
        
        # If no error occurs, the output will be the error accompanied by the negative 
        #state, serving as a flag.
        else:
          return -1, error

      except Exception as e:
        print(f'Error: {e}')


      string = string[1:]
      
    # If the string reaches the end, None is returned 
    return None, None