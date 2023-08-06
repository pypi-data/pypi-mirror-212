# pyjar

Move Python things to other modules, mostly for
backward-compatibility, such as when you want to refactor your code
but still need old pickles to be loadable, or particularly if you need
the new pickles to be byte-for-byte-identical to the old ones.

## installation

😄

You can `pip install pyjar` if you really want to, but you can also just
copy this public-domain code from `src/jar/__init__.py` directly into
your own project. You can even give it a name you like better.


## usage

```
from pyjar import jar


@jar('.old_module_name)
def my_function_that_i_moved_here():
    ...
```

The function (or class, or whatever) will still be importable from its
new location, but it will `pickle` as though it lives in the old
location. And as long as the module that defines the function itself
has been imported, old pickles pointing to the old location will
successfully unpickle.
