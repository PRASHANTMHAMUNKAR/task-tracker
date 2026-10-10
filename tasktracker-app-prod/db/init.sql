CREATE TABLE IF NOT EXISTS tasks (
    id         SERIAL PRIMARY KEY,
    title      VARCHAR(100) NOT NULL,
    done       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO tasks (title) VALUES
    ('Write the Dockerfiles'),
    ('Write docker-compose.yml'),
    ('Create the GitHub Actions workflow'),
    ('Create the Jenkinsfile');
