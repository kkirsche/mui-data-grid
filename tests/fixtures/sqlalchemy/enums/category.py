from enum import unique

from mui.compat import StrEnum


@unique
class Category(StrEnum):
    CATEGORY_0 = "cat-0"
    CATEGORY_1 = "cat-1"
    CATEGORY_2 = "cat-2"
    CATEGORY_3 = "cat-3"


CATEGORIES = list(Category)
CATEGORY_COUNT = len(CATEGORIES)


def category_from_id(id: int) -> Category:
    remainder = id % CATEGORY_COUNT
    for category in CATEGORIES:
        if str(category).endswith(str(remainder)):
            return category
    raise ValueError("Category does not exist with required suffix.")
