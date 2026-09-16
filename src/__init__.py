"""XPELAB Python package.

The Rust lab declares its modules in `src/lib.rs`:

    pub mod datasource;
    pub mod errors;
    ...

In Python, a directory containing an `__init__.py` IS the module. Nothing has
to be declared here: `src.models`, `src.routes`, ... are importable as soon as
the files exist. This file can stay empty, it is only here to say
"this folder is a package".
"""
