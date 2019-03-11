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

class DBAPPDetail(object):
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


class DBAPPCase(object):
    def __init__(self, id, ids_id, run, dependent, bench_name, expect_id, sqlinfo_id, type,
                 detail_id, suite_id, caps_id):
        self.id = id if id is not None else ''
        self.ids_id = ids_id if ids_id is not None else ''
        self.run = run if run is not None else ''
        self.dependent = dependent if dependent is not None else ''
        self.bench_name = bench_name if bench_name is not None else ''
        self.expect_id = expect_id if expect_id is not None else ''
        self.sqlinfo_id = sqlinfo_id if sqlinfo_id is not None else ''
        self.type = type if type is not None else ''
        self.detail_id = detail_id if detail_id is not None else ''
        self.suite_id = suite_id if suite_id is not None else ''
        self.caps_id = caps_id if caps_id is not None else ''


class DBAPPCaseExpect(object):
    def __init__(self, id, response_id, sql_check_func, sql_response_reust):
        self.id = id if id is not None is not None else ''
        self.response_id = response_id if response_id is not None else ''
        self.sql_check_func = sql_check_func if sql_check_func is not None else ''
        self.sql_response_result = sql_response_reust if sql_response_reust is not None else ''


class DBAPPCaseIds(object):
    def __init__(self, id, case_id, case_sub_id, case_name, case_app_name):
        self.id = id if id is not None else ''
        self.case_id = case_id if case_id is not None else ''
        self.case_sub_id = case_sub_id if case_sub_id is not None else ''
        self.case_name = case_name if case_name is not None else ''
        self.case_app_name = case_app_name if case_app_name is not None else ''


class DBAPPCaseCaps(object):
    def __init__(self, id, automation_name, platform_name, platform_version, device_name, app_package, app_activity, no_reset):
        self.id = id if id is not None else ''
        self.automation_name = automation_name if automation_name is not None else ''
        self.platform_name = platform_name if platform_name is not None else ''
        self.platform_version = platform_version if platform_version is not None else ''
        self.device_name = device_name if device_name is not None else ''
        self.app_package = app_package if app_package is not None else ''
        self.app_activity = app_activity if app_activity is not None else ''
        self.no_reset = no_reset if no_reset is not None else ''


class DBAPPCaseStage(object):
    def __init__(self, id, stage_id, name, operation, show_try, time_sleep, info, result_id, app_case_id):
        self.id = id if id is not None else ''
        self.stage_id = stage_id if stage_id is not None else ''
        self.name = name if name is not None else ''
        self.operation = operation if operation is not None else ''
        self.show_try = show_try if show_try is not None else ''
        self.time_sleep = time_sleep if time_sleep is not None else ''
        self.info = info if info is not None else ''
        self.result_id = result_id if result_id is not None else ''
        self.app_case_id = app_case_id if app_case_id is not None else ''


class DBAPPCaseStageResult(object):
    def __init__(self, id, result, exception):
        self.id = id if id is not None else ''
        self.result = result if result is not None else ''
        self.exception = exception if exception is not None else ''


class DBAPPCaseStagePath(object):
    def __init__(self, id, stage_id, find_type, find_value):
        self.id = id if id is not None else ''
        self.stage_id = stage_id if stage_id is not None else ''
        self.find_type = find_type if find_type is not None else ''
        self.find_value = find_value if find_value is not None else ''


class DBAPPCaseSqlinfo(object):
    def __init__(self, id, scripts_id, config_id, check_list_id):
        self.id = id if id is not None else ''
        self.scripts_id = scripts_id if scripts_id is not None else ''
        self.config_id = config_id if config_id is not None else ''
        self.check_list_id = check_list_id if check_list_id is not None else ''


class DBAPPCaseSqlinfoChecklist(object):
    def __init__(self, id, sql_response):
        self.id = id if id is not None else ''
        self.sql_response = sql_response if sql_response is not None else ''


class DBAPPCaseSqlinfoScript(object):
    def __init__(self, id, sql_response):
        self.id = id if id is not None else ''
        self.sql_response = sql_response if sql_response is not None else ''


