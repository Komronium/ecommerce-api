from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        print(self.__name__.lower())
        return self.__name__.lower()
