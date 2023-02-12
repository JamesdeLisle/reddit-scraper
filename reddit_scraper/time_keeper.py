
from datetime import datetime


class TimeKeeper:
    def __init__(self):
        self.checkpoint = datetime.now()
    
    def is_tomorrow(self) -> bool:
        new_checkpoint = datetime.now()
        if (new_checkpoint - self.checkpoint).days > 0:
            self.checkpoint = new_checkpoint
            return True
        else:
            return False
        