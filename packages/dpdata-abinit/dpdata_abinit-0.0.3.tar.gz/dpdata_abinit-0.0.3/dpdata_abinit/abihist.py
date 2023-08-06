from dpdata.format import Format
from dpdata_abinit.histnc import to_system_data

@Format.register("abihist")
class AbihistFormat(Format):
    def from_system(self, fname, **kwargs):
        return None

    def from_labeled_system(self, fname, **kwargs):
        return to_system_data(fname)



