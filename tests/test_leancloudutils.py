import unittest
from package_leancloud_utils import leancloud_utils as plu

__author__ = 'Jayvee'


class MyLeancloudTest(unittest.TestCase):
    # init unittest
    def setUp(self):
        pass

    # exit unittest
    def tearDown(self):
        pass

    def test_get_remote_data(self):
        # app_dict = plu.DataObject.AppDict()
        # case 1
        result = plu.LeancloudUtils.get_remote_data('app_dict', 0)
        self.assertEqual(result, [])

        # case 2
        expected_result = [{"app": "cn.jj", "degree": 0.9, "label": "gamer"},
                           {"app": "com.autonavi.minimap", "degree": 0.5, "label": "has_car"},
                           {"app": "com.android.cheyooh", "degree": 0.9, "label": "has_car"},
                           {"app": "cld.navi.mainframe", "degree": 0.5, "label": "has_car"},
                           {"app": "com.kplus.car", "degree": 0.9, "label": "has_car"},
                           {"app": "com.sdu.didi.gui", "degree": 1, "label": "has_car"},
                           {"app": "cn.eclicks.wzsearch", "degree": 0.9, "label": "has_car"},
                           {"app": "cn.com.tiros.android.navidog", "degree": 0.9, "label": "has_car"},
                           {"app": "com.autohome.mycar", "degree": 0.9, "label": "has_car"},
                           {"app": "cn.buding.martin", "degree": 0.8, "label": "has_car"}]
        result = plu.LeancloudUtils.get_remote_data('app_dict', 10)
        self.assertEqual(len(result) > 0, True)
