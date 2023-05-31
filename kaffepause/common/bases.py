from enum import Enum

import graphene

from kaffepause.authentication.decorators import login_required
from kaffepause.common.types import OutputErrorType


class Output:
    """
    A class to all public classes extend to
    standardize the output
    """

    success = graphene.Boolean(default_value=False)
    errors = graphene.Field(OutputErrorType)


class MutationMixin:
    @classmethod
    def mutate(cls, root, info, **input):
        return cls.resolve_mutation(root, info, **input)


class LoginRequiredMixin(MutationMixin):
    """
    All mutations which requires user to be verified should extend this class.
    """

    @classmethod
    @login_required
    def mutate(cls, root, info, **input):
        return cls.resolve_mutation(root, info, **input)


class NeomodelRelationshipEnum(Enum):
    """
    Base enum class for neomodel relationships.
    Allows for simple direct use of the enums name.
    """

    def __str__(self):
        return self.name

    __repr__ = __str__


class SectionNode(graphene.ObjectType):
    section_id = graphene.String()
    heading = graphene.String()
    is_empty = graphene.Boolean()
    emptyStateText = graphene.String()
    emptyStateActionText = graphene.String()

    def resolve_is_empty(parent, info):
        return not parent.items
