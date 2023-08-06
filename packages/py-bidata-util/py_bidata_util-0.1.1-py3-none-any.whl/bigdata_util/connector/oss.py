#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import oss2
from pydash import _


class OssConnector(oss2.Bucket):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0], dict):
            endpoint = _.get(args[0], 'endpoint')
            bucket_name = _.get(args[0], 'bucket')
            auth = oss2.Auth(_.get(args[0], 'accessId'), _.get(args[0], 'accessKey'))
            args = (auth, endpoint, bucket_name)
            super(OssConnector, self).__init__(*args, **kwargs)
        else:
            super(OssConnector, self).__init__(*args, **kwargs)
        pass
    
    def run(self):
        pass


if __name__ == '__main__':
    OssConnector().run()

