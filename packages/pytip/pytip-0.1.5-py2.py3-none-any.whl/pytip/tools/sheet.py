from typing import Any
import pandas
import openpyxl


class Excel:
    r"""다중 Sheet 를 갖는 Excel 파일 데이터 불러오기
    filepath : 엑셀파일
    @files -> (list) :: 폴더내 파일 가져오기
    @names -> (list) :: sheet 이름목록
    @sheet -> (DataFrame) """

    def __init__(self, file:str):
        self.wb = openpyxl.load_workbook(file)

    def __repr__(self) -> str:
        return 'Openpyxl Excel by worksheet'

    @property
    def names(self) -> list:
        r"""Excel WorkSheet 목록 가져오기"""
        return self.wb.sheetnames

    def sheet(self, name=None):
        r"""시트 데이터 가져오기"""
        if name:
            return pandas.DataFrame(self.wb[name].values)
        return pandas.DataFrame(self.wb[self.names[0]].values)
