import graphene

from kaffepause.accounts.types import AccountNode
from kaffepause.authentication.decorators import login_required


class AccountQuery(graphene.ObjectType):
    my_accounts = graphene.List(AccountNode)

    @login_required
    def resolve_my_accounts(root, info):
        return info.context.user.account.all()


class Query(AccountQuery, graphene.ObjectType):
    pass
