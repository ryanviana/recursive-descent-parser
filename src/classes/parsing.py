class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token = None
        self.advance()
    
    def createParsingTokens(self):
        self.tokens = [token.split(' -- ')[0] for token in self.tokens]
        print(self.tokens)

    def advance(self):
        self.current_token = self.next_token
        self.next_token = next(self.tokens, None)

    def match(self, expected_token):
        if self.current_token == expected_token:
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
            self.match("program")
            self.match("ident")
            self.match(";")
            self.corpo()
            self.match(".")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start"])

    def corpo(self):
        try:
            self.dc()
            self.match("begin")
            self.comandos()
            self.match("end")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start"])

    def dc(self):
        try:
            self.dc_c()
            self.dc_v()
            self.dc_p()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_variable", "simb_start", "simb_procedure"])

    def dc_c(self):
        try:
            while self.current_token == "simb_constant":
                self.match("simb_constant")
                self.match("simb_identifier")
                self.match("=")
                self.match("numero")
                self.match(";")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_variable", "simb_start", "simb_procedure"])

    def dc_v(self):
        try:
            while self.current_token == "simb_variable":
                self.match("simb_variable")
                self.variaveis()
                self.match(":")
                self.tipo_var()
                self.match(";")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start", "simb_procedure"])

    def tipo_var(self):
        try:
            if self.current_token in ["simb_type_real", "simb_type_integer"]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start", "simb_procedure"])

    def variaveis(self):
        try:
            self.match("simb_identifier")
            while self.current_token == ",":
                self.match(",")
                self.match("simb_identifier")
        except SyntaxError as e:
            print(e)
            self.panic_mode([":"])

    def dc_p(self):
        try:
            while self.current_token == "simb_procedure":
                self.match("simb_procedure")
                self.match("simb_identifier")
                self.parametros()
                self.match(";")
                self.corpo_p()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start"])

    def parametros(self):
        try:
            if self.current_token == "(":
                self.match("(")
                self.lista_par()
                self.match(")")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start", ";"])

    def lista_par(self):
        try:
            self.variaveis()
            self.match(":")
            self.tipo_var()
            while self.current_token == ";":
                self.match(";")
                self.lista_par()
        except SyntaxError as e:
            print(e)
            self.panic_mode([")"])

    def corpo_p(self):
        try:
            self.dc_loc()
            self.match("begin")
            self.comandos()
            self.match("end")
            self.match(";")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_procedure"])

    def dc_loc(self):
        try:
            self.dc_v()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_start", "simb_procedure"])

    def lista_arg(self):
        try:
            if self.current_token == "(":
                self.match("(")
                self.argumentos()
                self.match(")")
        except SyntaxError as e:
            print(e)
            self.panic_mode([")"])

    def argumentos(self):
        try:
            self.match("simb_identifier")
            while self.current_token == ";":
                self.match(";")
                self.argumentos()
        except SyntaxError as e:
            print(e)
            self.panic_mode([")"])

    def pfalsa(self):
        try:
            if self.current_token == "simb_else":
                self.match("simb_else")
                self.cmd()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_start"])

    def comandos(self):
        try:
            while self.current_token in ["simb_input", "simb_output", "simb_while", "simb_if", "simb_identifier", "simb_start"]:
                self.cmd()
                self.match(";")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_end"])
    def cmd(self):
        try:
            if self.current_token == "simb_input":
                self.match("simb_input")
                self.match("(")
                self.variaveis()
                self.match(")")
            elif self.current_token == "simb_output":
                self.match("simb_output")
                self.match("(")
                self.variaveis()
                self.match(")")
            elif self.current_token == "simb_while":
                self.match("simb_while")
                self.match("(")
                self.condicao()
                self.match(")")
                self.match("simb_do")
                self.cmd()
            elif self.current_token == "simb_if":
                self.match("simb_if")
                self.condicao()
                self.match("simb_then")
                self.cmd()
                self.pfalsa()
            elif self.current_token == "simb_identifier":
                self.match("simb_identifier")
                if self.current_token == ":=":
                    self.match(":=")
                    self.expressao()
                elif self.current_token == "(":
                    self.lista_arg()
            elif self.current_token == "simb_start":
                self.match("simb_start")
                self.comandos()
                self.match("simb_end")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_end"])

    def condicao(self):
        try:
            self.expressao()
            self.relacao()
            self.expressao()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_then"])

    def relacao(self):
        try:
            if self.current_token in ["simb_equal", "simb_not_equal", "simb_greater_equal", "simb_less_equal", "simb_greater", "simb_less"]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_number"])

    def expressao(self):
        try:
            self.termo()
            self.outros_termos()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_number"])

    def op_un(self):
        try:
            if self.current_token in ["simb_plus", "simb_minus"]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_number", "simb_open_parenthesis"])

    def outros_termos(self):
        try:
            if self.current_token in ["simb_plus", "simb_minus"]:
                self.op_ad()
                self.termo()
                self.outros_termos()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_close_parenthesis", "simb_semicolon", "simb_then"])

    def op_ad(self):
        try:
            if self.current_token in ["simb_plus", "simb_minus"]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_number", "simb_open_parenthesis"])

    def termo(self):
        try:
            self.op_un()
            self.fator()
            self.mais_fatores()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_close_parenthesis", "simb_semicolon", "simb_plus", "simb_minus", "simb_then"])

    def mais_fatores(self):
        try:
            if self.current_token in ["simb_mul", "simb_div"]:
                self.op_mul()
                self.fator()
                self.mais_fatores()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_close_parenthesis", "simb_semicolon", "simb_plus", "simb_minus", "simb_then"])

    def op_mul(self):
        try:
            if self.current_token in ["simb_mul", "simb_div"]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_identifier", "simb_number", "simb_open_parenthesis"])

    def fator(self):
        try:
            if self.current_token == "simb_identifier":
                self.match("simb_identifier")
            elif self.current_token == "numero":
                self.match("numero")
            elif self.current_token == "simb_open_parenthesis":
                self.match("simb_open_parenthesis")
                self.expressao()
                self.match("simb_close_parenthesis")
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_close_parenthesis", "simb_semicolon", "simb_mul", "simb_div", "simb_plus", "simb_minus", "simb_then"])

    def numero(self):
        try:
            if self.current_token in ["numero_int", "numero_real"]:
                self.advance()
        except SyntaxError as e:
            print(e)
            self.panic_mode(["simb_open_parenthesis", "simb_close_parenthesis", "simb_semicolon", "simb_mul", "simb_div", "simb_plus", "simb_minus", "simb_then"])
