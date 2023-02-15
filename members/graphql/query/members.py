import graphene
from members.models import Members
from members.graphql.types import UserBasicObj


class UserQuery(graphene.ObjectType):
    members = graphene.List(UserBasicObj)
    member = graphene.Field(UserBasicObj, id=graphene.ID())

    def resolve_members(self, info):
        return Members.objects.all()

    def resolve_member(self, info, **kwargs):
        id = kwargs.get("id")
        return Members.objects.get(id=id)


__all__ = [
    "UserQuery",
]
