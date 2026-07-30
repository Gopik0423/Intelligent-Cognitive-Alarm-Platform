"""Push-notification adapter with a deterministic local-development fallback."""
import logging
import os

from models.device_token import DeviceToken
from models.notification_log import NotificationLog

logger = logging.getLogger(__name__)


def _record(db, user_id: int, alarm_id: int, channel: str, status: str, title: str, body: str) -> dict:
    db.add(NotificationLog(user_id=user_id, alarm_id=alarm_id, channel=channel, status=status, title=title, body=body))
    return {"channel": channel, "status": status}


def send_alarm_notification(db, user_id: int, alarm_id: int, title: str, body: str) -> dict:
    """Deliver a data-only FCM notification when configured; otherwise log it.

    Mobile clients should use the payload's `event` and `alarm_id` to show their
    platform local full-screen alarm notification.
    """
    tokens = [row.token for row in db.query(DeviceToken).filter_by(user_id=user_id, is_active=True)]
    payload = {"event": "alarm_triggered", "alarm_id": str(alarm_id)}
    if not tokens:
        logger.info("Local notification: %s - %s", title, body)
        return _record(db, user_id, alarm_id, "local", "scheduled_for_client", title, body)

    try:
        import firebase_admin
        from firebase_admin import credentials, messaging

        if not firebase_admin._apps:
            credential_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE")
            if not credential_path:
                raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_FILE is not configured")
            firebase_admin.initialize_app(credentials.Certificate(credential_path))
        message = messaging.MulticastMessage(
            tokens=tokens,
            notification=messaging.Notification(title=title, body=body),
            data=payload,
        )
        response = messaging.send_each_for_multicast(message)
        result = _record(db, user_id, alarm_id, "fcm", "sent" if response.success_count else "failed", title, body)
        result["delivered"] = response.success_count
        return result
    except Exception as exc:  # A missing optional SDK must never stop an alarm.
        logger.warning("FCM unavailable; local fallback used: %s", exc)
        return _record(db, user_id, alarm_id, "local", "scheduled_for_client", title, body)
