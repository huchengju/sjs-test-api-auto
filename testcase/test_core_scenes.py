# -*- coding: UTF-8 -*-

from public.base.test_sjs_darp_api import TestDarp
import pytest, os
from config import globalparam
from public.common.response import Response
from public.common.tools import load
from public.common.log import reqTime



class TestCoreScenes(object):

    def setup(self):

        test_data = os.path.join(globalparam.config_file_path, "sjs_darp_api", 'request.json')
        self.data = load(test_data)
        self.test_core = TestDarp()
        self.test_core.setup()
        self.r = Response()

    def teardown(self):
        pass

    @pytest.mark.scenes
    def test_darp_company_add(self):
        test_data = self.data['darp_admin_login']['requestdata']
        test_data['userName'] = ''
        test_data['password'] = ''
        res = self.test_core.test_darp_admin_login(test_data)
        assert res.get('code') == 200





if __name__ == '__main__':

    # pytest.main(["-s","test_core_scenes.py::TestCoreScenes::test_tx_list_eth"])
    # pytest.main(["-s","test_core_scenes.py::TestCoreScenes"])
    pytest.main(["-s","-k","test_estimatefeetxs_eth"])
#     pytest.main(["-m","scenes"])
