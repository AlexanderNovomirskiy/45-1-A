# Использование библиотеки ElementTree(для работы с xml)
from xml.etree import ElementTree as etree
# Файл для представления метаданных
from дополнения.schema_classes import *


# Класс преобразования XDB в RAM
class xdb_to_ram:
    def __init__(self, path_to_file):
        self.schema = Schema()  # shema - класс метаданных
        self.tree = etree.parse(path_to_file)  # импорт данных из файла

    # Преобразуем XDB в RAM представление
    def parsing(self):
        root = self.tree.getroot()  # получение корня дерева
        self._parse_schema(root)  # перобразование данных в ram

    def _parse_schema(self, root):
        schema_attrib = root.attrib  # получение атрибутов
        for attrib in schema_attrib:  # цикл проверки атрибутов
            if attrib == "name":
                self.schema.name = root.attrib["name"]
            elif attrib == "version":
                self.schema.version = root.attrib["version"]
            elif attrib == "fulltext_engine":
                self.schema.fulltext_engine = root.attrib["fulltext_engine"]
            elif attrib == "description":
                self.schema.description = root.attrib["description"]

        # Преобразование доменов и таблиц
        self.schema.domains = self._parse_domain(root)
        self.schema.tables = self._parse_table(root)

    # Преобразуем домены
    def _parse_domain(self, root):
        domains = []
        # Перебираем дочерние элементы с именем "domains" корня дерева
        for child in root.iter("domains"):
            # Перебираем дочерние элементы элемента "domains"
            for domain in child:
                # Создаём переменную класса Domain
                temp_domain = Domain()
                # Получаем атрибуты текущего в цикле элемента
                domain_attrib = domain.attrib

                # Перебираем атрибуты элемента domain
                for attrib in domain_attrib:
                    if attrib == "name":
                        temp_domain.name = domain_attrib[attrib]

                    elif attrib == "description":
                        temp_domain.description = domain_attrib[attrib]

                    elif attrib == "type":
                        temp_domain.type = domain_attrib[attrib]

                    elif attrib == "align":
                        temp_domain.align = domain_attrib[attrib]

                    elif attrib == "length":
                        temp_domain.length = domain_attrib[attrib]

                    elif attrib == "width":
                        temp_domain.width = domain_attrib[attrib]

                    elif attrib == "precision":
                        temp_domain.precision = domain_attrib[attrib]

                    elif attrib == "char_length":
                        temp_domain.char_length = domain_attrib[attrib]

                    elif attrib == "scale":
                        temp_domain.scale = domain_attrib[attrib]

                    elif attrib == "props":
                        # Перебираем значения атрибута "props"
                        props = domain_attrib[attrib].split(", ")
                        for prop in props:
                            if prop == "show_null":
                                temp_domain.show_null = True

                            elif prop == "show_lead_nulls":
                                temp_domain.show_lead_nulls = True

                            elif prop == "thousand_separator":
                                temp_domain.thousand_separator = True

                            elif prop == "summable":
                                temp_domain.summable = True

                            elif prop == "case_sensitive":
                                temp_domain.case_sensitive = True

                            else:  # В случае обнаружения неизвестного свойства
                                print(
                                    "Неизвестное свойство %s у домена %s"
                                    % (prop, domain_attrib["name"])
                                )
                                exit(1)
                    else:  # В случае обнаружения неизвестного атрибута
                        print(
                            "Неизвестный атрибут %s у домена %s"
                            % (attrib, domain_attrib["name"])
                        )
                        exit(1)

                # Добавляем домен в массив доменов
                domains.append(temp_domain)

        return domains

    # Преобразуем таблицы
    def _parse_table(self, root):
        tables = []
        # Перебираем дочерние элементы с именем "tables" корня дерева
        for child in root.iter("tables"):
            # Перебираем дочерние элементы элемента "tables"
            for table in child:
                # Создаём переменную класса Table
                temp_table = Table()
                # Получаем атрибуты текущего в цикле элемента
                table_attrib = table.attrib

                # Перебираем атрибуты элемента
                for attrib in table_attrib:
                    if attrib == "name":
                        temp_table.name = table_attrib[attrib]

                    elif attrib == "description":
                        temp_table.description = table_attrib[attrib]

                    elif attrib == "ht_table_flags":
                        temp_table.ht_table_flags = table_attrib[attrib]

                    elif attrib == "access_level":
                        temp_table.access_level = table_attrib[attrib]

                    elif attrib == "temporal_mode":
                        temp_table.temporal_mode = table_attrib[attrib]

                    elif attrib == "means":
                        temp_table.means = table_attrib[attrib]

                    elif attrib == "props":
                        # Перебираем значения атрибута "props"
                        props = table_attrib[attrib].split(", ")
                        for prop in props:
                            if prop == "add":
                                temp_table.add = True

                            elif prop == "edit":
                                temp_table.edit = True

                            elif prop == "delete":
                                temp_table.delete = True

                            else:  # В случае обнаружения неизвестного свойства
                                print(
                                    "Неизвестное свойство '%s' у таблицы '%s'"
                                    % (prop, table_attrib["name"])
                                )
                                exit(1)
                    else:  # В случае обнаружения неизвестного атрибута
                        print(
                            "Неизвестный атрибут '%s' у таблицы '%s'"
                            % (attrib, table_attrib["name"])
                        )
                        exit(1)

                temp_table.fields = self._parse_fields(table)
                temp_table.constraints = self._parse_constraints(table)
                temp_table.indexes = self._parse_indexes(table)

                # Добавляем таблицу в массив таблиц
                tables.append(temp_table)

        return tables

    # Преобразуем поля
    def _parse_fields(self, table):
        fields = []
        # Перебираем дочерние элементы с именем "field" элемента table
        for field in table.iter("field"):
            # Создаём переменную класса Field
            temp_field = Field()
            # Получаем атрибуты текущего в цикле элемента
            field_attrib = field.attrib

            # Перебираем атрибуты элемента
            for attrib in field_attrib:
                if attrib == "name":
                    temp_field.name = field_attrib[attrib]

                elif attrib == "rname":
                    temp_field.rname = field_attrib[attrib]

                elif attrib == "domain":
                    temp_field.domain = field_attrib[attrib]

                elif attrib == "description":
                    temp_field.description = field_attrib[attrib]

                elif attrib == "props":
                    # Перебираем значения атрибута "props"
                    props = field_attrib[attrib].split(", ")
                    for prop in props:
                        if prop == "input":
                            temp_field.input = True

                        elif prop == "edit":
                            temp_field.edit = True

                        elif prop == "show_in_grid":
                            temp_field.show_in_grid = True

                        elif prop == "show_in_details":
                            temp_field.show_in_details = True

                        elif prop == "is_mean":
                            temp_field.is_mean = True

                        elif prop == "autocalculated":
                            temp_field.autocalculated = True

                        elif prop == "required":
                            temp_field.required = True

                        else:  # В случае обнаружения неизвестного свойства
                            print(
                                "Неизвестное свойство '%s' "
                                "у поля '%s' в таблице '%s'"
                                % (
                                    prop,
                                    field_attrib["name"],
                                    table.attrib["name"]
                                )
                            )
                            exit(1)
                else:  # В случае обнаружения неизвестного атрибута
                    print(
                        "Неизвестный атрибут '%s' у поля '%s' в таблице '%s'"
                        % (attrib, field_attrib["name"], table.attrib["name"])
                    )
                    exit(1)

            # Добавляем поле в массив полей
            fields.append(temp_field)

        return fields

    # Преобразуем ограничения
    def _parse_constraints(self, table):
        constraints = []
        # Перебираем дочерние элементы с именем "constraint" элемента table
        for constraint in table.iter("constraint"):
            # Создаём переменную класса Constraint
            temp_constraint = Constraint()
            # Получаем атрибуты текущего в цикле элемента
            constraint_attrib = constraint.attrib

            # Перебираем атрибуты элемента
            for attrib in constraint_attrib:
                if attrib == "name":
                    temp_constraint.name = constraint_attrib[attrib]

                elif attrib == "kind":
                    temp_constraint.kind = constraint_attrib[attrib]

                elif attrib == "items":
                    temp_constraint.items = constraint_attrib[attrib]

                elif attrib == "reference":
                    temp_constraint.reference = constraint_attrib[attrib]

                elif attrib == "expression":
                    temp_constraint.expression = constraint_attrib[attrib]

                elif attrib == "props":
                    # Перебираем значения атрибута "props"
                    props = constraint_attrib[attrib].split(", ")
                    for prop in props:
                        if prop == "has_value_edit":
                            temp_constraint.has_value_edit = True

                        elif prop == "cascading_delete":
                            temp_constraint.cascading_delete = True

                        elif prop == "full_cascading_delete":
                            temp_constraint.full_cascading_delete = True

                        else:  # В случае обнаружения неизвестного свойства
                            print(
                                "Неизвестное свойство '%s' "
                                "у ограничения '%s' в таблице '%s'"
                                % (
                                    prop,
                                    constraint_attrib["name"],
                                    table.attrib["name"]
                                )
                            )
                            exit(1)
                else:  # В случае обнаружения неизвестного атрибута
                    print(
                        "Неизвестный атрибут '%s' "
                        "у ограничения '%s' в таблице '%s'"
                        % (
                            attrib,
                            constraint_attrib["name"],
                            table.attrib["name"]
                        )
                    )
                    exit(1)

            # Добавляем ограничение в массив полей
            constraints.append(temp_constraint)

        return constraints

    # Преобразуем индексы
    def _parse_indexes(self, table):
        indexes = []
        # Перебираем дочерние элементы с именем "index" элемента table
        for index in table.iter("index"):
            # Создаём переменную класса Index
            temp_index = Index()
            # Получаем атрибуты текущего в цикле элемента
            index_attrib = index.attrib

            # Перебираем атрибуты элемента
            for attrib in index_attrib:
                if attrib == "name":
                    temp_index.name = index_attrib[attrib]

                elif attrib == "field":
                    temp_index.field = index_attrib[attrib]

                elif attrib == "expression":
                    temp_index.expression = index_attrib[attrib]

                elif attrib == "props":
                    # Перебираем значения атрибута "props"
                    props = index_attrib[attrib].split(", ")
                    for prop in props:
                        if prop == "uniqueness":
                            temp_index.uniqueness = True

                        elif prop == "fulltext":
                            temp_index.fulltext = True

                        elif prop == "local":
                            temp_index.local = True

                        elif prop == "descend":
                            temp_index.descend = True

                        else:  # В случае обнаружения неизвестного свойства
                            print(
                                "Неизвестное свойство '%s' "
                                "у индекса '%s' в таблице '%s'"
                                % (
                                    prop,
                                    index_attrib["name"],
                                    table.attrib["name"]
                                )
                            )
                            exit(1)
                else:  # В случае обнаружения неизвестного атрибута
                    print(
                        "Неизвестный атрибут '%s' "
                        "у индекса '%s' в таблице '%s'"
                        % (
                            attrib,
                            index_attrib["name"],
                            table.attrib["name"]
                        )
                    )
                    exit(1)

            # Добавляем индекс в массив полей
            indexes.append(temp_index)

        return indexes
