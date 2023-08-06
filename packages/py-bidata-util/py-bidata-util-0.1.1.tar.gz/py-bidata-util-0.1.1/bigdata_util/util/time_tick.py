#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from . import get_logger
import time

logger = get_logger(__file__)


class TimeTick:
    """
    用于记录程序运行时间，用法：
    clock = TimeTick()
    # do A...
    clock.tick('task A'); # task A cost 1000 seconds.
    # do B...
    """
    def __init__(self):
        self.start = time.clock()
        self.current = self.start
        self.tick_cnt = 0
        pass

    def get_tick_message(self, label, time_diff):
        if not label:
            label = 'default label %d' % self.tick_cnt

        return '[TimeTick] - ' + label + ' cost %.2f seconds.' % time_diff
        pass

    def tick(self, label=''):
        current = time.clock()
        time_diff = current - self.current
        self.current = current

        self.tick_cnt += 1
        logger.info(self.get_tick_message(label, time_diff))
        pass

