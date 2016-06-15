from lib.nekTestCase import *

###############################################################################
#  turbChannel: turbChannel.rea
###############################################################################

class TurbChannel(NekTestCase):

    example_subdir  = 'turbChannel'
    rea_file        = 'turbChannel'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.5')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres: ')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=140., label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
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
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox()
        self.mvn('box', self.__class__.rea_file)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
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
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox()
        self.mvn('box', self.__class__.rea_file)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        pres = self.get_value_from_log('PRES: ', column=-4)
        self.assertAlmostEqualDelayed(pres, target_val=0., delta=76., label='PRES')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=2, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        pres = self.get_value_from_log('PRES: ', column=-4)
        self.assertAlmostEqualDelayed(pres, target_val=0., delta=76., label='PRES')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        u_press = self.get_value_from_log('U-Press ', column=-5)
        self.assertAlmostEqualDelayed(u_press, target_val=0., delta=104., label='U-Press')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=4, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
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
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=162., label='gmres: ')

        delta = self.get_value_from_log('delta', column=-5, row=-1)
        self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
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
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=46., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):

        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=29., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=28., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=29., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=77., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.37986119139E-03, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=28., label='gmres')

        test_val = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(test_val, target_val=5.09547531705E-02, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])

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
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
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

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=34., label='gmres')

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=6.007702E-07, delta=1E-06, label='X err')

        yerr = self.get_value_from_log('Y err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(yerr, target_val=6.489061E-07, delta=1E-06, label='Y err')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=22., label='gmres')

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=6.759103E-05, delta=1E-06, label='X err')

        yerr = self.get_value_from_log('Y err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(yerr, target_val=7.842019E-05, delta=1E-06, label='Y err')

        self.assertDelayedFailures()

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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=17, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, 0.1, delta=17, label='total solver time')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        self.assertDelayedFailures()

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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
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

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        dragx = self.get_value_from_log('dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138790E+00, delta=1E-06, label='dragx')

        dragy = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragy, target_val=1.3040301E-07, delta=1E-06, label='dragy')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        dragx = self.get_value_from_log('dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138878E+00, delta=1e-05, label='dragx')

        dragy = self.get_value_from_log('dragy', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragy, target_val=3.2334222E-07, delta=1e-06, label='dragy')

        self.assertDelayedFailures()

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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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

class FsHydro(NekTestCase):
    example_subdir = 'fs_hydro'
    rea_file       = 'fs_hydro'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        # TODO: test fails in here and in legacy tests
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        # TODO: test fails in here and in legacy tests
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        phrase = self.get_phrase_from_log("ABORT: ")
        self.assertIsNotNullDelayed(phrase, 'ABORT')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200, label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=108., label='gmres')

        amp = self.get_value_from_log('AMP', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=-6.4616452E-05, delta=2e-03, label='AMP')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200, label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=108., label='gmres')

        amp = self.get_value_from_log('AMP', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=-6.4616452E-05, delta=2e-03, label='AMP')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  hemi; hemi
# ####################################################################

class Hemi(NekTestCase):
    example_subdir = 'hemi'
    rea_file = 'hemi'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=100., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=39., label='gmres')

        # TODO: This fails here and in legacy tests
        wmax = self.get_value_from_log('wmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(wmax, target_val=4.9173E-01, delta=1e-06, label='wmax')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=39., label='gmres')

        # TODO: This fails here and in legacy tests
        wmax = self.get_value_from_log('wmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(wmax, target_val=4.9173E-01, delta=1e-06, label='wmax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqual(solver_time, 0.1, delta=60.)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqual(gmres, 0., delta=34.)

        wmax = self.get_value_from_log('wmax', column=-2, row=-1)
        self.assertAlmostEqual(wmax, 4.7915E-01, delta=1e-06)

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6,)
        self.assertAlmostEqual(gmres, 0., delta=34.)

        wmax = self.get_value_from_log('wmax', column=-2, row=-1)
        self.assertAlmostEqual(wmax, 4.7915E-01, delta=1e-06)

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  kovasznay; kov.rea
####################################################################

class Kovasznay(NekTestCase):
    example_subdir = 'kovasznay'
    rea_file = 'kov'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=12, label='total solver time')

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=34, label='gmres')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=5.14316E-13, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=34, label='gmres')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=5.14316E-13, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=17, label='total solver time')

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=14, label='gmres')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=5.90551E-13, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=14, label='gmres')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=5.90551E-13, delta=1e-06, label='err')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  kov_st_state; kov_st_stokes.rea
####################################################################

