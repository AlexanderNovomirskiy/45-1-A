# Описание классов метаданных


# Класс схем
class Schema:
    # Конструктор класса
    def __init__(self):
        # Атрибуты
        self.name = None
        self.version = None
        self.fulltext_engine = None
        self.description = None

        # Массивы доменов и таблиц
        self.domains = []
        self.tables = []


# Класс доменов
class Domain:
    # Конструктор класса
    def __init__(self):
        # Атрибуты
        self.name = None
        self.description = None
        self.type = None
        self.length = None
        self.char_length = None
        self.precision = None
        self.scale = None
        self.width = None
        self.align = None

        # Свойства
        self.show_null = None
        self.show_lead_nulls = None
        self.thousands_separator = None
        self.summable = None
        self.case_sensitive = None


# Класс таблиц
class Table:
    # Конструктор класса
    def __init__(self):
        # Атрибуты
        self.name = None
        self.description = None
        self.ht_table_flags = None
        self.access_level = None
        self.temporal_mode = None
        self.means = None

        # Свойства
        self.add = None
        self.edit = None
        self.delete = None

        # Массивы полей, ограничений и индексов
        self.fields = []
        self.constraints = []
        self.indexes = []


# Класс полей
class Field:
    # Конструктор класса
    def __init__(self):
        # Атрибуты
        self.name = None
        self.rname = None
        self.domain = None
        self.description = None

        # Свойства
        self.input = None
        self.edit = None
        self.show_in_grid = None
        self.show_in_details = None
        self.is_mean = None
        self.autocalculated = None
        self.required = None


# Класс ограничений
class Constraint:
    # Конструктор класса
    def __init__(self):
        # Атрибуты
        self.name = None
        self.kind = None
        self.items = None
        self.reference = None
        self.expression = None

        # Свойства
        self.has_value_edit = None
        self.cascading_delete = None
        self.full_cascading_delete = None


# Класс индексов
class Index:
    def __init__(self):
        # Атрибуты
        self.name = None
        self.field = None
        self.expression = None

        # Свойства
        self.uniqueness = None
        self.fulltext = None
        self.local = None
        self.descend = None
