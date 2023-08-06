import logging

from mxcubecore.model.common import (
    CommonCollectionParamters,
    PathParameters,
    LegacyParameters,
    StandardCollectionParameters,
)


class AbstractSimpleCollect(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def prepare_acquisition(self):
        pass