class KovStState(NekTestCase):
    # Note: Legacy Analysis.py script only checked Pn-Pn-2 test cases
    example_subdir = 'kov_st_state'
    rea_file = 'kov_st_stokes'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=5, label='total solver time')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=8.55641E-10, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=8.55641E-10, delta=1e-06, label='err')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  lowMach_test; lowMach_test.rea
####################################################################

class LowMachTest(NekTestCase):
    example_subdir = 'lowmach_test'
    rea_file       = 'lowmach_test'

    def setUp(self):
        self.build_tools(['genmap'])

        # Tweak the .rea file and run genmap
        from re import sub
        cls = self.__class__
        rea_path = os.path.join(self.examples_root, cls.example_subdir, cls.rea_file+'.rea')
        with open(rea_path, 'r') as f:
            lines = [sub(r'^.*IFNAV.*$', '  T T IFNAV & IFADVC', l) for l in f]
        with open(rea_path, 'w') as f:
            f.writelines(lines)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40, label='total solver time')

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=100, label='gmres')

        vx = self.get_value_from_log(label='ERROR VX', column=-5, row=-1)
        self.assertAlmostEqualDelayed(vx, target_val=2.4635E-09, delta=1e-06, label='VX')

        t = self.get_value_from_log(label='ERROR T', column=-5, row=-1)
        self.assertAlmostEqualDelayed(t, target_val=4.5408E-12, delta=1e-06, label='T')

        qtl = self.get_value_from_log(label='ERROR QTL', column=-5, row=-1)
        self.assertAlmostEqualDelayed(qtl, target_val=2.6557E-06, delta=1e-06, label='QTL')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=100, label='gmres')

        vx = self.get_value_from_log(label='ERROR VX', column=-5, row=-1)
        self.assertAlmostEqualDelayed(vx, target_val=2.4635E-09, delta=1e-06, label='VX')

        t = self.get_value_from_log(label='ERROR T', column=-5, row=-1)
        self.assertAlmostEqualDelayed(t, target_val=4.5408E-12, delta=1e-06, label='T')

        qtl = self.get_value_from_log(label='ERROR QTL', column=-5, row=-1)
        self.assertAlmostEqualDelayed(qtl, target_val=2.6557E-06, delta=1e-06, label='QTL')

        # TODO: Add VX, T, QTL

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: For lowMach,")
        self.assertIsNotNullDelayed(phrase, label='ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        phrase = self.get_phrase_from_log("ABORT: For lowMach,")
        self.assertIsNotNullDelayed(phrase, label='ABORT: ')
        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  mhd; gpf.rea, gpf_m.rea, gpf_b.rea
####################################################################

class Mhd_Gpf(NekTestCase):
    example_subdir = 'mhd'
    rea_file = 'gpf'
    box_file = 'gpf'

    def setUp(self):
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox(box_file='gpf')
        self.run_genmap(rea_file='box')
        self.mvn('box', 'gpf')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        # TODO: This is expected to fail
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log("ABORT: MHD")
        self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        # TODO: This is expected to fail
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log("ABORT: MHD")
        self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=130, label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=15, label='gmres')

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=15, label='gmres')

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Mhd_GpfM(NekTestCase):
    example_subdir = 'mhd'
    rea_file = 'gpf_m'

    def setUp(self):
        import shutil
        # Probably a cleaner way to do this...
        # I'm just mimicking the
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox(box_file='gpf')
        self.run_genmap(rea_file='box')
        self.mvn('box', 'gpf')
        shutil.copy(
            os.path.join(self.examples_root, self.__class__.example_subdir, 'gpf.map'),
            os.path.join(self.examples_root, self.__class__.example_subdir, 'gpf_m.map')
        )

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_m', step_limit=None)

        phrase = self.get_phrase_from_log(label="ERROR: FDM")
        self.assertIsNotNullDelayed(phrase, label='ERROR: FDM')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_m', step_limit=None)

        phrase = self.get_phrase_from_log(label="ERROR: FDM")
        self.assertIsNotNullDelayed(phrase, label='ERROR: FDM')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_m', step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=130, label='total solver time')

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_m', step_limit=None)

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()


