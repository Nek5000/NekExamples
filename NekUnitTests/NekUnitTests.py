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
    def test_serialIter(self):
        test_val = self.get_value(label='gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=95.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value(label='gmres: ', column=-7)
        self.assertAlmostEqual(test_val, 0., delta=95.)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value(label='total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=200.)


@pn_pn_2_testcase
class TurbChannelPnPn2(TurbChannel):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1-2'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value(label='gmres: ', column=-6)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value(label='gmres: ', column=-6)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value(label='total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=140.)

###############################################################################
#  2d_eigtest
###############################################################################

# TODO: implement 2d_eigtest

###############################################################################
#  3dbox
###############################################################################

@pn_pn_testcase
class ThreeDBoxPnPn(ThreeDBox):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serial(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

    @parallel_test
    def test_parallel(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

@pn_pn_2_testcase
class ThreeDBoxPnPn2(ThreeDBox):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1-2'

    @serial_test
    def test_serial(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

    @parallel_test
    def test_parallel(self):
        phrase = self.get_phrase("end of time-step loop")
        self.assertIsNotNone(phrase)

###############################################################################
#  axi
###############################################################################

@pn_pn_testcase
class AxiPnPn(Axi):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        val = self.get_value('PRES: ', column=-4)
        self.assertAlmostEqual(val, 0., delta=76.)

    @parallel_test
    def test_parallelIter(self):
        val = self.get_value('PRES: ', column=-4)
        self.assertAlmostEqual(val, 0., delta=76.)

    @serial_test
    def test_serialTime(self):
        val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(val, 0.1, delta=2)


@pn_pn_2_testcase
class AxiPnPn2(Axi):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        val = self.get_value('U-Press ', column=-5)
        self.assertAlmostEqual(val, 0., delta=104.)

    @parallel_test
    def test_parallelIter(self):
        val = self.get_value('U-Press ', column=-5)
        self.assertAlmostEqual(val, 0., delta=104.)

    @serial_test
    def test_serialTime(self):
        val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(val, 0.1, delta=4)

####################################################################"
#  benard
####################################################################"

# TODO: implement benard

####################################################################"
#  blasius
####################################################################"

@pn_pn_testcase
class BlasiusPnPn(Blasius):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=162.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=162.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('delta', column=-5, line=-1)
        self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('delta', column=-5, line=-1)
        self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=30)

@pn_pn_2_testcase
class BlasiusPnPn2(Blasius):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=125.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=125.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('delta', column=-5, line=-1)
        self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('delta', column=-5, line=-1)
        self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=30)

####################################################################"
#  cone
####################################################################"

# TODO: implement cone

####################################################################"
#  conj_ht
####################################################################"

@pn_pn_testcase
class ConjHtPnPn(ConjHt):

    # TODO:

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=46.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=46.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('tmax', column=-2, line=-1)
        self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('tmax', column=-2, line=-1)
        self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=7)

@pn_pn_2_testcase
class ConjHtPnPn2(ConjHt):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=26.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('tmax', column=-2, line=-1)
        self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('tmax', column=-2, line=-1)
        self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=7)
