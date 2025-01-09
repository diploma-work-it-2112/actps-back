from sqlalchemy import text


insert_router = text("""
    insert into router(
        "model_name",
        "ip_address",
        "hostname",
        "created_at"
    ) values (
        :model_name,
        :ip_address,
        :hostname,
        :created_at
    ) returning id
""")

select_router = text("""
    select 
        id,
        model_name,
        ip_address,
        hostname,
        created_at
    from router
""")

select_router_by_id = text("""
    select 
        id,
        model_name,
        ip_address,
        hostname,
        created_at
    from router where id=:id
""")

update_router = text("""
    update router
    set 
        model_name=:model_name,
        ip_address=:ip_address,
        hostname=:hostname
    where id=:id
""")

delete_router = text("""
    delete from router where id=:id
""")

