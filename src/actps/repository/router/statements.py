from sqlalchemy import text


insert_router = text("""
    insert into router(
        "model_name",
        "ip_address",
        "hostname",
        "created_at",
        "color",
        "group_name"
    ) values (
        :model_name,
        :ip_address,
        :hostname,
        :created_at,
        :color,
        :group_name
    ) returning id
""")

select_router = text("""
    SELECT
        r.id AS router_id,
        r.model_name,
        r.ip_address AS router_ip,
        r.hostname AS router_hostname,
        r.created_at AS router_created_at,
        r.color AS router_color,
        r.group_name AS router_group_name,
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
    FROM router r
""")

select_router_by_id = text("""
    SELECT
        r.id AS router_id,
        r.model_name,
        r.ip_address AS router_ip,
        r.hostname AS router_hostname,
        r.created_at AS router_created_at,
        r.color AS router_color,
        r.group_name AS router_group_name,
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
    FROM router r where r.id=:id
""")

select_router_by_ip = text("""
    SELECT
        r.id AS router_id,
        r.model_name,
        r.ip_address AS router_ip,
        r.hostname AS router_hostname,
        r.created_at AS router_created_at,
        r.color AS router_color,
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

get_last_router = text("""
    SELECT * FROM router ORDER BY id DESC LIMIT 1
""")

