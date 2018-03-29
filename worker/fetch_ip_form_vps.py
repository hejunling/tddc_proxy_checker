# coding: utf-8
'''
Created on 2017年3月14日

@author: chenyitao
'''
import logging

import gevent
from paramiko.client import SSHClient


log = logging.getLogger(__name__)


class FetchIPFromVPS(object):
    """
    ADSL IP 管理
    """

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = self._remote()

    def get_ip(self):
        if self._check():
            return self._get_ip()
        for _ in range(15):
            self._redial()
            if self._check():
                return self._get_ip()
            gevent.sleep(1)

    def _check(self):
        ip = self._get_ip()
        if ip:
            if self._test():
                return ip
        return None

    def _remote(self):
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(hostname=self.host,
                       port=self.port,
                       username=self.username,
                       password=self.password)
        return client

    def redial(self):
        """
        重拨
        :return:
        """
        self._redial()
        return self.get_ip()

    def _redial(self):
        self.client.exec_command('pppoe-stop')
        self.client.exec_command('sleep 1')
        self.client.exec_command('pppoe-start')

    def _get_ip(self):
        _, stdout, stderr = self.client.exec_command('ifconfig')
        info = stdout.readlines()
        info = ''.join(info).split('ppp0')
        if len(info) != 2:
            log.warning('Network "ppp0" Not Found.')
            return None
        info = info[1]
        start_pos = info.find('inet') + 4# 任务回队列 时间重置
        end_pos = info.find('netmask')
        ip = info[start_pos: end_pos].strip()
        return ip if len(ip.split('.')) == 4 else None

    def _test(self):
        _, stdout, stderr = self.client.exec_command('curl baidu.com')
        info = ''.join(stdout.readlines())
        return info.find('content="0;url=http://www.baidu.com/"') > 0

    def _close(self):
        self.client.close()

    def __del__(self):
        self._close()


def main():
    print(FetchIPFromVPS().get_ip())


if __name__ == '__main__':
    main()
