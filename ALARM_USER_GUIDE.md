# Alarm, Notification, and Challenge Guide

## Alarm types

Use `POST /alarms/` with a bearer token to create an alarm.

- `daily`: rings every day at `alarm_time`.
- `weekly`: additionally provide `repeat_days`, using Monday `0` through Sunday `6`.
- `one_time`: additionally provide `one_time_date` (`YYYY-MM-DD`); it disables itself after firing.
- `smart`: uses the selected target `alarm_time`; a mobile client can calculate the target from sleep recommendations before saving it.

`snooze_duration_minutes` must be 1-60 and `max_snooze_count` must be 0-10.

## Wake-up workflow

1. The scheduler checks alarm rules every 30 seconds, and the mobile client should call `POST /alarms/{id}/trigger` when its local alarm fires.
2. A trigger creates an alarm event and a fresh cognitive verification session.
3. Snooze with `POST /alarms/{id}/snooze` (optional `{ "event_id": 12 }`). When the limit is reached, snooze is rejected.
4. Submit answers through `POST /verification/{verification_id}/submit?answer=...`. The server enforces `challenge_time_limit_seconds` (10–600 seconds); `GET /verification/{verification_id}` provides `seconds_remaining` for the client timer.
5. Only a successful verification may call `POST /alarms/{id}/dismiss?event_id=12`.

Inspect an alarm's recent runs using `GET /alarms/{id}/events`.

## Notifications

Register an FCM token with `POST /alarms/devices`:

```json
{ "token": "your-fcm-device-token", "platform": "android" }
```

Set `FIREBASE_SERVICE_ACCOUNT_FILE` to a Firebase service-account JSON file and install the packages in `Backend/requirements.txt` to enable Firebase Cloud Messaging. If either is absent or delivery fails, the API records a local-notification fallback and continues the alarm workflow; an alarm is never blocked by a push failure. Mobile apps should consume the data payload (`event=alarm_triggered`, `alarm_id`) to schedule the OS-specific full-screen/local alarm notification.

For a mobile local-notification implementation, fetch `GET /alarms/{id}/notification-schedule` after every create, update, or toggle action and mirror its `notification` object in Android/iOS. Delivery attempts can be audited through `GET /alarms/{id}/notifications`.

## Demo

1. Create a daily alarm a minute ahead, or create any alarm and call its `/trigger` endpoint.
2. Show the returned `event_id` and `verification_id`.
3. Snooze once, then show the event status changes to `snoozed`.
4. Use the verification endpoint to answer the generated challenge and dismiss the event.
5. Call `/alarms/{id}/events` to show the auditable final state.
