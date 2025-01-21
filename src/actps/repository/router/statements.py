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
        r.id as router_id,
        r.model_name,
        r.ip_address as router_ip_address,
        r.hostname as router_hostname,
        r.created_at as router_created_at,
        pc.id as computer_id,
        pc.ip_address as computer_ip_address,
        pc.hostname as computer_hostname,
        pc.created_at as computer_created_at
    from router r
    inner join personal_computer pc on pc.router_id = r.id
""")

select_router_by_id = text("""
    select 
        r.id as router_id,
        r.model_name,
        r.ip_address as router_ip_address,
        r.hostname as router_hostname,
        r.created_at as router_created_at,
        pc.id as computer_id,
        pc.ip_address as computer_ip_address,
        pc.hostname as computer_hostname,
        pc.created_at as computer_created_at
    from router r
    inner join personal_computer pc on pc.router_id = r.id
    where r.id=:id
""")

select_router_by_ip = text("""
    SELECT
        r.id AS router_id,
        r.model_name,
        r.ip_address AS router_ip,
        r.hostname AS router_hostname,
        r.created_at AS router_created_at,
        (
            SELECT json_agg(
                json_build_object(
                    'computer_id', pc.id,
                    'computer_ip', pc.ip_address,
                    'computer_hostname', pc.hostname,
                    'computer_created_at', pc.created_at
                )
            )
            FROM personal_computer pc
            WHERE pc.router_id = r.id
        ) AS computers
    FROM router r where r.ip_address=:ip
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

