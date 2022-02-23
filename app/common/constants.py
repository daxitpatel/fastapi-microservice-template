""" Third Party API List """
RABBITMQ_QUEUES_REPORT_API = "{rabbitmq_host}/api/queues/"
RABBITMQ_QUEUES_DETAILS_API = "{rabbitmq_host}/api/queues/{virtual_host}/{queue}"

RABBITMQ_CONSUMER_HEALTH_TEST_API = '/consumer-health-test'
APP_READINESS_API = '/k8/readiness'
APP_LIVENESS_API = '/k8/liveness'
APP_TERMINATION_API = '/k8/termination'


""" Date Format """
DT_FMT_dmy = '%d/%m/%y'  # 31/12/17
DT_FMT_bdYIMp = '%b %d %Y %I:%M %p'  # Jul 16 2017 08:46 PM
DT_FMT_ymdHMSf = '%Y-%m-%d %H:%M:%S.%f'  # 2017-07-19 06:58:20.370
DT_FMT_ymdHMSfz = '%Y-%m-%d %H:%M:%S.%f%z'  # 2017-07-19 06:58:20.370+00:00
DT_FMT_ymdHMS = '%Y-%m-%d %H:%M:%S'  # 2017-07-19 06:58:20
DT_FMT_Ymd = '%Y-%m-%d'  # 2017-09-11
DT_FMT_YMD = '%Y/%m/%d'
DT_FMT_ymdHM = '%Y-%m-%d %H:%M'
DT_FMT_dbYHMS = '%d-%b-%Y %H:%M:%S'
DT_FMT_dbYHMSf = '%d-%b-%Y %H:%M:%S.%f'
DT_FMT_HM = '%H:%M'
DT_FMT_ymdTHMSf = "%Y-%m-%dT%H:%M:%S.%f"
# Date Time format
YYYY_MM_DD_HH_MM_SS = "%Y-%m-%d %H:%M:%S"


# Request Headers
WT_CORRELATION_ID = 'CORRELATION_ID'
WT_USER_ID = 'USER_ID'


PREFETCH_COUNT = 'prefetch_count'

IGNORE_PATH_LOG = ['/k8/readiness', '/k8/liveness']
