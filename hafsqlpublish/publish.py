# encoding = 'utf-8'
import os

from haf.apihelper import Ids, Response, Request
from haf.case import HttpApiCase
from haf.common.database import MysqlTool, SQLConfig
from haf.common.log import Log
from haf.result import EndResult, Summary, Detail, HttpApiResult, AppResult, WebResult
from hafsqlpublish.createhaf import *
from hafsqlpublish.db_api import *
from hafsqlpublish.db_common import *
from hafsqlpublish.db_app import *
from hafsqlpublish.db_web import *

logger = Log.getLogger(__name__)
import traceback

rb = True


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
                        db_case_ids = DBAPPCaseIds(0, ids.id, ids.subid, ids.name, getattr(ids, "app_name"))
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
                        
                        expect = case.expect
                        db_case_expect = DBAPPCaseExpect(0, "0", getattr(expect, "sql_check_func", None) ,
                                                    getattr(expect, "sql_response_result", None))
                        case_expect_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_caseexpect(db_case_expect),
                                                        run_background=rb, commit=True)[1][0][0]

                        sqlinfo_config = case.sqlinfo.config if case.sqlinfo.config else SQLConfig()
                        db_case_sqlinfoconfig = DBAPPCaseSqlinfoConfig(0, sqlinfo_config.host, sqlinfo_config.port,
                                                                    sqlinfo_config.protocol, sqlinfo_config.username,
                                                                    sqlinfo_config.password)
                        sqlinfo_config_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_app_publish.insert_app_case_sqlinfoconfig(
                                                                                db_case_sqlinfoconfig),
                                                                            run_background=rb, commit=True)[1][0][0]

                        sqlinfo_checklist = case.sqlinfo.check_list
                        db_case_checklist = DBAPICaseSqlinfoChecklist(0, sqlinfo_checklist.get("sql_response", ''))
                        sqlinfo_checklist_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_app_publish.insert_app_case_sqlinfochecklist(
                                                                                db_case_checklist), run_background=rb,
                                                                            commit=True)[1][0][0]
                        sqlinfo_script = case.sqlinfo.scripts
                        db_case_script = DBAPPCaseSqlinfoScript(0, sqlinfo_script.get("sql_response", ''))
                        sqlinfo_script_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_app_publish.insert_app_case_sqlinfoscript(
                                                                                db_case_script), run_background=rb,
                                                                            commit=True)[1][0][0]
                        case_sqlinfo = DBAPPCaseSqlinfo(0, sqlinfo_script_id, sqlinfo_config_id, sqlinfo_checklist_id)
                        case_sqlinfo_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_sqlinfo(case_sqlinfo),
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
                            
                            stage_ = DBAPPCaseStage(0, stage.id, stage.name, stage.operation, stage.show_try, stage.time_sleep, stage.info, stage_result_id, case_id, stage.run_count)
                            stage_id = self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_stage(stage_),
                                                        run_background=rb, commit=True)[1][0][0]
                            for stage_path_type in stage.path.keys():
                                stage_path_value = stage.path.get(stage_path_type)
                                stage_path = DBAPPCaseStagePath(0, stage_id, stage_path_type, stage_path_value)
                                self.mysql_tool.connect_execute(self.sql_config, sql_app_publish.insert_app_case_stage_path(stage_path),
                                                        run_background=rb, commit=True)                

                    elif isinstance(result, WebResult):
                        sql_web_publish = SQLWebublish()
                        case = result.case
                        ids = case.ids
                        db_case_ids = DBWebCaseIds(0, ids.id, ids.subid, ids.name, getattr(ids, "web_name", getattr(ids, "web_name")))
                        case_ids_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case_ids(db_case_ids),
                                                        run_background=rb, commit=True)[1][0][0]
                                                        
                        case_detail = DBWebDetail(0, case.name, "", "",
                                            result.run_error, result.result, result.begin_time, result.end_time,
                                            result.log_dir, result.runner)
                        case_detail_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_detail(case_detail),
                                                        run_background=rb, commit=True)[1][0][0]
                        
                        caps = case.desired_caps
                        case_caps = DBWebCaseCaps(0, caps.platformName, caps.platformVersion, caps.start_url)

                        
                        caps_id = self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case_caps(case_caps),
                                                        run_background=rb, commit=True)[1][0][0]
                        
                        expect = case.expect
                        db_case_expect = DBWebCaseExpect(0, "0", getattr(expect, "sql_check_func", None) ,
                                                    getattr(expect, "sql_response_result", None))
                        case_expect_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_caseexpect(db_case_expect),
                                                        run_background=rb, commit=True)[1][0][0]

                        sqlinfo_config = case.sqlinfo.config if case.sqlinfo.config else SQLConfig()
                        db_case_sqlinfoconfig = DBWebCaseSqlinfoConfig(0, sqlinfo_config.host, sqlinfo_config.port,
                                                                    sqlinfo_config.protocol, sqlinfo_config.username,
                                                                    sqlinfo_config.password)
                        sqlinfo_config_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_web_publish.insert_web_case_sqlinfoconfig(
                                                                                db_case_sqlinfoconfig),
                                                                            run_background=rb, commit=True)[1][0][0]

                        sqlinfo_checklist = case.sqlinfo.check_list
                        db_case_checklist = DBAPICaseSqlinfoChecklist(0, sqlinfo_checklist.get("sql_response", ''))
                        sqlinfo_checklist_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_web_publish.insert_web_case_sqlinfochecklist(
                                                                                db_case_checklist), run_background=rb,
                                                                            commit=True)[1][0][0]
                        sqlinfo_script = case.sqlinfo.scripts
                        db_case_script = DBWebCaseSqlinfoScript(0, sqlinfo_script.get("sql_response", ''))
                        sqlinfo_script_id = self.mysql_tool.connect_execute(self.sql_config,
                                                                            sql_web_publish.insert_web_case_sqlinfoscript(
                                                                                db_case_script), run_background=rb,
                                                                            commit=True)[1][0][0]
                        case_sqlinfo = DBWebCaseSqlinfo(0, sqlinfo_script_id, sqlinfo_config_id, sqlinfo_checklist_id)
                        case_sqlinfo_id = \
                        self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case_sqlinfo(case_sqlinfo),
                                                        run_background=rb, commit=True)[1][0][0]

                        db_case = DBWebCase(0, case_ids_id, case.run, case.dependent, case.bench_name, case_expect_id, case_sqlinfo_id, case.type, case_detail_id,
                                        suite_id, caps_id)
                        case_id = self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case(db_case),
                                                        run_background=rb, commit=True)[1][0][0]
                        for stage_id in case.stages.keys():
                            stage = case.stages.get(stage_id)
                            stage_result = DBWebCaseStageResult(0, True, "None")
                            stage_result_id = self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case_stage_result(stage_result),
                                                        run_background=rb, commit=True)[1][0][0]
                            
                            stage_ = DBWebCaseStage(0, stage.id, stage.name, stage.operation, stage.show_try, stage.time_sleep, stage.info, stage_result_id, case_id, stage.run_count)
                            stage_id = self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case_stage(stage_),
                                                        run_background=rb, commit=True)[1][0][0]
                            for stage_path_type in stage.path.keys():
                                stage_path_value = stage.path.get(stage_path_type)
                                stage_path = DBWebCaseStagePath(0, stage_id, stage_path_type, stage_path_value)
                                self.mysql_tool.connect_execute(self.sql_config, sql_web_publish.insert_web_case_stage_path(stage_path),
                                                        run_background=rb, commit=True)             
        except Exception as e:
            logger.error(e)
            traceback.print_exc()




