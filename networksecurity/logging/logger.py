import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs")
os.makedirs(logs_path,exist_ok=True)

#/home/amisha/project/logs/09_27_2025_17_40_15.log
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
     filename=LOG_FILE_PATH,
     format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
     level=logging.INFO,
)

logger = logging.getLogger("networksecurity")

# %(asctime)s → Timestamp when the log was written.

# %(lineno)d → Line number in the source code where the log happened.

# %(name)s → Name of the logger (default: root).

# %(levelname)s → Type of message (INFO, WARNING, ERROR, etc.).

# %(message)s → The actual log message you write.

