from importlib.metadata import version

__version__ = version("dls_servbase")
del version

__all__ = ["__version__"]
