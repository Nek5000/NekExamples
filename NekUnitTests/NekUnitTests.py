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
    def test_gmres_serial(self):
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
    def test_gmres_serial(self):
        test_val = self.get_value(label='gmres: ', column=6)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @parallel_test
    def test_gmres_parallel(self):
        test_val = self.get_value(label='gmres: ', column=6)
        self.assertAlmostEqual(test_val, 0., delta=26.)

###############################################################################
#  2d_eigtest; eig1
###############################################################################

# TODO: implement 2d_eigtest, eig1

###############################################################################
#  3dbox, b3d
###############################################################################

@pn_pn_testcase
class ThreeDBoxPnPn(ThreeDBox):

    lx = 'lx1'
    ly = 'ly1'
    lz = 'lz1'

    @serial_test
    def test_endOfTimeStepLoop_serial(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

    @parallel_test
    def test_endOfTimeStepLoop_parallel(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

@pn_pn_2_testcase
class ThreeDBoxPnPn2(ThreeDBox):

    lx = 'lx1-2'
    ly = 'ly1-2'
    lz = 'lz1-2'

    @serial_test
    def test_endOfTimeStepLoop_serial(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

    @parallel_test
    def test_endOfTimeStepLoop_parallel(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)
