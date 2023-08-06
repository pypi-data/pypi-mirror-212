# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 14:29:16
# @Author  : Pane Li
# @File    : system_locators.py
"""
system_locators

"""
from playwright.sync_api import Page


class SystemTimeLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')
        self.utc_key = (
            'utc-12', 'utc-11', 'utc-10', 'utc-9', 'utc-8', 'utc-7', 'utc-6', 'utc-6_atlantic', 'utc-5',
            'utc-5_colombia', 'utc-4', 'utc-4_atlantic', 'utc-4_brazil', 'utc-3_30', 'utc-3', 'utc-3_brazil',
            'utc-3_guyana', 'utc-2', 'utc-1', 'utc', 'utc_england,', 'utc+1', 'utc+1_france', 'utc+2', 'utc+2_greece',
            'utc+3', 'utc+3_finland', 'utc+4', 'utc+5', 'utc+5_30', 'utc+6', 'utc+7', 'utc+8', 'utc+9', 'utc+9_30',
            'utc+10', 'utc+11', 'utc+12', 'utc+12_zealand')

    @property
    def system_time_status_locators(self) -> list:
        return [
            ('local_time',
             {'locator': self.page.locator(f'//label[text()="{self.locale.local_time}"]').locator('../../div[2]'),
              'type': 'text'}),
            ('device_time',
             {'locator': self.page.locator(f'//label[text()="{self.locale.device_time}"]').locator(
                 '../../div[2]/div/span/div/span'), 'type': 'text'}),
        ]

    @property
    def system_time_locators(self) -> list:
        return [
            ('time_zone', {'locator': self.page.locator('.ant-select.ant-select-enabled').first, 'type': 'select',
                           'param': {utc: self.locale.get(utc) for utc in self.utc_key}}),
            ('time_zone_apply',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-round').nth(0),
              'type': 'button'}),
            ('auto_daylight_saving_time',
             {'locator': self.page.locator('.ant-checkbox-input'), 'type': 'check'}),
            ('sync_time',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-round').nth(1), 'type': 'button'}),
            ('date', {'locator': self.page.locator('#date'), 'type': 'fill_date'}),
            ('time_', {'locator': self.page.locator('.ant-time-picker'), 'type': 'fill_date'}),
            ('apply_time',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-round').nth(2), 'type': 'button'}),
            ('enable_sntp_clients', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('sntp_interval', {'locator': self.page.locator('#update_interval'), 'type': 'text',
                               'relation': [('enable_sntp_clients', True)]}),
            ('sntp_servers', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('server_address', {'locator': self.pop_up.locator('#server_addr'), 'type': 'text'}),
                    ('port', {'locator': self.pop_up.locator('#port'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr', 'relation': [('enable_sntp_clients', True)]}),
            ('submit_sntp',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(0),
              'type': 'button'}),
            ('enable_ntp_server', {'locator': self.page.locator('#enable').nth(1), 'type': 'switch_button'}),
            ('pre_ntp_server', {'locator': self.page.locator('#master'), 'type': 'text',
                                'relation': [('enable_ntp_server', True)]}),
            ('source_interface', {'locator': self.page.locator('#source_interface'), 'type': 'select',
                                  'relation': [('enable_ntp_server', True)]}),
            ('source_ip', {'locator': self.page.locator('#source_ip'), 'type': 'select',
                           'relation': [('enable_ntp_server', True)]}),
            ('ntp_servers', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox'),
                'action_confirm': self.page.locator('.ant-popover-inner').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm'),
                "columns": [
                    ('server_address', {'locator': self.pop_up.locator('#server_addr'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr'}),
            ('submit_ntp',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(1),
              'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
        ]


class LogLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def log_locators(self) -> list:
        return [
            ('recent_lines',
             {'locator': self.page.locator('.ant-select-sm.ant-select.ant-select-enabled'), 'type': 'select',
              'param': {'all': self.locale.all_}}),
            ('refresh_policy', {'locator': self.page.locator('.ant-select.ant-select-enabled').nth(1), 'type': 'select',
                                'param': {'manual_refresh': self.locale.manual_refresh, 'sec': self.locale.sec,
                                          'min': self.locale.min}}),
            ('refresh', {'locator': self.page.locator('.ant-btn.ant-btn-sm'), 'type': 'button'}),
            (
                'clear_history_log',
                {'locator': self.page.locator('//button[@class="ant-btn"]').nth(0), 'type': 'button'}),
            ('clear_log', {'locator': self.page.locator('//button[@class="ant-btn"]').nth(1), 'type': 'button'}),
            ('download_log',
             {'locator': self.page.locator('//button[@class="ant-btn"]').nth(2), 'type': 'download_file'}),
            ('download_history_log',
             {'locator': self.page.locator('//button[@class="ant-btn"]').nth(3), 'type': 'download_file'}),
            ('download_diagnostic_data',
             {'locator': self.page.locator('//button[@class="ant-btn"]').nth(4), 'type': 'download_file'}),
            ('confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary.ant-btn-sm'),
              'type': 'button'}),

        ]

    @property
    def log_config_locators(self) -> list:
        return [
            ('enable_remote_server', {'locator': self.page.locator('#log_to_remote_enable'), 'type': 'check'}),
            ('remote_server', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('server_address', {'locator': self.pop_up.locator('#server_addr'), 'type': 'text'}),
                    ('port', {'locator': self.pop_up.locator('#server_port'), 'type': 'text'}),
                    ('errors_text', {'type': 'text_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                ]}, 'type': 'table_tr', 'relation': [('enable_remote_server', True)]}),
            ('log_to_console', {'locator': self.page.locator('#log_to_console'), 'type': 'check'}),
            ('history_log_file_size',
             {'locator': self.page.locator('//input[@class="ant-input-number-input"]'), 'type': 'text'}),
            ('history_log_level',
             {'locator': self.page.locator('.ant-select.ant-select-enabled'), 'type': 'select',
              'param': {'emergency': self.locale.emergency, 'alarm': self.locale.alarm,
                        'serious': self.locale.serious, 'error': self.locale.error, 'warning': self.locale.warning,
                        'notice': self.locale.notice, 'information': self.locale.information,
                        'debug': self.locale.debug}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit), 'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
        ]


class ConfigLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def config_locators(self) -> list:
        return [
            ('auto_save', {'locator': self.page.locator('//button[@role="switch"]').nth(0), 'type': 'switch_button'}),
            ('encrypted', {'locator': self.page.locator('//button[@role="switch"]').nth(1), 'type': 'switch_button'}),
            ('import_startup_config', {'locator': self.page.locator('//button[@class="ant-btn"]'), 'type': 'upload_file'}),
            ('import_config',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]').nth(0), 'type': 'button'}),
            ('reboot',
             {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'), 'type': 'button'}),

            ('export_startup_config',
             {'locator': self.page.locator('.ant-select.ant-select-enabled'), 'type': 'select',
              'param': {'emergency': self.locale.emergency, 'alarm': self.locale.alarm,
                        'serious': self.locale.serious, 'error': self.locale.error, 'warning': self.locale.warning,
                        'notice': self.locale.notice, 'information': self.locale.information,
                        'debug': self.locale.debug}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit), 'type': 'button'}),
            ('errors_text', {'type': 'text_messages'}),
            ('success_tip', {'type': 'tip_messages'}),
        ]


class SystemLocators(SystemTimeLocators, LogLocators):
    pass
