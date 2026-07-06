const express = require('express');
const { query } = require('./db');

const app = express();
const port = process.env.PORT || 4000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'alarm-platform' });
});

app.get('/users', async (req, res) => {
  try {
    const result = await query('SELECT id, name, email, created_at FROM users ORDER BY id');
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/devices', async (req, res) => {
  try {
    const result = await query(
      'SELECT d.id, d.name, d.type, d.status, d.user_id, u.name AS owner_name FROM devices d JOIN users u ON d.user_id = u.id ORDER BY d.id'
    );
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/alarms', async (req, res) => {
  try {
    const result = await query(
      `SELECT a.id, a.title, a.severity, a.trigger_threshold, a.is_active, a.device_id, d.name AS device_name, a.created_at
       FROM alarms a
       JOIN devices d ON a.device_id = d.id
       ORDER BY a.id`
    );
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/alarms', async (req, res) => {
  const { title, severity, trigger_threshold, device_id, is_active } = req.body;
  if (!title || !device_id) {
    return res.status(400).json({ error: 'title and device_id are required' });
  }

  try {
    const result = await query(
      'INSERT INTO alarms (title, severity, trigger_threshold, device_id, is_active) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [title, severity || 'medium', trigger_threshold || 0, device_id, is_active !== false]
    );
    res.status(201).json(result.rows[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

async function waitForDatabase(retries = 20) {
  while (retries > 0) {
    try {
      await query('SELECT 1');
      return;
    } catch (error) {
      retries -= 1;
      console.log('Waiting for database to be ready, retries left:', retries);
      await new Promise((resolve) => setTimeout(resolve, 1500));
    }
  }
  throw new Error('Database connection timed out.');
}

async function start() {
  try {
    await waitForDatabase();
    app.listen(port, () => {
      console.log(`Alarm platform API is running on port ${port}`);
    });
  } catch (error) {
    console.error('Failed to start service:', error.message);
    process.exit(1);
  }
}

start();
