import logging

import graphene
from graphql import GraphQLError

import kaffepause.users.types
from kaffepause.authentication.backend import Neo4jSessionBackend, Neo4jSocialBackend
from kaffepause.authentication.jwt import create_access_token

logger = logging.getLogger(__name__)


class ObtainJSONWebToken(graphene.Mutation):
    """
    Mutation to obtain a JSON Web Token
    """

    class Arguments:
        session_token = graphene.String(required=True)

    access_token = graphene.String()
    user = graphene.Field(lambda: kaffepause.users.types.UserNode)

    def mutate(self, info, session_token):
        """
        Mutation to obtain a JSON Web Token
        """
        user = Neo4jSessionBackend().authenticate(session_token=session_token)

        if user is None:
            raise GraphQLError("Invalid credentials")

        access_token = create_access_token(user)

        return ObtainJSONWebToken(access_token=access_token, user=user)


class SocialAuthJWT(graphene.Mutation):
    """
    Mutation to authenticate a user with a social media provider
    """

    class Arguments:
        provider = graphene.String(required=True)
        access_token = graphene.String(required=True)

    access_token = graphene.String()
    user = graphene.Field(lambda: kaffepause.users.types.UserNode)

    def mutate(self, info, provider, access_token):
        """
        Mutation to obtain a JSON Web Token
        """
        logger.debug(
            "Authenticating user with provider %s and access token %s",
            provider,
            access_token,
        )

        user = Neo4jSocialBackend().authenticate(
            provider=provider, access_token=access_token
        )

        if user is None:
            raise GraphQLError("Invalid credentials")

        logger.debug("User %s authenticated successfully", user)

        access_token = create_access_token(user)

        logger.debug("Access token %s created successfully", access_token)

        return ObtainJSONWebToken(access_token=access_token, user=user)
