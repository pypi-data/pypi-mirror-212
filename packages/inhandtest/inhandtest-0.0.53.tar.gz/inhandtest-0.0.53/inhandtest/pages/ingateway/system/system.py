# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 14:29:03
# @Author  : Pane Li
# @File    : system.py
"""
system

"""
import allure
from inhandtest.tools import loop_inspector
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class SystemTime(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言系统时间状态')
    @loop_inspector('system_time_status')
    def assert_status(self, **kwargs):
        """

        :param kwargs:
                     local_time: 00:00:00 ex: connect_time='"${value}".startswith("00:00")'
                     device_time: 00:00:00 ex: connect_time='"${value}".startswith("00:00")'
        :return:
        """
        self.access_menu('system.system_time')
        return self.eval_locator_attribute(kwargs, self.system_locators.system_time_status_locators)

    @allure.step('获取系统时间')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys: local_time device_time

        :return: 当key为列表或者元组时， 使用字典返回相关关键字的信息
        """
        self.access_menu('system.system_time')
        return self.get_text(keys, self.system_locators.system_time_status_locators)

    @allure.step('配置系统时间')
    def config(self, **kwargs):
        """ 配置系统时间, 无需配置时均不填写参数

        :param kwargs:
               time_zone: utc-12, utc-11, utc-10, utc-9, utc-8, utc-7, utc-6, utc-6_atlantic, utc-5, utc-5_colombia,
                          utc-4, utc-4_atlantic, utc-4_brazil, utc-3_30, utc-3, utc-3_brazil, utc-3_guyana, utc-2, utc-1, utc, utc_england,
                          utc+1, utc+1_france, utc+2, utc+2_greece, utc+3, utc+3_finland, utc+4, utc+5, utc+5_30, utc+6,
                          utc+7, utc+8, utc+9, utc+9_30, utc+10, utc+11, utc+12, utc+12_zealand
               time_zone_apply： True, False  ex time_zone_apply=True or time_zone_apply={'tip_messages': 'apply_success'}
               auto_daylight_saving_time: enable, disable ex: auto_daylight_saving_time='enable'
               sync_time: True, False ex: sync_time=True  or sync_time={'tip_messages': 'sync_success'}
               date: 2021-06-02 ex: date='2021-06-02'
               time_: 00:00:00 ex: time_='00:00:00'
               apply_time: True, False ex: apply_time=True or apply_time={'tip_messages': 'apply_success'}

               enable_sntp_clients: True, False ex: enable_sntp_clients=True
               sntp_interval: 60 ex: sntp_interval=60
               sntp_servers: [($action, **kwarg)]
                  ex: [('delete_all', )],
                 [('delete', '0.pool.ntp.org')]
                 [('add', {'server_address': '0.pool.ntp.org', 'port': '4444'})]
                     add parameter:
                     server_address:  0.pool.ntp.org ex: server_address="0.pool.ntp.org"
                     port: 4444 ex: port=4444
                     error_text: str or list
                     cancel: True, False
                 [('add', {'server_address': '0.pool.ntp.org', 'port': '4444', 'is_exists': '0.pool.ntp.org'})] 如果存在0.pool.ntp.org则不添加
                 [('edit', '0.pool.ntp.org', {'server_address': '1.pool.ntp.org'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit_sntp: True, False ex: submit_sntp=True or submit_sntp={'tip_messages': 'submit_success'}

               enable_ntp_server: True, False ex: enable_ntp_server=True
               pre_ntp_server: server_address ex: pre_ntp_server='0.pool.ntp.org'
               source_interface: Cellular 1、Bridge 1 ex: source_interface='Cellular 1'
               source_ip: 192.168.2.1 ex: source_ip='192.168.2.1'
               ntp_servers: [($action, **kwarg)]
                 ex: [('delete_all', )],
                 [('delete', '0.pool.ntp.org')]
                 [('add', {'server_address': '0.pool.ntp.org'})]
                     add parameter:
                     server_address:  0.pool.ntp.org ex: server_address="0.pool.ntp.org"
                     error_text: str or list
                     cancel: True, False
                 [('add', {'server_address': '0.pool.ntp.org',  'is_exists': '0.pool.ntp.org'})] 如果存在0.pool.ntp.org则不添加
                 [('edit', '0.pool.ntp.org', {'server_address': '1.pool.ntp.org'})]
                 [('enable', '0.pool.ntp.org', True)] or  [('enable', '0.pool.ntp.org', False)]
               error_text: str or list or tuple
               submit_ntp: True or False ex: submit_ntp=True  or  submit_ntp={'tip_messages': 'apply_success'}
               success_tip: True or False ex: success_tip=True or success_tip={'tip_messages': 'apply_success'}
        :return:
        """
        self.access_menu('system.system_time')
        self.agg_in(self.system_locators.system_time_locators, kwargs)


class Log(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('操作系统日志')
    def log(self, **kwargs):
        """

        :param kwargs:
                     recent_lines: 20,50,100,200,all ex: recent_lines='all'
                     refresh_policy: manual_refresh, 5sec, 10sec, 15sec, 30sec, 1min, 2min, 3min, 4min, 5min, 10min, 15min, 20min, 30min
                                     ex: refresh_policy='manual_refresh'
                     refresh: True, False ex: refresh=True or refresh={'wait_for_time': 3* 1000}
                     clear_history_log: True, False ex: clear_history_log=True
                     clear_log: True, False ex: clear_log=True
                     download_log: {'file_path': $file_path, 'file_name': $file_name} ex: download_log={'file_path': './tmp', 'file_name': 'log.log'}
                     download_history_log: {'file_path': $file_path, 'file_name': $file_name} ex: download_history_log={'file_path': './tmp', 'file_name': 'log.log'}
                     download_diagnostic_data: {'file_path': $file_path, 'file_name': $file_name} ex: download_diagnostic_data={'file_path': './tmp', 'file_name': 'log.log'}
        :return:
        """
        self.access_menu('system.log.log')
        if kwargs.get('refresh_policy') == 'manual_refresh' and kwargs.get('refresh') is None:
            kwargs.update({'refresh': {'wait_for_time': 3 * 1000}})
        if kwargs.get('clear_history_log') or kwargs.get('clear_log'):
            kwargs.update({'confirm': {'tip_messages': 'log_cleared'}})
        self.agg_in(self.system_locators.log_locators, kwargs)

    @allure.step('配置系统日志')
    def config(self, **kwargs):
        """ 配置系统时间, 无需配置时均不填写参数

        :param kwargs:
               enable_remote_server: True, False ex: enable_remote_server=True
               remote_server: [($action, **kwarg)]
                  ex: [('delete_all', )],
                 [('delete', 'log.server.com')]
                 [('add', {'server_address': 'log.server.com', 'port': '4444'})]
                     add parameter:
                     server_address:  0.pool.ntp.org ex: server_address="0.pool.ntp.org"
                     port: 4444 ex: port=4444
                     error_text: str or list
                     cancel: True, False
                 [('add', {'server_address': 'log.server.com', 'port': '4444', 'is_exists': 'log.server.com'})] 如果存在0.pool.ntp.org则不添加
                 [('edit', 'log.server.com', {'server_address': 'log.server.com.cn'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               log_to_console： check, uncheck  ex log_to_console='check'
               history_log_file_size: str, int ex: history_log_file_size='100' or history_log_file_size=100
               history_log_level: debug, information, notice, warning, error, serious, alarm, emergency ex: history_log_level='debug'
               error_text: str or list or tuple
               submit: True or False ex: submit=True  or  submit={'tip_messages': 'submit_success'}
               success_tip: True or False ex: success_tip=True or success_tip={'tip_messages': 'submit_success'}
        :return:
        """
        self.access_menu('system.log.configure')
        self.agg_in(self.system_locators.log_config_locators, kwargs)


class System:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.system_time: SystemTime = SystemTime(host, username, password, protocol, port, model, language, page,
                                                  locale)
        self.log: Log = Log(host, username, password, protocol, port, model, language, page, locale)
