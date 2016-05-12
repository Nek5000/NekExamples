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
    def test_gmres_parallel(self):
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

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

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

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1-2'

    @serial_test
    def test_endOfTimeStepLoop_serial(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

    @parallel_test
    def test_endOfTimeStepLoop_parallel(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

###############################################################################
#  3dbox, b3d
###############################################################################

@pn_pn_testcase
class AxiPnPn(Axi):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_pres_serial(self):
        val = self.get_value('PRES: ', column=4)
        self.assertAlmostEqual(val, 0., delta=76.)

    @parallel_test
    def test_pres_parallel(self):
        val = self.get_value('PRES: ', column=4)
        self.assertAlmostEqual(val, 0., delta=76.)

    @serial_test
    def test_totalSolverTime_serial(self):
        val = self.get_value('total solver time', column=2)
        self.assertAlmostEqual(val, 0.1, delta=2)


@pn_pn_2_testcase
class AxiPnPn2(Axi):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_uPress_serial(self):
        val = self.get_value('U-Press ', column=5)
        self.assertAlmostEqual(val, 0., delta=104.)

    @parallel_test
    def test_uPress_parallel(self):
        val = self.get_value('U-Press ', column=5)
        self.assertAlmostEqual(val, 0., delta=104.)

    @serial_test
    def test_totalSolverTime_serial(self):
        val = self.get_value('total solver time', column=2)
        self.assertAlmostEqual(val, 0.1, delta=4)
