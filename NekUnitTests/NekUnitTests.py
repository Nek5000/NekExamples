from tools.nekTestCase import *

###############################################################################
#  turbChannel: turbChannel.rea
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
#  2d_eigtest: eig1.rea
###############################################################################

# TODO: implement 2d_eigtest

###############################################################################
#  3dbox: b3d.rea
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
#  axi: axi.rea
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

####################################################################
#  benard: ray_9.rea, ray_dd.rea, ray_dn.rea, ray_nn.rea
####################################################################

# TODO: implement benard

####################################################################
#  blasius: blasius.rea
####################################################################

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

####################################################################
#  cone: cone.rea, cone016.rea, cone064.rea, cone256.rea
####################################################################

# TODO: implement cone

####################################################################
#  conj_ht: conj_ht.rea
####################################################################

@pn_pn_testcase
class ConjHtPnPn(ConjHt):

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

####################################################################
#  cyl_restart: ca.rea, cb.rea, pa.rea, pb.rea
####################################################################

@pn_pn_testcase
class CylRestartCaPnPn(CylRestartCa):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=85.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=85.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

@pn_pn_2_testcase
class CylRestartCaPnPn2(CylRestartCa):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=29.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=29.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

@pn_pn_testcase
class CylRestartCbPnPn(CylRestartCb):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=77.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=77.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

@pn_pn_2_testcase
class CylRestartCbPnPn2(CylRestartCb):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=28.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=28.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

@pn_pn_testcase
class CylRestartPaPnPn(CylRestartPa):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=85.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=85.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

@pn_pn_2_testcase
class CylRestartPaPnPn2(CylRestartPa):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=29.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=29.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

@pn_pn_testcase
class CylRestartPbPnPn(CylRestartPb):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=77.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=77.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)

@pn_pn_2_testcase
class CylRestartPbPnPn2(CylRestartPb):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=28.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=28.)

    @serial_test
    def test_serialError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

    @parallel_test
    def test_parallelError(self):
        test_val = self.get_value('dragy', column=-4, line=-1)
        self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)

####################################################################
#  eddy; eddy_uv.rea, amg_eddy.rea, htps_ed.rea
####################################################################

# TODO: implement eddy for amg_eddy.rea, htps_ed.rea

@pn_pn_testcase
class EddyEddyUvPnPn(EddyEddyUv):

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=34.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-7,)
        self.assertAlmostEqual(test_val, 0., delta=34.)

    @serial_test
    def test_serialXError(self):
        test_val = self.get_value('X err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 6.007702E-07, delta=1E-06)

    @parallel_test
    def test_parallelXError(self):
        test_val = self.get_value('X err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 6.007702E-07, delta=1E-06)

    @serial_test
    def test_serialYError(self):
        test_val = self.get_value('Y err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 6.489061E-07, delta=1E-06)

    @parallel_test
    def test_parallelYError(self):
        test_val = self.get_value('Y err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 6.489061E-07, delta=1E-06)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=80)

@pn_pn_2_testcase
class EddyEddyUvPnPn2(EddyEddyUv):

    lx2 = 'lx1-2'
    ly2 = 'ly1-2'
    lz2 = 'lz1'

    @serial_test
    def test_serialIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=22.)

    @parallel_test
    def test_parallelIter(self):
        test_val = self.get_value('gmres: ', column=-6,)
        self.assertAlmostEqual(test_val, 0., delta=22.)

    @serial_test
    def test_serialXError(self):
        test_val = self.get_value('X err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 6.759103E-05, delta=1E-06)

    @parallel_test
    def test_parallelXError(self):
        test_val = self.get_value('X err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 6.759103E-05, delta=1E-06)

    @serial_test
    def test_serialYError(self):
        test_val = self.get_value('Y err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 7.842019E-05, delta=1E-06)

    @parallel_test
    def test_parallelYError(self):
        test_val = self.get_value('Y err', column=-6, line=-1)
        self.assertAlmostEqual(test_val, 7.842019E-05, delta=1E-06)

    @serial_test
    def test_serialTime(self):
        test_val = self.get_value('total solver time', column=-2)
        self.assertAlmostEqual(test_val, 0.1, delta=80)

