-- =============================================================================
-- CodeForge Database Schema  (Step 3)
-- =============================================================================
-- Source of truth: ERD entities (USER, PROBLEMS, REVISION, ACTIVITY, TOPIC,
--                               ProblemTopic) and repository SQL queries.
-- Execution order: parents before children (FK dependency order).
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 1. USER
--    Single-user desktop application. "USER" is a reserved word in PostgreSQL
--    so the table name is double-quoted throughout.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "USER" (
    user_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

-- ---------------------------------------------------------------------------
-- 2. PROBLEMS
--    Platform + question-number pair must be unique (used by
--    get_problem_by_platform_and_question_number in ProblemRepository).
--    difficulty is constrained to the three values validated by ProblemService.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS PROBLEMS (
    problem_id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    platform             VARCHAR(100) NOT NULL,
    platform_question_no INTEGER      NOT NULL,
    title                VARCHAR(255) NOT NULL,
    difficulty           VARCHAR(10)  NOT NULL
                             CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
    problem_url          VARCHAR(500) NOT NULL,
    CONSTRAINT uq_problems_platform_qno UNIQUE (platform, platform_question_no)
);

-- ---------------------------------------------------------------------------
-- 3. REVISION
--    Each revision row belongs to an existing problem.
--    revision_type is a free-text label (e.g. "Quick", "Full") — not
--    constrained to an enum because RevisionService accepts any non-empty string.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS REVISION (
    revision_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    problem_id    INTEGER     NOT NULL REFERENCES PROBLEMS (problem_id)
                                  ON DELETE CASCADE,
    revision_date DATE        NOT NULL,
    revision_type VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------------------------
-- 4. TOPIC
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS TOPIC (
    topic_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    topic_name VARCHAR(100) NOT NULL UNIQUE
);

-- ---------------------------------------------------------------------------
-- 5. ProblemTopic  (associative / join table — many-to-many)
--    Composite PK as documented in TopicRepository and ERD.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ProblemTopic (
    problem_id INTEGER NOT NULL REFERENCES PROBLEMS (problem_id) ON DELETE CASCADE,
    topic_id   INTEGER NOT NULL REFERENCES TOPIC    (topic_id)   ON DELETE CASCADE,
    CONSTRAINT pk_problemtopic PRIMARY KEY (problem_id, topic_id)
);

-- ---------------------------------------------------------------------------
-- 6. ACTIVITY
--    activity_type is restricted to the two values produced by ActivityService.
--    ON DELETE CASCADE on problem_id so that deleting a problem also removes
--    its activity history (consistent with the single-user design).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ACTIVITY (
    activity_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id       INTEGER     NOT NULL REFERENCES "USER" (user_id),
    problem_id    INTEGER     NOT NULL REFERENCES PROBLEMS (problem_id)
                                  ON DELETE CASCADE,
    activity_date DATE        NOT NULL,
    activity_type VARCHAR(10) NOT NULL
                      CHECK (activity_type IN ('New', 'Revision'))
);

-- =============================================================================
-- Seed Data
-- =============================================================================
-- Minimum required: one USER row (user_id = 1) so that the single-user
-- activity design (user_id = 1 hard-coded in the application layer) works.
-- INSERT … ON CONFLICT DO NOTHING is idempotent — safe to re-run.
-- =============================================================================
INSERT INTO "USER" OVERRIDING SYSTEM VALUE
VALUES (1)
ON CONFLICT (user_id) DO NOTHING;
