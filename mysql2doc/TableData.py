__author__ = 'yanglikun'


class Field:
    def __init__(self, name=None, type=None, comment=None, nullable=None, isPK=None):
        super().__init__()
        self.name = name
        self.type = type
        self.comment = comment
        self.nullable = nullable
        self.isPK = isPK


class Index:
    def __init__(self, isUnique=None, name=None, seqNO=None, fieldName=None, comment=None):
        super().__init__()
        self.comment = comment
        self.fieldName = fieldName
        self.seqNO = seqNO
        self.name = name
        self.isUnique = isUnique


class Table:
    def __init__(self, name=None, comment=None):
        self.name = name
        self.fields = []
        self.indices = []
        self.comment = comment

    def addField(self, field):
        self.fields.append(field)

    def addIndex(self, index):
        self.indices.append(index)
