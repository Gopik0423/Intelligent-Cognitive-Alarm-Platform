from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from database.db import Base


class NotificationLog(Base):
    """Delivery record for FCM and the local-notification handoff."""

    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    alarm_id = Column(Integer, ForeignKey("alarms.id"), nullable=False, index=True)
    channel = Column(String, nullable=False)
    status = Column(String, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
