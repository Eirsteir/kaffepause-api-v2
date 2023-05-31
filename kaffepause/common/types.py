import graphene
from graphene import relay
from graphql import GraphQLError


class CountableConnection(relay.Connection):
    """Connection to include a total edges count."""

    class Meta:
        abstract = True

    count = graphene.Int()
    total_count = graphene.Int()

    def resolve_count(root, info, **kwargs):
        return len(root.edges)

    def resolve_total_count(root, info, **kwargs):
        return len(root.iterable)


class OutputErrorType(graphene.Scalar):
    class Meta:
        description = """
    Errors messages and codes mapped to
    fields or non fields errors.
    Example:
    {
        field_name: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        other_field: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        nonFieldErrors: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ]
    }
    """

    @staticmethod
    def serialize(errors):
        # This is stolen from chatgpt, I take no responsibility for this:)
        if not isinstance(errors, dict):
            raise GraphQLError("Invalid error format. Expected a dictionary.")

        error_output = {}

        # Map field-specific errors
        for field, field_errors in errors.items():
            if field == "nonFieldErrors":
                # Skip the nonFieldErrors key if present
                continue

            error_output[field] = []
            for error in field_errors:
                if (
                    not isinstance(error, dict)
                    or "message" not in error
                    or "code" not in error
                ):
                    raise GraphQLError(
                        "Invalid error format. Expected 'message' and 'code' keys in error dictionary."
                    )

                error_output[field].append(
                    {"message": error["message"], "code": error["code"]}
                )

        # Add non-field-specific errors if present
        if "nonFieldErrors" in errors:
            non_field_errors = errors["nonFieldErrors"]
            if not isinstance(non_field_errors, list):
                raise GraphQLError(
                    "Invalid error format. Expected a list for 'nonFieldErrors'."
                )

            error_output["nonFieldErrors"] = []
            for error in non_field_errors:
                if (
                    not isinstance(error, dict)
                    or "message" not in error
                    or "code" not in error
                ):
                    raise GraphQLError(
                        "Invalid error format. Expected 'message' and 'code' keys in error dictionary."
                    )

                error_output["nonFieldErrors"].append(
                    {"message": error["message"], "code": error["code"]}
                )

        return error_output
