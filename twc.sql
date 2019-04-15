create schema twc;

create table twc.client(
    id serial primary key,
    login text not null,
    access_token text not null,
    refresh_token text not null,
    expires_in integer not null,
    create_at timestamp not null default now()
);

create table twc.image(
    id serial primary key,
    filepath text not null,
    likecount integer not null default 0,
    dislikecount integer not null default 0,
    client_id integer not null references twc.client(id),
    create_at timestamp not null default now()
);

create table twc.image_like(
    id serial primary key,
    image_id integer not null references twc.image(id),
    client_id integer not null references twc.client(id),
    value boolean not null,
    create_at timestamp not null default now()
);

create or replace function on_image_like_after_insert()
returns trigger as $$
begin
    if NEW.value then
        update twc.image set
            likecount = likecount + 1
        where id=NEW.image_id;
    else
        update twc.image set
            dislikecount = dislikecount + 1
        where id=NEW.image_id;
    end if;

    return NEW;
end;
$$ language plpgsql;

create trigger image_like_after_insert_triger before insert on twc.image_like
    for each row execute procedure on_image_like_after_insert();

create or replace function on_image_like_after_delete()
returns trigger as $$
begin
    if OLD.value then
        update twc.image set
            likecount = likecount - 1
        where id=OLD.image_id;
    else
        update twc.image set
            dislikecount = dislikecount - 1
        where id=OLD.image_id;
    end if;

    return OLD;
end;
$$ language plpgsql;

create trigger image_like_before_delete_triger before delete on twc.image_like
  for each row execute procedure on_image_like_after_delete();