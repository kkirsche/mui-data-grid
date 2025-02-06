from mui.compat import StrEnum


def values_callable(enum: type[StrEnum]) -> list[str]:
    return [member.value for member in enum]
