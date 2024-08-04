from kibernikto.bots.cybernoone import Kibernikto
import datetime


class Kiberplanner(Kibernikto):
    def get_cur_system_message(self):
        extended_info = self.about_me.copy()

        now = datetime.datetime.now()
        print(now)
        extended_info['content'] += f"\n[current date and time: {now}]"
        return extended_info
