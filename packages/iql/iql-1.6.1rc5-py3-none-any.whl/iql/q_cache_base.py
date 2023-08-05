# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved
#


class QueryCacheBase:
    def save(self, key: str, data: object, prefix: str = "default", policy={}):
        pass

    def get(self, key: str, prefix: str = "default", policy={}) -> object:
        return None

    def clear(
        self,
        key: str,
        prefix: str = "default",
    ):
        pass

    def clear_all(self):
        pass
