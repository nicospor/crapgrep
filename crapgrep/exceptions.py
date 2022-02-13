class InvalidOption(Exception):
    def __init__(self, invalid_opt):
        self.invalid_opt = invalid_opt
    def get_message(self):
        return f"pygrep: invalid option -- '{self.invalid_opt}'"
    
class InvalidPattern(Exception):
    def __init__(self, pattern):
        self.invalid = pattern
    def get_message(self):
        return f"pygrep: invalid pattern -- '{self.invalid}'"
    
