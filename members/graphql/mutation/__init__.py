import graphene
from .account import *


class MemberMutation(AccountMutation, graphene.ObjectType):
    pass


__all__ = [
    "MemberMutation",
]
