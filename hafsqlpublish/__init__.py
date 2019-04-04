from hafsqlpublish.publish import Publish
import haf


@haf.hookimpl
def add_option(parse):
    """Here the caller expects us to return a list."""
    parse.add_argument("--sql-publish", "-sp", dest="sql_publish", default=False, type=bool,
                                     help="sql publish or not")
    parse.add_argument("--sql-publish-db", "-sp_db", dest="sql_publish_db", type=str, default="",
                                     help="sql publish db config, format like : host:port@username:password@database)")
                                             
    return parse


@haf.hookimpl
def publish_to_sql(args, results):
    if hasattr(args, 'sql_publish') and args.sql_publish:
        if isinstance(args.sql_publish_db, str):
            from haf.common.database import SQLConfig
            sql_config = SQLConfig()
            hp, up, db = args.sql_publish_db.split('@')
            host, port = hp.split(':')
            username, password = up.split(':')
            sc_dict = {
                "host": host, "port": int(port), "username": username, "password": password, "id":0, "sql_name": "haf-publish", "protocol": "mysql", "database": db
            }
            sql_config.constructor(sc_dict)
            args.sql_publish_db = sql_config
    publish = args.sql_publish if hasattr(args, 'sql_publish') else False
    config = args.sql_publish_db if hasattr(args, 'sql_publish_db') else None
    if publish and config:
        publish = Publish(config)
        publish.publish_result(results)