from typing import Tuple
from enum import Enum


class ReportMeta:
    medical_area: str
    subtype: str
    main_concept: str
    main_concept_code: str
    aux_concept_codes: Tuple
    year: int

    def __init__(self):
        self.medical_area = None
        self.subtype = None
        self.main_concept = None
        self.main_concept_code = None
        self.aux_concept_codes = None
        self.year = None


class Subtype(Enum):
    medical_area = 0
    subtype = 1
    main_concept = 2
    main_concept_code = 3
    aux_concept_codes = 4
    year = 5
