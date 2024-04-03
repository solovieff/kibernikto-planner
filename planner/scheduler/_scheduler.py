import asyncio
import datetime
import logging
import time
import traceback

import aiocron
import aiosqlite
from croniter import croniter

from kibernikto.telegram import comprehensive_dispatcher


async def start_scheduler():
    """
    Checking the tasks in the table every minute and reminding the user.
    Should be hidden in inside yr own custom dispatcher
    :return:
    :rtype:
    """
    async with aiosqlite.connect("plans.db") as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS plans(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, cron text, alert_message text, periodic boolean, last_run text)")

        async def check_tasks():
            logging.debug(f"-- running tasks check at {datetime.datetime.now()}")
            try:
                async with aiosqlite.connect("plans.db") as db:
                    now_dt = datetime.datetime.now()
                    db.row_factory = aiosqlite.Row
                    async with db.execute('SELECT * FROM plans where cron is not null') as cursor:
                        async for row in cursor:
                            print("===-===")
                            id = row['id']
                            cron_string = row['cron']
                            description = row['alert_message']
                            master_id = row['user_id']
                            periodic = row['periodic']

                            # using crontab for parsing the cron string only here
                            crnt = croniter(cron_string, start_time=now_dt)

                            # next_run_timestamp = crnt.get_next()
                            next_run_dt = crnt.get_next(ret_type=datetime.datetime)

                            print(f"now is {now_dt} next run is {next_run_dt} for {cron_string}")

                            time_diff = int(next_run_dt.timestamp() - now_dt.timestamp())

                            print(f"- event: {description}")
                            print(f"- cron: {cron_string}")
                            print(f"- now: {now_dt}")
                            print(f"- next: {next_run_dt}")
                            print(f"- diff: {time_diff} seconds")

                            if time_diff < 60:
                                await comprehensive_dispatcher.tg_bot.send_message(chat_id=master_id,
                                                                                   text=f"🔜🔜🔜\n{description}\n🔜🔜🔜")
                                if periodic:
                                    update_query = 'UPDATE plans SET last_run=? WHERE id=?'
                                    values = (str(next_run_dt), id)
                                else:
                                    update_query = 'UPDATE plans SET last_run=?, cron=? WHERE id=?'
                                    values = (str(next_run_dt), None, id)
                                print(update_query)
                                print(values)
                                await db.execute(update_query, values)
                                await db.commit()

            except Exception as exc:
                print(traceback.format_exc())
                raise RuntimeError("Failed to check the crons!")

        cron = aiocron.crontab('* * * * *', func=check_tasks, start=True)
