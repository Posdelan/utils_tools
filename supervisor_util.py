#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
import supervisor.xmlrpc


__author__ = 'Posdelan'
__version__ = '0.1'


class SuperClint(object):
    def __init__(self, socket_url_path):
        self.unix_socket_url = socket_url_path
        self.RUNNING = 20
        self.STARTING = 10
        self.STOPPED = 0
        try:
            self.rpc_proxy = xmlrpclib.Server('http://127.0.0.1', transport=supervisor.xmlrpc.SupervisorTransport(None, None, serverurl=self.unix_socket_url))
        except Exception as err:
            print 'connet err: %s' % err.message

    def get_all_process_info(self):
        """
        获取所有进程信息
        :return:
        """
        try:
            process_infos = self.rpc_proxy.supervisor.getAllProcessInfo()
            return process_infos
        except:
            return False

    def get_process_info(self, app_name):
        """
        获取指定process
        :return:
        """
        try:
            process_info = self.rpc_proxy.supervisor.getProcessInfo(app_name)
            return process_info
        except:
            return False

    def stop_process(self, app_name):
        """
        关闭指定进程
        :param app_name:
        :return:
        """
        # 需要首先判断该进程是否存在，并且还是运行状态
        if self.check_process_status(app_name, self.STARTING, self.RUNNING):
            return self.rpc_proxy.supervisor.stopProcess(app_name)
        return True

    def restart_process(self, app_name):
        """
        重启指定进程
        :param app_name:
        :return:
        """
        self.stop_process(app_name)
        return self.start_process(app_name)

    def start_process(self, app_name):
        """
        开启指定进程
        :param app_name:
        :return:
        """
        if self.check_process_status(app_name, self.STOPPED):
            return self.rpc_proxy.supervisor.startProcess(app_name)
        return True

    def check_process_status(self, app_name, *args):
        """
        检查process的运行状态

        """
        process_info = self.get_process_info(app_name=app_name)
        if process_info:
            state = process_info.get('state')
            if state not in args:
                return False
            return True

    def restart_all_apps(self):
        """
        重启所有的进程
        :return:
        """
        stop_state = self.rpc_proxy.supervisor.stopAllProcess()
        start_state = self.rpc_proxy.supervisor.startAllProcess()
        return stop_state and start_state

    def stop_all_apps(self):
        """
        关闭所有进程
        :return:
        """
        return self.rpc_proxy.supervisor.stopAllProcesses()

    def start_all_apps(self):
        """
        开启所有进程
        :return:
        """
        return self.rpc_proxy.supervisor.startAllProcesses()


def main():
    """
    main process
    """


if __name__ == '__main__':
    unix_socket_url = """unix:///home/centos/supervisor.sock"""
    supervisor_client = SuperClint(socket_url_path=unix_socket_url)
    # print supervisor_client.start_process(app_name='app_name')
    # print supervisor_client.stop_all_apps()
    print supervisor_client.get_process_info(app_name='')
    main()