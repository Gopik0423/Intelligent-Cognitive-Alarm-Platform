---
noteId: "90d65310788311f1b5ae91e0ae14354a"
tags: []

---

# Intelligent Cognitive Alarm Platform

## Overview

The Intelligent Cognitive Alarm Platform is an AI-powered smart alarm system that helps users wake up on time using cognitive challenges, analytics, and personalized recommendations.

## Features

- JWT Authentication & OAuth2 Login
- User Profile & Habit Management
- Smart Alarm Management
- AI-powered Cognitive Challenges
- Wake-up Verification
- Anti-Snooze Mechanism
- Performance Tracking
- Analytics
- Recommendation System
- Swagger API Documentation

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Google Gemini AI
- Docker

## System Architecture

```text
+---------+
|  User   |
+----+----+
     |
     v
+------------+
|  Frontend  |
+-----+------+
      |
      v
+----------------------+
|   FastAPI Backend    |
+-----+------+---------+
      |      |
      |      |
      v      v
 Gemini AI  PostgreSQL
```

## UML Use Case Diagram

```text
                +------+
                | User |
                +--+---+
                   |
   ---------------------------------------
   |       |       |       |             |
   v       v       v       v             v
 Login  Manage  Set Alarm  Solve    View Analytics
         Profile            Challenge   & Reports
```

## Project Modules

- Authentication
- User Management
- Alarm Management
- Cognitive Challenge Engine
- Wake-up Verification
- Performance Tracking
- Analytics
- Recommendation System
- Alarm scheduler, anti-snooze workflow, local/FCM notification integration

See [the alarm user guide](ALARM_USER_GUIDE.md) for the end-to-end trigger, challenge, snooze, and Firebase setup flow.
Use the [final demo runbook](FINAL_DEMO.md) for the presentation sequence.
