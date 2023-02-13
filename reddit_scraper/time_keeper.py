import sys
import logging
from datetime import datetime


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class TimeKeeper:
    def __init__(self):
        self.checkpoint = datetime.now()
    
    def is_tomorrow(self) -> bool:
        new_checkpoint = datetime.now()
        if (new_checkpoint - self.checkpoint).days > 0:
            self.checkpoint = new_checkpoint
            logger.info(f"It is tomorrow!")
            return True
        else:
            logger.info(f"It is not tomorrow.")
            return False
        