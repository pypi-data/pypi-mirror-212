from typing import Any, Optional, Callable


class Options:
    _instance = None

    def define(
            self,
            name: str,
            default: Any = None,
            type_: Optional[type] = None,
            help_: Optional[str] = None,
            callback: Optional[Callable] = None,
    ) -> None:
        if hasattr(self, name):
            raise Exception(f'name={name} has been defined')
        if type_:
            if not isinstance(default, type_):
                raise Exception(f'default={default} type is error')
        if callback:
            default = callback(default)
        self.__setattr__(name, default)

    def __getattr__(self, name: str):
        if hasattr(super(), name):
            return super().__getattr__(name)
        raise AttributeError("Unrecognized option %r" % name)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


options = Options()


def define(name: str,
           default: Any = None,
           type_: Optional[type] = None,
           help_: Optional[str] = None,
           callback: Optional[Callable] = None,
           ) -> None:
    return options.define(name=name, default=default, type_=type_, help_=help_, callback=callback)
