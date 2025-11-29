# YKS Private Tutoring Platform – Specification (MVP)

## 1. Product Overview

A platform that matches **YKS students** with **tutors** in **Istanbul** based on:

- Subject (TYT / AYT)
- Location (district-based, later fine-grained)
- Availability (common free time slots)
- Budget

The system:

- Manages **student and tutor profiles**
- Stores **availability slots**
- Creates **lesson requests & confirmed lessons**
- Keeps **lesson logs** (what was taught, when, where)
- Works on **mobile (iOS/Android)** and **web**

MVP focus: **core matching + scheduling + logging**. Payments, complex analytics, etc. can be added later.

---

## 2. User Roles

### 2.1 Student (and Parent acting as Student)

- Create account and profile
- Define current grade and YKS goals
- Define preferred subjects and lesson mode (online / in-person)
- Set home district (Istanbul) and optional neighborhood
- Set weekly availability
- Create lesson requests (e.g. “2x2 hours TYT Math per week”)
- Receive tutor suggestions (ranked list)
- Book lessons in available slots
- View upcoming and past lessons
- View lesson logs and progress

### 2.2 Tutor

- Create account and profile
- Define subjects and levels (11, 12, graduate)
- Set experience info (years, education, short bio)
- Set hourly rate
- Define **lesson mode**:
  - Student’s place
  - Tutor’s place
  - Common place (library, cafe, etc.)
  - Online
- Set base location (district) and districts they can travel to
- Set weekly availability slots
- Receive lesson requests / booking requests
- Confirm or propose new time
- Record lesson logs after each lesson
- See personal schedule and basic statistics

### 2.3 Admin

- View and manage all users
- Approve / reject tutors
- See all lessons and lesson logs
- Handle reports / complaints
- (Later) Manage payments, payouts, etc.

---

## 3. Key Use Cases (MVP)

1. **Student onboarding**
   - Sign up → verify email → create student profile
   - Fill:
     - Grade (11 / 12 / graduate)
     - Exam type: TYT, AYT (or both)
     - Target score / rank (optional)
     - Subjects needing support
     - Location: Istanbul district (+ optional neighborhood)
     - Lesson mode preference (online / in-person / both)
     - Weekly availability (time slots)

2. **Tutor onboarding**
   - Sign up → verify email → create tutor profile
   - Fill:
     - Education, university, department
     - Experience (years, short bio)
     - Subjects (Math, Geometry, Physics, Chemistry, Turkish, Literature, etc.)
     - Levels (11, 12, graduate)
     - Hourly rate (TRY / hour)
     - Base district + list of districts they can travel to
     - Lesson modes (student home / tutor home / common place / online)
     - Weekly availability (time slots)
   - Submit required documents (ID, student certificate, diploma)
   - Wait for admin approval (MVP: status field)

3. **Student requests a tutor**
   - Student creates a **LessonRequest**:
     - Subjects (one or multiple)
     - Weekly hours (e.g. 2x2 = 4 hours)
     - Budget range (min/max)
     - Preferred lesson mode
     - Preferred days/time ranges (optional if profile already has)

4. **System suggests tutors**
   - System matches student with tutors:
     - Same subject & level
     - Compatible lesson mode
     - Same or compatible district
     - Budget fit
     - Overlapping availability slots
   - Returns sorted list of tutors with a **match score**
   - For each tutor, system suggests **specific free slots** for first lesson

5. **Lesson booking**
   - Student selects a tutor and a suggested slot → sends booking request
   - Tutor:
     - Accepts → lesson becomes **confirmed**
     - Rejects → student notified
     - Proposes new time → student can accept/reject
   - Notifications (MVP: email + in-app; later push notifications)

6. **Lesson execution & logging**
   - Lesson happens (online / in-person)
   - After lesson:
     - Tutor fills **LessonLog**:
       - Topics covered
       - Homework given
       - Student performance notes
     - Student can see the log in their history

7. **Rating (basic, optional for early MVP)**
   - After lesson, student can rate tutor (1–5) and leave short text feedback.
   - Rating contributes to tutor’s overall score.

---

## 4. Non-Functional Requirements (MVP-Level)

- **Platforms**:
  - Backend: Flask + PostgreSQL
  - Mobile: React Native + Expo (iOS & Android)
  - Web: basic (React Native Web or later separate web client)
- **Authentication**:
  - JWT-based auth (access + optional refresh)
- **Security**:
  - Password hashing (e.g. Werkzeug)
  - Role-based access control
- **Performance**:
  - MVP scale: up to a few hundred users without optimization
- **Localization**:
  - Initial language: Turkish (UI)  
  - Internal names (entities, fields, endpoints): English

---

## 5. Data Model (MVP)

### 5.1 User

- `id` (uuid)
- `email` (unique)
- `password_hash`
- `role` (`student` | `tutor` | `admin`)
- `is_active` (bool)
- `created_at`
- `updated_at`

Relationships:
- One-to-one with `StudentProfile` or `TutorProfile` (depending on role)

---

### 5.2 StudentProfile

- `id`
- `user_id` (FK → User)
- `full_name`
- `grade` (`11`, `12`, `graduate`)
- `target_exam` (`TYT`, `AYT`, `BOTH`)
- `target_score` / `target_rank` (optional)
- `city` (default `Istanbul`)
- `district`
- `neighborhood` (optional, free text)
- `preferred_modes` (enum array: `online`, `in_person`, `hybrid`)
- `notes` (optional – free text)

---

### 5.3 TutorProfile

