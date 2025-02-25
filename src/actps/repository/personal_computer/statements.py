from sqlalchemy import text


insert_pc = text("""
    insert into personal_computer(
        "ip_address",
        "hostname",
        "router_id",
        "created_at"
    ) values (
        :ip_address,
        :hostname,
        :router_id,
        :created_at
    ) returning id
""")

select_pc = text("""
    select 
        id,
        ip_address,
        hostname,
        router_id,
        created_at
    from personal_computer
""")

select_pc_by_id = text("""
    select 
        id,
        ip_address,
        hostname,
        router_id,
        created_at
    from personal_computer where id=:id
""")

select_pc_by_hostname = text("""
    select 
        id,
        ip_address,
        hostname,
        router_id,
        created_at
    from personal_computer where hostname=:hostname
""")

update_pc = text("""
    update personal_computer
    set 
        ip_address=:ip_address,
        hostname=:hostname,
        router_id=:router_id
    where id=:id
""")

delete_pc = text("""
    delete from personal_computer where id=:id
""")

