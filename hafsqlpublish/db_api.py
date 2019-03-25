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


class DBAPIDetail(object):
    def __init__(self, id, case_name, result_check_response, result_check_sql_response, run_error, result, begin_time,
                 end_time, log_dir, runner):
        self.id = id if id is not None else ''
        self.case_name = case_name if case_name is not None else ''
        self.result_check_response = result_check_response if result_check_response is not None else ''
        self.result_check_sql_response = result_check_sql_response if result_check_sql_response is not None else ''
        self.run_error = run_error if run_error is not None else ''
        self.result = result if result is not None else ''
        self.begin_time = begin_time if begin_time is not None else ''
        self.end_time = end_time if end_time is not None else ''
        self.log_dir = log_dir if log_dir is not None else ''
        self.runner = runner if runner is not None else ''


class DBAPICase(object):
    def __init__(self, id, ids_id, run, dependent, bench_name, request_id, response_id, expect_id, sqlinfo_id, type,
                 detail_id, suite_id):
        self.id = id if id is not None else ''
        self.ids_id = ids_id if ids_id is not None else ''
        self.run = run if run is not None else ''
        self.dependent = dependent if dependent is not None else ''
        self.bench_name = bench_name if bench_name is not None else ''
        self.request_id = request_id if request_id is not None else ''
        self.response_id = response_id if response_id is not None else ''
        self.expect_id = expect_id if expect_id is not None else ''
        self.sqlinfo_id = sqlinfo_id if sqlinfo_id is not None else ''
        self.type = type if type is not None else ''
        self.detail_id = detail_id if detail_id is not None else ''
        self.suite_id = suite_id if suite_id is not None else ''


class DBAPICaseExpect(object):
    def __init__(self, id, response_id, sql_check_func, sql_response_reust):
        self.id = id if id is not None is not None else ''
        self.response_id = response_id if response_id is not None else ''
        self.sql_check_func = sql_check_func if sql_check_func is not None else ''
        self.sql_response_result = sql_response_reust if sql_response_reust is not None else ''


class DBAPICaseIds(object):
    def __init__(self, id, case_id, case_sub_id, case_name, case_api_name):
        self.id = id if id is not None else ''
        self.case_id = case_id if case_id is not None else ''
        self.case_sub_id = case_sub_id if case_sub_id is not None else ''
        self.case_name = case_name if case_name is not None else ''
        self.case_api_name = case_api_name if case_api_name is not None else ''


class DBAPICaseRequest(object):
    def __init__(self, id, header, data, url, method, protocol, host_port):
        self.id = id if id is not None else ''
        self.header = header if header is not None else ''
        self.data = data if data is not None else ''
        self.url = url if url is not None else ''
        self.method = method if method is not None else ''
        self.protocol = protocol if protocol is not None else ''
        self.host_port = host_port if host_port is not None else ''


class DBAPICaseResponse(object):
    def __init__(self, id, header, body, code):
        self.id = id if id is not None else ''
        self.header = header if header is not None else ''
        self.body = body if body is not None else ''
        self.code = code if code is not None else ''


class DBAPICaseSqlinfo(object):
    def __init__(self, id, scripts_id, config_id, check_list_id):
        self.id = id if id is not None else ''
        self.scripts_id = scripts_id if scripts_id is not None else ''
        self.config_id = config_id if config_id is not None else ''
        self.check_list_id = check_list_id if check_list_id is not None else ''


class DBAPICaseSqlinfoChecklist(object):
    def __init__(self, id, sql_response):
        self.id = id if id is not None else ''
        self.sql_response = sql_response if sql_response is not None else ''


class DBAPICaseSqlinfoScript(object):
    def __init__(self, id, sql_response):
        self.id = id if id is not None else ''
        self.sql_response = sql_response if sql_response is not None else ''


class DBAPICaseSqlinfoConfig(object):
    def __init__(self, id, host, port, type, username, password):
        self.id = id if id is not None else ''
        self.host = host if host is not None else ''
        self.port = port if port is not None else ''
        self.type = type if type is not None else ''
        self.username = username if username is not None else ''
        self.password = password if password is not None else ''


