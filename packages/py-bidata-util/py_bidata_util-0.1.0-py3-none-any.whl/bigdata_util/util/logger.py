#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import sys
import os


class MyLogger(logging.Logger):
    def debug(self, msg, *args, **kwargs):
        self.check_stdout()
        return super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.check_stdout()
        return super().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.check_stdout()
        return super().warning(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.check_stdout()
        return super().warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.check_stdout()
        return super().error(msg, *args, **kwargs)

    def check_stdout(self):
        self.clear_parent()
        stdout_list = list(filter(
            lambda x: x.name == 'stdout',
            self.handlers
        ))
        if len(stdout_list) > 0:
            stdout_list[0].stream = sys.stdout
        pass

    def clear_parent(self):
        c = self
        trace = 0
        while c:
            if trace > 0 and len(c.handlers) > 0:
                c.handlers = []
            if not c.propagate:
                c = None
            else:
                c = c.parent
            trace += 1
        pass


# 设置为我们自己的类
logging.setLoggerClass(MyLogger)


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    if os.environ.get('APP_ENV') is not None and os.environ.get('APP_ENV').lower().startswith('prod'):
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(level)
    
    # 确保多次调用时，只加一个handler
    handler_name = 'stdout'
    stdout_handler = list(filter(
        lambda x: x.name == handler_name,
        logger.handlers
    ))
    if len(stdout_handler) == 0:
        # handler = logging.StreamHandler(open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1))
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.set_name(handler_name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
