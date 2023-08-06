from pikanetwork.models import *


async def build_player(player_data: dict) -> Player:

    ranks = []

    friends = []

    for rank in player_data["ranks"]:
        ranks.append(GameRank(
            name=rank["name"],
            display_name=rank["displayName"],
            server=rank["server"],
            season=rank["season"]
        ))

    for friend_data in player_data["friends"]:

        friend = Friend(
            username=friend_data["username"],
            last_seen=friend_data["lastSeen"],
            online=friend_data["online"]
        )
        friends.append(friend)

    if player_data["clan"] is None:
        clan = None
    else:
        clan_data = player_data["clan"]

        members = []

        for member_raw_data in clan_data["members"]:
            member_data = member_raw_data["user"]
            member = ClanMember(
                username=member_data["username"],
                last_seen=member_data["lastSeen"],
                online=member_data["online"],
                join_date=member_raw_data["joinDate"]
            )
            members.append(member)

        clan = Clan(
            name=clan_data["name"],
            tag=clan_data["tag"],
            current_trophies=clan_data["currentTrophies"],
            creation_time=clan_data["creationTime"],
            members=members,
            owner=ClanOwner(
                username=clan_data["owner"]["username"],
                last_seen=clan_data["owner"]["lastSeen"],
                online=clan_data["owner"]["online"]
            ),
            level=clan_data["leveling"]["level"],
            experience=clan_data["leveling"]["exp"],
            total_experience=clan_data["leveling"]["totalExp"]
        )

    player = Player(
        username=player_data["username"],
        friend_status=player_data["friendStatus"],
        discord_verified=player_data["discord_verified"],
        last_seen=player_data["lastSeen"],
        ranks=ranks,
        email_verified=player_data["email_verified"],
        discord_boosting=player_data["discord_boosting"],
        clan=clan,
        rank=Rank(
            level=player_data["rank"]["level"],
            experience=player_data["rank"]["experience"],
            percentage=player_data["rank"]["percentage"],
            rank_display=player_data["rank"]["rankDisplay"]
        ),
        friends=friends
    )

    return player


async def build_player_leaderboard(leaderboard_data: dict) -> PlayerLeaderboard:

    attributes = {}

    for key in leaderboard_data:
        data = leaderboard_data[key]

        name = key.replace(" ", "_").lower()

        if data["entries"] is None:
            attributes[name] = None
        else:
            place = data["entries"][0]["place"]
            value = data["entries"][0]["value"]
            username = data["entries"][0]["id"]

            attributes[name] = PlayerLeaderboardBase(
                total_players=data["metadata"]["total"],
                place=place,
                value=value,
                username=username
            )

    return PlayerLeaderboard(**attributes)
