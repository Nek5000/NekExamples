from lib.nekTestCase import *

###############################################################################
#  turbChannel: turbChannel.rea
###############################################################################

class TurbChannel(NekTestCase):

    example_subdir  = 'turbChannel'
    rea_file        = 'turbChannel'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap(tol='0.5')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=140., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

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

    def setUp(self):
        self.build_tools(['clean', 'genbox', 'genmap'])
        self.run_genbox()
        self.mvn('box', self.__class__.rea_file)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

###############################################################################
#  axi: axi.rea
###############################################################################

class Axi(NekTestCase):
    example_subdir  = 'axi'
    rea_file        = 'axi'
    box_file        = 'axi'

    def setUp(self):
        self.build_tools(['clean', 'genbox', 'genmap'])
        self.run_genbox()
        self.mvn('box', self.__class__.rea_file)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        pres = self.get_value_from_log('PRES: ', column=-4)
        self.assertAlmostEqualDelayed(pres, target_val=0., delta=76., label='PRES')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=2, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        pres = self.get_value_from_log('PRES: ', column=-4)
        self.assertAlmostEqualDelayed(pres, target_val=0., delta=76., label='PRES')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        u_press = self.get_value_from_log('U-Press ', column=-5)
        self.assertAlmostEqualDelayed(u_press, target_val=0., delta=104., label='U-Press')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=4, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        u_press = self.get_value_from_log('U-Press ', column=-5)
        self.assertAlmostEqualDelayed(u_press, target_val=0., delta=104., label='U-Press')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()
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
class Blasius(NekTestCase):
    example_subdir  = 'blasius'
    rea_file        = 'blasius'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=162., label='gmres: ')

        delta = self.get_value_from_log('delta', column=-5, row=-1)
        self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=30., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=162., label='gmres: ')

        delta = self.get_value_from_log('delta', column=-5, row=-1)
        self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=125., label='gmres: ')

        delta = self.get_value_from_log('delta', column=-5, row=-1)
        self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=30., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=125., label='gmres: ')

        delta = self.get_value_from_log('delta', column=-5, row=-1)
        self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  cone: cone.rea, cone016.rea, cone064.rea, cone256.rea
# ####################################################################
#
# # TODO: implement cone
#
# ####################################################################
# #  conj_ht: conj_ht.rea
# ####################################################################

class ConjHt(NekTestCase):
    example_subdir  = 'conj_ht'
    rea_file        = 'conj_ht'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=46., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=7, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=46., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=7, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  cyl_restart: ca.rea, cb.rea, pa.rea, pb.rea
# ####################################################################

class CylRestart_Ca(NekTestCase):
    example_subdir  = 'cyl_restart'
    rea_file        = 'ca'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):

        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=29., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=29., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class CylRestart_Cb(NekTestCase):
    example_subdir  = 'cyl_restart'
    rea_file        = 'cb'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=28., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=28., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class CylRestart_Pa(NekTestCase):
    example_subdir  = 'cyl_restart'
    rea_file        = 'pa'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=29., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=29., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class CylRestart_Pb(NekTestCase):
    example_subdir  = 'cyl_restart'
    rea_file        = 'pb'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=28., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=28., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  eddy; eddy_uv.rea, amg_eddy.rea, htps_ed.rea
# ####################################################################

# TODO: implement eddy for amg_eddy.rea, htps_ed.rea

class Eddy_EddyUv(NekTestCase):
    example_subdir  = 'eddy'
    rea_file        = 'eddy_uv'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])

        # Tweak the .rea file and run genmap
        from re import sub
        cls = self.__class__
        rea_path = os.path.join(self.examples_root, cls.example_subdir, cls.rea_file+'.rea')
        with open(rea_path, 'r') as f:
            lines = [sub(r'^.*DIVERGENCE$', '      0.10000E-08', l) for l in f]
        with open(rea_path, 'w') as f:
            f.writelines(lines)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=34., label='gmres')

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=6.007702E-07, delta=1E-06, label='X err')

        yerr = self.get_value_from_log('Y err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(yerr, target_val=6.489061E-07, delta=1E-06, label='Y err')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=80, label='total solver time')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=34., label='gmres')

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=6.007702E-07, delta=1E-06, label='X err')

        yerr = self.get_value_from_log('Y err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(yerr, target_val=6.489061E-07, delta=1E-06, label='Y err')

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=22., label='gmres')

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=6.759103E-05, delta=1E-06, label='X err')

        yerr = self.get_value_from_log('Y err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(yerr, target_val=7.842019E-05, delta=1E-06, label='Y err')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, 0.1, delta=80, label='total solver time')

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=22., label='gmres')

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=6.759103E-05, delta=1E-06, label='X err')

        yerr = self.get_value_from_log('Y err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(yerr, target_val=7.842019E-05, delta=1E-06, label='Y err')

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  eddy_neknek: eddy_neknek.rea
# ####################################################################
#
# # TODO: implment eddy_neknek tests
#
# ####################################################################
# #  eddy_psi_omega; psi_omega.rea
# ####################################################################

class Eddy_PsiOmega(NekTestCase):
    example_subdir  = 'eddy_psi_omega'
    rea_file        = 'psi_omega'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=17, label='total solver time')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, 0.1, delta=17, label='total solver time')

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  expansion: expansion.rea
# ####################################################################
#
# # TODO: implement expansion tests
#
# ####################################################################
# #  ext_cyl; ext_cyl.rea
# ####################################################################

