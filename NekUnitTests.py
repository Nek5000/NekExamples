from tools.nekTestCase import *

###############################################################################
#  turbChannel: turbChannel.rea
###############################################################################

class TurbChannel(NekTestCase):

    example_subdir  = 'turbChannel'
    rea_file        = 'turbChannel'
    serial_script   = 'nek10s'
    parallel_script = 'nek10steps'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap(tol='0.5')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek()

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek()

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek()

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=140., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek()

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=140., label='total solver time')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ###############################################################################
# #  2d_eigtest: eig1.rea
# ###############################################################################
#
# # TODO: implement 2d_eigtest
#
# ###############################################################################
# #  3dbox: b3d.rea
# ###############################################################################

class ThreeDBox(NekTestCase):
    example_subdir  = '3dbox'
    rea_file        = 'b3d'
    box_file        = 'b3d'
    serial_script   = 'nek10s'
    parallel_script = 'nek10steps'

    def setUp(self):
        self.build_tools(['clean', 'genbox', 'genmap'])
        self.run_genbox()
        self.mvn('box', self.__class__.rea_file)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek()

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek()

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek()

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek()

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()
#
# ###############################################################################
# #  axi: axi.rea
# ###############################################################################
#
# @pn_pn_testcase
# class AxiPnPn(Axi):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         val = self.get_value('PRES: ', column=-4)
#         self.assertAlmostEqual(val, 0., delta=76.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         val = self.get_value('PRES: ', column=-4)
#         self.assertAlmostEqual(val, 0., delta=76.)
#
#     @serial_test
#     def test_serialTime(self):
#         val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(val, 0.1, delta=2)
#
#
# @pn_pn_2_testcase
# class AxiPnPn2(Axi):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         val = self.get_value('U-Press ', column=-5)
#         self.assertAlmostEqual(val, 0., delta=104.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         val = self.get_value('U-Press ', column=-5)
#         self.assertAlmostEqual(val, 0., delta=104.)
#
#     @serial_test
#     def test_serialTime(self):
#         val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(val, 0.1, delta=4)
#
# ####################################################################
# #  benard: ray_9.rea, ray_dd.rea, ray_dn.rea, ray_nn.rea
# ####################################################################
#
# # TODO: implement benard
#
# ####################################################################
# #  blasius: blasius.rea
# ####################################################################
#
# @pn_pn_testcase
# class BlasiusPnPn(Blasius):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=162.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=162.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('delta', column=-5, line=-1)
#         self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('delta', column=-5, line=-1)
#         self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=30)
#
# @pn_pn_2_testcase
# class BlasiusPnPn2(Blasius):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=125.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=125.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('delta', column=-5, line=-1)
#         self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('delta', column=-5, line=-1)
#         self.assertAlmostEqual(test_val, 1.26104, delta=1e-05)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=30)
#
# ####################################################################
# #  cone: cone.rea, cone016.rea, cone064.rea, cone256.rea
# ####################################################################
#
# # TODO: implement cone
#
# ####################################################################
# #  conj_ht: conj_ht.rea
# ####################################################################
#
# @pn_pn_testcase
# class ConjHtPnPn(ConjHt):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=46.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=46.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('tmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('tmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=7)
#
# @pn_pn_2_testcase
# class ConjHtPnPn2(ConjHt):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=26.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=26.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('tmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('tmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 1.31190E+01, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=7)
#
# ####################################################################
# #  cyl_restart: ca.rea, cb.rea, pa.rea, pb.rea
# ####################################################################
#
# @pn_pn_testcase
# class CylRestartCaPnPn(CylRestartCa):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=85.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=85.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
# @pn_pn_2_testcase
# class CylRestartCaPnPn2(CylRestartCa):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=29.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=29.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
# @pn_pn_testcase
# class CylRestartCbPnPn(CylRestartCb):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=77.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=77.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
# @pn_pn_2_testcase
# class CylRestartCbPnPn2(CylRestartCb):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=28.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=28.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
# @pn_pn_testcase
# class CylRestartPaPnPn(CylRestartPa):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=85.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=85.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
# @pn_pn_2_testcase
# class CylRestartPaPnPn2(CylRestartPa):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=29.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=29.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
# @pn_pn_testcase
# class CylRestartPbPnPn(CylRestartPb):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=77.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=77.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.37986119139E-03, delta=1E-06)
#
# @pn_pn_2_testcase
# class CylRestartPbPnPn2(CylRestartPb):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=28.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=28.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 5.09547531705E-02, delta=1E-06)
#
# ####################################################################
# #  eddy; eddy_uv.rea, amg_eddy.rea, htps_ed.rea
# ####################################################################
#
# # TODO: implement eddy for amg_eddy.rea, htps_ed.rea
#
# @pn_pn_testcase
# class EddyEddyUvPnPn(EddyEddyUv):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=34.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=34.)
#
#     @serial_test
#     def test_serialXError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 6.007702E-07, delta=1E-06)
#
#     @parallel_test
#     def test_parallelXError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 6.007702E-07, delta=1E-06)
#
#     @serial_test
#     def test_serialYError(self):
#         test_val = self.get_value('Y err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 6.489061E-07, delta=1E-06)
#
#     @parallel_test
#     def test_parallelYError(self):
#         test_val = self.get_value('Y err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 6.489061E-07, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=80)
#
# @pn_pn_2_testcase
# class EddyEddyUvPnPn2(EddyEddyUv):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=22.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=22.)
#
#     @serial_test
#     def test_serialXError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 6.759103E-05, delta=1E-06)
#
#     @parallel_test
#     def test_parallelXError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 6.759103E-05, delta=1E-06)
#
#     @serial_test
#     def test_serialYError(self):
#         test_val = self.get_value('Y err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 7.842019E-05, delta=1E-06)
#
#     @parallel_test
#     def test_parallelYError(self):
#         test_val = self.get_value('Y err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 7.842019E-05, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=80)
#
# ####################################################################
# #  eddy_neknek: eddy_neknek.rea
# ####################################################################
#
# # TODO: implment eddy_neknek tests
#
# ####################################################################
# #  eddy_psi_omega; psi_eddy.rea
# ####################################################################
#
# @pn_pn_testcase
# class EddyPsiOmegaPnPn(EddyPsiOmega):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 1.177007E-10, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 1.177007E-10, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=17)
#
# @pn_pn_2_testcase
# class EddyPsiOmegaPnPn2(EddyPsiOmega):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 1.177007E-10, delta=1E-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('X err', column=-6, line=-1)
#         self.assertAlmostEqual(test_val, 1.177007E-10, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=17)
#
# ####################################################################
# #  expansion: expansion.rea
# ####################################################################
#
# # TODO: implement expansion tests
#
# ####################################################################
# #  ext_cyl; ext_cyl.rea
# ####################################################################
#
# @pn_pn_testcase
# class ExtCylPnPn(ExtCyl):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=85.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=85.)
#
#     @serial_test
#     def test_serialXError(self):
#         test_val = self.get_value('dragx', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 1.2138790E+00, delta=1E-06)
#
#     @parallel_test
#     def test_parallelXError(self):
#         test_val = self.get_value('dragx', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 1.2138790E+00, delta=1E-06)
#
#     @serial_test
#     def test_serialYError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 1.3040301E-07, delta=1E-06)
#
#     @parallel_test
#     def test_parallelYError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 1.3040301E-07, delta=1E-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=400)
#
# @pn_pn_2_testcase
# class ExtCylPnPn2(ExtCyl):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=26.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=26.)
#
#     @serial_test
#     def test_serialXError(self):
#         test_val = self.get_value('dragx', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 1.2138878E+00, delta=1e-05)
#
#     @parallel_test
#     def test_parallelXError(self):
#         test_val = self.get_value('dragx', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 1.2138878E+00, delta=1e-05)
#
#     @serial_test
#     def test_serialYError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 3.2334222E-07, delta=1e-06)
#
#     @parallel_test
#     def test_parallelYError(self):
#         test_val = self.get_value('dragy', column=-4, line=-1)
#         self.assertAlmostEqual(test_val, 3.2334222E-07, delta=1e-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2)
#         self.assertAlmostEqual(test_val, 0.1, delta=380)
#
# ####################################################################
# #  fs_2; st1.rea, st2.rea, std_wv.rea
# ####################################################################

