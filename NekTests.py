#!/usr/bin/env python
from lib.nekTestCase import *
from unittest import skip

import re



# ###############################################################################
# #  2d_eigtest: eig1.rea
# ###############################################################################
#
# TODO: implement 2d_eigtest

# class TwoDEigtest(NekTestCase):
#     example_subdir  = '2d_eigtest'
#     rea_file        = 'eig1'
#
#     def setUp(self):
#         import shutil
#         cls = self.__class__
#
#         # Copy Nek5000 source and replace hmholtz.f
#         old_source_root = self.source_root
#         new_source_root = os.path.join(self.examples_root, cls.example_subdir, 'nek5000')
#         shutil.copytree(old_source_root, new_source_root)
#         shutil.copy(
#             os.path.join(self.examples_root, cls.example_subdir, 'hmholtz_b_prec.f'),
#             os.path.join(new_source_root, 'core', 'hmholtz.f')
#         )
#
#         self.source_root = new_source_root
#
#         self.build_tools(['genmap'])
#         self.run_genmap(tol='0.01')
#
#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         cls = self.__class__
#
#         self.config_size(lx2='lx1', ly2='ly1', lz2='lz1')
#
#         # Run all problems
#         for lx0 in range(1,17):
#             size0_path = os.path.join(self.examples_root, cls.example_subdir, 'SIZE0')
#             with open(size0_path, 'w') as f:
#                 f.write('{0}parameter (lx0 = {1} )'.format(' '*6, lx0))
#             for ext in ('.log', '.fld', '.his', '.sch', '.out', '.ore', '.nre'):
#                 fpath = os.path.join(self.examples_root, cls.example_subdir, cls.rea_file+ext)
#                 try:
#                     os.remove(fpath)
#                 except OSError:
#                     pass
#             self.build_nek()
#             self.run_nek(log_suffix='{0}.{1}'.format(self.log_suffix, lx0), step_limit=None)
#
#         # Append all logs
#         total_log = os.path.join(
#             self.examples_root,
#             cls.example_subdir,
#             '{0}.log.{1}{2}.{3}'.format(self.rea_file, self.mpi_procs, self.log_suffix, 'tot'))
#         try:
#             os.remove(total_log)
#         except OSError:
#             pass
#         with open(total_log, 'a') as f_out:
#             for lx0 in range(1,17):
#                 single_log = os.path.join(
#                     self.examples_root,
#                     cls.example_subdir,
#                     '{0}.log.{1}{2}.{3}'.format(self.rea_file, self.mpi_procs, self.log_suffix, lx0))
#                 with open(single_log, 'r') as f_in:
#                     f_out.writelines(f_in)
#
#         for i in (2, 3, 6, 10):
#             test_val = self.get_value_from_log(' {0}   '.format(i), column=-6, logfile=total_log)
#             self.assertAlmostEqual()
#

#
#

###############################################################################
#  axi: axi.rea
###############################################################################

class Axi(NekTestCase):
    example_subdir  = 'axi'
    case_name        = 'axi'

    def setUp(self):

        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '9',
            lx2       = 'lx1-2',
            lelg      = '500',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        pres = self.get_value_from_log('PRES ', column=-4)
        self.assertAlmostEqualDelayed(pres, target_val=0., delta=76., label='PRES')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        u_press = self.get_value_from_log('U-PRES ', column=-5)
        self.assertAlmostEqualDelayed(u_press, target_val=0., delta=82., label='U-PRES')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  benard: ray_9.rea
# ####################################################################

class Benard_Ray9(NekTestCase):
    example_subdir = 'benard'
    case_name = 'ray_9'

    def setUp(self):
        self.size_params = dict (
            ldim      = '2',
            lx1       = '12',
            lxd       = '16',
            lx2       = 'lx1-2',
            lelg      = '500',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )

        self.build_tools(['genmap'])
        self.run_genmap(rea_file='ray_9')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek(usr_file='ray_9')
        self.run_nek(rea_file='ray_9')

        gmres = self.get_value_from_log('gmres ', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        rac = self.get_value_from_log('converged_rac', column=-2)
        self.assertAlmostEqualDelayed(rac, target_val=1707.79, delta=0.01, label='rac')

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek(usr_file='ray_9')
        self.run_nek(rea_file='ray_9')

        gmres = self.get_value_from_log('gmres ', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=11., label='gmres')

        rac = self.get_value_from_log('converged_rac', column=-2)
        self.assertAlmostEqualDelayed(rac, target_val=1707.79, delta=0.01, label='rac')

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  blasius: blasius.rea
# ####################################################################
class Blasius(NekTestCase):
    example_subdir  = 'blasius'
    case_name        = 'blasius'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '1000',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#    @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=162., label='gmres')
# 
#         delta = self.get_value_from_log('delta', column=-5, row=-1)
#         self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=23.0, delta=5.75, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=162., label='gmres')

        delta = self.get_value_from_log('delta', column=-5, row=-1)
        self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=125., label='gmres')
# 
#         delta = self.get_value_from_log('delta', column=-5, row=-1)
#         self.assertAlmostEqualDelayed(delta, target_val=1.26104, delta=1e-05, label='delta')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=20.0, delta=5., label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=125., label='gmres')

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
    case_name        = 'conj_ht'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '4',
            lxd       = '7',
            lx2       = 'lx1',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log('gmres', column=-7,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=46., label='gmres')
