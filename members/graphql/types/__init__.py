import graphene
from members.models import Members


class UserBasicObj(
    graphene.ObjectType,
    description="Basic User Information",
):
    id = graphene.ID()
    firstName = graphene.String()
    lastName = graphene.String()
    email = graphene.String()
    isAgent = graphene.Boolean()

    def resolve_id(self, info):
        if isinstance(self, Members):
            return self.id

    def resolve_firstName(self, info):
        if isinstance(self, Members):
            return self.first_name

    def resolve_lastName(self, info):
        if isinstance(self, Members):
            return self.last_name

    def resolve_email(self, info):
        if isinstance(self, Members):
            return self.email

    def resolve_isAgent(self, info):
        if isinstance(self, Members):
            return self.is_agent