# TODO: fs_2/st1.rea tests fail legacy test suite and should be fixed
class Fs2_St1(NekTestCase):
    example_subdir  = 'fs_2'
    rea_file        = 'st1'
    serial_script   = 'nek200s'
    parallel_script = 'nek200steps'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap(tol='0.5')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek()

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek()

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek()

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=6.382414E-01, delta=1e-06, label='amp')

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=18.3, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek()

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=6.382414E-01, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# @pn_pn_testcase
# class Fs2St2PnPn(Fs2St2):
#
#     # TODO: These tests fail in legacy test suite and should be fixed
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serial(self):
#         phrase = self.get_phrase("ABORT: ")
#         self.assertIsNotNone(phrase)
#
#     @parallel_test
#     def test_parallel(self):
#         phrase = self.get_phrase("ABORT: ")
#         self.assertIsNotNone(phrase)
#
# @pn_pn_2_testcase
# class Fs2St2PnPn2(Fs2St2):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=38.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=38.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('amp', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 6.376171E-01, delta=1e-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('amp', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 6.376171E-01, delta=1e-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2,)
#         self.assertAlmostEqual(test_val, 0.1, delta=23)
#
# @pn_pn_testcase
# class Fs2StdWvPnPn(Fs2StdWv):
#
#     # TODO: These tests fail in legacy test suite and should be fixed
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serial(self):
#         phrase = self.get_phrase("ABORT: ")
#         self.assertIsNotNone(phrase)
#
#     @parallel_test
#     def test_parallel(self):
#         phrase = self.get_phrase("ABORT: ")
#         self.assertIsNotNone(phrase)
#
# @pn_pn_2_testcase
# class Fs2StdWvPnPn2(Fs2StdWv):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=20.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=20.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('amp', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 1.403287E-01, delta=1e-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('amp', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 1.403287E-01, delta=1e-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2,)
#         self.assertAlmostEqual(test_val, 0.1, delta=21)
#
# ####################################################################
# #  fs_hydro: fs_hydro.rea
# ####################################################################
#
# @pn_pn_testcase
# class FsHydroPnPn(FsHydro):
#
#     # TODO: These tests fail in legacy test suite and should be fixed
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serial(self):
#         phrase = self.get_phrase("ABORT: ")
#         self.assertIsNotNone(phrase)
#
#     @parallel_test
#     def test_parallel(self):
#         phrase = self.get_phrase("ABORT: ")
#         self.assertIsNotNone(phrase)
#
# @pn_pn_2_testcase
# class FsHydroPnPn2(FsHydro):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=108.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=108.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('AMP', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, -6.4616452E-05, delta=2e-03)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('AMP', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, -6.4616452E-05, delta=2e-03)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2,)
#         self.assertAlmostEqual(test_val, 0.1, delta=200)
#
# ####################################################################
# #  hemi; hemi
# ####################################################################
#
# @pn_pn_testcase
# class HemiPnPn(Hemi):
#
#     lx2 = 'lx1'
#     ly2 = 'ly1'
#     lz2 = 'lz1'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=39.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-7,)
#         self.assertAlmostEqual(test_val, 0., delta=39.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('wmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 4.9173E-01, delta=1e-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('wmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 4.9173E-01, delta=1e-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2,)
#         self.assertAlmostEqual(test_val, 0.1, delta=100)
#
# @pn_pn_2_testcase
# class HemiPnPn2(Hemi):
#
#     lx2 = 'lx1-2'
#     ly2 = 'ly1-2'
#     lz2 = 'lz1-2'
#
#     @serial_test
#     def test_serialIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=34.)
#
#     @parallel_test
#     def test_parallelIter(self):
#         test_val = self.get_value('gmres: ', column=-6,)
#         self.assertAlmostEqual(test_val, 0., delta=34.)
#
#     @serial_test
#     def test_serialError(self):
#         test_val = self.get_value('wmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 4.7915E-01, delta=1e-06)
#
#     @parallel_test
#     def test_parallelError(self):
#         test_val = self.get_value('wmax', column=-2, line=-1)
#         self.assertAlmostEqual(test_val, 4.7915E-01, delta=1e-06)
#
#     @serial_test
#     def test_serialTime(self):
#         test_val = self.get_value('total solver time', column=-2,)
#         self.assertAlmostEqual(test_val, 0.1, delta=100)
