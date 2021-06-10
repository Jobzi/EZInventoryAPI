from enum import Enum


class StatusConstants(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    DELETED = 'DELETED'


class OperationConstants(Enum):
    ADD = 'ADD'
    REMOVE = 'REMOVE'


class DniTypes(Enum):
    STANDARD = 'STANDARD'
    RUC = 'RUC'
    PASSPORT = 'PASSPORT'


class MessureUnits(Enum):
    UNITS = "UNIT"
    GRAMS = "GRAMS"
    LITRE = "LITRE"
    METERS = "METER"


class DbDialects(Enum):
    POSTGRESQL = 'postgresql'
    SQLITE = 'sqlite'
