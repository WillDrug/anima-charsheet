

class RuleError(Exception):
    pass

class CodeError(Exception):
    pass

class NotFound(CodeError):
    pass

class NotEnoughData(CodeError):
    pass

class OverLimit(RuleError):
    pass

class Panik(CodeError):
    pass

class FollowTheRules(CodeError):
    pass