from datetime import timedelta
from itertools import product
from operator import ge, gt, le, lt
from typing import Optional

from pytest import mark
from sqlalchemy import and_, or_
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Query, Session
from typing_extensions import Literal

from mui.v5.grid import GridFilterModel, GridLinkOperator
from mui.v5.integrations.sqlalchemy.filter import apply_filter_to_query_from_model
from mui.v5.integrations.sqlalchemy.resolver import Resolver
from tests.conftest import FIRST_DATE_DATETIME, calculate_grouping_id
from tests.fixtures.sqlalchemy import ParentModel

LINK_OPERATOR_ARGVALUES = (GridLinkOperator.And, GridLinkOperator.Or, None)


def _sql_link_operator_from(
    link_operator: Optional[GridLinkOperator],
) -> Literal["AND", "OR"]:
    return "AND" if link_operator == GridLinkOperator.And else "OR"


@mark.parametrize(
    argnames=("link_operator"),
    argvalues=LINK_OPERATOR_ARGVALUES,
)
def test_apply_eq_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
    target_parent_id: int,
) -> None:
    TARGET_GROUP = calculate_grouping_id(model_id=target_parent_id)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": target_parent_id,
                    "operator_value": "==",
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": "==",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.id = ?" in compiled_str
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id = ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == target_parent_id
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                ParentModel.id == target_parent_id,
                ParentModel.grouping_id == TARGET_GROUP,
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert row.id == target_parent_id
            assert row.grouping_id == TARGET_GROUP
        else:
            assert row.id == target_parent_id or row.grouping_id == TARGET_GROUP


@mark.parametrize(
    argnames=("expected_id", "link_operator"),
    argvalues=((4, GridLinkOperator.And), (1, GridLinkOperator.Or), (1, None)),
)
def test_apply_is_datetime_apply_filter_to_query_from_model_single_field(
    expected_id: int,
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    THIRD_DAY = FIRST_DATE_DATETIME + timedelta(days=3)
    # sqlite doesn't support the concept of timezones, so we get a naive datetime
    # back from the database
    ROW_THIRD_DAY = THIRD_DAY.replace(tzinfo=None)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "created_at",
                    "value": THIRD_DAY.isoformat(),
                    "operator_value": "is",
                },
                {
                    "column_field": "id",
                    "value": expected_id,
                    "operator_value": "is",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.created_at = ?" in compiled_str
    assert f"{sql_link_operator} {ParentModel.__tablename__}.id = ?" in compiled_str
    assert compiled.params["created_at_1"] == THIRD_DAY
    assert compiled.params["id_1"] == expected_id

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                ParentModel.created_at == THIRD_DAY,
                ParentModel.id == expected_id,
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert row is not None
            assert row.id == expected_id
            assert row.created_at == ROW_THIRD_DAY
        else:
            assert row.id == expected_id or row.created_at == ROW_THIRD_DAY


@mark.parametrize(argnames=("link_operator"), argvalues=LINK_OPERATOR_ARGVALUES)
def test_apply_ne_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
    target_parent_id: int,
) -> None:
    TARGET_GROUP = calculate_grouping_id(model_id=target_parent_id)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": target_parent_id,
                    "operator_value": "!=",
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": "!=",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.id != ?" in compiled_str
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id != ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == target_parent_id
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                ParentModel.id != target_parent_id,
                ParentModel.grouping_id != TARGET_GROUP,
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert row.id != target_parent_id
            assert row.grouping_id != TARGET_GROUP
        else:
            assert row.id != target_parent_id or row.grouping_id != TARGET_GROUP


@mark.parametrize(
    argnames=("operator", "link_operator"),
    argvalues=(tuple(product(("<", ">"), LINK_OPERATOR_ARGVALUES))),
)
def test_apply_gt_lt_apply_filter_to_query_from_model_multiple_fields(
    operator: str,
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
    target_parent_id: int,
) -> None:
    TARGET_GROUP = calculate_grouping_id(model_id=target_parent_id)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": target_parent_id,
                    "operator_value": operator,
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": operator,
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.id {operator} ?" in compiled_str
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id {operator} ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == target_parent_id
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    op = gt if operator == ">" else lt
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                op(ParentModel.id, target_parent_id),
                op(ParentModel.grouping_id, TARGET_GROUP),
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert op(row.id, target_parent_id)
            assert op(row.grouping_id, TARGET_GROUP)
        else:
            assert op(row.id, target_parent_id) or op(row.grouping_id, TARGET_GROUP)


