BASE_DIR = "/mnt/disks/wrf-mod"
RUN_DIR = "STATIONS_{run_date}"
DATE_FORMAT = "%Y-%m-%d"

STATION_TMS_FILE_NAME = "{station_name}_{model_name}_{run_date}.txt"
TIME_INDEX_FILE_NAME = "dates.txt"

STATIONS = [
    {'name': 'Waga', 'id_in_db': 100045, 'name_in_db': 'Waga'},
    {'name': 'Urumewella', 'id_in_db': 100063, 'name_in_db': 'Urumewella'},
    {'name': 'Ruwanwella', 'id_in_db': 300003, 'name_in_db': 'Ruwanwella'},
    {'name': 'Orugodawatta', 'id_in_db': 100038, 'name_in_db': 'Orugodawatta'},
    {'name': 'Norwood', 'id_in_db': 100008, 'name_in_db': 'Norwood'},
    {'name': 'Norton_reservoir', 'id_in_db': 100074, 'name_in_db': 'Norton Reservoir'},
    {'name': 'Naula', 'id_in_db': 100072, 'name_in_db': 'Naula'},
    {'name': 'Mutwal', 'id_in_db': 100061, 'name_in_db': 'Mutwal'},
    {'name': 'Mulleriyawa', 'id_in_db': 100057, 'name_in_db': 'Mulleriyawa'},
    {'name': 'Malabe', 'id_in_db': 100059, 'name_in_db': 'Malabe'},
    {'name': 'Mahapallegama', 'id_in_db': 100039, 'name_in_db': 'Mahapallegama'},
    {'name': 'Kottawa', 'id_in_db': 100042, 'name_in_db': 'Kottawa North Dharmapala School'},
    {'name': 'Kotmale', 'id_in_db': 100073, 'name_in_db': 'Kotmale'},
    {'name': 'Kitulgala', 'id_in_db': 100007, 'name_in_db': 'Kitulgala'},
    {'name': 'Jaffna', 'id_in_db': 100040, 'name_in_db': 'Jaffna'},
    {'name': 'Ibattara2', 'id_in_db': 100043, 'name_in_db': 'IBATTARA2'},
    {'name': 'Holombuwa', 'id_in_db': 100006, 'name_in_db': 'Holombuwa'},
    {'name': 'Hingurana', 'id_in_db': 100037, 'name_in_db': 'Hingurana'},
    {'name': 'Glencourse', 'id_in_db': 100004, 'name_in_db': 'Glencourse'},
    {'name': 'Dickoya', 'id_in_db': 100060, 'name_in_db': 'Dickoya'},
    {'name': 'Deraniyagala', 'id_in_db': 300004, 'name_in_db': 'Deraniyagala'},
    {'name': 'Ambewela', 'id_in_db': 100046, 'name_in_db': 'Ambewela Farm'},
]

TMS_META = {
    'run_name': 'evening_18hrs',
    'station_name': '',
    'variable': 'Precipitation',
    'variable_id': 1,
    'unit': 'mm',
    'unit_id': 1,
    'event_type': '',
    'source': ''
}

WRF_MODELS = [
    {'name': 'A', 'name_in_db': 'wrfv3A', 'id_in_db': 31},
    {'name': 'C', 'name_in_db': 'wrfv3C', 'id_in_db': 32},
    {'name': 'E', 'name_in_db': 'wrfv3E', 'id_in_db': 33},
    {'name': 'SE', 'name_in_db': 'wrfv3SE', 'id_in_db': 34}
]

DB_CONFIG = {
    "host": "",
    "port": 3306,
    "user": "",
    "password": "",
    "db": "curw"
}