# 
#         tmax = self.get_value_from_log('tmax', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(tmax, target_val=13.1073, delta=1E-06, label='tmax')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=9.5, delta=2.4, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=46., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=13.1073, delta=1E-06, label='tmax')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log('gmres', column=-6,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')
# 
#         tmax = self.get_value_from_log('tmax', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.5, delta=1.6, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        tmax = self.get_value_from_log('tmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(tmax, target_val=1.31190E+01, delta=1E-06, label='tmax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  cyl_restart: ca.rea, cb.rea, pa.rea, pb.rea
# ####################################################################

class CylRestart_C(NekTestCase):
    example_subdir  = 'cyl_restart'
    case_name        = 'ca'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '8',
            lx2       = 'lx1-2',
            lelg      = '200',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')
        self.run_genmap(rea_file='cb', tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         import os.path
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres_a = self.get_value_from_log('gmres', column=-7, row=-1,)
#         ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
#         ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)
# 
#         self.build_nek(usr_file='cb')
#         self.run_nek(rea_file='cb',step_limit=None)
#         
#         logfl = os.path.join(
#                 self.examples_root,
#                 self.example_subdir,
#                 '{0}.log.{1}{2}'.format('cb', self.mpi_procs, self.log_suffix)
#             )
# 
#         gmres_b = self.get_value_from_log('gmres', column=-7, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=1., label='gmres b')
# 
#         test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')
# 
#         test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        import os.path
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres_a = self.get_value_from_log('gmres', column=-7, row=-1,)
        ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
        ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)

        self.build_nek(usr_file='cb')
        self.run_nek(rea_file='cb',step_limit=None)
        
        logfl = os.path.join(
                self.examples_root,
                self.example_subdir,
                '{0}.log.{1}{2}'.format('cb', self.mpi_procs, self.log_suffix)
            )

        gmres_b = self.get_value_from_log('gmres', column=-7, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=1., label='gmres b')

        test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')

        test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         import os.path
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres_a = self.get_value_from_log('gmres', column=-6, row=-1,)
#         ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
#         ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)
# 
#         self.build_nek(usr_file='cb')
#         self.run_nek(rea_file='cb',step_limit=None)
#         
#         logfl = os.path.join(
#                 self.examples_root,
#                 self.example_subdir,
#                 '{0}.log.{1}{2}'.format('cb', self.mpi_procs, self.log_suffix)
#             )
# 
#         gmres_b = self.get_value_from_log('gmres', column=-6, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=1., label='gmres b')
# 
#         test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')
# 
#         test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        import os.path
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres_a = self.get_value_from_log('gmres', column=-6, row=-1,)
        ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
        ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)

        self.build_nek(usr_file='cb')
        self.run_nek(rea_file='cb',step_limit=None)
        
        logfl = os.path.join(
                self.examples_root,
                self.example_subdir,
                '{0}.log.{1}{2}'.format('cb', self.mpi_procs, self.log_suffix)
            )

        gmres_b = self.get_value_from_log('gmres', column=-6, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=1., label='gmres b')

        test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')

        test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class CylRestart_P(NekTestCase):
    example_subdir  = 'cyl_restart'
    case_name        = 'pa'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '8',
            lx2       = 'lx1-2',
            lelg      = '200',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')
        self.run_genmap(rea_file='pb', tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         import os.path
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres_a = self.get_value_from_log('gmres', column=-7, row=-1,)
#         ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
#         ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)
# 
#         self.build_nek(usr_file='pb')
#         self.run_nek(rea_file='pb',step_limit=None)
#         
#         logfl = os.path.join(
#                 self.examples_root,
#                 self.example_subdir,
#                 '{0}.log.{1}{2}'.format('pb', self.mpi_procs, self.log_suffix)
#             )
# 
#         gmres_b = self.get_value_from_log('gmres', column=-7, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=5., label='gmres b')
# 
#         test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')
# 
#         test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        import os.path
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres_a = self.get_value_from_log('gmres', column=-7, row=-1,)
        ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
        ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)

        self.build_nek(usr_file='pb')
        self.run_nek(rea_file='pb',step_limit=None)
        
        logfl = os.path.join(
                self.examples_root,
                self.example_subdir,
                '{0}.log.{1}{2}'.format('pb', self.mpi_procs, self.log_suffix)
            )

        gmres_b = self.get_value_from_log('gmres', column=-7, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=5., label='gmres b')

        test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')

        test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         import os.path
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres_a = self.get_value_from_log('gmres', column=-6, row=-1,)
#         ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
#         ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)
# 
#         self.build_nek(usr_file='pb')
#         self.run_nek(rea_file='pb',step_limit=None)
#         
#         logfl = os.path.join(
#                 self.examples_root,
#                 self.example_subdir,
#                 '{0}.log.{1}{2}'.format('pb', self.mpi_procs, self.log_suffix)
#             )
# 
#         gmres_b = self.get_value_from_log('gmres', column=-6, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=5., label='gmres b')
# 
#         test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')
# 
#         test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
#         self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        import os.path
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres_a = self.get_value_from_log('gmres', column=-6, row=-1,)
        ref_val_x = self.get_value_from_log('1dragx', column=-4, row=-1)
        ref_val_y = self.get_value_from_log('1dragy', column=-4, row=-1)

        self.build_nek(usr_file='pb')
        self.run_nek(rea_file='pb',step_limit=None)
        
        logfl = os.path.join(
                self.examples_root,
                self.example_subdir,
                '{0}.log.{1}{2}'.format('pb', self.mpi_procs, self.log_suffix)
            )

        gmres_b = self.get_value_from_log('gmres', column=-6, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(gmres_b, target_val=gmres_a, delta=5., label='gmres b')

        test_val_x = self.get_value_from_log('1dragx', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_x, target_val=ref_val_x, delta=1E-06, label='1dragx')

        test_val_y = self.get_value_from_log('1dragy', column=-4, row=-1, logfile=logfl)
        self.assertAlmostEqualDelayed(test_val_y, target_val=ref_val_y, delta=1E-06, label='1dragy')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  eddy_psi_omega; psi_omega.rea
# ####################################################################

class Eddy_PsiOmega(NekTestCase):
    example_subdir  = 'eddy_psi_omega'
    case_name        = 'psi_omega'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '16',
            lxd       = '24',
            lx2       = 'lx1-2',
            lelg      = '300',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         xerr = self.get_value_from_log('X err', column=-6, row=-1)
#         self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=14.0, delta=3.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        xerr = self.get_value_from_log('X err', column=-6, row=-1)
        self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         xerr = self.get_value_from_log('X err', column=-6, row=-1)
#         self.assertAlmostEqualDelayed(xerr, target_val=1.177007E-10, delta=1E-06, label='X err')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=13.5, delta=3.4, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
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
    case_name        = 'ext_cyl'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '9',
            lx2       = 'lx1-2',
            lelg      = '1500',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=1000)
