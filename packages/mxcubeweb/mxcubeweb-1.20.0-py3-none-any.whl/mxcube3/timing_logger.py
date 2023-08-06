import logging
import os

from logging.handlers import TimedRotatingFileHandler


def enable_timing_logger(log_file):
    fname = log_file + ".timing"
    timing_logger = logging.getLogger("timing")
    fmt = "%(asctime)s |%(name)-7s|%(levelname)-7s| %(message)s"
    log_formatter = logging.Formatter(fmt)

    timing_log_file_handler = TimedRotatingFileHandler(
        fname, when="midnight", backupCount=7
    )

    os.chmod(fname, 0o666)

    timing_log_file_handler.setFormatter(log_formatter)

    timing_logger.setLevel(logging.DEBUG)
    timing_logger.addHandler(timing_log_file_handler)

    LOG_LEVEL_ENTER_NUM = 10
    LOG_LEVEL_EXIT_NUM = 11

    logging.addLevelName(LOG_LEVEL_ENTER_NUM, "START")
    logging.addLevelName(LOG_LEVEL_EXIT_NUM, "END")

    def start(self, tag, message="", *args, **kws):
        if self.isEnabledFor(LOG_LEVEL_ENTER_NUM):
            # Yes, logger takes its '*args' as 'args'.
            self._log(LOG_LEVEL_ENTER_NUM, tag.upper() + " | " + message, args, **kws)

    logging.Logger.start = start

    def end(self, tag, message="", *args, **kws):
        if self.isEnabledFor(LOG_LEVEL_EXIT_NUM):
            # Yes, logger takes its '*args' as 'args'.
            self._log(LOG_LEVEL_EXIT_NUM, tag.upper() + " | " + message, args, **kws)

    logging.Logger.end = end