class Mhd_GpfB(NekTestCase):
    example_subdir = 'mhd'
    rea_file = 'gpf_b'

    def setUp(self):
        # Probably a cleaner way to do this...
        # I'm just mimicking the
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox(box_file='gpf')
        self.run_genmap(rea_file='box')
        self.mvn('box', 'gpf')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_b', step_limit=None)

        phrase = self.get_phrase_from_log("ABORT: MHD")
        self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_b', step_limit=None)

        phrase = self.get_phrase_from_log("ABORT: MHD")
        self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_b', step_limit=None)

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek(rea_file='gpf')
        self.run_nek(rea_file='gpf_b', step_limit=None)

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()



####################################################################
#  os7000; u3_t020_n13.rea
####################################################################

class Os7000(NekTestCase):
    example_subdir = 'os7000'
    rea_file = 'u3_t020_n13'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')

        # TODO: This fails here and in legacy tests
        egn = self.get_value_from_log(label='egn', column=-2, row=-1)
        self.assertAlmostEqualDelayed(egn, target_val=4.74494769e-05, delta=1e-06, label='egn')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')

        # TODO: This fails here and in legacy tests
        egn = self.get_value_from_log(label='egn', column=-2, row=-1)
        self.assertAlmostEqualDelayed(egn, target_val=4.74494769e-05, delta=1e-06, label='egn')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')

        egn = self.get_value_from_log(label='egn', column=-2, row=-1)
        self.assertAlmostEqualDelayed(egn, target_val=5.93471252E-05, delta=1e-06, label='egn')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')

        egn = self.get_value_from_log(label='egn', column=-2, row=-1)
        self.assertAlmostEqualDelayed(egn, target_val=5.93471252E-05, delta=1e-06, label='egn')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  peris; peris.rea
####################################################################

class Peris(NekTestCase):
    example_subdir = 'peris'
    rea_file = 'peris'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('ABORT: ')
        self.assertIsNotNullDelayed(phrase, label='ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('ABORT: ')
        self.assertIsNotNullDelayed(phrase, label='ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log(label='total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=13., label='total solver time')

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log(label='gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  pipe; helix.rea, stenosis.rea
####################################################################

class Pipe_Helix(NekTestCase):
    example_subdir = 'pipe'
    rea_file = 'helix'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=22., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=61., label='gmres')

        # TODO: This fails here and in legacy tests
        err2 = self.get_value_from_log('err2', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=1.9077617E+00, delta=1e-06, label='err2')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=61., label='gmres')

        # TODO: This fails here and in legacy tests
        err2 = self.get_value_from_log('err2', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=1.9077617E+00, delta=1e-06, label='err2')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=22., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=123., label='gmres')

        err2 = self.get_value_from_log('err2', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=1.9072258E+00, delta=1e-06, label='err2')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=123., label='gmres')

        err2 = self.get_value_from_log('err2', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=1.9072258E+00, delta=1e-06, label='err2')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Pipe_Stenosis(NekTestCase):
    example_subdir = 'pipe'
    rea_file = 'stenosis'

    def setUp(self):
        n2to3_input = [
            'w2dcyl020a',
            'stenosis',
            '0                      ascii output',
            '20                     input number of levels: (1, 2, 3,... etc.?):',
            '0                      input z min:',
            '10                     input z max:',
            '1                      input gain (0=custom,1=uniform,other=geometric spacing):',
            'n                      This is for CEM: yes or no:',
            'v                      Enter Z (5) boundary condition (P,v,O):',
            'O                      Enter Z (6) boundary condition (v,O):',
            'y                      Formatted .rea file? (y or Y):',
        ]
        self.build_tools(['n2to3', 'genmap'])
        self.run_n2to3(n2to3_input)
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=80., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=196., label='gmres')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=196., label='gmres')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=51., label='gmres')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=51., label='gmres')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  rayleigh; ray1.rea, ray2.rea
####################################################################

class Rayleigh_Ray1(NekTestCase):
    example_subdir  = 'rayleigh'
    rea_file        = 'ray1'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap(rea_file='ray1')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
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
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=32., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=2.792052E-03, delta=1e-03, label='umax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.build_tools(['genmap', 'genbox'])
        self.run_genbox(box_file='ray2')
        self.run_genmap(rea_file='box')
        self.mvn('box', 'ray2')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
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
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek(rea_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=31, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=4.549071E-03, delta=1e-05, label='umax')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
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

