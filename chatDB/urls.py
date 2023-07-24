from chatDB import views

urls = [
    (r"/connection_db", views.connection_db),
    (r"/get_tables", views.get_tables_by_database),
    (r"/get_database_conf", views.get_database_conf),
    (r"/execute_sql", views.execute_sql),
]