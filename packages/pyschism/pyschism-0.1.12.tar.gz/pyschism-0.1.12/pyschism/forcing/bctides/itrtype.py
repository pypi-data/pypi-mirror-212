from pyschism.forcing.bctides.bctypes import Bctype


class Itrtype(Bctype):

    @property
    def itrtype(self) -> int:
        '''Returns integer representig SCHISM itrtype code for bctides.in'''

    @property
    def forcing_digit(self):
        return self.itrtype

    def get_boundary_string(self, hgrid, boundary):
        return ''


class UniformTimeHistoryTracer(Itrtype):

    def __init__(self, time_history):
        raise NotImplementedError(f'{self.__class__.__name__}')
        self.time_history = time_history

    @property
    def itrtype(self) -> int:
        return 1


class ConstantTracer(Itrtype):

    def __init__(self, value):
        raise NotImplementedError(f'{self.__class__.__name__}')
        self.value = value

    @property
    def itrtype(self) -> int:
        return 2


class TracerInitialConditions(Itrtype):

    def __init__(self):
        raise NotImplementedError(f'{self.__class__.__name__}')

    @property
    def itrtype(self):
        return 3


class SpatiallyVaryingTimeHistoryTracer(Itrtype):

    def __init__(self, data_source):
        self.data_source = data_source

    @property
    def itrtype(self):
        return 4


class Itrtype1(UniformTimeHistoryTracer):
    pass


class Itrtype2(ConstantTracer):
    pass


class Itrtype3(TracerInitialConditions):
    pass


class Itrtype4(SpatiallyVaryingTimeHistoryTracer):
    pass
