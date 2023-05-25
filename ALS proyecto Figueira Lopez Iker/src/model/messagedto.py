from datetime import datetime


class MessageDto:
    def __init__(self, msg):
        self._msg = msg
        self._time = datetime.now()

    @property
    def msg(self):
        return self._msg

    @property
    def time(self):
        return self._time.strftime("%d/%m/%Y")

    def __str__(self):
        Autor= self.msg.split(":")[0]
        Mensaje=self.msg.split(":")[1]
        return f"{Autor} ({self.time}): \"{Mensaje}\""