class SQLAPIPublish(object):
    def __init__(self):
        pass

    def insert_api_detail(self, db_detail: DBAPIDetail):
        if isinstance(db_detail.result_check_response, list) or isinstance(db_detail.result_check_response, tuple):
            result_check_response = ";".join([str(x) for x in db_detail.result_check_response])
        else:
            result_check_response = str(db_detail.result_check_response)
        if isinstance(db_detail.result_check_sql_response, list) or isinstance(db_detail.result_check_sql_response,
                                                                               tuple):
            result_check_sql_response = ";".join([str(x) for x in db_detail.result_check_sql_response])
        else:
            result_check_sql_response = str(db_detail.result_check_sql_response)
        result_check_response = result_check_response.replace(r'\\', r'/').replace('"', r'\"').replace("'", r'\'')
        result_check_sql_response = result_check_sql_response.replace(r'\\', r'/').replace('"', r'\"').replace("'", r'\'')
        run_error = str(db_detail.run_error).replace(r'\\', r'\/').replace('"', r'\"').replace("'", r'\'')
        sql_sc = [
            f"""insert into api_detail ( case_name, result_check_response, result_check_sql_response, run_error, result, begin_time, end_time, log_dir, runner)
                    values ('{db_detail.case_name}', '{result_check_response}', '{result_check_sql_response}',
                            '{run_error}', '{db_detail.result}', '{db_detail.begin_time}', '{db_detail.end_time}', '{db_detail.log_dir}', '{db_detail.runner}');""",
            f" SELECT @@IDENTITY AS Id "]
        return sql_sc

    def insert_api_case(self, db_case: DBAPICase):
        if isinstance(db_case.dependent, list):
            dependent = ";".join([str(x) for x in db_case.dependent])
        else:
            dependent = str(db_case.dependent)
        sql_sc = [
            f"""insert into api_case (ids_id, `run`, dependent, bench_name, request_id, response_id, expect_id, sqlinfo_id, `type`, suite_id, detail_id) 
                    values ('{db_case.ids_id}', '{db_case.run}', '{dependent}', '{db_case.bench_name}', '{db_case.request_id}', '{db_case.response_id}', '{db_case.expect_id}', '{db_case.sqlinfo_id}', '{db_case.type}', '{db_case.suite_id}', '{db_case.detail_id}'); """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_api_caseexpect(self, db_case_expect: DBAPICaseExpect):
        if isinstance(db_case_expect.sql_check_func, list) or isinstance(db_case_expect.sql_check_func, tuple):
            check_func = ",".join([str(x) for x in db_case_expect.sql_check_func])
        else:
            check_func = 'null'
        if isinstance(db_case_expect.sql_response_result, list) or isinstance(db_case_expect.sql_response_result, tuple):
            sql_response_result = ",".join([str(x) for x in db_case_expect.sql_response_result])
        else:
            sql_response_result = str(db_case_expect.sql_response_result)
        sql_response_result = sql_response_result.replace('\\', r'\/').replace('"', r'\"').replace("'", r'\'')
        sql_sc = [
            f"""insert into api_case_expect (response_id, sql_check_func, sql_response_result)
                    values ('{db_case_expect.response_id}', '{check_func}', '{sql_response_result}');""",
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_api_case_ids(self, db_caseid: DBAPICaseIds):
        sql_sc = [
            f"""insert into api_case_ids (case_id, case_sub_id, case_name, case_api_name) 
                    values ('{db_caseid.case_id}', '{db_caseid.case_sub_id}', '{db_caseid.case_name}', '{db_caseid.case_api_name}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_api_case_request(self, db_caserequest: DBAPICaseRequest):
        header = str(db_caserequest.header).replace('\\', r'/').replace('"', r'\"').replace("'", r'\'')
        data = str(db_caserequest.data).replace('\\', r'/').replace('"', r'\"').replace("'", r'\'')
        sql_sc = [
            f"""insert into api_case_request (`header`, `data`, `url`, `method`, `protocol`, `host_port`) 
                    values ('{header}', '{data}', '{db_caserequest.url}', '{db_caserequest.method}', '{db_caserequest.protocol}', '{db_caserequest.host_port}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_api_case_response(self, db_caseresponse: DBAPICaseResponse):
        header = str(db_caseresponse.header).replace('\\', r'/').replace('"', r'\"').replace("'", r'\'')
        body = str(db_caseresponse.body).replace('\\', r'/').replace('"', r'\"').replace("'", r'\'')
        sql_sc = [
            f"""insert into api_case_response (`header`, `body`, `code`) 
                    values ('{header}', '{body}', '{db_caseresponse.code}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_api_case_sqlinfo(self, db_casesqlinfo: DBAPICaseSqlinfo):
        sql_sc = [
            f"""insert into api_case_sqlinfo (scripts_id, config_id, check_list_id)
                    values ('{db_casesqlinfo.scripts_id}', '{db_casesqlinfo.config_id}', '{db_casesqlinfo.check_list_id}'); """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_api_case_sqlinfochecklist(self, db_casesqlinfo_checklist: DBAPICaseSqlinfoChecklist):
        if isinstance(db_casesqlinfo_checklist.sql_response, list) or isinstance(db_casesqlinfo_checklist.sql_response,
                                                                                 tuple):
            sql_response_checklist = ";".join([str(x) for x in db_casesqlinfo_checklist.sql_response])
        else:
            sql_response_checklist = str(db_casesqlinfo_checklist.sql_response)

        sql_response_checklist = sql_response_checklist.replace(r'\\', r'/').replace('"', r'\"').replace("'", r'\'')
        sql_sc = [
            f"""insert into api_case_sqlinfo_checklist (sql_response) values ('{sql_response_checklist}');""",
            f"SELECT @@IDENTITY AS Id "]
        return sql_sc

    def insert_api_case_sqlinfoscript(self, db_casesqlinfo_script: DBAPICaseSqlinfoScript):
        if isinstance(db_casesqlinfo_script.sql_response, list) or isinstance(db_casesqlinfo_script.sql_response,
                                                                              tuple):
            sql_response_script = ";".join([str(x) for x in db_casesqlinfo_script.sql_response])
        else:
            sql_response_script = str(db_casesqlinfo_script.sql_response)
        sql_sc = [
            f"""insert into api_case_sqlinfo_script (sql_response) values ('{sql_response_script}');""",
            f" SELECT @@IDENTITY AS Id "]
        return sql_sc

    def insert_api_case_sqlinfoconfig(self, db_casesqlinfo_config: DBAPICaseSqlinfoConfig):
        sql_sc = [
            f"""insert into api_case_sqlinfo_config (`host`, `port`, `type`, `username`, `password`)
                    values ('{db_casesqlinfo_config.host}', '{db_casesqlinfo_config.port}', '{db_casesqlinfo_config.type}', '{db_casesqlinfo_config.username}', '{db_casesqlinfo_config.password}')""",
            f" SELECT @@IDENTITY AS Id "]
        return sql_sc
