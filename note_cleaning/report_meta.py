from typing import Tuple
from enum import Enum


class ReportMeta:
    record_type: str = None
    department: str = None
    main_concept: str = None
    main_concept_code: str = None
    aux_concept_codes: Tuple = None
    year: int

    def __init__(self):
        self.record_type = None
        self.department = None
        self.main_concept = None
        self.main_concept_code = None
        self.aux_concept_codes = None
        self.year = None


class Subtype(Enum):
    record_type = 0
    department = 1
    main_concept = 2
    main_concept_code = 3
    aux_concept_codes = 4
    year = 5
