from ute_cloud_reservation_api.api import CloudReservationApi
from ute_cloud_dispatcher_api.api import CloudDispatcherApi
from  ute_cloud_reservation_api.exception import *
from ute_cloud_common_api.exception import *
import getopt
import sys
import os
import logging
import csv
import datetime

# if __name__ == '__main__' and __package__ is None:
#     from os import sys, path
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#     print CloudReservationApi.__doc__

persons_id = {
    "hanbing":"41343a5b14d0d0bada0543f2633f742c988dfd1a",
    "yuema": "3a2d5fc66950f9ecda31da236f5953d959aeae87",
    "laibao": "d97d6034ba7c3fb1e559850644a8a07e73cee976",
    "loong": "bb8b43faf1a446e89cda8569f3e708f650d70dfc",
    "yahliu": "53a005825bb2fab4f419f53ad19c057ea3c5c79a"
}
person_id = persons_id['yuema']
FSMr4_trunk = {
    'enb_build': "TL00_FSM4_9999_170622_016673",
    'cloud_type': 'CLOUD_R4P_L',
    'ute_build': '1726.01.00'
}
FSMr3_trunk = {
    'enb_build': "TL00_ENB_9999_170618_063166",
    'cloud_type': 'CLOUD_F',
    'ute_build': '1726.00.01'
}
FSMr4_17A = {
    'enb_build': "TL17A_ENB_0000_000085_000004",
    'cloud_type': 'CLOUD_R4P_L',
    'ute_build': '1726.01.00'
}
FSMr3_17A = {
    'enb_build': "TL17A_ENB_0000_000085_000004",
    'cloud_type': 'CLOUD_F',
    'ute_build': '1726.01.00'
}

# user set info
reserve_info = {
    "yuema":FSMr3_17A,
    "hanbing":FSMr3_17A,
    "laibao": FSMr4_17A,
    "loong": FSMr4_17A,
    "yahliu":FSMr4_17A
}





if __name__ == "__main__":
    log_opts = ["help", "create", "reserve", "remove", "verbose", "branch"]
    options, args = getopt.getopt(sys.argv[1:], 'hsrRvstemfg', log_opts)
    print options,args