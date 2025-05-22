from sqlalchemy import text


insert_warning = text("""
    insert into warning(
        "hostname",
        "type",
        "message",
        "created_at"
    ) values (
        :hostname,
        :type,
        :message,
        :created_at
    ) returning id
""")

select_warning = text("""
    select 
        id,
        hostname,
        type,
        message,
        created_at
    from warning
""")

select_warning_by_id = text("""
    select 
        id,
        hostname,
        type,
        message,
        created_at
    from warning
    where id = :id
""")

update_warning = text("""
    update warning
    set 
        hostname = :hostname,
        type = :type,
        message = :message,
        created_at = :created_at
    where id = :id
""")

delete_warning = text("""
    delete from warning where id = :id
""")
