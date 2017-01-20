__author__ = 'yanglikun'
from sqlalchemy import create_engine
from mysql2doc.config import dbConfigMap
from mysql2doc.config import dbConfig
from sqlalchemy import inspect
from mysql2doc import TableData


def getFieldsCommentMap(engine, table_name):
    return {row['Field']: row['Comment'] for row in engine.execute('show full columns from ' + table_name)}


def getFields(engine, inspector, table_name, fieldCommentMap):
    pkArr = inspector.get_primary_keys(table_name)
    fields = []
    for column in inspector.get_columns(table_name):
        field = TableData.Field()
        field.name = column['name']
        field.type = str(column['type']).lower()
        field.nullable = column['nullable']
        field.isPK = (column['name'] in pkArr)
        field.comment = fieldCommentMap[column['name']]
        fields.append(field)
    return fields;


def getTableComment(engine, inspector, table_name):
    tableCommentSql = "SELECT table_comment as tableComment  FROM INFORMATION_SCHEMA.TABLES  WHERE table_schema='%s' AND table_name='%s'" % (
        dbConfig.databaseName, table_name)
    tableComment = ''
    for row in engine.execute(tableCommentSql):
        tableComment = row['tableComment']
    return tableComment


def getIndices(engine, inspector, table_name, fieldCommentMap):
    indices = []
    for idx in engine.execute('SHOW INDEX FROM  ' + table_name):
        index = TableData.Index()
        index.isUnique = (idx['Non_unique'] == 0)
        index.name = str(idx['Key_name'])
        fieldName = idx['Column_name']
        index.fieldName = str(fieldName).lower()
        index.comment = fieldCommentMap[fieldName]
        index.seqNO = str(idx['Seq_in_index'])
        indices.append(index)
    return indices


def generateTableData():
    dburl = "mysql+pymysql://{userName}:{password}@{host}/{databaseName}?charset={charset}".format(**dbConfigMap)
    engine = create_engine(dburl)
    inspector = inspect(engine)
    retTabls = []
    for table_name in inspector.get_table_names():
        table = TableData.Table(table_name)
        fieldsCommentMap = getFieldsCommentMap(engine, table_name)
        table.fields = getFields(engine, inspector, table_name, fieldsCommentMap)
        table.indices = getIndices(engine, inspector, table_name, fieldsCommentMap)
        table.comment = getTableComment(engine, inspector, table_name)
        retTabls.append(table)
    return retTabls