# 
#         gmres = self.get_value_from_log('gmres', column=-7,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')
# 
#         dragx = self.get_value_from_log('1dragx', column=-4, row=-1)
#         self.assertAlmostEqualDelayed(dragx, target_val=1.2138790E+00, delta=5E-05, label='1dragx')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=85., label='gmres')

        dragx = self.get_value_from_log('1dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2138790E+00, delta=5E-05, label='1dragx')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=1000)
# 
#         gmres = self.get_value_from_log('gmres', column=-6,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')
# 
#         dragx = self.get_value_from_log('1dragx', column=-4, row=-1)
#         self.assertAlmostEqualDelayed(dragx, target_val=1.2139229E+00, delta=5e-05, label='1dragx')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        dragx = self.get_value_from_log('1dragx', column=-4, row=-1)
        self.assertAlmostEqualDelayed(dragx, target_val=1.2139229E+00, delta=5e-05, label='1dragx')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  fs_2; st1.rea, st2.rea, std_wv.rea
# ####################################################################

class Fs2_St1(NekTestCase):
    example_subdir  = 'fs_2'
    case_name        = 'st1'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '9',
            lx2       = 'lx1-2',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#    @pn_pn_serial
#    def test_PnPn_Serial(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=200)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')
#
#        amp = self.get_value_from_log('amp', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=6.382379E-01, delta=1e-06, label='amp')
#
#        solver_time = self.get_value_from_log('total solver time', column=-2,)
#        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=18.3, label='total solver time')
#
#        self.assertDelayedFailures()
#
#    @pn_pn_parallel
#    def test_PnPn_Parallel(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=200)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')
#
#        amp = self.get_value_from_log('amp', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=6.382379E-01, delta=1e-06, label='amp')
#
#        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-6,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')
# 
#         amp = self.get_value_from_log('amp', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(amp, target_val=0.6382379, delta=1e-06, label='amp')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2,)
#         self.assertAlmostEqualDelayed(solver_time, target_val=7.5, delta=1.9, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=0.6382379, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Fs2_St2(NekTestCase):
    example_subdir  = 'fs_2'
    case_name        = 'st2'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '9',
            lx2       = 'lx1-2',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#    @pn_pn_serial
#    def test_PnPn_Serial(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=200)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')
#
#        amp = self.get_value_from_log('amp', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=6.376125E-01, delta=1e-06, label='amp')
#
#        solver_time = self.get_value_from_log('total solver time', column=-2,)
#        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=23, label='total solver time')
#
#        self.assertDelayedFailures()
#
#    @pn_pn_parallel
#    def test_PnPn_Parallel(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=200)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')
#
#        amp = self.get_value_from_log('amp', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=6.376125E-01, delta=1e-06, label='amp')
#
#        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-6,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')
# 
#         amp = self.get_value_from_log('amp', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(amp, target_val=0.6376125, delta=1e-06, label='amp')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2,)
#         self.assertAlmostEqualDelayed(solver_time, target_val=7.5, delta=1.9, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=38., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=0.6376125, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Fs2_StdWv(NekTestCase):
    example_subdir  = 'fs_2'
    case_name        = 'std_wv'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '6',
            lxd       = '9',
            lx2       = 'lx1-2',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#    @pn_pn_serial
#    def test_PnPn_Serial(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=200)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=20., label='gmres')
#
#        amp = self.get_value_from_log('amp', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=1.403036E-01, delta=1e-06, label='amp')
#
#        solver_time = self.get_value_from_log('total solver time', column=-2,)
#        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=21., label='total solver time')
#
#        self.assertDelayedFailures()
#
#    @pn_pn_parallel
#    def test_PnPn_Parallel(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=200)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=20., label='gmres')
#
#        amp = self.get_value_from_log('amp', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=1.403036E-01, delta=1e-06, label='amp')
#
#        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-6,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=20., label='gmres')
# 
#         amp = self.get_value_from_log('amp', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(amp, target_val=0.1403036, delta=1e-06, label='amp')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2,)
#         self.assertAlmostEqualDelayed(solver_time, target_val=7.0, delta=1.75, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=20., label='gmres')

        amp = self.get_value_from_log('amp', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=0.1403036, delta=1e-06, label='amp')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  fs_hydro: fs_hydro.rea
# ####################################################################

class FsHydro(NekTestCase):
    example_subdir = 'fs_hydro'
    case_name       = 'fs_hydro'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '12',
            lxd       = '18',
            lx2       = 'lx1-2',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '20',
            lely      = '60',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#    @pn_pn_serial
#    def test_PnPn_Serial(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=1000)
#
#        solver_time = self.get_value_from_log('total solver time', column=-2,)
#        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=200, label='total solver time')
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=108., label='gmres')
#
#        amp = self.get_value_from_log('AMP', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=-6.4616452E-05, delta=2e-03, label='AMP')
#
#        self.assertDelayedFailures()
#
#    @pn_pn_parallel
#    def test_PnPn_Parallel(self):
#        self.size_params['lx2']='lx1'
#        self.config_size()
#        self.build_nek()
#        self.run_nek(step_limit=1000)
#
#        gmres = self.get_value_from_log('gmres', column=-7,)
#        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=108., label='gmres')
#
#        amp = self.get_value_from_log('AMP', column=-2, row=-1)
#        self.assertAlmostEqualDelayed(amp, target_val=-6.4616452E-05, delta=2e-03, label='AMP')
#
#        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=1000)
# 
#         gmres = self.get_value_from_log('gmres', column=-6,)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=108., label='gmres')
# 
#         amp = self.get_value_from_log('AMP', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(amp, target_val=-6.4616452E-05, delta=2e-03, label='AMP')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2,)
#         self.assertAlmostEqualDelayed(solver_time, target_val=106.0, delta=26.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=108., label='gmres')

        amp = self.get_value_from_log('AMP', column=-2, row=-1)
        self.assertAlmostEqualDelayed(amp, target_val=-6.4616452E-05, delta=2e-03, label='AMP')

        solver_time = self.get_value_from_log('total solver time', column=-2,)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=55.0, label='total solver time')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ####################################################################
