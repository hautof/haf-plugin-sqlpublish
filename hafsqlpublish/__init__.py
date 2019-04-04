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
def publish_to_sql(publish, config, results):
    if publish:
        publish = Publish(config)
        publish.publish_result(results)