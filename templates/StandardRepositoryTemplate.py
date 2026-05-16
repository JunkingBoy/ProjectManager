from dataclasses import dataclass

@dataclass
class StandardUserRepositoryTemplate:
    uid: str | None
    phone: str | None
    email: str | None
    password: str | None

    @property
    def info(self) -> dict: return self.__dict__.copy()