# #  hemi; hemi
# ####################################################################

class Hemi(NekTestCase):
    example_subdir = 'hemi'
    case_name = 'hemi'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '5',
            lxd       = '7',
            lx2       = 'lx1',
            lelg      = '2100',
            lpmin     = '2',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=39., label='gmres')

        wmax = self.get_value_from_log('wmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(wmax, target_val=4.9173E-01, delta=1e-05, label='wmax')

        self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6,)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=34., label='gmres')

        wmax = self.get_value_from_log('wmax', column=-2, row=-1)
        self.assertAlmostEqualDelayed(wmax, target_val=0.48305, delta=1e-05, label='wmax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  incl_def
####################################################################

class InclDef(NekTestCase):
    example_subdir = 'incl_def'
    case_name = 'incl_def'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1',
            lelg      = '100',
            ldimt     = '2',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

    @pn_pn_serial
    def test_PnPn_Serial(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log('All include files added with success')
        self.assertIsNotNullDelayed(phrase, label='All include files added with success')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()


####################################################################
#  kovasznay; kov.rea
####################################################################

class Kovasznay(NekTestCase):
    example_subdir = 'kovasznay'
    case_name = 'kov'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '14',
            lxd       = '20',
            lx2       = 'lx1',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=34, label='gmres')
# 
#         err = self.get_value_from_log(label='err', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(err, target_val=5.14316E-13, delta=1e-06, label='err')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=10.75, delta=2.7, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=34, label='gmres')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=5.14316E-13, delta=1e-06, label='err')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=14, label='gmres')
# 
#         err = self.get_value_from_log(label='err', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(err, target_val=5.90551E-13, delta=1e-06, label='err')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=10.0, delta=2.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log(label='gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=14, label='gmres')

        err = self.get_value_from_log(label='err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=5.90551E-13, delta=1e-06, label='err')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()


####################################################################
#  lowMach_test; lowMach_test.rea
####################################################################

class LowMachTest(NekTestCase):
    example_subdir = 'lowMach_test'
    case_name       = 'lowMach_test'

    def setUp(self):
        self.size_params = dict (
            ldim      = '2',
            lx1       = '14',
            lxd       = '20',
            lx2       = 'lx1-0',
            lx1m      = 'lx1',
            lelg      = '500',
        )
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2'] = 'lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=35, label='gmres')

        vx = self.get_value_from_log(label='ERROR VX', column=-5, row=-1)
        self.assertAlmostEqualDelayed(vx, target_val=2.6938e-09, delta=1e-10, label='VX')

        errt = self.get_value_from_log(label='ERROR T', column=-5, row=-1)
        self.assertAlmostEqualDelayed(errt, target_val=4.5532e-12, delta=1e-13, label='T')

        qtl = self.get_value_from_log(label='ERROR QTL', column=-5, row=-1)
        self.assertAlmostEqualDelayed(qtl, target_val=2.6557E-06, delta=1e-07, label='QTL')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  mhd; gpf.rea, gpf_m.rea, gpf_b.rea
####################################################################

class Mhd_Gpf(NekTestCase):
    example_subdir = 'mhd'
    case_name = 'gpf'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '6',
            lxd       = '1+3*lx1/2',
            lx2       = 'lx1-2',
            lelg      = '150',
            ldimt     = '2',
            lhis      = '200',
            lelx      = '4',
            lely      = '4',
            lelz      = '8',
            lx1m      = '1',
            lbelt     = 'lelt',
            lpelt     = '1',
            lcvelt    = '1',
            lfdm      = '1',
        )
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox(box_file='gpf')
        self.run_genmap(rea_file='box', tol='0.01')
        self.mvn('box', 'gpf')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         # TODO: This is expected to fail
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         phrase = self.get_phrase_from_log("ABORT: MHD")
#         self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        # TODO: This is expected to fail
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log("ABORT: MHD")
        self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=15, label='gmres')
# 
#         rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
#         self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=139.5, delta=34.9, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=15, label='gmres')

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()



