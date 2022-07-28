import datetime


class User_timer():
    def __init__(self, time):
        self.cooldown_time = time
        self.last_send = None

    def cooldown(self):
        self.last_send = datetime.datetime.now()

    def check_cooldown(self):
        if (self.last_send == None):
            return True
        difference = datetime.datetime.now() - self.last_send
        return difference.total_seconds() > self.cooldown_time
