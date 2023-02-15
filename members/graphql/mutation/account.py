import graphene
from members.models import Members
from ..inputs.account import MemberCreationInput
from ..types import UserBasicObj
from django.db.models import Q
from ims.graphql.APIException import APIException


class MemberCreationResponse(
    graphene.ObjectType, description="Response for member creation"
):
    returning = graphene.Field(
        UserBasicObj, description="Member creation fields to be returned"
    )


class CreateMember(graphene.Mutation, description="Create a new member"):
    class Arguments:
        input = graphene.Argument(
            MemberCreationInput,
            required=True,
            description="Fields required to create a new member",
        )

    Output = MemberCreationResponse

    @staticmethod
    def mutate(root, info, input=None):
        try:
            member = Members.objects.get(email=input.email)
            if member.email == input.email:
                raise APIException("Username already taken.", code="USERNAME_TAKEN")
        except Members.DoesNotExist:
            if len(input.firstName) < 4 or len(input.lastName) < 4:
                raise APIException("Name is too short.", code="NAME_TOO_SHORT")
            if input.password is None:
                raise APIException("Password is required.", code="PASSWORD_REQUIRED")
            if len(input.password) < 8:
                raise APIException("Password is too short.", code="PASSWORD_TOO_SHORT")
            member = Members.objects.create(
                email=input.email,
                first_name=input.firstName,
                last_name=input.lastName,
            )
            member.set_password(input.password)
            member.save()
            return MemberCreationResponse(returning=member)


class AccountMutation(graphene.ObjectType):
    create_member = CreateMember.Field()


__all__ = [
    "AccountMutation",
]
