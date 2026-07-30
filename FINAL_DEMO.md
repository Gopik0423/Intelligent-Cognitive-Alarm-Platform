# Final Demo Runbook

Run from `Backend` after installing requirements:

```powershell
uvicorn main:app --reload
```

1. Register and sign in a demo user (`POST /register`, then `POST /login`), and set the returned bearer token in Swagger at `http://127.0.0.1:8000/docs`.
2. Create a weekly alarm via `POST /alarms/` using `repeat_days: [0,1,2,3,4]`, `challenge_time_limit_seconds: 30`, and a small snooze limit.
3. Call `GET /alarms/{id}/notification-schedule` to show the local Android/iOS alarm payload. Optionally register an FCM token with `POST /alarms/devices`.
4. Call `POST /alarms/{id}/trigger`. Show the returned `event_id` and `verification_id`; then open `GET /alarms/{id}/notifications` to show FCM delivery or local fallback audit data.
5. Call `POST /alarms/{id}/snooze` once. Show the `retrigger_at` response and explain that the scheduler turns it back to `triggered` automatically.
6. Open `GET /verification/{verification_id}` to demonstrate the server-authoritative countdown. Submit an answer before the deadline, then dismiss using `POST /alarms/{id}/dismiss?event_id=...`.
7. Finish with `GET /alarms/{id}/events` to show the persisted triggered/snoozed/dismissed audit trail.

For Firebase delivery, set `FIREBASE_SERVICE_ACCOUNT_FILE` to the secured path of a Firebase service-account JSON before starting the API. Do not commit that credential file.
