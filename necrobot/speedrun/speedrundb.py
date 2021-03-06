"""
Module for interacting with the speedruns table of the database.
"""

import datetime

from necrobot.database.dbconnect import DBConnect
from necrobot.database.dbutil import tn
from necrobot.race import racedb
from necrobot.race.raceinfo import RaceInfo
from necrobot.user.necrouser import NecroUser


async def submit(
        necro_user: NecroUser,
        category_race_info: RaceInfo,
        category_score: int,
        vod_url: str,
        submission_time: datetime.datetime = None
) -> None:
    category_type_id = await racedb.get_race_type_id(race_info=category_race_info, register=True)

    params = (
        necro_user.user_id,
        category_type_id,
        category_score,
        vod_url,
        submission_time
    )
    async with DBConnect(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO {speedruns}
            (user_id, type_id, score, vod, submission_time)
            VALUES (%s, %s, %s, %s, %s)
            """.format(speedruns=tn('speedruns')),
            params
        )


async def get_raw_data():
    async with DBConnect(commit=False) as cursor:
        cursor.execute(
            """
            SELECT 
                submission_id,
                user_id,
                type_id,
                score,
                vod,
                submission_time,
                verified
            FROM {speedruns}
            ORDER BY -submission_time DESC
            """.format(speedruns=tn('speedruns'))
        )
        return cursor.fetchall()


async def set_verified(run_id: int, verified: bool):
    async with DBConnect(commit=True) as cursor:
        params = (verified, run_id,)
        cursor.execute(
            """
            UPDATE {speedruns}
            SET verified = %s
            WHERE submission_id = %s
            """.format(speedruns=tn('speedruns')),
            params
        )
