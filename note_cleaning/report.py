from typing import List, Dict, Tuple, T
from itertools import islice
from more_itertools import peekable
from io import IOBase
import regex

from .report_meta import ReportMeta, Subtype


class Report:
    id_: int
    meta: ReportMeta
    content: List[str]

    def __init__(self, id_):
        self.id_ = int(id_)
        self.content = list()

    def read(self, lines: List[str], index: int):
        index = self.read_meta(lines, index)
        index = self.read_content(lines, index)
        return index

    def read_meta(self, lines: List[str], index: int) -> int:
        self.meta = ReportMeta()
        for metaindex in range(6):
            raw = lines[index + metaindex]
            meta_type = Subtype(metaindex)
            setattr(self.meta, meta_type.name,
                    self.meta_cleaner(raw, meta_type))
        return index + 9

    def meta_cleaner(self, raw: str, subtype: Subtype):
        basics = [Subtype(i) for i in [0, 1, 2, 3, 5]]
        if subtype in basics:
            return raw.strip()
        elif subtype == Subtype.aux_concept_codes:
            return raw.split(',')
        else:
            raise ValueError('Uncleanable subtype, verify data')

    def read_content(self, lines: List[str], index: int) -> int:
        while index < (len(lines) - 1):
            if report_id(lines[index]) is None:
                self.content.append(lines[index])
                index += 1
            else:
                return index
        return len(lines)


def report_id(line):
    id_ = regex.search('REPORT_ID=\d+', line)
    if id_ is not None:
        id_ = regex.search('\d+', id_.group())
        return id_.group()
    return None