@mark.parametrize(
    argnames=("operator", "link_operator"),
    argvalues=(tuple(product(("<=", ">="), LINK_OPERATOR_ARGVALUES))),
)
def test_apply_ge_le_apply_filter_to_query_from_model_multiple_fields(
    operator: str,
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
    target_parent_id: int,
) -> None:
    TARGET_GROUP = calculate_grouping_id(model_id=target_parent_id)
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": target_parent_id,
                    "operator_value": operator,
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUP,
                    "operator_value": operator,
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.id {operator} ?" in compiled_str
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id {operator} ?"
        in compiled_str
    )
    assert compiled.params["id_1"] == target_parent_id
    assert compiled.params["grouping_id_1"] == TARGET_GROUP

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    op = ge if operator == ">=" else le
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                op(ParentModel.id, target_parent_id),
                op(ParentModel.grouping_id, TARGET_GROUP),
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert op(row.id, target_parent_id)
            assert op(row.grouping_id, TARGET_GROUP)
        else:
            assert op(row.id, target_parent_id) or op(row.grouping_id, TARGET_GROUP)


@mark.parametrize(
    argnames=("field", "link_operator"),
    argvalues=tuple(product(("id", "null_field"), LINK_OPERATOR_ARGVALUES)),
)
def test_apply_is_empty_apply_filter_to_query_from_model_multiple_fields(
    field: str,
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": field,
                    "value": None,
                    "operator_value": "isEmpty",
                },
                {
                    "column_field": "grouping_id",
                    "value": None,
                    "operatorValue": "isEmpty",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.{field} IS NULL" in compiled_str
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id IS NULL"
        in compiled_str
    )

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                getattr(ParentModel, field) is None,
                ParentModel.grouping_id is None,
            )
        )
        .count()
    )

    assert row_count == expected_row_count

    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert getattr(row, field) is None
            assert row.grouping_id is None
        else:
            assert getattr(row, field) is None or row.grouping_id is None


@mark.parametrize(
    argnames=("field", "link_operator"),
    argvalues=tuple(product(("id", "null_field"), LINK_OPERATOR_ARGVALUES)),
)
def test_apply_is_not_empty_apply_filter_to_query_from_model_multiple_fields(
    field: str,
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": field,
                    "value": None,
                    "operator_value": "isNotEmpty",
                },
                {
                    "column_field": "grouping_id",
                    "value": None,
                    "operator_value": "isNotEmpty",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE {ParentModel.__tablename__}.{field} IS NOT NULL" in compiled_str
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id IS NOT NULL"
        in compiled_str
    )

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                # don't use is, that's pointer comparison not value
                getattr(ParentModel, field) != None,  # noqa: E711
                ParentModel.grouping_id != None,  # noqa: E711
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert getattr(row, field) is not None
            assert row.grouping_id is not None
        else:
            # Or branch
            assert row.null_field is not None or row.grouping_id is not None


