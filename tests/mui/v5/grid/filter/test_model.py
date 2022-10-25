from types import NoneType

from hypothesis import given
from hypothesis import strategies as st

from mui.v5.grid.filter.item import GridFilterItem
from mui.v5.grid.filter.model import GridFilterModel
from mui.v5.grid.link.operator import GridLinkOperator

from .test_item import CamelCaseGridFilterItemData, SnakeCaseGridFilterItemData

valid_operators = [
    "and",
    "or",
    GridLinkOperator.And,
    GridLinkOperator.Or,
    None,
]

CamelCaseGridFilterModelData = st.fixed_dictionaries(  # type: ignore[misc]
    {
        "items": st.lists(
            st.one_of(SnakeCaseGridFilterItemData, CamelCaseGridFilterItemData)
        ),
    },
    optional={
        "linkOperator": st.sampled_from(valid_operators),
        "quickFilterLogicOperator": st.sampled_from(valid_operators),
        "quickFilterValues": st.one_of(
            st.lists(st.one_of(st.text(), st.none(), st.booleans(), st.floats())),
            st.none(),
        ),
    },
)
SnakeCaseGridFilterModelData = st.fixed_dictionaries(  # type: ignore[misc]
    {
        "items": st.lists(
            st.one_of(SnakeCaseGridFilterItemData, CamelCaseGridFilterItemData)
        ),
    },
    optional={
        "link_operator": st.sampled_from(valid_operators),
        "quick_filter_logic_operator": st.sampled_from(valid_operators),
        "quickFilterValues": st.one_of(
            st.lists(st.one_of(st.text(), st.none(), st.booleans(), st.floats())),
            st.none(),
        ),
    },
)


@given(CamelCaseGridFilterModelData)
def test_valid_grid_filter_model_camel_case_parse(
    filter_item_dict: dict[str, object]
) -> None:
    parsed = GridFilterModel.parse_obj(filter_item_dict)
    assert isinstance(parsed.items, list)
    assert all(isinstance(item, GridFilterItem) for item in parsed.items)
    assert isinstance(parsed.link_operator, (GridLinkOperator, NoneType))
    assert isinstance(parsed.quick_filter_logic_operator, (GridLinkOperator, NoneType))
    assert isinstance(parsed.quick_filter_values, (list, NoneType))


@given(SnakeCaseGridFilterModelData)
def test_valid_grid_filter_model_snake_case_parse(
    filter_item_dict: dict[str, object]
) -> None:
    parsed = GridFilterModel.parse_obj(filter_item_dict)
    assert isinstance(parsed.items, list)
    assert all(isinstance(item, GridFilterItem) for item in parsed.items)
    assert isinstance(parsed.link_operator, (GridLinkOperator, NoneType))
    assert isinstance(parsed.quick_filter_logic_operator, (GridLinkOperator, NoneType))
    assert isinstance(parsed.quick_filter_values, (list, NoneType))
