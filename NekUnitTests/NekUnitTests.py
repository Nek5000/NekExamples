from tools.nekTestCase import *

###############################################################################
#  turbChannel
###############################################################################

@pn_pn_testcase
class TurbChannelPnPn(TurbChannel):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_GmresSerial(self):
        test_val = self.get_value(label='gmres: ', column=7,)
        self.assertAlmostEqual(test_val, 0., delta=95.)

    @parallel_test
    def test_GmresParallel(self):
        test_val = self.get_value(label='gmres: ', column=7)
        self.assertAlmostEqual(test_val, 0., delta=95.)

@pn_pn_2_testcase
class TurbChannelPnPn2(TurbChannel):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1-2'

    @serial_test
    def test_GmresSerial(self):
        test_val = self.get_value(label='gmres: ', column=6)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @parallel_test
    def test_GmresParallel(self):
        test_val = self.get_value(label='gmres: ', column=6)
        self.assertAlmostEqual(test_val, 0., delta=26.)

###############################################################################
#  2d_eigtest; eig1
###############################################################################

# TODO: implement 2d_eigtest, eig1

###############################################################################
#  3dbox, b3d
###############################################################################

#
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
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     def setUpClass(cls):
#         cls.get_opts()
#         run_meshgen('genbox', ['b3d.box'],
#                     cwd=os.path.join(cls.examples_root, cls.example_subdir))
#         mvn('box', 'b3d', cwd=os.path.join(cls.examples_root, cls.example_subdir))
#         run_nek_script()
#
#     def test_EndOfTimeStepLoopSerial(self):
#         cls     = self.__class__
#         logfile = cls.parallel_logs["1"] if cls.ifmpi else cls.serial_log
#         phrase  = get_phrase("end of time-step loop", logfile)
#         self.assertIsNotNone(phrase)
#
#     @skip_unless_mpi
#     def test_EndOfTimeStepLoopParallel(self):
#         cls     = self.__class__
#         logfile = cls.parallel_logs["4"]
#         phrase  = get_phrase("end of time-step loop", logfile)
#         self.assertIsNotNone(phrase)
#
# if __name__ == '__main__':
#     unittest.main()
#
# class BThreeD(NekTestCase)
#
#     example_subdir = '3dbox'

