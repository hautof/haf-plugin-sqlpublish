/*
Navicat MySQL Data Transfer

Source Server         : 192.168.41.208
Source Server Version : 50722
Source Host           : 192.168.41.208:3306
Source Database       : haf_publish

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2019-04-01 11:37:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for api_case
-- ----------------------------
DROP TABLE IF EXISTS `api_case`;
CREATE TABLE `api_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ids_id` int(11) DEFAULT NULL,
  `run` int(255) DEFAULT NULL,
  `dependent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bench_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `request_id` int(11) DEFAULT NULL,
  `response_id` int(11) DEFAULT NULL,
  `expect_id` int(11) DEFAULT NULL,
  `sqlinfo_id` int(11) DEFAULT NULL,
  `type` int(255) DEFAULT NULL,
  `suite_id` int(11) DEFAULT NULL,
  `detail_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `suite_id_` (`suite_id`),
  KEY `case_sqlinfo` (`sqlinfo_id`),
  KEY `case_response_` (`response_id`),
  KEY `case_request_` (`request_id`),
  KEY `detail_` (`detail_id`),
  KEY `case_expect_` (`expect_id`),
  KEY `ids_id` (`ids_id`),
  CONSTRAINT `case_expect_` FOREIGN KEY (`expect_id`) REFERENCES `api_case_expect` (`id`),
  CONSTRAINT `case_request_` FOREIGN KEY (`request_id`) REFERENCES `api_case_request` (`id`),
  CONSTRAINT `case_response_` FOREIGN KEY (`response_id`) REFERENCES `api_case_response` (`id`),
  CONSTRAINT `case_sqlinfo` FOREIGN KEY (`sqlinfo_id`) REFERENCES `api_case_sqlinfo` (`id`),
  CONSTRAINT `detail_` FOREIGN KEY (`detail_id`) REFERENCES `api_detail` (`id`),
  CONSTRAINT `ids_id_` FOREIGN KEY (`ids_id`) REFERENCES `api_case_ids` (`id`),
  CONSTRAINT `suite_id_` FOREIGN KEY (`suite_id`) REFERENCES `suite` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29757 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_expect
-- ----------------------------
DROP TABLE IF EXISTS `api_case_expect`;
CREATE TABLE `api_case_expect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) DEFAULT NULL,
  `sql_check_func` varchar(255) DEFAULT NULL,
  `sql_response_result` text CHARACTER SET utf8,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29842 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_ids
-- ----------------------------
DROP TABLE IF EXISTS `api_case_ids`;
CREATE TABLE `api_case_ids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` int(11) DEFAULT NULL,
  `case_sub_id` int(11) DEFAULT NULL,
  `case_name` varchar(255) DEFAULT NULL,
  `case_api_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29910 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_request
-- ----------------------------
DROP TABLE IF EXISTS `api_case_request`;
CREATE TABLE `api_case_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `header` longtext CHARACTER SET utf8mb4,
  `data` longtext CHARACTER SET utf8mb4,
  `url` varchar(255) DEFAULT NULL,
  `method` varchar(255) DEFAULT NULL,
  `protocol` varchar(255) DEFAULT NULL,
  `host_port` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29869 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_response
-- ----------------------------
DROP TABLE IF EXISTS `api_case_response`;
CREATE TABLE `api_case_response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `header` longtext CHARACTER SET utf8mb4,
  `body` longtext CHARACTER SET utf8mb4,
  `code` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29886 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_sqlinfo
-- ----------------------------
DROP TABLE IF EXISTS `api_case_sqlinfo`;
CREATE TABLE `api_case_sqlinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scripts_id` int(11) DEFAULT NULL,
  `config` varchar(255) DEFAULT NULL,
  `config_id` int(11) DEFAULT NULL,
  `check_list_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `checklist` (`check_list_id`),
  KEY `script` (`scripts_id`),
  KEY `config` (`config_id`),
  CONSTRAINT `checklist` FOREIGN KEY (`check_list_id`) REFERENCES `api_case_sqlinfo_checklist` (`id`),
  CONSTRAINT `config` FOREIGN KEY (`config_id`) REFERENCES `api_case_sqlinfo_config` (`id`),
  CONSTRAINT `script` FOREIGN KEY (`scripts_id`) REFERENCES `api_case_sqlinfo_script` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29782 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_sqlinfo_checklist
-- ----------------------------
DROP TABLE IF EXISTS `api_case_sqlinfo_checklist`;
CREATE TABLE `api_case_sqlinfo_checklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29798 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_sqlinfo_config
-- ----------------------------
DROP TABLE IF EXISTS `api_case_sqlinfo_config`;
CREATE TABLE `api_case_sqlinfo_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29787 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_case_sqlinfo_script
-- ----------------------------
DROP TABLE IF EXISTS `api_case_sqlinfo_script`;
CREATE TABLE `api_case_sqlinfo_script` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` text CHARACTER SET utf8,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29819 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for api_detail
-- ----------------------------
DROP TABLE IF EXISTS `api_detail`;
CREATE TABLE `api_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) DEFAULT NULL,
  `result_check_response` text,
  `result_check_sql_response` text,
  `run_error` text CHARACTER SET utf8,
  `result` text,
  `begin_time` varchar(255) DEFAULT NULL,
  `end_time` varchar(255) DEFAULT NULL,
  `log_dir` text,
  `runner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29759 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case
-- ----------------------------
DROP TABLE IF EXISTS `app_case`;
CREATE TABLE `app_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ids_id` int(11) DEFAULT NULL,
  `run` int(255) DEFAULT NULL,
  `dependent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bench_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `expect_id` int(11) DEFAULT NULL,
  `sqlinfo_id` int(11) DEFAULT NULL,
  `type` int(255) DEFAULT NULL,
  `suite_id` int(11) DEFAULT NULL,
  `detail_id` int(11) DEFAULT NULL,
  `caps_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `suite_id_app` (`suite_id`),
  KEY `case_expect_app` (`expect_id`),
  KEY `ids_id_app` (`ids_id`),
  KEY `sqlinfo_id_app` (`sqlinfo_id`),
  KEY `detail` (`detail_id`),
  KEY `caps_id` (`caps_id`),
  CONSTRAINT `capid` FOREIGN KEY (`caps_id`) REFERENCES `app_case_caps` (`id`),
  CONSTRAINT `case_expect_app` FOREIGN KEY (`expect_id`) REFERENCES `app_case_expect` (`id`),
  CONSTRAINT `detail` FOREIGN KEY (`detail_id`) REFERENCES `app_detail` (`id`),
  CONSTRAINT `ids_id_app` FOREIGN KEY (`ids_id`) REFERENCES `app_case_ids` (`id`),
  CONSTRAINT `sqlinfo_id_app` FOREIGN KEY (`sqlinfo_id`) REFERENCES `app_case_sqlinfo` (`id`),
  CONSTRAINT `suite_id_app` FOREIGN KEY (`suite_id`) REFERENCES `suite` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14315 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_caps
-- ----------------------------
DROP TABLE IF EXISTS `app_case_caps`;
CREATE TABLE `app_case_caps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `automation_name` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `platform_name` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `platform_version` varchar(255) DEFAULT NULL,
  `device_name` varchar(255) DEFAULT NULL,
  `app_package` varchar(255) DEFAULT NULL,
  `app_activity` varchar(255) DEFAULT NULL,
  `no_reset` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `result` (`no_reset`)
) ENGINE=InnoDB AUTO_INCREMENT=14397 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_expect
-- ----------------------------
DROP TABLE IF EXISTS `app_case_expect`;
CREATE TABLE `app_case_expect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) DEFAULT NULL,
  `sql_check_func` varchar(255) DEFAULT NULL,
  `sql_response_result` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14379 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_ids
-- ----------------------------
DROP TABLE IF EXISTS `app_case_ids`;
CREATE TABLE `app_case_ids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` int(11) DEFAULT NULL,
  `case_sub_id` int(11) DEFAULT NULL,
  `case_name` varchar(255) DEFAULT NULL,
  `case_app_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14439 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_sqlinfo
-- ----------------------------
DROP TABLE IF EXISTS `app_case_sqlinfo`;
CREATE TABLE `app_case_sqlinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scripts_id` int(11) DEFAULT NULL,
  `config` varchar(255) DEFAULT NULL,
  `config_id` int(11) DEFAULT NULL,
  `check_list_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `script_id` (`scripts_id`),
  KEY `checklistid` (`check_list_id`),
  KEY `configid` (`config_id`),
  CONSTRAINT `checklistid` FOREIGN KEY (`check_list_id`) REFERENCES `app_case_sqlinfo_checklist` (`id`),
  CONSTRAINT `configid` FOREIGN KEY (`config_id`) REFERENCES `app_case_sqlinfo_config` (`id`),
  CONSTRAINT `script_id` FOREIGN KEY (`scripts_id`) REFERENCES `app_case_sqlinfo_script` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14339 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_sqlinfo_checklist
-- ----------------------------
DROP TABLE IF EXISTS `app_case_sqlinfo_checklist`;
CREATE TABLE `app_case_sqlinfo_checklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14354 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_sqlinfo_config
-- ----------------------------
DROP TABLE IF EXISTS `app_case_sqlinfo_config`;
CREATE TABLE `app_case_sqlinfo_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14345 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_sqlinfo_script
-- ----------------------------
DROP TABLE IF EXISTS `app_case_sqlinfo_script`;
CREATE TABLE `app_case_sqlinfo_script` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14369 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_stage
-- ----------------------------
DROP TABLE IF EXISTS `app_case_stage`;
CREATE TABLE `app_case_stage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stage_id` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `operation` varchar(255) DEFAULT NULL,
  `show_try` varchar(255) DEFAULT NULL,
  `time_sleep` varchar(255) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `result_id` int(11) DEFAULT NULL,
  `app_case_id` int(11) DEFAULT NULL,
  `run_count` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `result` (`result_id`),
  KEY `case` (`app_case_id`),
  CONSTRAINT `case` FOREIGN KEY (`app_case_id`) REFERENCES `app_case` (`id`),
  CONSTRAINT `result` FOREIGN KEY (`result_id`) REFERENCES `app_case_stage_result` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14396 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_stage_path
-- ----------------------------
DROP TABLE IF EXISTS `app_case_stage_path`;
CREATE TABLE `app_case_stage_path` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stage_id` int(11) DEFAULT NULL,
  `find_type` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `find_value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stage` (`stage_id`),
  CONSTRAINT `stage` FOREIGN KEY (`stage_id`) REFERENCES `app_case_stage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14378 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_case_stage_result
-- ----------------------------
DROP TABLE IF EXISTS `app_case_stage_result`;
CREATE TABLE `app_case_stage_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `result` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `exception` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14412 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for app_detail
-- ----------------------------
DROP TABLE IF EXISTS `app_detail`;
CREATE TABLE `app_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) DEFAULT NULL,
  `result_check_response` varchar(255) DEFAULT NULL,
  `result_check_sql_response` varchar(255) DEFAULT NULL,
  `run_error` text,
  `result` text,
  `begin_time` varchar(255) DEFAULT NULL,
  `end_time` varchar(255) DEFAULT NULL,
  `log_dir` varchar(255) DEFAULT NULL,
  `runner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14331 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for main
-- ----------------------------
DROP TABLE IF EXISTS `main`;
CREATE TABLE `main` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `begin_time` varchar(255) DEFAULT NULL,
  `end_time` varchar(255) DEFAULT NULL,
  `duration_time` int(255) DEFAULT NULL,
  `passed` int(255) DEFAULT NULL,
  `failed` int(255) DEFAULT NULL,
  `skip` int(255) DEFAULT NULL,
  `error` int(255) DEFAULT NULL,
  `suite_name` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=961 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for suite
-- ----------------------------
DROP TABLE IF EXISTS `suite`;
CREATE TABLE `suite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `main_id` int(11) NOT NULL,
  `suite_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_id` (`main_id`),
  CONSTRAINT `main_id` FOREIGN KEY (`main_id`) REFERENCES `main` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13566 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for summary
-- ----------------------------
DROP TABLE IF EXISTS `summary`;
CREATE TABLE `summary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `passed` int(255) DEFAULT NULL,
  `failed` int(255) DEFAULT NULL,
  `skip` int(255) DEFAULT NULL,
  `error` int(255) DEFAULT NULL,
  `all` int(255) DEFAULT NULL,
  `base_url` varchar(255) DEFAULT NULL,
  `begin_time` varchar(255) DEFAULT NULL,
  `end_time` varchar(255) DEFAULT NULL,
  `duration_time` int(11) DEFAULT NULL,
  `suite_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `suite_id` (`suite_id`),
  CONSTRAINT `suite_id` FOREIGN KEY (`suite_id`) REFERENCES `suite` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13557 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case
-- ----------------------------
DROP TABLE IF EXISTS `web_case`;
CREATE TABLE `web_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ids_id` int(11) DEFAULT NULL,
  `run` int(255) DEFAULT NULL,
  `dependent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bench_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `expect_id` int(11) DEFAULT NULL,
  `sqlinfo_id` int(11) DEFAULT NULL,
  `type` int(255) DEFAULT NULL,
  `suite_id` int(11) DEFAULT NULL,
  `detail_id` int(11) DEFAULT NULL,
  `caps_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `suite_id_app` (`suite_id`),
  KEY `case_expect_app` (`expect_id`),
  KEY `ids_id_app` (`ids_id`),
  KEY `sqlinfo_id_app` (`sqlinfo_id`),
  KEY `detail` (`detail_id`),
  KEY `caps_id` (`caps_id`),
  CONSTRAINT `web_case_ibfk_1` FOREIGN KEY (`caps_id`) REFERENCES `web_case_caps` (`id`),
  CONSTRAINT `web_case_ibfk_2` FOREIGN KEY (`expect_id`) REFERENCES `web_case_expect` (`id`),
  CONSTRAINT `web_case_ibfk_3` FOREIGN KEY (`detail_id`) REFERENCES `web_detail` (`id`),
  CONSTRAINT `web_case_ibfk_4` FOREIGN KEY (`ids_id`) REFERENCES `web_case_ids` (`id`),
  CONSTRAINT `web_case_ibfk_5` FOREIGN KEY (`sqlinfo_id`) REFERENCES `web_case_sqlinfo` (`id`),
  CONSTRAINT `web_case_ibfk_6` FOREIGN KEY (`suite_id`) REFERENCES `suite` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14324 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_caps
-- ----------------------------
DROP TABLE IF EXISTS `web_case_caps`;
CREATE TABLE `web_case_caps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform_name` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `platform_version` varchar(255) DEFAULT NULL,
  `start_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14406 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_expect
-- ----------------------------
DROP TABLE IF EXISTS `web_case_expect`;
CREATE TABLE `web_case_expect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) DEFAULT NULL,
  `sql_check_func` varchar(255) DEFAULT NULL,
  `sql_response_result` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14388 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_ids
-- ----------------------------
DROP TABLE IF EXISTS `web_case_ids`;
CREATE TABLE `web_case_ids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` int(11) DEFAULT NULL,
  `case_sub_id` int(11) DEFAULT NULL,
  `case_name` varchar(255) DEFAULT NULL,
  `case_web_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14447 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_sqlinfo
-- ----------------------------
DROP TABLE IF EXISTS `web_case_sqlinfo`;
CREATE TABLE `web_case_sqlinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scripts_id` int(11) DEFAULT NULL,
  `config` varchar(255) DEFAULT NULL,
  `config_id` int(11) DEFAULT NULL,
  `check_list_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `script_id` (`scripts_id`),
  KEY `checklistid` (`check_list_id`),
  KEY `configid` (`config_id`),
  CONSTRAINT `web_case_sqlinfo_ibfk_1` FOREIGN KEY (`check_list_id`) REFERENCES `web_case_sqlinfo_checklist` (`id`),
  CONSTRAINT `web_case_sqlinfo_ibfk_2` FOREIGN KEY (`config_id`) REFERENCES `web_case_sqlinfo_config` (`id`),
  CONSTRAINT `web_case_sqlinfo_ibfk_3` FOREIGN KEY (`scripts_id`) REFERENCES `web_case_sqlinfo_script` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14348 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_sqlinfo_checklist
-- ----------------------------
DROP TABLE IF EXISTS `web_case_sqlinfo_checklist`;
CREATE TABLE `web_case_sqlinfo_checklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14363 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_sqlinfo_config
-- ----------------------------
DROP TABLE IF EXISTS `web_case_sqlinfo_config`;
CREATE TABLE `web_case_sqlinfo_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14354 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_sqlinfo_script
-- ----------------------------
DROP TABLE IF EXISTS `web_case_sqlinfo_script`;
CREATE TABLE `web_case_sqlinfo_script` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sql_response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14378 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_stage
-- ----------------------------
DROP TABLE IF EXISTS `web_case_stage`;
CREATE TABLE `web_case_stage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stage_id` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `operation` varchar(255) DEFAULT NULL,
  `show_try` varchar(255) DEFAULT NULL,
  `time_sleep` varchar(255) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `result_id` int(11) DEFAULT NULL,
  `web_case_id` int(11) DEFAULT NULL,
  `run_count` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `result` (`result_id`),
  KEY `case` (`web_case_id`),
  CONSTRAINT `123` FOREIGN KEY (`web_case_id`) REFERENCES `web_case` (`id`),
  CONSTRAINT `web_case_stage_ibfk_2` FOREIGN KEY (`result_id`) REFERENCES `web_case_stage_result` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14416 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_stage_path
-- ----------------------------
DROP TABLE IF EXISTS `web_case_stage_path`;
CREATE TABLE `web_case_stage_path` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stage_id` int(11) DEFAULT NULL,
  `find_type` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `find_value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stage` (`stage_id`),
  CONSTRAINT `web_case_stage_path_ibfk_1` FOREIGN KEY (`stage_id`) REFERENCES `web_case_stage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14396 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_case_stage_result
-- ----------------------------
DROP TABLE IF EXISTS `web_case_stage_result`;
CREATE TABLE `web_case_stage_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `result` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `exception` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14434 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for web_detail
-- ----------------------------
DROP TABLE IF EXISTS `web_detail`;
CREATE TABLE `web_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) DEFAULT NULL,
  `result_check_response` varchar(255) DEFAULT NULL,
  `result_check_sql_response` varchar(255) DEFAULT NULL,
  `run_error` text,
  `result` text,
  `begin_time` varchar(255) DEFAULT NULL,
  `end_time` varchar(255) DEFAULT NULL,
  `log_dir` varchar(255) DEFAULT NULL,
  `runner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14339 DEFAULT CHARSET=latin1;
