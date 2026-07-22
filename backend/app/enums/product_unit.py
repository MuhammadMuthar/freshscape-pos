from enum import Enum


class ProductUnit(str, Enum):
    PCS = "pcs"
    KG = "kg"
    LITRE = "litre"
    BOX = "box"
    PACK = "pack"