class DBAPPCaseSqlinfoConfig(object):
    def __init__(self, id, host, port, type, username, password):
        self.id = id if id is not None else ''
        self.host = host if host is not None else ''
        self.port = port if port is not None else ''
        self.type = type if type is not None else ''
        self.username = username if username is not None else ''
        self.password = password if password is not None else ''


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


class SQLAPPublish(object):
    def __init__(self):
        pass

    def insert_app_detail(self, db_detail: DBAPPDetail):
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
            f"""insert into app_detail ( case_name, result_check_response, result_check_sql_response, run_error, result, begin_time, end_time, log_dir, runner)
                    values ('{db_detail.case_name}', '{result_check_response}', '{result_check_sql_response}',
                            '{run_error}', '{db_detail.result}', '{db_detail.begin_time}', '{db_detail.end_time}', '{db_detail.log_dir}', '{db_detail.runner}');""",
            f" SELECT @@IDENTITY AS Id "]
        return sql_sc

    def insert_app_case(self, db_case: DBAPPCase):
        if isinstance(db_case.dependent, list):
            dependent = ";".join([str(x) for x in db_case.dependent])
        else:
            dependent = str(db_case.dependent)
        sql_sc = [
            f"""insert into app_case (ids_id, `run`, dependent, bench_name,  request_id, response_id, expect_id, sqlinfo_id, `type`, suite_id, detail_id, caps_id) 
                    values ('{db_case.ids_id}', '{db_case.run}', '{dependent}', '{db_case.bench_name}', '{db_case.request_id}', '{db_case.response_id}', '{db_case.expect_id}', '{db_case.sqlinfo_id}', '{db_case.type}', '{db_case.suite_id}', '{db_case.detail_id}', '{db_case.caps_id}'); """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_caseexpect(self, db_case_expect: DBAPPCaseExpect):
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
            f"""insert into app_case_expect (response_id, sql_check_func, sql_response_result)
                    values ('{db_case_expect.response_id}', '{check_func}', '{sql_response_result}');""",
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_ids(self, db_caseid: DBAPPCaseIds):
        sql_sc = [
            f"""insert into app_case_ids (case_id, case_sub_id, case_name, case_app_name) 
                    values ('{db_caseid.case_id}', '{db_caseid.case_sub_id}', '{db_caseid.case_name}', '{db_caseid.case_app_name}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_caps(self, db_caps: DBAPPCaseCaps):
        sql_sc = [
            f"""insert into app_case_caps (automation_name, platform_name, device_name, app_package, app_activity, no_reset) 
                    values ('{db_caps.automation_name}', '{db_caps.platform_name}', '{db_caps.device_name}', '{db_caps.app_package}', '{db_caps.app_activity}', '{db_caps.no_reset}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_stage_result(self, db_case_stage_result: DBAPPCaseStageResult):
        sql_sc = [
            f"""insert into app_case_stage_result (result, `exception`) 
                    values ('{db_case_stage_result.result}', '{db_case_stage_result.exception}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_stage(self, db_case_stage: DBAPPCaseStage):
        sql_sc = [
            f"""insert into app_case_stage (stage_id, name, operation, show_try, time_sleep, info, result_id, app_case_id) 
                    values ('{db_case_stage.stage_id}', '{db_case_stage.name}', '{db_case_stage.operation}', '{db_case_stage.show_try}', '{db_case_stage.time_sleep}', '{db_case_stage.info}', '{db_case_stage.result_id}', '{db_case_stage.app_case_id}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_stage_path(self, db_case_stage_path: DBAPPCaseStagePath):
        sql_sc = [
            f"""insert into app_case_stage_path (stage_id, find_type, find_value) 
                    values ('{db_case_stage_path.stage_id}', '{db_case_stage_path.find_type}', '{db_case_stage_path.find_value}');""",
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_sqlinfo(self, db_casesqlinfo: DBAPPCaseSqlinfo):
        sql_sc = [
            f"""insert into app_case_sqlinfo (scripts_id, config_id, check_list_id)
                    values ('{db_casesqlinfo.scripts_id}', '{db_casesqlinfo.config_id}', '{db_casesqlinfo.check_list_id}'); """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_sqlinfochecklist(self, db_casesqlinfo_checklist: DBAPPCaseSqlinfoChecklist):
        if isinstance(db_casesqlinfo_checklist.sql_response, list) or isinstance(db_casesqlinfo_checklist.sql_response,
                                                                                 tuple):
            sql_response_checklist = ";".join([str(x) for x in db_casesqlinfo_checklist.sql_response])
        else:
            sql_response_checklist = str(db_casesqlinfo_checklist.sql_response)

        sql_response_checklist = sql_response_checklist.replace(r'\\', r'/').replace('"', r'\"').replace("'", r'\'')
        sql_sc = [
            f"""insert into app_case_sqlinfo_checklist (sql_response) values ('{sql_response_checklist}');""",
            f"SELECT @@IDENTITY AS Id "]
        return sql_sc

    def insert_api_case_sqlinfoscript(self, db_casesqlinfo_script: DBAPPCaseSqlinfoScript):
        if isinstance(db_casesqlinfo_script.sql_response, list) or isinstance(db_casesqlinfo_script.sql_response,
                                                                              tuple):
            sql_response_script = ";".join([str(x) for x in db_casesqlinfo_script.sql_response])
        else:
            sql_response_script = str(db_casesqlinfo_script.sql_response)
        sql_sc = [
            f"""insert into app_case_sqlinfo_script (sql_response) values ('{sql_response_script}');""",
            f" SELECT @@IDENTITY AS Id "]
        return sql_sc

    def insert_app_case_sqlinfoconfig(self, db_casesqlinfo_config: DBAPPCaseSqlinfoConfig):
        sql_sc = [
            f"""insert into app_case_sqlinfo_config (`host`, `port`, `type`, `username`, `password`)
                    values ('{db_casesqlinfo_config.host}', '{db_casesqlinfo_config.port}', '{db_casesqlinfo_config.type}', '{db_casesqlinfo_config.username}', '{db_casesqlinfo_config.password}')""",
            f" SELECT @@IDENTITY AS Id "]
        return sql_sc


class Publish(object):
    def __init__(self, sql_config: SQLConfig):
        self.sql_config = sql_config

        self.mysql_tool = MysqlTool()

    # no use here from now
    #
    #     def load_sql_script(self):
    #         local_dir = os.path.dirname(__file__)
    #         sql_script_path = f"{local_dir}/../resource/sqlpublish/haf_publish.sql"
    #         logger.info(f"load sql script file : {sql_script_path}")
    #         if os.path.exists(sql_script_path):
    #             with open(sql_script_path) as f:
    #                 self.sql_script = f.read().replace("\n", "")
    #             return True
    #         else:
    #             logger.error(f"do not found sql file : {sql_script_path}")
    #             return False
    #

    def check_db_exists(self):
        try:
            sql_check = "show databases"
            result = self.mysql_tool.connect_execute(self.sql_config, sql_check, run_background=rb, commit=True)
            if len(result) > 0 and len(result[0]) > 0:
                for x in result[0]:
                    if "haf_publish" in x:
                        return True
            return False
        except Exception as e:
            logger.error(e)

    def create_database(self):
        try:
            if not self.check_db_exists():
                for case in create_case:
                    self.mysql_tool.connect_execute(self.sql_config, case)
        except Exception as e:
            logger.error(e)

    def publish_result(self, results: EndResult):

        if not results:
            logger.error("no result need publish")
            return
        self.create_database()
        try:
            sql_publish = SQLPublish()
            db_main = DBMain(0, results.name, results.begin_time, results.end_time, results.duration, results.passed,
                             results.failed, results.skip, results.error,
                             ",".join(results.suite_name) if isinstance(results.suite_name, list) or isinstance(
                                 results.suite_name, tuple) else 'null')
            main_id = \
            self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_main(db_main), run_background=rb,
                                            commit=True)[1][0][0]
            for suite_name in results.suite_name:
                db_suite = DBSuite(0, main_id, suite_name)
                suite_id = self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_suite(db_suite),
                                                           run_background=rb, commit=True)[1][0][0]

                s = results.summary.get(suite_name)
                db_summary = DBSummary(0, suite_name, s.passed, s.failed, s.skip, s.error, s.all, s.base_url,
                                       s.begin_time, s.end_time, s.duration, suite_id)
                self.mysql_tool.connect_execute(self.sql_config, sql_publish.insert_summary(db_summary),
                                                run_background=rb, commit=True)[1][0][0]

                d = results.details.get(suite_name)

                for result in d.cases:
                    if isinstance(result, HttpApiResult):
                        sql_api_publish = SQLAPIPublish()
                        case = result.case
                        ids = case.ids
                        db_case_ids = DBAPICaseIds(0, ids.id, ids.subid, ids.name, ids.api_name)
                        case_ids_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_case_ids(db_case_ids),
                                                        run_background=rb, commit=True)[1][0][0]

                        response = case.response
                        db_case_response = DBAPICaseResponse(0, response.header, response.body, response.code)
                        case_response_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_case_response(db_case_response),
                                                        run_background=rb, commit=True)[1][0][0]

                        request = case.request
                        db_case_request = DBAPICaseRequest(0, request.header, request.data, request.url, request.method,
                                                        request.protocol, request.host_port)
                        case_request_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_case_request(db_case_request),
                                                        run_background=rb, commit=True)[1][0][0]

                        expect = case.expect
                        db_case_expect = DBAPICaseExpect(0, case_response_id, expect.sql_check_func,
                                                    expect.sql_response_result)
                        case_expect_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_caseexpect(db_case_expect),
                                                        run_background=rb, commit=True)[1][0][0]

                        sqlinfo_script = case.sqlinfo.scripts
                        db_case_script = DBAPICaseSqlinfoScript(0, sqlinfo_script.get("sql_response", ''))
                        sqlinfo_script_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_api_publish.insert_api_case_sqlinfoscript(
                                                                                db_case_script), run_background=rb,
                                                                            commit=True)[1][0][0]

                        sqlinfo_checklist = case.sqlinfo.check_list
                        db_case_checklist = DBAPICaseSqlinfoChecklist(0, sqlinfo_checklist.get("sql_response", ''))
                        sqlinfo_checklist_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_api_publish.insert_api_case_sqlinfochecklist(
                                                                                db_case_checklist), run_background=rb,
                                                                            commit=True)[1][0][0]

                        sqlinfo_config = case.sqlinfo.config if case.sqlinfo.config else SQLConfig()
                        db_case_sqlinfoconfig = DBAPICaseSqlinfoConfig(0, sqlinfo_config.host, sqlinfo_config.port,
                                                                    sqlinfo_config.protocol, sqlinfo_config.username,
                                                                    sqlinfo_config.password)
                        sqlinfo_config_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_api_publish.insert_api_case_sqlinfoconfig(
                                                                                db_case_sqlinfoconfig),
                                                                            run_background=rb, commit=True)[1][0][0]

                        case_sqlinfo = DBAPICaseSqlinfo(0, sqlinfo_script_id, sqlinfo_config_id, sqlinfo_checklist_id)
                        case_sqlinfo_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_case_sqlinfo(case_sqlinfo),
                                                        run_background=rb, commit=True)[1][0][0]

                        case_detail = DBAPIDetail(0, case.name, result.result_check_response, result.result_check_sql_response,
                                            result.run_error, result.result, result.begin_time, result.end_time,
                                            result.log_dir, result.runner)
                        case_detail_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_detail(case_detail),
                                                        run_background=rb, commit=True)[1][0][0]

                        db_case = DBAPICase(0, case_ids_id, case.run, case.dependent, case.bench_name, case_request_id,
                                        case_response_id, case_expect_id, case_sqlinfo_id, case.type, case_detail_id,
                                        suite_id)
                        self.mysql_tool.connect_execute(self.sql_config, sql_api_publish.insert_api_case(db_case),
                                                        run_background=rb, commit=True)[1][0][0]
                    elif isinstance(result, AppResult):
                        sql_app_publish = SQLAPPublish()
                        case = result.case
                        ids = case.ids
                        db_case_ids = DBAPPCaseIds(0, ids.id, ids.subid, ids.name, ids.app_name)
                        case_ids_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_ids(db_case_ids),
                                                        run_background=rb, commit=True)[1][0][0]
                                                        
                        case_detail = DBAPPDetail(0, case.name, "", "",
                                            result.run_error, result.result, result.begin_time, result.end_time,
                                            result.log_dir, result.runner)
                        case_detail_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_detail(case_detail),
                                                        run_background=rb, commit=True)[1][0][0]
                        
                        caps = case.desired_caps
                        case_caps = DBAPPCaseCaps(0, caps.automationName, caps.platformName, caps.platformVersion, caps.deviceName, caps.appPackage, caps.appActivity, caps.noReset)
                        
                        caps_id = self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_caps(case_caps),
                                                        run_background=rb, commit=True)[1][0][0]
                        db_case = DBAPPCase(0, case_ids_id, case.run, case.dependent, case.bench_name, case_expect_id, case_sqlinfo_id, case.type, case_detail_id,
                                        suite_id, caps_id)
                        case_id = self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case(db_case),
                                                        run_background=rb, commit=True)[1][0][0]
                        for stage_id in case.stages.keys():
                            stage = case.stages.get(stage_id)
                            stage_result = DBAPPCaseStageResult(0, True, "None")
                            stage_result_id = self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_stage_result(stage_result),
                                                        run_background=rb, commit=True)[1][0][0]
                            stage_ = DBAPPCaseStage(0, stage.id, stage.name, stage.operation, stage.show_try, stage.time_sleep, stage.info, stage_result_id, case_id)
                            stage_id = self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_stage(stage_),
                                                        run_background=rb, commit=True)[1][0][0]
                            for stage_path_type in stage.path.keys():
                                stage_path_value = stage.path.get(stage_path_type)
                                stage_path = DBAPPCaseStagePath(0, stage_id, stage_path_type, stage_path_value)
                                self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_stage_path(stage_path),
                                                        run_background=rb, commit=True)
                        
                        expect = case.expect
                        db_case_expect = DBAPPCaseExpect(0, "0", expect.sql_check_func,
                                                    expect.sql_response_result)
                        case_expect_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_caseexpect(db_case_expect),
                                                        run_background=rb, commit=True)[1][0][0]

                        sqlinfo_script = case.sqlinfo.scripts
                        db_case_script = DBAPPCaseSqlinfoScript(0, sqlinfo_script.get("sql_response", ''))
                        sqlinfo_script_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_app_publish.insert_app_case_sqlinfoscript(
                                                                                db_case_script), run_background=rb,
                                                                            commit=True)[1][0][0]

                        sqlinfo_checklist = case.sqlinfo.check_list
                        db_case_checklist = DBAPICaseSqlinfoChecklist(0, sqlinfo_checklist.get("sql_response", ''))
                        sqlinfo_checklist_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_app_publish.insert_app_case_sqlinfochecklist(
                                                                                db_case_checklist), run_background=rb,
                                                                            commit=True)[1][0][0]

                        sqlinfo_config = case.sqlinfo.config if case.sqlinfo.config else SQLConfig()
                        db_case_sqlinfoconfig = DBAPPCaseSqlinfoConfig(0, sqlinfo_config.host, sqlinfo_config.port,
                                                                    sqlinfo_config.protocol, sqlinfo_config.username,
                                                                    sqlinfo_config.password)
                        sqlinfo_config_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_app_publish.insert_app_case_sqlinfoconfig(
                                                                                db_case_sqlinfoconfig),
                                                                            run_background=rb, commit=True)[1][0][0]

                        case_sqlinfo = DBAPPCaseSqlinfo(0, sqlinfo_script_id, sqlinfo_config_id, sqlinfo_checklist_id)
                        case_sqlinfo_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_sqlinfo(case_sqlinfo),
                                                        run_background=rb, commit=True)[1][0][0]

        except Exception as e:
            logger.error(e)
            traceback.print_exc()




