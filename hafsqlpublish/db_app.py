# encoding = 'utf-8'
import os

from haf.apihelper import Ids, Response, Request
from haf.case import HttpApiCase, AppCase
from haf.common.database import MysqlTool, SQLConfig
from haf.common.log import Log
from haf.result import EndResult, Summary, Detail, HttpApiResult, AppResult
from hafsqlpublish.createhaf import *

logger = Log.getLogger(__name__)
import traceback

rb = True


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
    def __init__(self, id, stage_id, name, operation, show_try, time_sleep, info, result_id, app_case_id, run_count):
        self.id = id if id is not None else ''
        self.stage_id = stage_id if stage_id is not None else ''
        self.name = name if name is not None else ''
        self.operation = operation if operation is not None else ''
        self.show_try = show_try if show_try is not None else ''
        self.time_sleep = time_sleep if time_sleep is not None else ''
        self.info = info if info is not None else ''
        self.result_id = result_id if result_id is not None else ''
        self.app_case_id = app_case_id if app_case_id is not None else ''
        self.run_count = run_count if run_count is not None else ''


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
            f"""insert into app_case (ids_id, `run`, dependent, bench_name, expect_id, sqlinfo_id, `type`, suite_id, detail_id, caps_id) 
                    values ('{db_case.ids_id}', '{db_case.run}', '{dependent}', '{db_case.bench_name}', '{db_case.expect_id}', '{db_case.sqlinfo_id}', '{db_case.type}', '{db_case.suite_id}', '{db_case.detail_id}', '{db_case.caps_id}'); """,
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
        info = db_case_stage.info
        if isinstance(info, dict):
            x = ""
            for key in info.keys():
                x+=f"{key}={info.get(key)}"
        else:
            x = ""
        info = x 
        sql_sc = [
            f"""insert into app_case_stage (stage_id, name, operation, show_try, time_sleep, info, result_id, app_case_id, run_count) 
                    values ('{db_case_stage.stage_id}', '{db_case_stage.name}', '{db_case_stage.operation}', '{db_case_stage.show_try}', '{db_case_stage.time_sleep}', '{info}', '{db_case_stage.result_id}', '{db_case_stage.app_case_id}', '{db_case_stage.run_count}');  """,
            f"SELECT @@IDENTITY AS Id"]
        return sql_sc

    def insert_app_case_stage_path(self, db_case_stage_path: DBAPPCaseStagePath):
        path = db_case_stage_path.find_value
        if isinstance(path, str):
            path = path.replace("'", "\\'").replace('"', '\\"')
        sql_sc = [
            f"""insert into app_case_stage_path (stage_id, find_type, find_value) 
                    values ('{db_case_stage_path.stage_id}', '{db_case_stage_path.find_type}', '{path}');""",
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

    def insert_app_case_sqlinfoscript(self, db_casesqlinfo_script: DBAPPCaseSqlinfoScript):
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
