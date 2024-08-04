import datetime
import json
import logging
import traceback

import aiosqlite
import fujson
from croniter import croniter


# https://pypi.org/project/cron-schedule-triggers/

async def plan_event(cron_string: str, alert_message: str, periodic: bool = False, key: str = "unknown"):
    """Plan the event"""

    plan_info = {
        "result": f"{alert_message} planned!"
    }

    try:
        logging.info(f"adding {alert_message} at {cron_string}. Periodic: {periodic}")
        croniterchik = croniter(cron_string)

        next_run = croniterchik.get_next(ret_type=datetime.datetime)
        logging.info(f"first run: {next_run}")
        await _add_event(cron=cron_string, alert_message=alert_message, periodic=periodic, user_id=key)
    except Exception as error:
        print(traceback.format_exc())
        return {
            "result": f"{error} happened!"
        }

    return plan_info


def plan_event_tool():
    return {
        "type": "function",
        "function": {
            "name": "plan_event",
            "description": "Use this function ONLY when directly asked to plan or remind about something."
                           "Do not call it, if you are not asked to!"
                           "It adds cron job for the given event. So be accurrate when creating cron string",
            "parameters": {
                "type": "object",
                "properties": {
                    "cron_string": {
                        "type": "string",
                        "description": "Cron string you create depending on user request."
                                       " for example: 5 4 * * * which means At 04:05. "
                                       "Or 5 0 * 8 * which means At 00:05 in August. Don't forget that you know the "
                                       "current date and time!"
                    },
                    "alert_message": {
                        "type": "string",
                        "description": "Planned event message to be sent to the user."
                                       "This message will be used in a reminder send to user. Be creative and address the user in this field."
                                       "For example: Call mother in 2 hours -> Please call your mother"
                    },
                    "periodic": {
                        "type": "boolean",
                        "description": "If the notification should be send periodically. For example:"
                                       "Call mother in 2 hours: not a periodic task"
                                       "Drink water every 2 hours: a periodic task"
                    },
                },
                "required": ["cron_string", "alert_message", "periodic"]
            }
        }
    }


async def _add_event(cron, alert_message, periodic, user_id):
    async with aiosqlite.connect("plans.db") as db:
        values = (cron, alert_message, periodic, user_id)
        insert_query = "INSERT INTO plans ('cron', 'alert_message', 'periodic', 'user_id') VALUES (?, ?, ?, ?)"

        print(insert_query)

        await db.execute(insert_query, values)
        await db.commit()
