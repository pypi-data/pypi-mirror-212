__all__ = ["TokenError", "UnknownError"]


class Error(Exception):
    pass


class TokenError(Error):
    def __str__(self):
        return (
            f"! attempt to re-issue the token failed ! > "
            f'{self.args[0] if len(self.args) == 1 else ", ".join(self.args)} '
        )


class UnknownError(Error):
    def __str__(self):
        return (
            f"! an unexpected error occurred ! > "
            f'{self.args[0] if len(self.args) == 1 else ", ".join(self.args)} '
        )
