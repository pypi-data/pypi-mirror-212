from typing import Dict, Optional, Type

from django.db.models import Field, Model, QuerySet
from django.db.models.sql import Query
from django.db.models.sql.constants import INNER

from .compiler import SQLJoinCompiler
from .exception import JoinError


class JoinQuery(Query):
    compiler = 'SQLJoinCompiler'
    alias_prefix = 'J'

    def __init__(self, model: Optional[Type[Model]], alias_cols: bool = True):
        super().__init__(model=model, alias_cols=alias_cols)
        self._join_type: str = ''
        self._join_nullable: bool = False
        self._join_fields: Dict[str, Field] = {}

    def add_join_values(self, join_type: str = INNER, nullable: bool = False, **join_fields) -> None:
        self._join_type = join_type
        self._join_nullable = nullable
        self._join_fields = join_fields

    def get_compiler(self, *args, **kwargs) -> SQLJoinCompiler:
        comp: SQLJoinCompiler = super().get_compiler(*args, **kwargs)  # type: ignore[assignment]
        if self._join_fields:
            comp.setup_unrelated_joins(join_type=self._join_type, nullable=self._join_nullable, **self._join_fields)
        return comp


class JoinQuerySet(QuerySet):

    def join(self, join_type=INNER, nullable=False, **join_fields) -> 'JoinQuerySet':
        # can't be joined on itself
        # for FK use *_id field: id=Person.department_id
        for v in join_fields.values():
            if v.field.model == self.model:
                raise JoinError('Unable to join on the same model.')

        self.query: JoinQuery = self.query.chain(JoinQuery)  # type: ignore[assignment]
        self.query.add_join_values(**join_fields)
        return self