- `id`
- `user_id` (FK → User)
- `full_name`
- `title` (e.g. “Math Teacher”, “Boğaziçi MIS Student”)
- `bio` (short description)
- `education` (university, department)
- `experience_years` (int)
- `hourly_rate` (numeric)
- `base_city` (default `Istanbul`)
- `base_district`
- `lesson_modes` (enum array: `student_home`, `tutor_home`, `common_place`, `online`)
- `teaching_levels` (array: `11`, `12`, `graduate`)
- `status` (`pending`, `approved`, `rejected`)
- `avg_rating` (float, computed)
- `rating_count` (int, computed)

---

### 5.4 Subject

- `id`
- `name` (e.g. `TYT Mathematics`, `AYT Physics`)
- `category` (`TYT`, `AYT`)
- (Optional) `order_index` for listing

---

### 5.5 TutorSubject

Many-to-many between TutorProfile and Subject.

- `id`
- `tutor_id` (FK → TutorProfile)
- `subject_id` (FK → Subject)

---

### 5.6 TutorDistrict

Many-to-many between TutorProfile and districts they can travel to.

- `id`
- `tutor_id` (FK → TutorProfile)
- `district` (string, e.g. `Beşiktaş`, `Kadıköy`)

---

### 5.7 AvailabilitySlot

Represents a recurring weekly time window.

- `id`
- `user_id` (FK → User)
- `day_of_week` (0–6; 0 = Monday)
- `start_time` (time)
- `end_time` (time)

Used for both students and tutors.

---

### 5.8 LessonRequest

Created by a student to define what they need.

- `id`
- `student_id` (FK → StudentProfile)
- `subject_ids` (array of subject IDs)
- `preferred_modes` (enum array)
- `budget_min` (numeric, optional)
- `budget_max` (numeric, optional)
- `weekly_hours` (float, e.g. 4.0)
- `additional_notes` (text)
- `status` (`open`, `matched`, `closed`, `cancelled`)
- `created_at`
- `updated_at`

---

### 5.9 Lesson

A specific scheduled lesson between a student and a tutor.

- `id`
- `tutor_id` (FK → TutorProfile)
- `student_id` (FK → StudentProfile)
- `subject_id` (FK → Subject)
- `start_datetime`
- `end_datetime`
- `mode` (`online`, `student_home`, `tutor_home`, `common_place`)
- `location_description` (string; address or “online link”)
- `status` (`pending`, `confirmed`, `completed`, `cancelled`)
- `created_at`
- `updated_at`

---

### 5.10 LessonLog

Details for a completed lesson.

- `id`
- `lesson_id` (FK → Lesson)
- `topics_covered` (text)
- `homework_assigned` (text, optional)
- `tutor_notes` (text, optional)
- `created_at`

---

### 5.11 Review (optional for early MVP)

- `id`
- `lesson_id` (FK → Lesson)
- `student_id` (FK → StudentProfile)
- `tutor_id` (FK → TutorProfile)
- `rating` (1–5)
- `comment` (text, optional)
- `created_at`

---

## 6. Matching Logic (MVP)

The matching algorithm runs when:

- A student creates/updates a `LessonRequest`  
  or
- A student explicitly requests matches from a screen.

Steps:

1. **Load student context**
   - `StudentProfile`
   - Student `AvailabilitySlot`s
   - `LessonRequest` details

2. **Filter tutors**
   - Tutor is `approved`
   - Tutor teaches at least one requested subject
   - Tutor supports at least one of the request’s `preferred_modes`
   - If in-person is required:
     - Tutor’s `TutorDistrict` includes the student’s district, **or**
     - Student and tutor share base district

3. **Check availability overlap**
   - For each tutor:
     - Compare student’s `AvailabilitySlot`s with tutor’s `AvailabilitySlot`s
     - If at least one overlapping slot exists → candidate

4. **Score tutors**
   Example scoring:
   - Subject match: +50
   - Same district (base_district): +30
   - TutorDistrict includes student district: +20
   - Budget fit:
     - If tutor.hourly_rate within [budget_min, budget_max] → +20
     - Else if slightly outside → +5
   - Overlapping availability → +20
   - Tutor avg_rating:
     - rating ≥ 4.5 → +10
     - rating ≥ 4.0 → +5

5. **Return top candidates**
   - Sort by `score` DESC
   - Limit: top 10
   - For each tutor, compute first 2–3 suggested lesson slots using overlapping availability.

---

## 7. API Overview (MVP – High Level)

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Profiles

- `GET /students/me`
- `POST /students/me` (create/update)
- `GET /tutors/me`
- `POST /tutors/me` (create/update)

### Availability

- `GET /availability/me`
- `POST /availability` (create slot)
- `PUT /availability/{id}`
- `DELETE /availability/{id}`

### Lesson Requests & Matching

- `POST /lesson-requests`
- `GET /lesson-requests/me`
- `GET /lesson-requests/{id}`
- `POST /lesson-requests/{id}/match`  
  → returns list of tutor candidates + proposed slots

### Lessons

- `POST /lessons` (create booking request)
- `GET /lessons/me` (student: my lessons, tutor: my lessons)
- `PATCH /lessons/{id}` (change status: confirm / cancel)

### Lesson Logs

- `POST /lessons/{id}/log`
- `GET /lessons/{id}/log`

### Reviews (optional MVP+1)

- `POST /lessons/{id}/review`
- `GET /tutors/{id}/reviews`

---

## 8. Future Extensions (out of MVP scope)

- Online payment and commission system
- Real-time chat between student and tutor
- Detailed analytics and progress dashboards
- Route optimization / travel time estimation via Maps API
- Group lessons or small study groups
- School-specific packages (e.g. agreements with schools or dershanes)

---
