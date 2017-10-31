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

# ----------------------------------------------------------------------------------------------------------------------
# user set info
reserve_info = {
    "yuema":FSMr3_17A,
    "hanbing":FSMr3_17A,
    "laibao": FSMr4_17A,
    "loong": FSMr4_17A,
    "yahliu":FSMr4_17A
}
#single_run_flatform = [FSMr4_trunk]
single_run_flatform = [FSMr4_17A]
single_run_case = [
    "testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_50_UEs_VOIP.robot",#R4,cit,pass
    #"testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_1_UE_No_VOIP.robot",#cit
    #"testsuite/hangzhou/trunk/DevHZ1/LBT3217/LBT3217_ping_Idle_UE.robot",#crt
    "testsuite/hangzhou/trunk/DevHZ1/LTE2912/LTE2912-A-b_17_GBR_UL_QCI1.robot",#R4,crt,pass
    "testsuite/hangzhou/trunk/DevHZ1/LTE2912/LTE2912-A-b_15_NBR_DL.robot",#R4,crt,pass
    #"testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_1_A_a_modify_one_bearer.robot", #R4,cit,pass
    #"testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_2_A_a_modify_two_bearer.robot" #R4,crt,pass
]
single_run_for_17A_list =[
    #["testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_50_UEs_VOIP.robot",FSMr3_17A],
    ["testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_1_UE_No_VOIP.robot",FSMr3_17A],
    ["testsuite/hangzhou/trunk/DevHZ1/LBT3217/LBT3217_ping_Idle_UE.robot",FSMr3_17A],
    #["testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_1_A_a_modify_one_bearer.robot",FSMr3_17A],
    #["testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_2_A_a_modify_two_bearer.robot",FSMr3_17A],pass
    #["testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_50_UEs_VOIP.robot", FSMr4_17A], #pass
    #["testsuite/hangzhou/trunk/DevHZ1/LTE2912/LTE2912-A-b_17_GBR_UL_QCI1.robot", FSMr4_17A],
    #["testsuite/hangzhou/trunk/DevHZ1/LTE2912/LTE2912-A-b_15_NBR_DL.robot", FSMr4_17A],
    #["testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_1_A_a_modify_one_bearer.robot", FSMr4_17A],#pass
    ["testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_2_A_a_modify_two_bearer.robot", FSMr4_17A]
]
# ----------------------------------------------------------------------------------------------------------------------

single_run_log = "single_run.csv"
_reservation = CloudReservationApi(person_id)
_dispatcher = CloudDispatcherApi(person_id)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
log.addHandler(ch)
fh = logging.FileHandler(filename="log.txt", mode="a")
log.addHandler(fh)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s ")
ch.setFormatter(formatter)
fh.setFormatter((formatter))
log.info("set log information")


# log.setLevel(logging.DEBUG)

def reserve_a_server():
    _reservation.create_reservation(testline_type='CLOUD_F', enb_build=enb_build)


