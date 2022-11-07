from enum import unique

from mui.compat import StrEnum


@unique
class Category(StrEnum):
    CATEGORY_1 = "cat-1"
    CATEGORY_2 = "cat-2"
    CATEGORY_3 = "cat-3"
    CATEGORY_4 = "cat-4"
