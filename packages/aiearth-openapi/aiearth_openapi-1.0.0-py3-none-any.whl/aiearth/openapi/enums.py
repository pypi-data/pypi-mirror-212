from enum import Enum


class PublishStatus(Enum):
    """
    影像发布的状态
    """
    # 发布排队中
    WAITING_SCHEDULED = "WAITING_SCHEDULED"
    # 发布中
    WAITING = "WAITING"
    # 发布成功
    PUBLISHDONE = "PUBLISHDONE"
    # 发布失败
    PUBLISHFAIL = "PUBLISHFAIL"


class JobStatus(Enum):
    """
    任务运行的状态
    """
    # 提交任务准备中
    SUBMITTING = 5
    # 任务排队中
    WAITING = 0
    # 任务已经完成
    FINISHED = 1
    # 任务已经失败
    ERROR = 2
    # 任务进行中
    PROCESSING = 3


class AIJobAPP(Enum):
    """
    AI解译任务的APP
    """
    # 建筑物提取
    BUILDING_EXTRACTION = "building_extraction"
    # 大棚提取
    GREENHOUSE_EXTRACTION = "greenhouse_extraction"
    # 地物分类
    LAND_COVER_CLASSIFICATION = "land_cover_classification"
    # 光伏电厂识别
    PV_PLANT = "pv_plant"
    # 拦河坝识别
    BARRAGE = "barrage"
    # 通用变化检测
    CONSTRUCTION_CHANGE = "construction_change"
    # 变化多分类
    MULTICLASS = "multiclass"
    # 地块提取
    FARMLAND_EXTRACTION_REMOTE_SENSING = "farmland_extraction_remote_sensing"
    # SAR水体提取
    SAR_WATER = "sar_water"
    # 建筑物变化检测
    BUILDING_CHANGE = "building_change"
    # 农田变化检测
    FARMLAND_CHANGE = "farmland_change"
    # 去雾处理
    REMOVE_CLOUD_HAZE = "remove_cloud_haze"
    # 路网提取
    ROADMAP_EXTRACT = "roadmap_extract"
    # 路网中心线提取
    ROADMAP_MIDLINE_EXTRACT = "roadmap_midline_extract"
    # 云检测
    CLOUD_DETECTION = "cloud_detection"
    # 通用变化检测（中分辨率）
    SENTINEL2_CD = "sentinel2_cd"
    # 哨兵2地物分类
    LOW_RESOLUTION_LANDCOVER = "low_resolution_landcover"
    # 风机提取
    WIND_TURBINE_EXTRACTION = "wind_turbine_extraction"
    # 自训练通用变化检测
    TRAINING_NEW_COMMON_CHANGE_DETECTION = "training_new_common_change_detection"
    # 自训练地物分类
    TRAINING_NEW_LAND_CLASSIFICATION = "training_new_land_classification"
    # 自训练多分类变化检测
    TRAINING_NEW_MULTI_CHANGE_DETECTION = "training_new_multi_change_detection"
    # 自训练目标提取
    TRAINING_NEW_OBJECT_EXTRACTION = "training_new_object_extraction"


class RasterFileType(Enum):
    """
    栅格影像文件类型
    """
    TIFF = "tiff"
    IMG = "img"


class AttachRasterFileType(Enum):
    """
    栅格影像附属文件的类型
    """
    RPB = "rpb"
    RPC = "rpc"
    TFW = "tfw"
    IGE = "ige"


class MapServiceProjectionType(Enum):
    """
    地图服务投影类型
    """
    # 经纬度投影
    LONGLAT = "longlat"
    # 墨卡托投影
    MERCATOR = "mercator"


class UserDataFromType(Enum):
    """
    个人数据来源类型
    """
    # 个人上传数据
    PERSONAL = "personal"
    # 任务（AI，GIS基础工具）产出结果
    RESULT = "result"
    # 开发者模式导出任务
    DEVELOPER_EXPORT = "developer_export"


class DataType(Enum):
    """
    数据类型
    """
    # 栅格
    RATSER = "raster"
    # 矢量
    VECTOR = "vector"
    # 地图服务
    MAP_SERVICE = "map_service"

class DownloadStatus(Enum):
    INITED = "inited"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"

class JobOutDataType(Enum):
    RASTER = 0
    VECTOR = 1