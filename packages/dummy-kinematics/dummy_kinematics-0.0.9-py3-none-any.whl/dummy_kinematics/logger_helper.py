import logging

class Logger_helper:

    @staticmethod
    def init_logger():
        """生成logger, 默认同时输出到console和log文件

        Returns logger
        -------
        """

        logger = logging.getLogger(__name__)

        # 文件和console格式
        file_handler_formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s - %(filename)s -%(pathname)s")
        console_handler_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s",
                                                      datefmt="%Y-%m-%d %H:%M:%S")

        # 文件hdler
        file_handler = logging.FileHandler(
            filename="./testlog.log", encoding="utf-8")
        file_handler.setFormatter(fmt=file_handler_formatter)
        file_handler.setLevel(level=logging.DEBUG)

        # console hdler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt=console_handler_formatter)
        console_handler.setLevel(level=logging.DEBUG)

        # logger settings
        logger.setLevel(level=logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


logger = Logger_helper.init_logger()