def reserve_servers():
    try:
        fb = open("reserve_info.csv", "r")
        pre_data = csv.reader(fb)
        pre_test_lines = []
        pre_test_lines = {egg[0]: egg[1] for egg in pre_data}
        log.info("pre reserved testline:{}".format(pre_test_lines))
        fb.close()
    except:
        pre_test_lines = []

    fb = open("reserve_info.csv", "wb")
    writer = csv.writer(fb)
    test_lines = []
    for name in reserve_info:
        person_id = persons_id[name]
        reservation = CloudReservationApi(person_id)
        reserve_type = reserve_info[name]
        if reserve_type == FSMr3_trunk:
            reserve_type1 = FSMr3_trunk
        elif reserve_type == FSMr4_trunk:
            reserve_type1 = FSMr4_trunk
        elif reserve_type == FSMr3_17A:
            reserve_type1 = FSMr3_17A
        elif reserve_type == FSMr4_17A:
            reserve_type1 = FSMr4_17A
        elif reserve_type == FSMr3_17SP:
            reserve_type1 = FSMr3_17SP
        elif reserve_type == FSMr4_17SP:
            reserve_type1 = FSMr4_17SP
        else: None
        cloud_type = reserve_type1['cloud_type']
        enb_build = reserve_type1['enb_build']
        ute_build = reserve_type1['ute_build']
        try:
            id = reservation.create_reservation(testline_type=cloud_type, enb_build=enb_build, ute_build=ute_build,
                                                duration=420)
            log.info("Succeed to reserve test line for token {},reserve_id is {}".format(name, id))
            test_lines.append([name, id])
        except ApiMaxReservationCountExceededException, e:
            log.info("Failed to reserve for token {},{}".format(name, e))
            if name in pre_test_lines.keys():
                test_lines.append([name, pre_test_lines[name]])
        except ApiUnauthorizedException, e:
            log.info("Failed to reserve for token {},e".format(name, e))
        except ApiParametersValidationFailException, e:
            log.info("Failed to reserve for token {},{}".format(name, e))
    writer.writerows(test_lines)
    fb.close()


def get_reservation_details():
    fb = open("reserve_info.csv", "r")
    reader = csv.reader(fb)
    for egg in reader:
        log.info("cloud test line:{},{},{}".format(egg[0], egg[1], _reservation.get_reservation_status(egg[1])))
        log.info(_reservation.get_reservation_details(egg[1]))
    fb.close()


def extend_reservation():
    fb = open("reserve_info.csv", "r")
    reader = csv.reader(fb)
    import datetime
    usable_testline = []
    for foo in reader:
        name = foo[0]
        reservation_id = foo[1]
        person_id = persons_id[name]
        reservation = CloudReservationApi(person_id)
        # log.info("cloud test line:{},{},{}".format(name, reservation_id, _reservation.get_reservation_status(reservation_id)))
        bar = reservation.get_reservation_details(reservation_id)
        print name
        log.info("testline:{},{},{},{},{}".format(name, bar['testline']['name'], bar['testline']['address'],bar['testline_type'],bar['enb_build']))
        try:
            reservation.extend_reservation(reservation_id, duration=180)
            log.info("succeed to extend")
            usable_testline.append([name, bar['testline']['name'], bar['testline']['address'], bar['enb_build'],bar['testline_type']])
        except ApiTooEarlyExtendAttemptException, e:
            log.info("failed to extend,{}".format(e))
            usable_testline.append([name, bar['testline']['name'], bar['testline']['address'], bar['enb_build'],bar['testline_type']])
        except ApiWrongReservationStatusFoundException, e:
            log.info("failed to extend,{}".format(e))
        except ApiUnknownException,e:
            log.info("failed to extend,{}".format(e))
    print "usable testline:"
    for foo in usable_testline:
        print foo
    fb.close()


def release_one_testline(release_reservation_owner):
    for foo in release_reservation_owner:
        reservation = CloudReservationApi(persons_id[foo])
        latest_reserve_id = reservation.list_my_reservations()[0]
        reservation.release_reservation(latest_reserve_id)
        log.info("{}:{} is released.".format(foo, latest_reserve_id))


def force_release():
    for foo in persons_id:
        reservation = CloudReservationApi(persons_id[foo])
        latest_reserve_id = reservation.list_my_reservations()[0]
        reservation.release_reservation(latest_reserve_id)
        log.info("{}:{} is released.".format(foo, latest_reserve_id))


def get_latest_reservation():
    for foo in persons_id:
        reservation = CloudReservationApi(persons_id[foo])
        latest_reserve_id = reservation.list_my_reservations()[0]
        log.info("{},{}.".format(foo, latest_reserve_id))


def get_reservation_status():
    print _reservation.get_reservation_status(915425)


def get_black_list():
    black_list = [case['path'] for case in _dispatcher.testsuite_blacklist_list()]
    return black_list


