"""
2024, Written by the CrunchRev Authors

Module description: controls tokens which are similar to CSRF ones.
"""

import threading
import time
import secrets

class Token:
    def __init__(self):
        self.avaliable_tokens = []
        return None
    
    def internal_add_temporary_item(self, item, timeout=60):
        self.avaliable_tokens.append(item)
        threading.Timer(timeout, self.internal_remove_item, [item]).start()

    def internal_remove_item(self, item):
        if item in self.avaliable_tokens:
            self.avaliable_tokens.remove(item)

    def generateToken(self):
        secretToken = secrets.token_hex(64)

        self.internal_add_temporary_item(secretToken, timeout=120)
        return secretToken

    def checkToken(self, token):
        if token in self.avaliable_tokens:
            self.avaliable_tokens.remove(token)
            return True
        else:
            return False