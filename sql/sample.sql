CREATE SCHEMA IF NOT EXISTS sample;


CREATE TABLE IF NOT EXISTS sample.interest (
  id         serial primary key,
  user_id    varchar(21)  not null,
  created_at timestamp    not null default current_timestamp,
  deleted_at timestamp,
  topic      varchar(100) not null,
  category   varchar(50)  not null,
  title      varchar(100) not null,
  body       text         not null,
  action_url text
);


DO $$
  BEGIN
    FOR i IN 1..1000 LOOP
      INSERT INTO sample.interest (
        user_id, created_at, deleted_at, topic, category, title, body
      )
      VALUES
        (
          'user_' || floor(random() * 20),
          now() - (random() * (interval '365 days')),
          case when (random() < 0.1) then now() - (random() * (interval '365 days')) else null end,
          'topic_' || floor(random() * 5),
          'category_' || floor(random() * 3),
          'title_' || random(),
          'body_' || random()
        );
    END LOOP;
  END
$$;
