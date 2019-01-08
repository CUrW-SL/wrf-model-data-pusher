from config import \
    BASE_DIR, \
    RUN_DIR, \
    DATE_FORMAT, \
    STATION_TMS_FILE_NAME, \
    TIME_INDEX_FILE_NAME, \
    STATIONS, \
    WRF_MODELS, \
    DB_CONFIG, \
    TMS_META

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from os import path

from data_layer.base import get_engine, get_sessionmaker
from data_layer.timeseries import Timeseries


def read_time_index(run_dir, time_index_file_name):
    time_index_fp = path.join(run_dir, time_index_file_name)
    with open(time_index_fp) as time_index_file:
        tmi = pd.read_csv(time_index_file, parse_dates=True, names=['time'], index_col=0)
        return tmi.index


def read_rainfall(run_dir, file_name):
    rainfall_fp = path.join(run_dir, file_name)
    arr = np.loadtxt(rainfall_fp)
    return arr


def separate_rainfall_for_event_types(zeroth_day, rainfall_data_frame):
    _0_d = zeroth_day
    _1_d_before = _0_d - timedelta(days=1)
    _1_d_after = _0_d + timedelta(days=1)
    _2_d_after = _0_d + timedelta(days=2)
    _3_d_after = _0_d + timedelta(days=3)

    rainfall_1_d_before = rainfall_data_frame.loc[_1_d_before:(_0_d - timedelta(seconds=1))]
    rainfall_0_d = rainfall_data_frame.loc[_0_d:(_1_d_after - timedelta(seconds=1))]
    rainfall_1_d_after = rainfall_data_frame.loc[_1_d_after:(_2_d_after - timedelta(seconds=1))]
    rainfall_2_d_after = rainfall_data_frame.loc[_2_d_after:(_3_d_after - timedelta(seconds=1))]

    return [
        {'event_type_id_in_db': 15, 'event_type': 'Forecast-1-d-before', 'rainfall': rainfall_1_d_before},
        {'event_type_id_in_db': 16, 'event_type': 'Forecast-0-d', 'rainfall': rainfall_0_d},
        {'event_type_id_in_db': 17, 'event_type': 'Forecast-1-d-after', 'rainfall': rainfall_1_d_after},
        {'event_type_id_in_db': 18, 'event_type': 'Forecast-2-d-after', 'rainfall': rainfall_2_d_after},
    ]


today = datetime.strptime(datetime.utcnow().strftime(DATE_FORMAT), DATE_FORMAT)
run_date = today - timedelta(days=1)
run_dir = path.join(BASE_DIR, RUN_DIR.format(run_date=run_date.strftime(DATE_FORMAT)))
TIME_INDEX = read_time_index(run_dir, TIME_INDEX_FILE_NAME)

print("######### Startting for %s ##########" % run_date.strftime(DATE_FORMAT))
for station in STATIONS:
    for wrf_model in WRF_MODELS:

        rainfall_file_name = STATION_TMS_FILE_NAME.format(
            station_name=station['name'],
            model_name=wrf_model['name'],
            run_date=run_date.strftime(DATE_FORMAT)
        )
        rainfall_arr = read_rainfall(run_dir, rainfall_file_name)[0: TIME_INDEX.size]
        rainfall_df = pd.DataFrame({'time': TIME_INDEX, 'value': rainfall_arr}).set_index(keys='time')

        db_engine = get_engine(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            db=DB_CONFIG['db']
        )
        tms_adapter = Timeseries(get_sessionmaker(engine=db_engine))

        TMS_META['station_name'] = station['name_in_db']
        TMS_META['source'] = wrf_model['name_in_db']

        tmss = separate_rainfall_for_event_types(today, rainfall_df)
        for tms in tmss:
            TMS_META['event_type'] = tms['event_type']
            tms_id = tms_adapter.get_timeseries_id(TMS_META)
            if tms_id is None:
                tms_id = tms_adapter.create_timeseries_id(
                    run_name=TMS_META['run_name'],
                    station={'name': station['name_in_db'], 'id': station['id_in_db']},
                    event_type={'name': tms['event_type'], 'id': tms['event_type_id_in_db']},
                    source={'name': wrf_model['name_in_db'], 'id': wrf_model['id_in_db']},
                    variable={'name': TMS_META['variable'], 'id': TMS_META['variable_id']},
                    unit={'name': TMS_META['unit'], 'id': TMS_META['unit_id']}
                )
            tms_adapter.update_timeseries(tms_id, tms['rainfall'], True)
            print("Pushed data to tms_id: %s" % tms_id)
