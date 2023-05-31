from graphql import GraphQLError


class DefaultError(GraphQLError):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)