class Mhd_GpfB(NekTestCase):
    example_subdir = 'mhd'
    case_name = 'gpf_b'

    def setUp(self):
        # Probably a cleaner way to do this...
        # I'm just mimicking the
        self.size_params = dict(
            ldim      = '3',
            lx1       = '6',
            lxd       = '1+3*lx1/2',
            lx2       = 'lx1-2',
            lelg      = '150',
            ldimt     = '2',
            lhis      = '200',
            lelx      = '4',
            lely      = '4',
            lelz      = '8',
            lx1m      = '1',
            lbelt     = 'lelt',
            lpelt     = '1',
            lcvelt    = '1',
            lfdm      = '1',
        )
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox(box_file='gpf')
        self.run_genmap(rea_file='box', tol='0.01')
        self.mvn('box', 'gpf_b')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek(usr_file='gpf')
#         self.run_nek(rea_file='gpf_b', step_limit=None)
# 
#         phrase = self.get_phrase_from_log("ABORT: MHD")
#         self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek(usr_file='gpf')
        self.run_nek(rea_file='gpf_b', step_limit=None)

        phrase = self.get_phrase_from_log("ABORT: MHD")
        self.assertIsNotNullDelayed(phrase, label='ABORT: MHD')
        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek(usr_file='gpf')
#         self.run_nek(rea_file='gpf_b', step_limit=None)
# 
#         rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
#         self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek(usr_file='gpf')
        self.run_nek(rea_file='gpf_b', step_limit=None)

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Mhd_GpfM(NekTestCase):
    example_subdir = 'mhd'
    case_name = 'gpf_m'

    def setUp(self):
        import shutil
        # Probably a cleaner way to do this...
        # I'm just mimicking the
        self.size_params = dict(
            ldim      = '3',
            lx1       = '6',
            lxd       = '1+3*lx1/2',
            lx2       = 'lx1-2',
            lelg      = '150',
            ldimt     = '2',
            lhis      = '200',
            lelx      = '4',
            lely      = '4',
            lelz      = '8',
            lx1m      = '1',
            lbelt     = 'lelt',
            lpelt     = '1',
            lcvelt    = '1',
            lfdm      = '1',
        )
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox(box_file='gpf')
        self.run_genmap(rea_file='box', tol='0.01')
        self.mvn('box', 'gpf')
        shutil.copy(
            os.path.join(self.examples_root, self.__class__.example_subdir, 'gpf.map'),
            os.path.join(self.examples_root, self.__class__.example_subdir, 'gpf_m.map')
        )

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek(usr_file='gpf')
#         self.run_nek(rea_file='gpf_m', step_limit=None)
# 
#         phrase = self.get_phrase_from_log(label="ERROR: FDM")
#         self.assertIsNotNullDelayed(phrase, label='ERROR: FDM')
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek(usr_file='gpf')
        self.run_nek(rea_file='gpf_m', step_limit=None)

        phrase = self.get_phrase_from_log(label="ERROR: FDM")
        self.assertIsNotNullDelayed(phrase, label='ERROR: FDM')
        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek(usr_file='gpf')
#         self.run_nek(rea_file='gpf_m', step_limit=None)
# 
#         rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
#         self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=124.0, delta=31.0, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek(usr_file='gpf')
        self.run_nek(rea_file='gpf_m', step_limit=None)

        rtavg = self.get_value_from_log('rtavg_gr_Em', column=-4, row=-1)
        self.assertAlmostEqualDelayed(rtavg, target_val=2.56712250E-01, delta=.02, label='rtavg')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  mv_cyl with CVODE
####################################################################

class MvCylCvode(NekTestCase):
    example_subdir = 'mv_cyl'
    case_name = 'mv_cyl'

    def setUp(self):
        self.size_params = dict (
            ldim     = '2',
            lx1      = '8',
            lxd      = '12',
            lx2      = 'lx1-0',
            lx1m     = 'lx1',
            lelg     = '500',
            ldimt    = '10',
            lcvelt   = 'lelt',
        )
        self.config_size()
        self.build_tools(['genmap'])
        self.run_genmap()

    @pn_pn_parallel
    def test_PnPn_Parallel_Steps1e3(self):
        self.pplist +='CVODE'
        self.log_suffix += '.steps_1e3'
        self.config_parfile({'GENERAL' : {'numSteps' : '1e3', 'dt' : '1e-3'}})
        self.build_nek()
        self.run_nek()

        err3 = self.get_value_from_log('err', column=-3, row=-1)
        self.assertAlmostEqualDelayed(err3, target_val=0.1743079E-03, delta=1e-6, label='err (column -3)')

        err2 = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=0.6348537E-06, delta=1e-9, label='err (column -2)')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  os7000; u3_t020_n13.rea
####################################################################

class Os7000(NekTestCase):
    example_subdir = 'os7000'
    case_name = 'u3_t020_n13'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '14',
            lxd       = '3*lx1/2',
            lx2       = 'lx1-2',
            lelg      = '100',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=1000)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')
# 
#         egn = self.get_value_from_log(label='egn', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(egn, target_val=4.74494769e-05, delta=1e-06, label='egn')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=22.0, delta=5.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')

        egn = self.get_value_from_log(label='egn', column=-2, row=-1)
        self.assertAlmostEqualDelayed(egn, target_val=4.74494769e-05, delta=1e-06, label='egn')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=1000)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=43., label='gmres')
# 
#         egn = self.get_value_from_log(label='egn', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(egn, target_val=5.93471252E-05, delta=1e-06, label='egn')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=22.0, delta=5.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=1000)

        gmres = self.get_value_from_log(label='gmres', column=-6)
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
    case_name = 'peris'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '6',
            lxd       = '9',
            lx2       = 'lx1',
            lelg      = '200',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.5, delta=1.6, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=4.2, delta=1.05, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log(label='gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  pipe; helix.rea, stenosis.rea
####################################################################

class Pipe_Helix(NekTestCase):
    example_subdir = 'pipe'
    case_name = 'helix'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '6',
            lxd       = '10',
            lx2       = 'lx1-2',
            lelg      = '500',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=61., label='gmres')
