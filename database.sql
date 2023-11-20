CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    url_id bigint REFERENCES urls(id),
    status_code int,
    h1 text,
    title text,
    description text,
    created_at timestamp
)