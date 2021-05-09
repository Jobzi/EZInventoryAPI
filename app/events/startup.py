from app.db.postgre_connector import PostgreSqlConnector


def init_database_session(conector_class: 'PostgreSqlConnector') -> None:
    conector_class.init_db_session()
