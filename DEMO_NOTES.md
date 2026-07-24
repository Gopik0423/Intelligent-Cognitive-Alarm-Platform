Quick demo script — Intelligent Cognitive Alarm Platform

Prerequisites
- Docker Desktop running on Windows
- Open PowerShell in the project root: C:\Users\janar\OneDrive\Desktop\Intelligent-Cognitive-Alarm-Platform

Start the stack
```powershell
docker-compose up --build -d
```

Ports used (local -> container)
- API: http://localhost:4001 -> container:4000
- Postgres: host 5433 -> container:5432

Health check
```powershell
curl http://localhost:4001/health
# expected: {"status":"ok","service":"alarm-platform"}
```

Useful demo queries
```powershell
# List users
curl http://localhost:4001/users

# List devices
curl http://localhost:4001/devices

# List alarms
curl http://localhost:4001/alarms

# Create a new alarm (replace device_id with an ID from /devices)
curl -X POST http://localhost:4001/alarms -H "Content-Type: application/json" -d '{"title":"Demo Alarm","severity":"low","trigger_threshold":10,"device_id":1}'
```

Show live logs
```powershell
docker-compose logs --tail=200 api
docker-compose logs --tail=200 db
```

Inspect Postgres (inside compose)
```powershell
# open a psql shell as the created DB user
docker-compose exec db psql -U alarm_user -d alarm_platform
# or run a single query
docker-compose exec db psql -U alarm_user -d alarm_platform -c "SELECT id,name,email,created_at FROM users;"
```

Stop the demo
```powershell
docker-compose down
```

Suggested short demo flow (4 minutes)
1. Start Docker and run `docker-compose up --build -d` (30s)
2. Show `curl http://localhost:4001/health` (10s)
3. Show `curl http://localhost:4001/users` and `/devices` to demonstrate seeded data (40s)
4. Create a new alarm with `POST /alarms`, then `GET /alarms` to show it persisted (60s)
5. Tail `docker-compose logs --tail=200 api` to show service startup logs and runtime messages (40s)
6. End and run `docker-compose down` (10s)

Notes
- Host ports were remapped to avoid conflicts: API -> 4001, Postgres -> 5433.
- If a host port is already taken, change the mapping in `docker-compose.yml` under the `ports` section.