class ExtCyl(NekTestCase):
    example_subdir  = 'ext_cyl'
    rea_file        = 'ext_cyl'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        dragx = self.get_value_from_log('dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138790E+00, delta=1E-06, label='dragx')

        dragy = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragy, target_val=1.3040301E-07, delta=1E-06, label='dragy')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=400, label='total solver time')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        dragx = self.get_value_from_log('dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138790E+00, delta=1E-06, label='dragx')

        dragy = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragy, target_val=1.3040301E-07, delta=1E-06, label='dragy')

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        dragx = self.get_value_from_log('dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138878E+00, delta=1e-05, label='dragx')

        dragy = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragy, target_val=3.2334222E-07, delta=1e-06, label='dragy')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=380, label='total solver time')

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        dragx = self.get_value_from_log('dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138878E+00, delta=1e-05, label='dragx')

        dragy = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragy, target_val=3.2334222E-07, delta=1e-06, label='dragy')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=380, label='total solver time')

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  fs_2; st1.rea, st2.rea, std_wv.rea
# ####################################################################

# TODO: fs_2/st1.rea tests fail.  They also fail legacy tests in the same ways
class Fs2_St1(NekTestCase):
    example_subdir  = 'fs_2'
    rea_file        = 'st1'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

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
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=6.382414E-01, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()


# TODO: fs_2/st2.rea tests fail.  They also fail legacy tests in the same ways
class Fs2_St2(NekTestCase):
    example_subdir  = 'fs_2'
    rea_file        = 'st2'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=6.376171E-01, delta=1e-06, label='amp')

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=23, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=6.376171E-01, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Fs2_StdWv(NekTestCase):
    example_subdir  = 'fs_2'
    rea_file        = 'std_wv'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=20., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=1.403287E-01, delta=1e-06, label='amp')

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=21., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=20., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=1.403287E-01, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

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
####################################################################
#  kovasznay; kov.rea
####################################################################

####################################################################
#  kov_st_state; kov_st_stokes.rea
####################################################################

####################################################################
#  lowMach_test; lowMach_test.rea
####################################################################

####################################################################
#  mhd; gpf.rea, gpf_m.rea, gpf_b.rea
####################################################################

####################################################################
#  os7000; u3_t020_n13.rea
####################################################################

####################################################################
#  peris; peris.rea
####################################################################

####################################################################
#  pipe; helix.rea, stenosis.rea
####################################################################

####################################################################
#  rayleigh; ray1.rea, ray2.rea
####################################################################

class Rayleigh_Ray1(NekTestCase):
    example_subdir  = 'rayleigh'
    rea_file        = 'ray1'

    def setUp(self):
        self.build_tools(['clean', 'genmap'])
        self.run_genmap(rea_file='ray1')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=32., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=2.792052E-03, delta=1e-03, label='umax')

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=3., label='total solver time')

        self.assertDelayedFailures()


    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=32., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=2.792052E-03, delta=1e-03, label='umax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=11., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=4.831113E-03, delta=1e-05, label='umax')

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=3., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=11., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=4.831113E-03, delta=1e-05, label='umax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Rayleigh_Ray2(NekTestCase):
    example_subdir  = 'rayleigh'
    rea_file        = 'ray2'
    box_file        = 'ray2'

    def setUp(self):
        self.build_tools(['clean', 'genmap', 'genbox'])
        self.run_genbox(box_file='ray2')
        self.run_genmap(rea_file='box')
        self.mvn('box', 'ray2')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=31, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=4.549071E-03, delta=1e-05, label='umax')

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=3., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx='lx1', ly='ly1', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=31, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=4.549071E-03, delta=1e-05, label='umax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=11, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=6.728787E-03, delta=1e-05, label='umax')

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=3., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx='lx1-2', ly='ly1-2', lz='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=11, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=6.728787E-03, delta=1e-05, label='umax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()





####################################################################
#  strat; re10f1000p1000.rea, re10f1000p0001.rea
####################################################################

####################################################################
#  solid; solid.rea
####################################################################

####################################################################
#  shear4; shear4.rea, thin.rea
####################################################################

####################################################################
#  var_vis; var_vis.rea
####################################################################

####################################################################
#  vortex; r1854a.rea
####################################################################

####################################################################
#  vortex2; v2d
####################################################################
