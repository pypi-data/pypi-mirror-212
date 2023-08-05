from typing import Optional


class DeletedException(AttributeError):
    pass


def deleted(func, cls_name: Optional[str] = None):
    msg = f"'{func.__qualname__}' has been marked as deleted"
    if cls_name:
        msg = f"'{cls_name}.{func.__name__}' has been marked as deleted"

    def new_func(*args, **kwargs):
        nonlocal func
        raise DeletedException(msg)
    return new_func


class ImplicitDataDeleterMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls_functions = set()
        for k, v in namespace.items():
            if callable(v):
                if hasattr(v, "__objclass__"):
                    if v.__objclass__ in {object}:
                        continue

                elif hasattr(v, "__module__"):
                    if v.__module__ in {'builtins', None}:
                        continue

                cls_functions.add(v)

        parent_functions = set()
        for base in bases:
            for k, v in base.__dict__.items():
                if callable(v):
                    parent_functions.add(v)

        parent_dct = {func.__name__: func for func in parent_functions}
        cls_dct = {func.__name__: func for func in cls_functions}
        to_delete = set({k: v for k, v in parent_dct.items()
                         if k not in cls_dct}.values())
        for func in to_delete:
            if func.__name__ in dir(object):
                if func.__name__ in {"__init__"}:
                    continue
                namespace[func.__name__] = object.__dict__[func.__name__]
            elif func.__name__ in {"__len__", "__bool__"}:
                namespace[func.__name__] = lambda self: True
            else:
                namespace[func.__name__] = deleted(func, name)

        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "ImplicitDataDeleterMeta",
    "DeletedException"
]
