from библиотеки import sqlite3
from дополнения.schema_classes import *
from дополнения.dbd_const import *


class ram_to_dbd:
    def __init__(self, path_to_file, schema):
        self.schema = schema
        self.connect = sqlite3.connect(path_to_file)  # Подключаемся
        self.cursor = self.connect.cursor()
        self.cursor.executescript(SQL_DBD_INIT)  # Создаём таблицы из dbd_const

    def parsing(self):
        self._parse_schema()
        self._parse_domains()
        self._parse_tables()
        self._parse_fields()
        self._parse_constraints()
        self._parse_indexes()

        self.connect.close()  # Закрываем соединение

    # Преобразуем схему
    def _parse_schema(self):
        self.schema_id = 1
        # Вставляем данные из ram в dbd$schemas
        self.cursor.execute(
            """
                insert into dbd$schemas(
                    fulltext_engine,
                    version,
                    name,
                    description
                )
                values (?, ?, ?, ?)
            """,
            (
                self.schema.fulltext_engine,
                self.schema.version,
                self.schema.name,
                self.schema.description
            )
        )
        self.connect.commit()

    # Преобразуем домены
    def _parse_domains(self):
        self.cursor.execute("begin transaction")  # Начинаем транзакцию
        uuid = 0  # Переменная для задания уникального uuid
        # Циклом вставляем домены из ram в dbd$domains
        for domain in self.schema.domains:
            uuid += 1
            # Вставляем данные из ram в dbd$
            self.cursor.execute(
                """
                    insert into dbd$domains(
                        data_type_id,
                        name,
                        description,
                        align,
                        length,
                        width,
                        precision,
                        char_length,
                        scale,
                        show_null,
                        show_lead_nulls,
                        thousands_separator,
                        summable,
                        case_sensitive,
                        uuid
                    )
                    values (
                            (select id from dbd$data_types where type_id = ?),
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """,
                (
                    domain.type,
                    domain.name,
                    domain.description,
                    domain.align,
                    domain.length,
                    domain.width,
                    domain.precision,
                    domain.char_length,
                    domain.scale,
                    domain.show_null,
                    domain.show_lead_nulls,
                    domain.thousands_separator,
                    domain.summable,
                    domain.case_sensitive,
                    "domain_" + str(uuid)
                )
            )

        self.connect.commit()  # Подтверждаем транзакцию

    # Преобразуем таблицы
    def _parse_tables(self):
        self.cursor.execute("begin transaction")  # Начинаем транзакцию
        uuid = 0  # Переменная для задания уникального uuid
        # Циклом вставляем таблицы из ram в dbd$tables
        for table in self.schema.tables:
            uuid += 1
            self.cursor.execute(
                """
                    insert into dbd$tables (
                        schema_id,
                        name,
                        description,
                        ht_table_flags,
                        access_level,
                        temporal_mode,
                        means,
                        can_add,
                        can_edit,
                        can_delete,
                        uuid
                    )
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.schema_id,
                    table.name,
                    table.description,
                    table.ht_table_flags,
                    table.access_level,
                    table.temporal_mode,
                    table.means,
                    table.add,
                    table.edit,
                    table.delete,
                    "table_" + str(uuid)
                )
            )

        self.connect.commit()  # Подтверждаем транзакцию

    # Преобразуем поля
    def _parse_fields(self):
        self.cursor.execute("begin transaction")  # Начинаем транзакцию
        uuid = 0  # Переменная для задания уникального uuid
        # Циклом вставляем поля из ram в dbd$fields
        for table in self.schema.tables:
            for field in table.fields:
                uuid += 1
                self.cursor.execute(
                    """
                        insert into dbd$fields (
                            table_id,
                            domain_id,
                            position,
                            name,
                            russian_short_name,
                            description,
                            can_input,
                            can_edit,
                            show_in_grid,
                            show_in_details,
                            is_mean,
                            autocalculated,
                            required,
                            uuid
                        )
                        values (
                                (select id from dbd$tables
                                    where dbd$tables.name = ?),
                                (select id from dbd$domains
                                    where dbd$domains.name = ?),
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                    """,
                    (
                        table.name,
                        field.domain,
                        table.fields.index(field) + 1,
                        field.name,
                        field.rname,
                        field.description,
                        field.input,
                        field.edit,
                        field.show_in_grid,
                        field.show_in_details,
                        field.is_mean,
                        field.autocalculated,
                        field.required,
                        "field_" + str(uuid)
                    )
                )

        self.connect.commit()  # Подтверждаем транзакцию

    # Преобразуем ограничения
    def _parse_constraints(self):
        self.cursor.execute("begin transaction")  # Начинаем транзакцию
        uuid = 0  # Переменная для задания уникального uuid
        # Циклом вставляем ограничения из ram
        # в dbd$constraints и dbd$constraint_details
        for table in self.schema.tables:
            for constraint in table.constraints:
                uuid += 1

                name = constraint.name
                if not name:  # Если отсутствует имя, создаём временное
                    name = "temp_name_" + str(uuid)

                cascading_delete = None
                if constraint.cascading_delete:
                    cascading_delete = False
                elif constraint.full_cascading_delete:
                    cascading_delete = True

                # Вставляем в dbd$constraints
                self.cursor.execute(
                    """
                        insert into dbd$constraints(
                            table_id,
                            reference,
                            name,
                            constraint_type,
                            expression,
                            unique_key_id,
                            has_value_edit,
                            cascading_delete,
                            uuid
                        )
                        values (
                                (select id from dbd$tables
                                    where dbd$tables.name = ?),
                                (select id from dbd$tables
                                    where dbd$tables.name = ?),
                                ?, ?, ?, ?, ?, ?, ?
                        )
                    """,
                    (
                        table.name,
                        constraint.reference,
                        name,
                        constraint.kind[0],
                        constraint.expression,
                        "",
                        constraint.has_value_edit,
                        cascading_delete,
                        "constraint_" + str(uuid)
                    )
                )

                # Вставялем в dbd$constraint_details
                self.cursor.execute(
                    """
                        insert into dbd$constraint_details(
                            constraint_id,
                            position,
                            field_id
                        )
                        values (
                                (select id from dbd$constraints
                                    where dbd$constraints.name = ?),
                                ?,
                                (select id from dbd$fields
                                    where dbd$fields.name = ?)
                        )
                    """,
                    (
                        name,
                        table.constraints.index(constraint) + 1,
                        constraint.items
                    )
                )

        # Удаляем временные имена
        self.cursor.execute(
            """
                update dbd$constraints
                set name=NULL
                where name like 'temp_name_%'
            """
        )

        self.connect.commit()  # Подтверждаем транзакцию

    # Преобразуем индексы
    def _parse_indexes(self):
        uuid = 0
        self.cursor.execute("begin transaction")
        for table in self.schema.tables:
            for index in table.indexes:
                uuid += 1
                kind = None
                if index.uniqueness:
                    kind = 'U'
                elif index.fulltext:
                    kind = 'T'

                name = index.name
                if not name:  # Если отсутствует имя, создаём временное
                    name = "temp_name_" + str(uuid)

                # Вставляем в dbd$indexes
                self.cursor.execute(
                    """
                        insert into dbd$indexes(
                            table_id,
                            name,
                            local,
                            kind,
                            uuid
                        )
                        values (
                                (select id from dbd$tables
                                    where dbd$tables.name = ?),
                                ?, ?, ?, ?
                        )
                    """,
                    (
                        table.name,
                        name,
                        index.local,
                        kind,
                        "index_" + str(uuid)
                    )
                )

                # Вставялем в dbd$index_details
                self.cursor.execute(
                    """
                        insert into dbd$index_details(
                            index_id,
                            field_id,
                            position,
                            expression,
                            descend
                        )
                        values (
                                (select id from dbd$indexes
                                    where dbd$indexes.name = ?),
                                (select id from dbd$fields
                                    where dbd$fields.name = ?),
                                ?, ?, ?
                        )
                    """,
                    (
                        name,
                        index.field,
                        table.indexes.index(index) + 1,
                        index.expression,
                        index.descend
                    )
                )

        # Удаляем временные имена
        self.cursor.execute(
            """
                update dbd$indexes
                set name=NULL
                where name like 'temp_name_%'
            """
        )
        self.connect.commit()  # Подтверждаем транзакцию