class Strat_P1000(NekTestCase):
    example_subdir = 'strat'
    rea_file = 're10f1000p1000'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=140, label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=80, label='total solver time')

        upres = self.get_value_from_log('U-PRES', column=-6)
        self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        upres = self.get_value_from_log('U-PRES', column=-6)
        self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Strat_P0001(NekTestCase):
    example_subdir = 'strat'
    rea_file = 're10f1000p0001'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=140, label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=80, label='total solver time')

        upres = self.get_value_from_log('U-PRES', column=-6)
        self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=200)

        upres = self.get_value_from_log('U-PRES', column=-6)
        self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  solid; solid.rea
####################################################################

class Solid(NekTestCase):
    example_subdir = 'solid'
    rea_file = 'solid'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log(label='ABORT: ')
        self.assertIsNotNullDelayed(phrase, label='ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log(label='ABORT: ')
        self.assertIsNotNullDelayed(phrase, label='ABORT: ')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=None)

        error = self.get_value_from_log('error', column=-2, row=-1)
        self.assertAlmostEqualDelayed(error, target_val=7.821228E-05, delta=1e-06, label='error')
        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=None)

        error = self.get_value_from_log('error', column=-2, row=-1)
        self.assertAlmostEqualDelayed(error, target_val=7.821228E-05, delta=1e-06, label='error')
        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  shear4; shear4.rea, thin.rea
####################################################################

class Shear4_Shear4(NekTestCase):
    example_subdir = 'shear4'
    rea_file = 'shear4'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=10., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=10., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Shear4_Thin(NekTestCase):
    example_subdir = 'shear4'
    rea_file = 'thin'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=10., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=9.991753E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=9.991753E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=10., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=9.991556E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=9.991556E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  taylor; taylor.rea
####################################################################

class Taylor(NekTestCase):
    example_subdir = 'taylor'
    rea_file = 'taylor'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=23., label='gmres')

        tq = self.get_value_from_log('tq', column=-5, row=-1)
        self.assertAlmostEqualDelayed(tq, target_val=4.13037E-06, delta=1e-06, label='tq')

        err = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=2.973648E-09, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=23., label='gmres')

        tq = self.get_value_from_log('tq', column=-5, row=-1)
        self.assertAlmostEqualDelayed(tq, target_val=4.13037E-06, delta=1e-06, label='tq')

        err = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=2.973648E-09, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=14, label='gmres')

        tq = self.get_value_from_log('tq', column=-5, row=-1)
        self.assertAlmostEqualDelayed(tq, target_val=4.10783E-06, delta=1e-06, label='tq')

        err = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=2.826284E-10, delta=1e-06, label='err')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=14, label='gmres')

        tq = self.get_value_from_log('tq', column=-5, row=-1)
        self.assertAlmostEqualDelayed(tq, target_val=4.10783E-06, delta=1e-06, label='tq')

        err = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=2.826284E-10, delta=1e-06, label='err')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  var_vis; var_vis.rea
####################################################################

class VarVis(NekTestCase):
    example_subdir = 'var_vis'
    rea_file = 'st2'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        # TODO: This fails here and in legacy tests
        phrase = self.get_phrase_from_log('ABORT: ')
        self.assertIsNotNullDelayed(phrase, label='ABORT')
        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        # TODO: This fails here and in legacy tests
        phrase = self.get_phrase_from_log('ABORT: ')
        self.assertIsNotNullDelayed(phrase, label='ABORT')
        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=30, label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=19, label='gmres')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=19, label='gmres')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  vortex; r1854a.rea
####################################################################

class Vortex(NekTestCase):
    example_subdir = 'vortex'
    rea_file = 'r1854a'

    def setUp(self):
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=60., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=65., label='gmres')

        vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
        self.assertAlmostEqualDelayed(vmin, target_val=-1.910312E-03, delta=1e-05, label='VMIN')

        self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres: ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=65., label='gmres')

        vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
        self.assertAlmostEqualDelayed(vmin, target_val=-1.910312E-03, delta=1e-05, label='VMIN')

        self.assertDelayedFailures()

    @pn_pn_2_serial
    def test_PnPn2_Serial(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=50., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')

        vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
        self.assertAlmostEqualDelayed(vmin, target_val=-1.839120E-03, delta=1e-05, label='VMIN')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.config_size(lx2='lx1-2', ly2='ly1-2', lz2='lz1-2')
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=50., label='total solver time')

        gmres = self.get_value_from_log('gmres: ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')

        vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
        self.assertAlmostEqualDelayed(vmin, target_val=-1.839120E-03, delta=1e-05, label='VMIN')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  vortex2; v2d
####################################################################
