from enum import Enum
from environment.environment import Shape

class DOFType(Enum):
    POSITION = 0
    ORIENTATION = 1
    ROTATION = 2 # TODO add support for manipulators

class DOF:  
    def __init__(self, name, type, range):
        self.name = name
        self.type = type
        self.range = range

class Robot:
    def __init__(self, name, dofs):
        self.name = name
        self.dofs = dofs
    
    def is_valid(self, env, q) -> tuple[bool, Shape]:
        raise NotImplementedError("is_valid not implemented for base class")