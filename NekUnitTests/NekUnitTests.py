from tools.nekTestCase import *
from tools.nekFileParse import *

###############################################################################
#  turbChannel
###############################################################################

class TurbChannelPnPn(NekTestCase):

    example_subdir = 'turbChannel'
    rea_file       = 'turbChannel'

    meshgen = ['genmap', 'turbchannel', '0.5']

    serial_script     = 'nek10s'
    serial_log_suffix = '.pn-pn.serial'

    parallel_script     = 'nek10steps'
    parallel_log_suffix = '.pn-pn.parallel'

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    def test_GmresSerial(self):
        cls      = self.__class__
        logfile  = cls.parallel_logs["1"] if cls.ifmpi else cls.serial_log
        test_val = get_value(label='gmres: ', column=7, logfile=logfile)
        self.assertAlmostEqual(test_val, 0., delta=95.)

    @skip_unless_mpi
    def test_GmresParallel(self):
        cls = self.__class__
        logfile  = cls.parallel_logs["4"]
        test_val = get_value(label='gmres: ', column=7, logfile=logfile)
        self.assertAlmostEqual(test_val, 0., delta=95.)

class TurbChannelPnPn2(NekTestCase):

    example_subdir = "turbChannel"
    rea_file       = 'turbChannel'

    serial_script     = 'nek10s'
    serial_log_suffix = '.pn-pn-2.serial'

    parallel_script     = 'nek10steps'
    parallel_log_suffix = '.pn-pn-2.parallel'

    meshgen = ['genmap', 'turbchannel', '0.5']

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1-2'

    def test_GmresSerial(self):
        cls      = self.__class__
        logfile  = cls.parallel_logs["1"] if cls.ifmpi else cls.serial_log
        test_val = get_value(label='gmres: ', column=6, logfile=logfile)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @skip_unless_mpi
    def test_GmresParallel(self):
        cls = self.__class__
        logfile  = cls.parallel_logs["4"]
        test_val = get_value(label='gmres: ', column=6, logfile=logfile)
        self.assertAlmostEqual(test_val, 0., delta=26.)

###############################################################################
#  2d_eigtest; eig1
###############################################################################

# TODO: implement 2d_eigtest, eig1

###############################################################################
#  3dbox, b3d
###############################################################################


# class ThreeDBoxPnPn(NekTestCase):
#
#     example_subdir = '3dbox'
#     rea_file       = 'b3d'
#
#     serial_script     = 'nek10s'
#     serial_log_suffix = '.pn-pn.serial'
#
#     parallel_script     = 'nek10steps'
#     parallel_log_suffix = '.pn-pn.parallel'
#
#     meshgen = ['genmap', 'turbchannel', '0.5']
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     def test_GmresSerial(self):
#         """ Greps gmres from logs """
#         cls = self.__class__
#         if not cls.ifmpi:
#             logfile      = cls.serial_log
#         else:
#             logfile      = cls.parallel_logs["1"]
#         self.check_value(
#             logfile      = logfile,
#             label        = 'gmres: ',
#             target_value = 0.,
#             delta        = 95.,
#             column       = 7
#         )
#
#     @skip_unless_mpi
#     def test_GmresParallel(self):
#         """ Greps gmres from logs """
#         cls = self.__class__
#         self.check_value(
#             logfile      = cls.parallel_logs["4"],
#             label        = 'gmres: ',
#             target_value = 0.,
#             delta        = 95.,
#             column       = 7
#         )


if __name__ == '__main__':
    unittest.main()
