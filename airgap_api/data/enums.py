from enum import auto
from strenum import UppercaseStrEnum, StrEnum


class AirportIATACodes(UppercaseStrEnum):
    MAG = auto()


class AirportICAOCodes(UppercaseStrEnum):
    AYMD = auto()


class AirportDataType(StrEnum):
    Airport = "airport"
