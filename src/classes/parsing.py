import constants.constants as constants
from constants.constants import keyword_tokens_dict

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = next(self.tokens, None)
        self.next_token = next(self.tokens, None)

    def advance(self):
        self.current_token = self.next_token
        self.next_token = next(self.tokens, None)

    def match(self, expected_token):
        if self.current_token == expected_token:
            print(self.current_token)
            self.advance()
        else:
            raise SyntaxError(f"Expected {expected_token}, found {self.current_token}")

    def parse(self):
        
        self.programa()
        if self.current_token is not None:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def panic_mode(self, synchronization_set):
        while self.current_token is not None and self.current_token not in synchronization_set:
            self.advance()

    def programa(self):
        try:
            self.match(keyword_tokens_dict['program'])
            self.match(keyword_tokens_dict['ident'])
            self.match("semicolon_symbol")
            self.corpo()
            self.match(".")
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program']])

    def corpo(self):
        try:
            self.dc()
            self.match(keyword_tokens_dict['begin'])
            self.comandos()
            self.match(keyword_tokens_dict['end'])
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program']])

    def dc(self):
        try:
            self.dc_c()
            self.dc_v()
            self.dc_p()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['var'], keyword_tokens_dict['program'], keyword_tokens_dict['procedure']])

    def dc_c(self):
        try:
            while self.current_token == keyword_tokens_dict['const']:
                self.match(keyword_tokens_dict['const'])
                self.match(keyword_tokens_dict['ident'])
                self.match("assignment_symbol")
                self.numero()
                self.match("semicolon_symbol")
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['var'], keyword_tokens_dict['program'], keyword_tokens_dict['procedure']])

    def dc_v(self):
        try:
            while self.current_token == keyword_tokens_dict['var']:
                self.match(keyword_tokens_dict['var'])
                self.variaveis()
                self.match("colon_symbol")
                self.tipo_var()
                self.match("semicolon_symbol")
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program'], keyword_tokens_dict['procedure']])

    def tipo_var(self):
        try:
            if self.current_token in [keyword_tokens_dict['real'], keyword_tokens_dict['integer']]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program'], keyword_tokens_dict['procedure']])

    #This concatenate procedures 'variaveis' and 'mais_var'.
    def variaveis(self):
        try:
            self.match(keyword_tokens_dict['ident'])
            while self.current_token == ",":
                self.match(",")
                self.match(keyword_tokens_dict['ident'])
        except SyntaxError as e:
            print(e)
            self.panic_mode([":"])

    def dc_p(self):
        try:
            while self.current_token == keyword_tokens_dict['procedure']:
                self.match(keyword_tokens_dict['procedure'])
                self.match(keyword_tokens_dict['ident'])
                self.parametros()
                self.match("semicolon_symbol")
                self.corpo_p()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program']])

    def parametros(self):
        try:
            if self.current_token == "opening_parenthesis_symbol":
                self.match("opening_parenthesis_symbol")
                self.lista_par()
                self.match("closing_parenthesis_symbol")
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program'], "semicolon_symbol"])

    #This concatenate procedures 'lista_par' and 'mais_par'.
    def lista_par(self):
        try:
            self.variaveis()
            self.match("colon_symbol")
            self.tipo_var()
            while self.current_token == "semicolon_symbol":
                self.match("semicolon_symbol")
                self.lista_par()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["closing_parenthesis_symbol"])

    def corpo_p(self):
        try:
            self.dc_loc()
            self.match(keyword_tokens_dict['begin'])
            self.comandos()
            self.match(keyword_tokens_dict['end'])
            self.match("semicolon_symbol")
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['procedure']])

    def dc_loc(self):
        try:
            self.dc_v()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['program'], keyword_tokens_dict['procedure']])

    def lista_arg(self):
        try:
            if self.current_token == "opening_parenthesis_symbol":
                self.match("opening_parenthesis_symbol")
                self.argumentos()
                self.match("closing_parenthesis_symbol")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["closing_parenthesis_symbol"])

    def argumentos(self):
        try:
            self.match(keyword_tokens_dict['ident'])
            while self.current_token == "semicolon_symbol":
                self.match("semicolon_symbol")
                self.argumentos()
        except SyntaxError as e:
            print(e)
            self.panic_mode([")"])

    def pfalsa(self):
        try:
            if self.current_token == keyword_tokens_dict['else']:
                self.match(keyword_tokens_dict['else'])
                self.cmd()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['program']])

    def comandos(self):
        try:
            while self.current_token in [keyword_tokens_dict['read'], keyword_tokens_dict['write'], keyword_tokens_dict['while'], keyword_tokens_dict['if'], keyword_tokens_dict['ident'], keyword_tokens_dict['begin']]:
                self.cmd()
                self.match("semicolon_symbol")
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['end']])

    def cmd(self):
        try:
            if self.current_token == keyword_tokens_dict['read']:
                self.match(keyword_tokens_dict['read'])
                self.match("opening_parenthesis_symbol")
                self.variaveis()
                self.match("closing_parenthesis_symbol")
            elif self.current_token == keyword_tokens_dict['write']:
                self.match(keyword_tokens_dict['write'])
                self.match("opening_parenthesis_symbol")
                self.variaveis()
                self.match("closing_parenthesis_symbol")
            elif self.current_token == keyword_tokens_dict['while']:
                self.match(keyword_tokens_dict['while'])
                self.match("opening_parenthesis_symbol")
                self.condicao()
                self.match("closing_parenthesis_symbol")
                self.match(keyword_tokens_dict['do'])
                self.cmd()
            elif self.current_token == keyword_tokens_dict['if']:
                self.match(keyword_tokens_dict['if'])
                self.condicao()
                self.match(keyword_tokens_dict['then'])
                self.cmd()
                self.pfalsa()
            elif self.current_token == keyword_tokens_dict['ident']:
                self.match(keyword_tokens_dict['ident'])
                if self.current_token == "assignment_symbol":
                    self.match("assignment_symbol")
                    self.expressao()
                elif self.current_token == "opening_parenthesis_symbol":
                    self.lista_arg()
            elif self.current_token == keyword_tokens_dict['begin']:
                self.match(keyword_tokens_dict['begin'])
                self.comandos()
                self.match(keyword_tokens_dict['end'])
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['end']])

    def condicao(self):
        try:
            self.expressao()
            self.relacao()
            self.expressao()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['then']])

    def relacao(self):
        try:
            if self.current_token in [keyword_tokens_dict['equal'], keyword_tokens_dict['not_equal'], keyword_tokens_dict['greater_equal'], keyword_tokens_dict['less_equal'], keyword_tokens_dict['greater'], keyword_tokens_dict['less']]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['number']])

    def expressao(self):
        try:
            self.termo()
            self.outros_termos()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['number']])

    def op_un(self):
        try:
            if self.current_token in [keyword_tokens_dict['plus'], keyword_tokens_dict['minus']]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['number'], keyword_tokens_dict['open_parenthesis']])

    def outros_termos(self):
        try:
            if self.current_token in [keyword_tokens_dict['plus'], keyword_tokens_dict['minus']]:
                self.op_ad()
                self.termo()
                self.outros_termos()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['close_parenthesis'], keyword_tokens_dict['semicolon'], keyword_tokens_dict['then']])

    def op_ad(self):
        try:
            if self.current_token in [keyword_tokens_dict['plus'], keyword_tokens_dict['minus']]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['number'], keyword_tokens_dict['open_parenthesis']])

    def termo(self):
        try:
            self.op_un()
            self.fator()
            self.mais_fatores()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['close_parenthesis'], keyword_tokens_dict['semicolon'], keyword_tokens_dict['plus'], keyword_tokens_dict['minus'], keyword_tokens_dict['then']])

    def mais_fatores(self):
        try:
            if self.current_token in [keyword_tokens_dict['mul'], keyword_tokens_dict['div']]:
                self.op_mul()
                self.fator()
                self.mais_fatores()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['close_parenthesis'], keyword_tokens_dict['semicolon'], keyword_tokens_dict['plus'], keyword_tokens_dict['minus'], keyword_tokens_dict['then']])

    def op_mul(self):
        try:
            if self.current_token in [keyword_tokens_dict['mul'], keyword_tokens_dict['div']]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['ident'], keyword_tokens_dict['number'], keyword_tokens_dict['open_parenthesis']])

    def fator(self):
        try:
            if self.current_token == keyword_tokens_dict['ident']:
                self.match(keyword_tokens_dict['ident'])
            elif self.current_token == keyword_tokens_dict['open_parenthesis']:
                self.match(keyword_tokens_dict['open_parenthesis'])
                self.expressao()
                self.match(keyword_tokens_dict['close_parenthesis'])
            else:  
                #self.current_token == keyword_tokens_dict['numero']:
                #self.match(keyword_tokens_dict['numero'])
                self.numero()
            
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['close_parenthesis'], keyword_tokens_dict['semicolon'], keyword_tokens_dict['mul'], keyword_tokens_dict['div'], keyword_tokens_dict['plus'], keyword_tokens_dict['minus'], keyword_tokens_dict['then']])

    def numero(self):
        try:
            if self.current_token in [keyword_tokens_dict['numero_int'], keyword_tokens_dict['numero_real']]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode([keyword_tokens_dict['open_parenthesis'], keyword_tokens_dict['close_parenthesis'], keyword_tokens_dict['semicolon'], keyword_tokens_dict['mul'], keyword_tokens_dict['div'], keyword_tokens_dict['plus'], keyword_tokens_dict['minus'], keyword_tokens_dict['then']])
