from types import NoneType

from hypothesis import given
from hypothesis import strategies as st

from mui.v5.grid.filter.item import GridFilterItem
from mui.v5.grid.link.operator import GridLinkOperator

valid_operators = [
    "and",
    "or",
    GridLinkOperator.And,
    GridLinkOperator.Or,
    None,
]

CamelCaseGridFilterItemData = st.fixed_dictionaries(  # type: ignore[misc]
    mapping={
        "columnField": st.text(),
    },
    optional={
        "id": st.one_of(st.text(), st.integers(), st.none()),
        "operatorValue": st.text(),
        "value": st.one_of(st.text(), st.none(), st.booleans(), st.floats()),
    },
)
SnakeCaseGridFilterItemData = st.fixed_dictionaries(  # type: ignore[misc]
    mapping={
        "column_field": st.text(),
    },
    optional={
        "id": st.one_of(st.text(), st.integers(), st.none()),
        "operator_value": st.text(),
        "value": st.one_of(st.text(), st.none(), st.booleans(), st.floats()),
    },
)


@given(filter_item_dict=CamelCaseGridFilterItemData)
def test_parse_valid_grid_filter_item_camel_case_dict(
    filter_item_dict: dict[str, object]
) -> None:
    assert "columnField" in filter_item_dict
    parsed = GridFilterItem.parse_obj(filter_item_dict)
    assert isinstance(parsed.column_field, str)
    assert isinstance(parsed.id, (str, int, NoneType))
    assert isinstance(parsed.operator_value, (str, NoneType))
    assert isinstance(parsed.value, (str, NoneType, bool, float))


@given(filter_item_dict=SnakeCaseGridFilterItemData)
def test_parse_valid_grid_filter_item_snake_case_dict(
    filter_item_dict: dict[str, object]
) -> None:
    assert "column_field" in filter_item_dict
    parsed = GridFilterItem.parse_obj(filter_item_dict)
    assert isinstance(parsed.column_field, str)
    assert isinstance(parsed.id, (str, int, NoneType))
    assert isinstance(parsed.operator_value, (str, NoneType))
    assert isinstance(parsed.value, (str, NoneType, bool, float))
