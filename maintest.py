# coding:utf-8

import sys
import time
import pytest

from config import url,globalparam
from public.common.terminal import Shell
from public.common.sendmail import SendMail
from public.common.log import Log

# 测试报告路径
rp = globalparam.report_path
# 指定目录执行
test_path = 'testcase/'

''' jenkins 执行 '''
# if __name__ == '__main__':
#
#     mark_label = "-m"
#     if (len(sys.argv) > 0):
#         if (sys.argv[1].startswith("-m")):
#             mark_label = sys.argv[1]
#         report = sys.argv[2]
#         env = sys.argv[3]
#
#     '''指定标签执行'''
#     pytest.main([mark_label,
#                  '--alluredir',
#                  report,
#                  "--envopt",
#                  env
#                  ])
    # sendmail = SendMail()
    # sendmail.send_report("test", report_url)


'''脚本内执行'''
if __name__ == '__main__':

    shell = Shell()
    log = Log()

    t = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    allure_result_path = '{0}/result/{1}/xml/'.format(rp, t)
    allure_report_path = '{0}/result/{1}/html/'.format(rp, t)

    pytest.main([
                '-m',
                 "darp_api and api_smoke",
                 '--alluredir',
                 allure_result_path,
                 "--envopt",
                 "testing"
                 ])

    cmd = 'allure generate --clean %s -o %s' % (allure_result_path, allure_report_path)

    try:
        message = shell.invoke(cmd)
        log.info(message)
        log.info('shell 执行成功！！')

    except Exception:
        log.error('执行用例失败，请检查环境配置')
        raise

    # sendmail = SendMail()
    # sendmail.send_report("test", report_url)
