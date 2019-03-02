import sqlite3
from дополнения.schema_classes import *
from дополнения.dbd_const import *


class dbd_to_ram:
    def __init__(self, path_to_file):
        self.connect = sqlite3.connect(path_to_file)
        self.cursor = self.connect.cursor()

    def parsing(self):
        self._parse_schema()
        self._parse_domains()
        self._parse_tables()
        self.connect.close()

    # Преобразуем схему
    def _parse_schema(self):
        self.schema = Schema()
        # Получаем данные из dbd$schemas
        schema = self.cursor.execute(
            """
                select name, version, fulltext_engine, description
                from dbd$schemas
            """).fetchone()
        # Заполняем
        self.schema.name = str_to_int(schema[0])
        self.schema.version = str_to_int(schema[1])
        self.schema.fulltext_engine = str_to_int(schema[2])
        self.schema.description = str_to_int(schema[3])

    # Преобразуем домены
    def _parse_domains(self):
        self.schema.domains = []
        # SQL-запрос для получения данных из dbd$domains
        select = """
            select
                d.name,
                d.description,
                t.type_id,
                d.length,
                d.char_length,
                d.precision,
                d.scale,
                d.width,
                d.align,
                d.show_null,
                d.show_lead_nulls,
                d.thousands_separator,
                d.summable,
                d.case_sensitive
            from 'dbd$domains' d
            left join (select id, type_id from dbd$data_types) t
            where d.data_type_id = t.id
        """
        # Получаем данные и просматриваем их в цикле
        for domain in self.cursor.execute(select).fetchall():
            temp_domain = Domain()
            temp_domain.name = str_to_int(domain[0])
            temp_domain.description = str_to_int(domain[1])
            temp_domain.type = str_to_int(domain[2])
            temp_domain.length = str_to_int(domain[3])
            temp_domain.char_length = str_to_int(domain[4])
            temp_domain.precision = str_to_int(domain[5])
            temp_domain.scale = str_to_int(domain[6])
            temp_domain.width = str_to_int(domain[7])
            temp_domain.align = str_to_int(domain[8])

            temp_domain.show_null = str_to_int(domain[9])
            temp_domain.show_lead_nulls = str_to_int(domain[10])
            temp_domain.thousands_separator = str_to_int(domain[11])
            temp_domain.summable = str_to_int(domain[12])
            temp_domain.case_sensitive = str_to_int(domain[13])

            self.schema.domains.append(temp_domain)

    # Преобразуем таблицы
    def _parse_tables(self):
        self.schema.tables = []
        # SQL-запрос для получения данных из dbd$tables
        select = """
            select
                name,
                description,
                ht_table_flags,
                access_level,
                temporal_mode,
                means,
                can_add,
                can_edit,
                can_delete,
                id
            from 'dbd$tables'
        """
        # Получаем данные и просматриваем их в цикле
        for table in self.cursor.execute(select).fetchall():
            temp_table = Table()
            temp_table.name = str_to_int(table[0])
            temp_table.description = str_to_int(table[1])
            temp_table.ht_table_flags = str_to_int(table[2])
            temp_table.access_level = str_to_int(table[3])
            temp_table.temporal_mode = str_to_int(table[4])
            temp_table.means = str_to_int(table[5])

            temp_table.add = str_to_int(table[6])
            temp_table.edit = str_to_int(table[7])
            temp_table.delete = str_to_int(table[8])

            temp_table.fields = self._parse_fields(table[9])
            temp_table.constraints = self._parse_constraints(table[9])
            temp_table.indexes = self._parse_indexes(table[9])

            self.schema.tables.append(temp_table)

    # Преобразуем поля
    def _parse_fields(self, tid):
        fields = []
        # SQL-запрос для получения данных из dbd$fields и dbd$domains
        select = """
            select
                f.name,
                f.russian_short_name,
                d.name,
                f.description,
                f.can_input,
                f.can_edit,
                f.show_in_grid,
                f.show_in_details,
                f.is_mean,
                f.autocalculated,
                f.required
            from 'dbd$fields' f
            left join (select id, name from 'dbd$domains') d
            where f.domain_id = d.id and f.table_id = :tid
        """
        # Получаем данные и просматриваем их в цикле
        for field in self.cursor.execute(select, {"tid": tid}).fetchall():
            temp_field = Field()
            temp_field.name = str_to_int(field[0])
            temp_field.rname = str_to_int(field[1])
            temp_field.domain = str_to_int(field[2])
            temp_field.description = str_to_int(field[3])

            temp_field.input = str_to_int(field[4])
            temp_field.edit = str_to_int(field[5])
            temp_field.show_in_grid = str_to_int(field[6])
            temp_field.show_in_details = str_to_int(field[7])
            temp_field.is_mean = str_to_int(field[8])
            temp_field.autocalculated = str_to_int(field[9])
            temp_field.required = str_to_int(field[10])

            fields.append(temp_field)

        return fields

    # Преобразуем ограничения
    def _parse_constraints(self, tid):
        constraints = []
        # SQL-запрос для получения данных из dbd$
        select = """
            select
                c.name,
                c.constraint_type,
                f.name,
                ref_t.name,
                c.expression,
                c.has_value_edit,
                c.cascading_delete
            from 'dbd$constraints' c
            left join (select * from 'dbd$constraint_details') cd
                on cd.constraint_id = c.id
            left join (select id, name from 'dbd$tables') t
                on c.table_id = t.id
            left join (select id, name from 'dbd$fields') f
                on cd.field_id = f.id
            left join (select id, name from 'dbd$tables') ref_t
                on c.reference = ref_t.id
            where t.id = :tid
            group by c.table_id, cd.position
        """
        # Получаем данные и просматриваем их в цикле
        for constraint in self.cursor.execute(select, {"tid": tid}).fetchall():
            temp_constraint = Constraint()
            temp_constraint.name = str_to_int(constraint[0])
            kind = "PRIMARY"
            if constraint[1] == "F":
                kind = "FOREIGN"
            temp_constraint.kind = kind
            temp_constraint.items = str_to_int(constraint[2])
            temp_constraint.reference = str_to_int(constraint[3])
            temp_constraint.expression = str_to_int(constraint[4])
            temp_constraint.has_value_edit = str_to_int(constraint[5])

            if constraint[6] is not None:
                if constraint[6]:
                    temp_constraint.full_cascading_delete = True
                else:
                    temp_constraint.cascading_delete = True

            #
            constraints.append(temp_constraint)

        return constraints

    # Преобразуем индексы
    def _parse_indexes(self, tid):
        indexes = []
        # SQL-запрос для получения данных из dbd$
        select = """
                select
                i.name,
                f.name,
                i_d.expression,
                i.local,
                i.kind,
                i_d.descend
                from 'dbd$indexes' i, 'dbd$index_details' i_d
                left join (select id, name from 'dbd$fields') f
                    on i_d.field_id = f.id
                left join (select id, name from 'dbd$tables') t
                    on i.table_id = t.id
                where i_d.index_id = i.id and i.table_id = :tid
                order by i.table_id, i_d.position
        """
        # Получаем данные и просматриваем их в цикле
        for index in self.cursor.execute(select, {"tid": tid}).fetchall():
            temp_index = Index()
            temp_index.name = str_to_int(index[0])
            temp_index.field = str_to_int(index[1])
            temp_index.expression = str_to_int(index[2])
            temp_index.local = str_to_int(index[3])

            if index[4] == 'U':
                temp_index.uniqueness = True
            elif index[4] == 'T':
                temp_index.fulltext = True

            temp_index.descend = str_to_int(index[5])
            indexes.append(temp_index)

        return indexes


def str_to_int(value):
    if isinstance(value, int) or isinstance(value, float):
        value = str(value)
    return value
