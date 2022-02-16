class InvalidOptionError(Exception):
    def __init__(self, invalid_opt):
        self.invalid_opt = invalid_opt

    def get_message(self):
        return f"crapgrep: invalid option -- '{self.invalid_opt}'"


class InvalidPatternError(Exception):
    def __init__(self, pattern):
        self.invalid = pattern

    def get_message(self):
        return f"crapgrep: invalid pattern -- '{self.invalid}'"
