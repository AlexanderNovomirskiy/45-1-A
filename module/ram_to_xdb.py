from библиотеки.xml.etree import ElementTree
from дополнения.schema_classes import *
from библиотеки.xml.dom import minidom


class ram_to_xdb:
    def __init__(self, path_to_file, schema):
        self.schema = schema
        self.file = path_to_file

    # Преобразуем RAM в XDB
    def parsing(self):
        # Создаём корень
        self.root = ElementTree.Element("dbd_schema")
        fulltext = self.schema.fulltext_engine
        version = self.schema.version
        name = self.schema.name
        description = self.schema.description

        # Добавление атрибутов схемы
        if fulltext and fulltext != "":
            self.root.set("fulltext_engine", fulltext)

        if version and version != "":
            self.root.set("version", version)

        if name and name != "":
            self.root.set("name", name)

        if description and description != "":
            self.root.set("description", description)

        custom = ElementTree.Element("custom")
        self.root.append(custom)

        self.root.append(self._parse_domains())
        self.root.append(self._parse_tables())

        self._write_to_file()

    # Получаем XDB-файл
    def _write_to_file(self):
        tree = minidom.parseString(ElementTree.tostring(self.root))\
            .toprettyxml(indent="  ", encoding="utf-8")

        with open(self.file, 'wb') as f:
            f.write(tree)

    # Преобразуем домены
    def _parse_domains(self):
        domains = ElementTree.Element("domains")
        for domain in self.schema.domains:
            temp_domain = ElementTree.Element("domain")

            # Добавляем атрибуты домена
            if domain.name and domain.name != "":
                temp_domain.set("name", domain.name)

            if domain.description and domain.description != "":
                temp_domain.set("description", domain.description)

            if domain.type and domain.type != "":
                temp_domain.set("type", domain.type)

            if domain.align and domain.align != "":
                temp_domain.set("align", domain.align)

            if domain.length is not None:
                temp_domain.set("length", domain.length)

            if domain.width is not None:
                temp_domain.set("width", domain.width)

            if domain.precision is not None:
                temp_domain.set("precision", domain.precision)

            # Добавляем свойства домена
            prop = ""
            prop += "show_null, " if domain.show_null else ""
            prop += "show_lead_nulls, " if domain.show_lead_nulls else ""
            if domain.thousands_separator:
                prop += "thousands_separator, "
            prop += "summable, " if domain.summable else ""
            prop += "case_sensitive, " if domain.case_sensitive else ""

            if len(prop) > 0:  # Есди свойства у домена есть
                prop = prop[0:len(prop) - 2]
                temp_domain.set("props", prop)

            if domain.char_length is not None:
                temp_domain.set("char_length", domain.char_length)

            if domain.scale is not None:
                temp_domain.set("scale", domain.scale)

            # Добавляем полученный дочерний элемент
            domains.append(temp_domain)

        return domains

    # Преобразуем таблицы
    def _parse_tables(self):
        tables = ElementTree.Element("tables")
        for table in self.schema.tables:
            temp_table = ElementTree.Element("table")

            # Добавляем атрибуты таблицы
            if table.name and table.name != "":
                temp_table.set("name", table.name)

            if table.description and table.description != "":
                temp_table.set("description", table.description)

            # Добавляем свойства таблицы
            prop = ""
            prop += "add, " if table.add else ""
            prop += "edit, " if table.edit else ""
            prop += "delete, " if table.delete else ""
            if len(prop) > 0:  # Есди свойства у таблицы есть
                prop = prop[0:len(prop) - 2]
                temp_table.set("props", prop)

            if table.ht_table_flags and table.ht_table_flags != "":
                temp_table.set("ht_table_flags", table.ht_table_flags)

            if table.access_level is not None:
                temp_table.set("access_level", table.access_level)

            if table.temporal_mode and table.temporal_mode != "":
                temp_table.set("temporal_mode", table.temporal_mode)

            if table.means and table.means != "":
                temp_table.set("means", table.means)

            self._parse_fields(table, temp_table)
            self._parse_constraints(table, temp_table)
            self._parse_indexes(table, temp_table)

            # Добавляем полученный дочерний элемент
            tables.append(temp_table)

        return tables

    # Преобразуем поля
    def _parse_fields(self, table, temp_table):
        for field in table.fields:
            temp_field = ElementTree.Element("field")

            # Добавляем атрибуты поля
            if field.name and field.name != "":
                temp_field.set("name", field.name)

            if field.rname and field.rname != "":
                temp_field.set("rname", field.rname)

            if field.domain and field.domain != "":
                temp_field.set("domain", field.domain)

            if field.description and field.description != "":
                temp_field.set("description", field.description)

            # Добавляем свойства поля
            prop = ""
            prop += "input, " if field.input else ""
            prop += "edit, " if field.edit else ""
            prop += "show_in_grid, " if field.show_in_grid else ""
            prop += "show_in_details, " if field.show_in_details else ""
            prop += "is_mean, " if field.is_mean else ""
            prop += "autocalculated, " if field.autocalculated else ""
            prop += "required, " if field.required else ""
            if len(prop) > 0:  # Есди свойства у поля есть
                prop = prop[0:len(prop) - 2]
                temp_field.set("props", prop)

            # Добавляем полученный дочерний элемент
            temp_table.append(temp_field)

    # Преобразуем ограничения
    def _parse_constraints(self, table, temp_table):
        for constraint in table.constraints:
            temp_constraint = ElementTree.Element("constraint")

            # Добавляем атрибуты ограничения
            if constraint.name and constraint.name != "":
                temp_constraint.set("name", constraint.name)

            if constraint.kind and constraint.kind != "":
                temp_constraint.set("kind", constraint.kind)

            if constraint.items and constraint.items != "":
                temp_constraint.set("items", constraint.items)

            if constraint.reference and constraint.reference != "":
                temp_constraint.set("reference", constraint.reference)

            if constraint.expression and constraint.expression != "":
                temp_constraint.set("expression", constraint.expression)

            # Добавляем свойства ограничения
            prop = ""
            prop += "has_value_edit, " if constraint.has_value_edit else ""
            prop += "cascading_delete, " if constraint.cascading_delete else ""
            if constraint.full_cascading_delete:
                prop += "full_cascading_delete, "
            else:
                prop += ""
            if len(prop) > 0:  # Есди свойства у ограничения есть
                prop = prop[0:len(prop) - 2]
                temp_constraint.set("props", prop)

            # Добавляем полученный дочерний элемент
            temp_table.append(temp_constraint)

    # Преобразуем индексы
    def _parse_indexes(self, table, temp_table):
        for index in table.indexes:
            temp_index = ElementTree.Element("index")

            # Добавляем атрибуты ограничения
            if index.name and index.name != "":
                temp_index.set("name", index.name)

            if index.field and index.field != "":
                temp_index.set("field", index.field)

            # Добавляем свойства индекса
            prop = ""
            prop += "uniqueness, " if index.uniqueness else ""
            prop += "fulltext, " if index.fulltext else ""
            prop += "local, " if index.local else ""
            prop += "expression, " if index.expression else ""
            prop += "descend, " if index.descend else ""
            if len(prop) > 0:  # Есди свойства у индекса есть
                prop = prop[0:len(prop) - 2]
                temp_index.set("props", prop)

            # Добавляем полученный дочерний элемент
            temp_table.append(temp_index)
