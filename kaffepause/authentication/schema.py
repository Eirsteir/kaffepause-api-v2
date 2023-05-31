import graphene

from kaffepause.authentication.mutations import ObtainJSONWebToken, SocialAuthJWT


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    social_auth = SocialAuthJWT.Field()
