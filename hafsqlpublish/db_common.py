# encoding = 'utf-8'
import os

from haf.apihelper import Ids, Response, Request
from haf.case import HttpApiCase
from haf.common.database import MysqlTool, SQLConfig
from haf.common.log import Log
from haf.result import EndResult, Summary, Detail, HttpApiResult, AppResult
from hafsqlpublish.createhaf import *

logger = Log.getLogger(__name__)
import traceback

rb = True


class DBMain(object):
    def __init__(self, id, name, begin_time, end_time, duration_time, passed, failed, skip, error, suite_name):
        self.id = id if id is not None else ''
        self.name = name if name is not None else ''
        self.begin_time = begin_time if begin_time is not None else ''
        self.end_time = end_time if end_time is not None else ''
        self.duration_time = duration_time if duration_time is not None else ''
        self.passed = passed if passed is not None else ''
        self.failed = failed if failed is not None else ''
        self.skip = skip if skip is not None else ''
        self.error = error if error is not None else ''
        self.suite_name = suite_name if suite_name is not None else ''


class DBSuite(object):
    def __init__(self, id, main_id, suite_name):
        self.id = id if id is not None else ''
        self.main_id = main_id if main_id is not None else ''
        self.suite_name = suite_name if suite_name is not None else ''


class DBSummary(object):
    def __init__(self, id, name, passed, failed, skip, error, all, base_url, begin_time, end_time, duration_time,
                 suite_id):
        self.id = id if id is not None else ''
        self.name = name if name is not None else ''
        self.passed = passed if passed is not None else ''
        self.failed = failed if failed is not None else ''
        self.skip = skip if skip is not None else ''
        self.error = error if error is not None else ''
        self.all = all if all is not None else ''
        self.base_url = base_url if base_url is not None else ''
        self.begin_time = begin_time if begin_time is not None else ''
        self.end_time = end_time if end_time is not None else ''
        self.duration_time = duration_time if duration_time is not None else ''
        self.suite_id = suite_id if suite_id is not None else ''


class SQLPublish(object):
    def __init__(self):
        pass
    
    def insert_main(self, db_main: DBMain):
        sql_sc = [
            f"""insert into main (`name`, begin_time, end_time, duration_time, passed, failed, skip, error, suite_name) 
                    values ('{db_main.name}', '{db_main.begin_time}', '{db_main.end_time}', '{db_main.duration_time}', '{db_main.passed}', '{db_main.failed}', '{db_main.skip}', '{db_main.error}', '{db_main.suite_name}'); """,
            f"select @@IDENTITY AS Id"
        ]
        return sql_sc

    def insert_suite(self, db_suite: DBSuite):
        sql_sc = [
            f"""insert into suite (main_id, suite_name)
                    values ('{db_suite.main_id}', '{db_suite.suite_name}');""",
            f" SELECT @@IDENTITY AS Id "
        ]
        return sql_sc

    def insert_summary(self, db_summary: DBSummary):
        sql_sc = [
            f"""insert into summary (`name`, passed, failed, skip, error, `all`, base_url, begin_time, end_time, duration_time, suite_id)
                    values ('{db_summary.name}', '{db_summary.passed}', '{db_summary.failed}', '{db_summary.skip}', '{db_summary.error}', '{db_summary.all}', '{db_summary.base_url}', '{db_summary.begin_time}', '{db_summary.end_time}', '{db_summary.duration_time}', '{db_summary.suite_id}');""",
            f" SELECT @@IDENTITY AS Id"]
        return sql_sc
