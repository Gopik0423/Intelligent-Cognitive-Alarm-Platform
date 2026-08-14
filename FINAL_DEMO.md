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

## Alarm Intelligence Workflow

1. Open `GET /difficulty/get?user_id={user_id}` to show the user's current
   earned level. A new user starts at an age-appropriate level.
2. Complete practice challenges or submit answers during a live verification.
   Every answer is logged as performance data and updates the same level:
   three consecutive correct answers increase it by one; two consecutive
   wrong answers decrease it by one.
3. Start another challenge or verification. Its generated question uses that
   updated level, demonstrating that the change affects the real alarm rather
   than only the dashboard.
4. After at least four attempts, open
   `GET /recommendation/{user_id}/alarm-intelligence`. The response contains
   the active difficulty, behavioral trends, explainable actions, and
   `validated: true`. It will emit only one difficulty action (increase,
   decrease, or maintain), so conflicting advice cannot reach the client.
5. Open the Recommendations page to show the same validated actions alongside
   sleep, wake-up, productivity, and habit guidance.

For Firebase delivery, set `FIREBASE_SERVICE_ACCOUNT_FILE` to the secured path of a Firebase service-account JSON before starting the API. Do not commit that credential file.