def move_one_case_from_black_list(case):
    _dispatcher.testsuite_blacklist_remove(case)
    print case + "is removed"


def remove_black_list():
    log.debug("in remove_black_list function")
    case_list = [
        "testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_50_UEs_VOIP.robot",
        "testsuite/hangzhou/trunk/DevHZ1/LTE2493/LTE2493_A_1_UE_No_VOIP.robot",
        "testsuite/hangzhou/trunk/DevHZ1/LBT3217/LBT3217_ping_Idle_UE.robot",
        "testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_1_A_a_modify_one_bearer.robot",
        "testsuite/hangzhou/trunk/DevHZ1/LTE1321/LTE1321_2_A_a_modify_two_bearer.robot"
    ]
    black_list = get_black_list()
    log.debug(black_list)
    for case in case_list:
        move_one_case_from_black_list(case) if case in black_list else None


def single_run():
    case_list = single_run_case
    fb = open(single_run_log,"a+")
    for env_info in single_run_flatform:
        for case in case_list:
            create_id = _dispatcher.create_single_run(
                test_path=case,
                testline_type=env_info['cloud_type'],
                enb_build=env_info['enb_build']
            )
            log.debug("{} is created on {} on {},create Id is {}".format(case, env_info['cloud_type'], env_info['enb_build'], create_id))
            fb.write("{},{},{},{},{},{},{}\n".format(case.split("/")[-1], create_id, env_info['cloud_type'],env_info['enb_build'],env_info['enb_build'].split("_")[0], env_info['enb_build'].split("_")[1], datetime.datetime.now().ctime()))
    fb.close()

def single_run_for_17A():
    fb = open(single_run_log,"a+")
    for case in single_run_for_17A_list:
        test_path = case[0]
        case_name = case[0].split("/")[-1]
        cloud_type = case[1]['cloud_type']
        enb_build = case[1]['enb_build']
        create_id = _dispatcher.create_single_run(
            test_path=test_path,
            testline_type=cloud_type,
            enb_build=enb_build
        )
        log.debug("{} is created on {} on {},create Id is {}".format(test_path, cloud_type, enb_build, create_id))
        fb.write("{},{},{},{},{},{},{}\n".format(case_name, create_id, cloud_type, enb_build, enb_build.split("_")[0], enb_build.split("_")[1], datetime.datetime.now().ctime()))
    fb.close()

def get_run_status():
    print _dispatcher.get_test_execution_status(991733)


def help():
    log.debug("set help")


# get_black_list()
# remove_black_list()
# single_run()
# get_reservation_status()

if __name__ == "__main__":
    log_opts = ["help", "create", "reserve", "remove", "verbose", "branch"]
    options, args = getopt.getopt(sys.argv[1:], 'hsrRvstemfg', log_opts)

    for (command, arg) in options:
        if command in ['-v', '--verbose']:
            log.debug("before set to verbose method")
            log.setLevel(logging.DEBUG)
            log.debug("set to verbose method")
        elif command in ['-h', '--help']:
            help()
        elif command in ['-s', '--single']:
            single_run()
        elif command in ['-r', '--reserve']:
            reserve_servers()
        elif command in ['-R', '--remove']:
            log.debug("Remove case from black list")
            remove_black_list()
        elif command in ['-s']:
            log.debug("get run status")
            get_run_status()
        elif command in ['-t']:
            log.debug("get reservation details")
            get_reservation_details()
        elif command in ['-e']:
            log.debug("extend reservations")
            extend_reservation()
        elif command in ['-m']:
            log.debug("release_one_testline")
            release_one_testline(["laibao","loong","yahliu"])
        elif command in ['-f']:
            log.debug("force release_one_testline all")
            force_release()
        elif command in ['-g']:
            get_latest_reservation()
        elif command in ['--branch']:
            single_run_for_17A()
        else:
            pass
