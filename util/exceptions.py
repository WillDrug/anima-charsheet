

class RuleError(Exception):
    pass

class CodeError(Exception):
    pass

class CheekyHack(Exception):
    pass

class NotFound(CodeError):
    pass

class NotEnoughData(CodeError):
    pass

class OverLimit(RuleError):
    pass

class Panik(CodeError):
    pass

class MergedResource(CheekyHack):
    pass

class NotAvailable(RuleError):
    pass

class NotAllowed(RuleError):
    pass

class NotCompatible(RuleError):
    pass

class PrerequisiteError(RuleError):
    pass

class NotEnough(RuleError):
    pass