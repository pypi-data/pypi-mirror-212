import pathlib
from unittest import TestCase

import numpy as np

CURRENT_DIR_PATH = pathlib.Path(__file__).parent.absolute()


class BaseTestCase(TestCase):
    EXAMPLE_TRACKING_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("example_resources/alb_tracking_mode_record.osef")
    )
    LIGHT_TRACKING_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("resources/light_tracking_record.osef")
    )
    SLAM_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("example_resources/alb_slam_mode_record.osef")
    )
    PASSTHROUGH_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("example_resources/alb_passthrough_mode_record.osef")
    )
    EDGE_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("resources/edge_tracking_record.osef")
    )
    OBJECT_SLAM_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("resources/object_slam_record.osef")
    )
    ZONE_3D_FILEPATH = str(CURRENT_DIR_PATH.joinpath("resources/3d_zones_record.osef"))
    MOBILE_TRACKING_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("resources/mobile_tracking_record.osef")
    )
    MOBILE_TRACKING_GPS_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("resources/mobile_tracking_gps_record.osef")
    )
    PRECISE_GPS_ROAD_MARKINGS_FILEPATH = str(
        CURRENT_DIR_PATH.joinpath("resources/gps_precise_road_markings.osef")
    )
    ONE_FRAME_TRACKING_RECORD = str(
        CURRENT_DIR_PATH.joinpath("example_resources/one_frame_tracking_record.osef")
    )
    CARLA_OSEF_RECORD = str(
        CURRENT_DIR_PATH.joinpath("resources/point_cloud_carla.osef")
    )
    DIVERGENCE_RECORD = str(
        CURRENT_DIR_PATH.joinpath("resources/divergence_record.osef")
    )
    BACKGROUND_STREAM_RECORD = str(
        CURRENT_DIR_PATH.joinpath("resources/background_stream_edge_to_fusion.osef")
    )
    LIDAR_SPEED_RECORD = str(CURRENT_DIR_PATH.joinpath("resources/lidar_speeds.osef"))
    MAPPING_RECORD = str(CURRENT_DIR_PATH.joinpath("resources/mapping.osef"))
    COVARIANCES_RECORD = str(CURRENT_DIR_PATH.joinpath("resources/covariances.osef"))

    ALL_RECORD_PATHS = [
        EXAMPLE_TRACKING_FILEPATH,
        LIGHT_TRACKING_FILEPATH,
        SLAM_FILEPATH,
        PASSTHROUGH_FILEPATH,
        EDGE_FILEPATH,
        OBJECT_SLAM_FILEPATH,
        ZONE_3D_FILEPATH,
        MOBILE_TRACKING_FILEPATH,
        MOBILE_TRACKING_GPS_FILEPATH,
        PRECISE_GPS_ROAD_MARKINGS_FILEPATH,
        ONE_FRAME_TRACKING_RECORD,
        CARLA_OSEF_RECORD,
        DIVERGENCE_RECORD,
        BACKGROUND_STREAM_RECORD,
        LIDAR_SPEED_RECORD,
        MAPPING_RECORD,
        COVARIANCES_RECORD,
    ]

    OSEF_SPEC_FILEPATH = str(CURRENT_DIR_PATH.joinpath("resources/osefTypes.yaml"))

    def compare_dict(self, ref_dict: dict, dict_to_check: dict):
        for key, value in ref_dict.items():
            if isinstance(value, dict):
                self.compare_dict(value, dict_to_check[key])
            elif isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict):
                    for index, elem in enumerate(value):
                        self.compare_dict(elem, dict_to_check[key][index])
                else:
                    self.assertEqual(value, dict_to_check[key])
            elif isinstance(value, np.ndarray):
                if value.dtype.names is None:
                    np.testing.assert_almost_equal(value, dict_to_check[key])
                else:
                    self.assertEqual(value.tolist(), dict_to_check[key].tolist())
            else:
                self.assertEqual(value, dict_to_check[key])