# 
#         err2 = self.get_value_from_log('err2', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(err2, target_val=1.9077617E+00, delta=1e-06, label='err2')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.6, delta=1.65, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=61., label='gmres')

        err2 = self.get_value_from_log('err2', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=1.9077617E+00, delta=1e-06, label='err2')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=123., label='gmres')
# 
#         err2 = self.get_value_from_log('err2', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(err2, target_val=1.9072258E+00, delta=1e-06, label='err2')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=11.5, delta=2.9, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=123., label='gmres')

        err2 = self.get_value_from_log('err2', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err2, target_val=1.9072258E+00, delta=1e-06, label='err2')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Pipe_Stenosis(NekTestCase):
    example_subdir = 'pipe'
    case_name = 'stenosis'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '6',
            lxd       = '10',
            lx2       = 'lx1-2',
            lelg      = '500',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
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
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=196., label='gmres')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=27.5, delta=6.9, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=196., label='gmres')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=51., label='gmres')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=23.5, delta=5.9, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=51., label='gmres')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  rayleigh; ray1.rea, ray2.rea
####################################################################

class Rayleigh_Ray1(NekTestCase):
    example_subdir  = 'rayleigh'
    case_name        = 'ray1'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '12',
            lxd       = '18',
            lx2       = 'lx1',
            lelg      = '50',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(rea_file='ray1', tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek(usr_file='ray0')
#         self.run_nek(rea_file='ray1', step_limit=200)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=32., label='gmres')
# 
#         umax = self.get_value_from_log(label='umax', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(umax, target_val=0.00377251, delta=2e-05, label='umax')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=2.0, delta=0.5, label='total solver time')
# 
#         self.assertDelayedFailures()


    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek(usr_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=32., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=0.00377251, delta=2e-05, label='umax')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek(usr_file='ray0')
#         self.run_nek(rea_file='ray1', step_limit=200)
# 
#         gmres = self.get_value_from_log(label='gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=11., label='gmres')
# 
#         umax = self.get_value_from_log(label='umax', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(umax, target_val=4.831113E-03, delta=2e-05, label='umax')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=1.5, delta=0.4, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek(usr_file='ray0')
        self.run_nek(rea_file='ray1', step_limit=200)

        gmres = self.get_value_from_log(label='gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=11., label='gmres')

        umax = self.get_value_from_log(label='umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=4.831113E-03, delta=2e-05, label='umax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Rayleigh_Ray2(NekTestCase):
    example_subdir  = 'rayleigh'
    case_name        = 'ray2'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '12',
            lxd       = '18',
            lx2       = 'lx1',
            lelg      = '50',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap', 'genbox'])
        self.run_genbox(box_file='ray2')
        self.run_genmap(rea_file='box', tol='0.01')
        self.mvn('box', 'ray2')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek(usr_file='ray0')
#         self.run_nek(rea_file='ray2', step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=31, label='gmres')
# 
#         umax = self.get_value_from_log('umax', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(umax, target_val=0.00551992, delta=1e-04, label='umax')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=1.6, delta=0.4, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek(usr_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=31, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=0.00551992, delta=1e-04, label='umax')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek(usr_file='ray0')
#         self.run_nek(rea_file='ray2', step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=11, label='gmres')
# 
#         umax = self.get_value_from_log('umax', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(umax, target_val=0.006621465, delta=1e-04, label='umax')
# 
#         solver_time = self.get_value_from_log(label='total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=1.4, delta=0.35, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek(usr_file='ray0')
        self.run_nek(rea_file='ray2', step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=11, label='gmres')

        umax = self.get_value_from_log('umax', column=-3, row=-1)
        self.assertAlmostEqualDelayed(umax, target_val=0.006621465, delta=1e-04, label='umax')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  shear4; shear4.rea, thin.rea
####################################################################

class Shear4_Shear4(NekTestCase):
    example_subdir = 'shear4'
    case_name = 'shear4'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '9',
            lxd       = '13',
            lx2       = 'lx1-2',
            lelg      = '300',
            ldimt     = '4',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '16',
            lely      = '16',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')
# 
#         vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.5, delta=1.6, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')
# 
#         vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.5, delta=1.6, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=3.031328E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Shear4_Thin(NekTestCase):
    example_subdir = 'shear4'
    case_name = 'thin'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '9',
            lxd       = '13',
            lx2       = 'lx1-2',
            lelg      = '300',
            ldimt     = '4',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '16',
            lely      = '16',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')
# 
#         vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(vort, target_val=9.991753E+01, delta=1e-06, label='peak vorticity')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.0, delta=1.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=9.991753E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')
# 
#         vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
#         self.assertAlmostEqualDelayed(vort, target_val=9.991556E+01, delta=1e-06, label='peak vorticity')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=6.2, delta=1.55, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=17., label='gmres')

        vort = self.get_value_from_log('peak vorticity', column=-3, row=-1)
        self.assertAlmostEqualDelayed(vort, target_val=9.991556E+01, delta=1e-06, label='peak vorticity')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()


####################################################################
#  smoother; lpt.par
####################################################################

class Smooth(NekTestCase):
    example_subdir = 'smoother'
    case_name = 'lpt'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '3',
            lxd       = '4',
            lx2       = 'lx1',
            lelg      = '10000',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        phrase = self.get_phrase_from_log('Mesh smoothing completed.')
        self.assertIsNotNullDelayed(phrase, label='Mesh smoothing completed.')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  solid; solid.rea
####################################################################

class Solid(NekTestCase):
    example_subdir = 'solid'
    case_name = 'solid'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '50',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         error = self.get_value_from_log('error', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(error, target_val=7.821228E-05, delta=1e-06, label='error')
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        error = self.get_value_from_log('error', column=-2, row=-1)
        self.assertAlmostEqualDelayed(error, target_val=7.821228E-05, delta=1e-06, label='error')
        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         error = self.get_value_from_log('error', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(error, target_val=7.821228E-05, delta=1e-06, label='error')
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        error = self.get_value_from_log('error', column=-2, row=-1)
        self.assertAlmostEqualDelayed(error, target_val=7.821228E-05, delta=1e-06, label='error')
        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  strat; re10f1000p1000.rea, re10f1000p0001.rea
####################################################################

class Strat_P0001(NekTestCase):
    example_subdir = 'strat'
    case_name = 're10f1000p0001'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '400',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=58.5, delta=14.6, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         upres = self.get_value_from_log('U-PRES', column=-6)
#         self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=53.0, delta=13.3, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        upres = self.get_value_from_log('U-PRES', column=-6)
        self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

class Strat_P1000(NekTestCase):
    example_subdir = 'strat'
    case_name = 're10f1000p1000'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '400',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=60.5, delta=15.1, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0, delta=60, label='gmres')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=200)
# 
#         upres = self.get_value_from_log('U-PRES', column=-6)
#         self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=53.5, delta=13.4, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=200)

        upres = self.get_value_from_log('U-PRES', column=-6)
        self.assertAlmostEqualDelayed(upres, target_val=0, delta=27, label='U-PRES')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  taylor; taylor.rea
####################################################################

class Taylor(NekTestCase):
    example_subdir = 'taylor'
    case_name = 'taylor'

    def setUp(self):
        self.size_params = dict(
            ldim      = '2',
            lx1       = '10',
            lxd       = '16',
            lx2       = 'lx1-2',
            lelg      = '20',
            ldimt     = '1',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=23., label='gmres')
# 
#         tq = self.get_value_from_log('tq', column=-5, row=-1)
#         self.assertAlmostEqualDelayed(tq, target_val=4.13037E-06, delta=1e-06, label='tq')
# 
#         err = self.get_value_from_log('err', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(err, target_val=2.973648E-09, delta=1e-06, label='err')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=33.5, delta=8.4, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=23., label='gmres')

        tq = self.get_value_from_log('tq', column=-5, row=-1)
        self.assertAlmostEqualDelayed(tq, target_val=4.13037E-06, delta=1e-06, label='tq')

        err = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=2.973648E-09, delta=1e-06, label='err')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=14, label='gmres')
# 
#         tq = self.get_value_from_log('tq', column=-5, row=-1)
#         self.assertAlmostEqualDelayed(tq, target_val=4.10783E-06, delta=1e-06, label='tq')
# 
#         err = self.get_value_from_log('err', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(err, target_val=2.826284E-10, delta=1e-06, label='err')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=20., delta=5., label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=40., label='total solver time')

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=14, label='gmres')

        tq = self.get_value_from_log('tq', column=-5, row=-1)
        self.assertAlmostEqualDelayed(tq, target_val=4.10783E-06, delta=1e-06, label='tq')

        err = self.get_value_from_log('err', column=-2, row=-1)
        self.assertAlmostEqualDelayed(err, target_val=2.826284E-10, delta=1e-06, label='err')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

