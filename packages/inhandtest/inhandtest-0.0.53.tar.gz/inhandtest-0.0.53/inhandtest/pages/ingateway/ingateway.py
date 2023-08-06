# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 16:09:27
# @Author  : Pane Li
# @File    : ingateway.py
"""
ingateway

"""
import logging

from playwright.sync_api import Page
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.edge_computing.python_edge_computing import EdgeComputing
from inhandtest.pages.ingateway.network.network import Network
from inhandtest.pages.ingateway.overview.overview import Overview
from inhandtest.pages.ingateway.system.system import System
from inhandtest.pages.locale import in_setting
from inhandtest.telnet import Telnet


class InGateway(BasePage):

    def __init__(self, host: str, super_user: str, super_password: str, page: Page = None, model='IG902',
                 language='en', protocol='https', port=443, username='adm', password='123456', telnet=True):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=in_setting)
        if telnet:
            self.telnet = Telnet(model, host, super_user, super_password)
        else:
            self.telnet = None
        if self.language == 'en':
            self.telnet.send_cli(command='language English', type_='user')
        else:
            self.telnet.send_cli(command='language Chinese', type_='user')
        self.login()
        self.overview = Overview(host, username, password, protocol, port, model, language, self.page, self.locale)
        self.network: Network = Network(host, username, password, protocol, port, model, language, self.page,
                                        self.locale)
        self.edge = EdgeComputing(host, username, password, protocol, port, model, language, self.page, self.locale)
        self.system = System(host, username, password, protocol, port, model, language, self.page, self.locale)


if __name__ == '__main__':
    from inhandtest.tools import enable_log

    enable_log(console_level=logging.DEBUG)
    with InGateway('10.5.24.96', 'inhand', '64391099@inhand') as device:
        device.system.log.config(remote_server=[('add', {'server_address': 'log.server.com', 'port': 514})],
                                 log_to_console=True, history_log_file_size=100, history_log_level='warning',
                                 submit={'tip_messages': 'submit_success'})
        device.page.wait_for_timeout(10 * 1000)
