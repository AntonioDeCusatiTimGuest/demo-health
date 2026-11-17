import logging
try:
    import rospy
except: 
    pass


class UtilLogs:

    @staticmethod
    def pylog_level(level):
        if level == 'DEBUG':
            return logging.DEBUG
        elif level == 'INFO':
            return logging.INFO
        elif level == 'WARNING':
            return logging.WARNING
        elif level == 'ERROR':
            return logging.ERROR
        else: 
            return logging.ERROR

    @staticmethod
    def roslog_level(level):
        if level == 'DEBUG':
            return rospy.DEBUG
        elif level == 'INFO':
            return rospy.INFO
        elif level == 'WARNING':
            return rospy.WARNING
        elif level == 'ERROR':
            return rospy.ERROR
        else: 
            return rospy.ERROR

    @staticmethod
    def ros_logger_format(logger_name, level):
        log_format = logging.Formatter(fmt='%(asctime)s - ROS - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.getLogger(logger_name).propagate = 0
        if not len(logging.getLogger(logger_name).handlers):
            ch = logging.StreamHandler()
            ch.setFormatter(log_format)
            logging.getLogger(logger_name).addHandler(ch)
        logging.getLogger(logger_name).setLevel(UtilLogs.pylog_level(level))
        
    @staticmethod
    def python_logger_format(logger_name, level): 
        log_format = logging.Formatter(fmt='%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.getLogger(logger_name).propagate = 0
        if not len(logging.getLogger(logger_name).handlers):
            ch = logging.StreamHandler()
            ch.setFormatter(log_format)
            logging.getLogger(logger_name).addHandler(ch)
        logging.getLogger(logger_name).setLevel(UtilLogs.pylog_level(level))