# ###############################################################################
# #  3dbox: b3d.rea
# ###############################################################################

class ThreeDBox(NekTestCase):
    example_subdir  = '3dbox'
    case_name        = 'b3d'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '520',
            ldimt     = '1',
            lhis      = '100',
            lelx      = '8',
            lely      = '8',
            lelz      = '8',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genbox', 'genmap'])
        self.run_genbox()
        self.mvn('box', self.__class__.case_name)
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         phrase = self.get_phrase_from_log('end of time-step loop')
#         self.assertIsNotNullDelayed(phrase, label='end of time-step loop')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         phrase = self.get_phrase_from_log('end of time-step loop')
#         self.assertIsNotNullDelayed(phrase, label='end of time-step loop')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        phrase = self.get_phrase_from_log('end of time-step loop')
        self.assertIsNotNullDelayed(phrase, label='end of time-step loop')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

###############################################################################
#  turbChannel: turbChannel.rea
###############################################################################

class TurbChannel(NekTestCase):
    example_subdir = 'turbChannel'
    case_name = 'turbChannel'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '600',
            ldimt     = '3',
            lhis      = '100',
            lelx      = '8',
            lely      = '8',
            lelz      = '8',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=34.0, delta=8.5, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=95., label='gmres')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=25.0, label='total solver time')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=35.0, delta=8.75, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=26., label='gmres')

        solver_time = self.get_value_from_log('total solver time', column=-2)
        self.assertAlmostEqualDelayed(solver_time, target_val=0.1, delta=25.0, label='total solver time')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  vortex; r1854a.rea
####################################################################

class Vortex(NekTestCase):
    example_subdir = 'vortex'
    case_name = 'r1854a'

    def setUp(self):
        self.size_params = dict(
            ldim      = '3',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '200',
            ldimt     = '2',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '1',
            lely      = '1',
            lelz      = '1',
            lx1m      = '1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-7)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=65., label='gmres')
# 
#         vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(vmin, target_val=-1.910312E-03, delta=1e-05, label='VMIN')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=13.2, delta=3.3, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-7)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=65., label='gmres')

        vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
        self.assertAlmostEqualDelayed(vmin, target_val=-1.910312E-03, delta=1e-05, label='VMIN')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=10)
