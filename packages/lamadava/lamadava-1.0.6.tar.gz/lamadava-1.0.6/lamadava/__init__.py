try:
    from .api import Client
    from .asyncapi import AsyncClient
except ImportError:
    def Client(*args, **kwargs):
        import sys
        print(
            "The lamadava client could not init because the required "
            "dependencies were not installed.\nMake sure you've installed "
            "everything with: pip install 'lamadava'"
        )
        sys.exit(1)
    AsyncClient = Client

__all__ = ["Client", "AsyncClient"]
