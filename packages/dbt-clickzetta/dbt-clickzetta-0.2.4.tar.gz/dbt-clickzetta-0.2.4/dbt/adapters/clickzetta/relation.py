from dataclasses import dataclass, field
from dbt.adapters.base.relation import BaseRelation, Policy
from dbt.exceptions import DbtRuntimeError


@dataclass
class ClickZettaQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False


@dataclass(frozen=True, eq=False, repr=False)
class ClickZettaRelation(BaseRelation):
    quote_policy: ClickZettaQuotePolicy = field(default_factory=lambda: ClickZettaQuotePolicy())
    quote_character = "`"

    def __post_init__(self):
        if self.database != self.schema and self.database:
            raise DbtRuntimeError("Cannot set database in clickzetta!")

    def render(self):
        # if self.include_policy.database and self.include_policy.schema:
        #     raise DbtRuntimeError(
        #         "Got a clickzetta relation with schema and database set to "
        #         "include, but only one can be set"
        #     )
        return super().render()
