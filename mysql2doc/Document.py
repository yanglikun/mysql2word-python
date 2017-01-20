__author__ = 'yanglikun'
from docx import Document
from operator import attrgetter
from mysql2doc import DB


class Word:
    def __bold(ele, text):
        ele.paragraphs[0].add_run(text).bold = True

    def __addTable(document, table, seqNO):
        document.add_heading("{} {}".format(seqNO, table.name), level=1)
        document.add_paragraph(table.comment)
        tableGrid = document.add_table(rows=1, cols=4, style='TableGrid')
        titleRow = tableGrid.rows[0].cells
        Word.__bold(titleRow[0], '字段')
        titleRow[1].text = '类型'
        titleRow[2].text = '备注'
        titleRow[3].text = '允许为空'
        for field in table.fields:
            row = tableGrid.add_row().cells
            row[0].text = field.name
            row[1].text = field.type
            row[2].text = field.comment
            if field.nullable:
                row[3].text = '是'
            else:
                row[3].text = '否'
        document.add_paragraph()
        document.add_paragraph('索引列', style='ListBullet')
        idxTableGrid = document.add_table(rows=1, cols=5, style='TableGrid')
        idxTitleRow = idxTableGrid.rows[0].cells
        Word.__bold(idxTitleRow[0], '唯一索引')
        idxTitleRow[1].text = '索引名称'
        idxTitleRow[2].text = '索引顺序'
        idxTitleRow[3].text = '字段'
        idxTitleRow[4].text = '备注'
        for index in table.indices:
            idxRow = idxTableGrid.add_row().cells
            if index.isUnique:
                Word.__bold(idxRow[0], '是');
            else:
                Word.__bold(idxRow[0], '否');
            idxRow[1].text = index.name
            idxRow[2].text = index.seqNO
            idxRow[3].text = index.fieldName
            idxRow[4].text = index.comment
        pass

    def createFile(fileName='table'):
        document = Document()
        document.add_heading('数据库表结构', 0)
        document.add_paragraph('数据库表结构')
        for idx, table in enumerate(DB.generateTableData()):
            Word.__addTable(document, table, idx)
        document.add_page_break()
        document.save(fileName + '.docx')