@mark.parametrize(argnames=("link_operator"), argvalues=(LINK_OPERATOR_ARGVALUES))
def test_apply_is_any_of_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    TARGET_IDS = [1, 2, 3]
    TARGET_GROUPS = list(
        {calculate_grouping_id(model_id=TARGET_ID) for TARGET_ID in TARGET_IDS}
    )

    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "id",
                    "value": TARGET_IDS,
                    "operator_value": "isAnyOf",
                },
                {
                    "column_field": "grouping_id",
                    "value": TARGET_GROUPS,
                    "operator_value": "isAnyOf",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert (
        f"WHERE {ParentModel.__tablename__}.id IN (__[POSTCOMPILE_id_1])"
        in compiled_str
    )
    assert (
        f"{sql_link_operator} {ParentModel.__tablename__}.grouping_id IN "
        + "(__[POSTCOMPILE_grouping_id_1])"
        in compiled_str
    )
    assert compiled.params["id_1"] == TARGET_IDS
    assert compiled.params["grouping_id_1"] == TARGET_GROUPS

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                ParentModel.id.in_(TARGET_IDS),
                ParentModel.grouping_id.in_(TARGET_GROUPS),
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert row.id in TARGET_IDS
            assert row.grouping_id in TARGET_GROUPS
        else:
            assert row.id in TARGET_IDS or row.grouping_id in TARGET_GROUPS


@mark.parametrize(argnames=("link_operator"), argvalues=(LINK_OPERATOR_ARGVALUES))
def test_apply_contains_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "name",
                    "value": ParentModel.__name__,
                    "operator_value": "contains",
                },
                {
                    "column_field": "grouping_id",
                    "value": 0,
                    "operator_value": "contains",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert (
        f"WHERE ({ParentModel.__tablename__}.name LIKE '%' || ? || '%')" in compiled_str
    )
    assert (
        f"{sql_link_operator} ({ParentModel.__tablename__}.grouping_id LIKE "
        + "'%' || ? || '%')"
        in compiled_str
    )
    assert compiled.params["name_1"] == ParentModel.__name__
    assert compiled.params["grouping_id_1"] == 0

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                ParentModel.name.contains(ParentModel.__name__),
                ParentModel.grouping_id.contains(0),
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert ParentModel.__name__ in row.name
            assert "0" in str(row.grouping_id)
        else:
            assert ParentModel.__name__ in row.name or "0" in str(row.grouping_id)


@mark.parametrize(argnames=("link_operator"), argvalues=(LINK_OPERATOR_ARGVALUES))
def test_apply_starts_with_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "name",
                    "value": ParentModel.__name__,
                    "operator_value": "startsWith",
                },
                {
                    "column_field": "grouping_id",
                    "value": 0,
                    "operator_value": "startsWith",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE ({ParentModel.__tablename__}.name LIKE ? || '%')" in compiled_str
    assert (
        f"{sql_link_operator} ({ParentModel.__tablename__}.grouping_id LIKE ? || '%')"
        in compiled_str
    )
    assert compiled.params["name_1"] == ParentModel.__name__
    assert compiled.params["grouping_id_1"] == 0

    rows = filtered_query.all()
    row_count = filtered_query.count()
    join_filter = and_ if link_operator == GridLinkOperator.And else or_
    expected_row_count = (
        session.query(ParentModel)
        .filter(
            join_filter(
                ParentModel.name.startswith(ParentModel.__name__),
                ParentModel.grouping_id.startswith(0),
            )
        )
        .count()
    )
    assert row_count == expected_row_count
    for row in rows:
        if link_operator == GridLinkOperator.And:
            assert row.name.startswith(ParentModel.__name__)
            assert str(row.grouping_id).startswith("0")
        else:
            assert row.name.startswith(ParentModel.__name__) or str(
                row.grouping_id
            ).startswith("0")


@mark.parametrize(argnames=("link_operator"), argvalues=(LINK_OPERATOR_ARGVALUES))
def test_apply_ends_with_apply_filter_to_query_from_model_multiple_fields(
    link_operator: Optional[GridLinkOperator],
    session: Session,
    query: "Query[ParentModel]",
    resolver: Resolver,
) -> None:
    VALUE = "0"
    model = GridFilterModel.parse_obj(
        {
            "items": [
                {
                    "column_field": "name",
                    "value": VALUE,
                    "operator_value": "endsWith",
                },
                {
                    "column_field": "grouping_id",
                    "value": VALUE,
                    "operator_value": "endsWith",
                },
            ],
            "link_operator": link_operator,
            "quick_filter_logic_operator": None,
            "quick_filter_values": None,
        }
    )
    filtered_query = apply_filter_to_query_from_model(
        query=query, model=model, resolver=resolver
    )
    compiled = filtered_query.statement.compile(dialect=sqlite.dialect())
    compiled_str = str(compiled)
    sql_link_operator = _sql_link_operator_from(link_operator=link_operator)
    assert f"WHERE ({ParentModel.__tablename__}.name LIKE '%' || ?)" in compiled_str
    assert (
        f"{sql_link_operator} ({ParentModel.__tablename__}.grouping_id LIKE '%' || ?)"
        in compiled_str
    )
    assert compiled.params["name_1"] == VALUE
    assert compiled.params["grouping_id_1"] == VALUE

    rows = filtered_query.all()
    row_count = filtered_query.count()
    if link_operator == GridLinkOperator.And:
        expected_row_count = (
            session.query(ParentModel)
            .filter(
                and_(
                    ParentModel.name.endswith(VALUE),
                    ParentModel.grouping_id.endswith(VALUE),
                )
            )
            .count()
        )
        assert row_count == expected_row_count
        assert all(row.name.endswith(VALUE) for row in rows)
        assert all(str(row.grouping_id).endswith(VALUE) for row in rows)
    else:
        expected_row_count = (
            session.query(ParentModel)
            .filter(
                or_(
                    ParentModel.name.endswith(VALUE),
                    ParentModel.grouping_id.endswith(VALUE),
                )
            )
            .count()
        )
        assert row_count == expected_row_count
        assert all(
            row.name.endswith(VALUE) or str(row.grouping_id).endswith(VALUE)
            for row in rows
        )
