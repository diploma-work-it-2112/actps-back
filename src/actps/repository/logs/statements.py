insert_package_log = text("""
    insert into package_log(
        "message",
        "ip_source",
        "ip_destination",
        "mac_source",
        "mac_destination",
        "port_source",
        "port_destination",
        "web_host_name",
        "pc_id",
        "time",
        "created_at"
    ) values (
        :message,
        :ip_source,
        :ip_destination,
        :mac_source,
        :mac_destination,
        :port_source,
        :port_destination,
        :web_host_name,
        :pc_id,
        :time,
        :created_at
    ) returning id
""")

select_package_log = text("""
    select 
        id,
        message,
        ip_source,
        ip_destination,
        mac_source,
        mac_destination,
        port_source,
        port_destination,
        web_host_name,
        pc_id,
        time,
        created_at
    from package_log
""")

select_package_log_by_id = text("""
    select 
        id,
        message,
        ip_source,
        ip_destination,
        mac_source,
        mac_destination,
        port_source,
        port_destination,
        web_host_name,
        pc_id,
        time,
        created_at
    from package_log
    where id=:id
""")

select_package_log_by_pc_id = text("""
    select 
        id,
        message,
        ip_source,
        ip_destination,
        mac_source,
        mac_destination,
        port_source,
        port_destination,
        web_host_name,
        pc_id,
        time,
        created_at
    from package_log
    where pc_id = :pc_id
""")


update_package_log = text("""
    update package_log
    set 
        message=:message,
        ip_source=:ip_source,
        ip_destination=:ip_destination,
        mac_source=:mac_source,
        mac_destination=:mac_destination,
        port_source=:port_source,
        port_destination=:port_destination,
        web_host_name=:web_host_name,
        pc_id=:pc_id,
        time=:time,
        created_at=:created_at
    where id=:id
""")

delete_package_log = text("""
    delete from package_log where id=:id
""")

