from typing import List

from neomodel import db

from kaffepause.relationships.enums import NonRelatedRelationship, UserRelationship
from kaffepause.users.models import User


def get_friends(user: User) -> List[User]:
    return user.friends.all()


def get_incoming_requests(
    user: User,
) -> List[User]:
    return user.incoming_friend_requests.all()


def get_outgoing_requests(
    user: User,
) -> List[User]:
    return user.outgoing_friend_requests.all()


def relationship_exists(user, other):
    """
    Returns boolean whether or not a relationship
    of any kind exists between the given users.
    """
    query = f"""
    MATCH (user:User)-[:{UserRelationship.ARE_FRIENDS}|
        {UserRelationship.REQUESTING_FRIENDSHIP}]-(other:User)
    WHERE user.id = $user_uuid AND other.id = $other_uuid
    RETURN other
    """
    params = dict(user_uuid=user.uuid, other_uuid=other.uuid)
    results, meta = db.cypher_query(query, params)
    people = [User.inflate(row[0]) for row in results]
    return people


def get_friendship_status(actor: User, user: User) -> object:
    """
    Returns the friendship status as viewed by the actor.
    If no such friendship exists, a default value of 'CAN_REQUEST' is returned.
    """
    # TODO: Differ between requested direction
    if actor == user:
        return None
    # query = f"""
    # MATCH (subject:User {{id: $subject_uuid}})
    # -[r:{UserRelationship.ARE_FRIENDS} | {UserRelationship.REQUESTING_FRIENDSHIP}]
    # -(person:User {{id: $person_uuid}})
    # return TYPE(r)
    # """
    #
    # params = dict(subject_uuid=actor.uuid, person_uuid=user.uuid)
    # results, meta = db.cypher_query(query, params)
    # status = results[0][0] if results else str(NonRelatedRelationship.CAN_REQUEST)

    if actor.friends.is_connected(user):
        status = str(UserRelationship.ARE_FRIENDS)
    elif actor.outgoing_friend_requests.is_connected(user):
        status = str(NonRelatedRelationship.OUTGOING_REQUEST)
    elif actor.incoming_friend_requests.is_connected(user):
        status = str(NonRelatedRelationship.INCOMING_REQUEST)
    else:
        status = str(NonRelatedRelationship.CAN_REQUEST)

    return status


def get_social_context_between(actor: User, other: User) -> str:
    mutual_friends_count = get_mutual_friends_count(actor=actor, user=other)
    count = mutual_friends_count if mutual_friends_count else "Ingen"
    return f"{count} felles venner"


def get_mutual_friends_count(actor: User, user: User) -> int:
    """Returns the mutual friends for the given users."""
    query = f"""
    MATCH (subject:User {{id: $subject_uuid}})
    -[:{UserRelationship.ARE_FRIENDS}]-(n)-[:{UserRelationship.ARE_FRIENDS}]
    -(person:User {{id: $person_uuid}})
    WHERE subject <> n
    RETURN count(n)
    """
    params = dict(subject_uuid=actor.uuid, person_uuid=user.uuid)
    results, meta = db.cypher_query(query, params)
    mutual_friends_count = results[0][0]

    return mutual_friends_count


def get_friend_recommendations(user, limit=10):
    """
    Recommends friends for a given user
    based on the number of mutual friends and shared campus and groups.

    Args:
        current_user_uuid (str): The UUID of the current user.

    Returns:
        list of tuples: A list of recommended user UUIDs
        along with their campus and group membership status.

    Raises:
        Neo4jError: If there was an error executing the query.
    """
    query = """
        MATCH (u:User {id: $user_uuid})-[:ARE_FRIENDS]
            -(f:User)-[:ARE_FRIENDS]-(recommended_user:User)
        WHERE NOT (u)-[:ARE_FRIENDS]-(recommended_user)
            AND NOT recommended_user.id = $user_uuid
        WITH recommended_user, u, COUNT(f) AS mutual_friends
        OPTIONAL MATCH (u)-[:PREFERRED_LOCATION]->
            (u_loc:Location)<-[:PREFERRED_LOCATION]-(recommended_user)
        WITH recommended_user, u, mutual_friends, u_loc,
             [(recommended_user)-[:ARE_FRIENDS]-(f:User) | f.id] AS friends_uuids,
             [(recommended_user)-[:HAS_MEMBER]-(g:Group) | g.id] AS group_uuids
        ORDER BY mutual_friends DESC
        WITH recommended_user, u, mutual_friends, u_loc, friends_uuids, group_uuids,
             [loc IN [(recommended_user)-[:PREFERRED_LOCATION]->(loc:Location) | loc]
                WHERE loc = u_loc | loc] AS same_campus,
             [(recommended_user)-[:HAS_MEMBER]-(g:Group)
                WHERE NOT (u)-[:HAS_MEMBER]-(g) | g] AS same_group
        RETURN recommended_user
        //, same_campus, same_group, mutual_friends
        LIMIT $limit
    """
    params = dict(user_uuid=user.uuid, limit=limit)
    results, meta = db.cypher_query(query, params)
    recommendations = [User.inflate(row[0]) for row in results]

    return recommendations
