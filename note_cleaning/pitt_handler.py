from typing import List, Dict, Tuple, T
from more_itertools import peekable

from note_cleaning.report import Report, report_id
from util.db_util import DatabaseHandle


class PittHandler:
    reports: List[Report]

    def __init__(self):
        self.reports: List[Report] = list()

    def split_reports(self, note: str):
        ''' note: filename for set of UPitt clinical notes'''
        current_pid = 0
        lines = [x.strip() for x in
                 open(note, 'r').readlines()]
        index = 0
        while index < (len(lines) - 1):
            current_pid = report_id(lines[index])
            index += 1
            self.reports.append(Report(current_pid))
            index = self.reports[-1].read(lines, index)

    def to_files(self, dir_, outfile_base='pitt_report_'):
        for report in self.reports:
            report.content = [(line + '\n')
                              for line in report.content
                              if line != '']
            fname = f'{outfile_base}{report.id_}'
            path = f'{dir_}/{fname}.txt'
            with open(path, 'w+') as outfile:
                outfile.writelines(report.content)

    def meta_to_db(self, params, table='meta', drop=False):
        handle = DatabaseHandle(params=params)
        handle.create_meta_table(table=table, drop=drop)
        meta = list()
        for report in self.reports:
            # We can do this because the order of info
            # in ReportMeta = order in db_util.create_meta_table
            meta.append(
                tuple([
                    report.id_,
                    *list(vars(report.meta).values())]))
        handle.populate_meta(data=meta)
