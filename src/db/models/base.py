from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

