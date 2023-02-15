import graphene
from .members import UserQuery


class MemberQueries(UserQuery, graphene.ObjectType):
    pass


__all__ = [
    "MemberQueries",
]
