import logging
import json
from datetime import datetime

logger = logging.getLogger("audit")

def log_user_action(action, user_obj):
    # FIXED: Sanitize sensitive data before logging
    safe_obj = {
        "username": user_obj.get("username"),
        "active": user_obj.get("active"),
        # Exclude password_hash and ssn
    }
    logger.info(f"User performed {action}: {json.dumps(safe_obj)}")

import logging.handlers

handler = logging.handlers.RotatingFileHandler('audit.log', maxBytes=1000000, backupCount=5)
logger.addHandler(handler)

def send_to_datadog(log_entry):
    # Fake
    pass