# 
#         gmres = self.get_value_from_log('gmres', column=-6)
#         self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')
# 
#         vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(vmin, target_val=-1.839120E-03, delta=1e-05, label='VMIN')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=13.0, delta=3.25, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=10)

        gmres = self.get_value_from_log('gmres', column=-6)
        self.assertAlmostEqualDelayed(gmres, target_val=0., delta=18., label='gmres')

        vmin = self.get_value_from_log('VMIN', column=-2, row=-1)
        self.assertAlmostEqualDelayed(vmin, target_val=-1.839120E-03, delta=1e-05, label='VMIN')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()

####################################################################
#  vortex2; v2d
####################################################################

class Vortex2(NekTestCase):
    example_subdir = 'vortex2'
    case_name = 'v2d'

    def setUp(self):
        import re
        self.size_params = dict(
            ldim      = '2',
            lx1       = '8',
            lxd       = '12',
            lx2       = 'lx1-2',
            lelg      = '300',
            ldimt     = '4',
            lhis      = '100',
            lpert     = '1',
            toteq     = '1',
            lelx      = '20',
            lely      = '60',
            lelz      = '1',
            mprev     = '80',
            lgmres    = '40',
            lx1m      = 'lx1',
            lbelt     = '1',
            lpelt     = '1',
            lcvelt    = '1',
        )
        self.build_tools(['genmap'])
        self.run_genmap(tol='0.01')

        # Tweak .rea file
        rea_file_path = os.path.join(self.examples_root, self.__class__.example_subdir, self.case_name + '.rea')
        with open(rea_file_path, 'r') as f:
            lines = [re.sub(r'(^\s+[\d.]+\s+p11.*$)', r' 8000\g<1>', l) for l in f]
        with open(rea_file_path, 'w') as f:
            f.writelines(lines)

        # Extra tweaks to the SIZE file
        size_file_path = os.path.join(self.examples_root, self.__class__.example_subdir, 'SIZE')
        with open(size_file_path, 'r') as f:
            lines = f.readlines()

        lines = [re.sub(
            r'( {6}parameter *)\(lx1=10,ly1=lx1,lz1=1,lelt=80,lelv=lelt\)( *)',
            r'\g<1>(lx1=8,ly1=lx1,lz1=1,lelt=80,lelv=lelt)\g<2>', l, flags=re.I) for l in lines]
        lines = [re.sub(
            r'( {6}parameter *)\(lxd=15,lyd=lxd,lzd=1\)( *)',
            r'\g<1>(lxd=12,lyd=lxd,lzd=1)\g<2>', l, flags=re.I) for l in lines]

        with open(size_file_path, 'w') as f:
            f.writelines(lines)

#     @pn_pn_serial
#     def test_PnPn_Serial(self):
#         self.size_params['lx2']='lx1'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         pres = self.get_value_from_log('PRES', column=-4)
#         self.assertAlmostEqualDelayed(pres, target_val=0., delta=100., label='PRES')
# 
#         umin = self.get_value_from_log('umin', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(umin, target_val=-1.453402E-03, delta=1e-03, label='umin')
# 
#         torqx = self.get_value_from_log('1torqx', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(torqx, target_val=-1.7399905E-07, delta=1e-06, label='1torqx')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=51.0, delta=12.8, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.size_params['lx2']='lx1'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        pres = self.get_value_from_log('PRES', column=-4)
        self.assertAlmostEqualDelayed(pres, target_val=0., delta=100., label='PRES')

        umin = self.get_value_from_log('umin', column=-2, row=-1)
        self.assertAlmostEqualDelayed(umin, target_val=-1.453402E-03, delta=1e-03, label='umin')

        torqx = self.get_value_from_log('1torqx', column=-2, row=-1)
        self.assertAlmostEqualDelayed(torqx, target_val=-1.7399905E-07, delta=1e-06, label='1torqx')

        self.assertDelayedFailures()

#     @pn_pn_2_serial
#     def test_PnPn2_Serial(self):
#         self.size_params['lx2']='lx1-2'
#         self.config_size()
#         self.build_nek()
#         self.run_nek(step_limit=None)
# 
#         upress = self.get_value_from_log('U-PRES', column=-5)
#         self.assertAlmostEqualDelayed(upress, target_val=0., delta=100, label='U-PRES')
# 
#         umin = self.get_value_from_log('umin', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(umin, target_val=-2.448980E-03, delta=1e-03, label='umin')
# 
#         torqx = self.get_value_from_log('1torqx', column=-2, row=-1)
#         self.assertAlmostEqualDelayed(torqx, target_val=-1.6276138E-07, delta=1e-06, label='1torqx')
# 
#         solver_time = self.get_value_from_log('total solver time', column=-2)
#         self.assertAlmostEqualDelayed(solver_time, target_val=56.0, delta=14, label='total solver time')
# 
#         self.assertDelayedFailures()

    @pn_pn_2_parallel
    def test_PnPn2_Parallel(self):
        self.size_params['lx2']='lx1-2'
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        upress = self.get_value_from_log('U-PRES', column=-5)
        self.assertAlmostEqualDelayed(upress, target_val=0., delta=100, label='U-PRES')

        umin = self.get_value_from_log('umin', column=-2, row=-1)
        self.assertAlmostEqualDelayed(umin, target_val=-2.448980E-03, delta=1e-03, label='umin')

        torqx = self.get_value_from_log('1torqx', column=-2, row=-1)
        self.assertAlmostEqualDelayed(torqx, target_val=-1.6276138E-07, delta=1e-06, label='1torqx')

        self.assertDelayedFailures()

    def tearDown(self):
        self.move_logs()
