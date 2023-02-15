import graphene


class MemberCreationInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="Email address of the user")
    password = graphene.String(description="Login password for the user")
    firstName = graphene.String()
    lastName = graphene.String()


__all__ = [
    "MemberCreationInput",
]
