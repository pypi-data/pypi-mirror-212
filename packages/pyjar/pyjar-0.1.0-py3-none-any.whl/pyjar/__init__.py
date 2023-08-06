"""This code was written by Peter Gaultney and is in the public domain.

There's no need to install this module - just copy this single file into your project.
"""
import importlib
import sys
import typing as ty

T = ty.TypeVar("T")


def _new_module(mod_name: str):
    spec = importlib.machinery.ModuleSpec(mod_name, None)
    return importlib.util.module_from_spec(spec)  # type: ignore


def _absolute_from_relative(relative_to: str, path: str) -> str:
    if not path.startswith("."):
        return path

    module_path = path.lstrip(".")
    num_up = len(path) - len(module_path)
    return ".".join(filter(None, [*relative_to.split(".")[:-num_up], module_path]))


def _put_thing_in_module(thing: T, module_name: str) -> T:
    # preliminary magic
    module_name = _absolute_from_relative(thing.__module__, module_name)
    if module_name not in sys.modules:
        sys.modules[module_name] = _new_module(module_name)
    mod = sys.modules[module_name]
    setattr(mod, thing.__name__, thing)  # type: ignore
    thing.__module__ = module_name  # this is the main magic
    return thing


def jar(module_name: str) -> ty.Callable[[T], T]:
    """Put a thing into a different module, usually for
    backward-compatiblity in something like pickle.

    Module name can be relative/dotted, e.g.

    .sibling
    ..aunt
    ..great_uncle
    ..great_aunt.first_cousin.second_cousin.second_cousin_once_removed

    If it does not begin with a dot, it will be considered to be
    fully-qualified.
    """

    def deco(thing: T) -> T:
        return _put_thing_in_module(thing, module_name)

    return deco
