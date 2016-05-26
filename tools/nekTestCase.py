import unittest
import os
from functools import wraps

###############################################################################
#  DECORATORS
###############################################################################

def pn_pn_serial(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.mpi_procs = 1
        self.log_suffix = '.pn_pn'
        if self.ifmpi:
            self.log_suffix += '.parallel'
        else:
            self.log_suffix += '.serial'
        method(self, *args, **kwargs)
    return wrapper

def pn_pn_2_serial(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.mpi_procs = 1
        self.log_suffix = '.pn_pn_2'
        if self.ifmpi:
            self.log_suffix += '.parallel'
        else:
            self.log_suffix= '.serial'
        method(self, *args, **kwargs)
    return wrapper

def pn_pn_parallel(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.mpi_procs = 4
        if not self.ifmpi:
            self.skipTest("Skipping \"{0}\"; MPI is not enabled.".format(self.id()))
        else:
            self.log_suffix = '.pn_pn'
            if self.ifmpi:
                self.log_suffix += '.parallel'
            else:
                self.log_suffix += '.serial'
            method(self, *args, **kwargs)
    return wrapper

def pn_pn_2_parallel(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.mpi_procs = 4
        if not self.ifmpi:
            self.skipTest("Skipping \"{0}\"; MPI is not enabled.".format(self.id()))
        else:
            # Set number of mpi procs
            self.log_suffix = '.pn_pn_2'
            if self.ifmpi:
                self.log_suffix += '.parallel'
            else:
                self.log_suffix += '.serial'
            method(self, *args, **kwargs)
    return wrapper

###############################################################################
#  BASE TEST CASE
###############################################################################

class NekTestCase(unittest.TestCase):
    """ Base class for Nek unittests

    This defines a setUpClass method to:
        (a) get the relevant environment variables for compilers, directories
        (b) add env vars to maketools, makenek
        (b) build tools
    All subclassed TestCases will need to do these things.

    Class attributes:
        f77 (str):            The Fortran 77 compiler to use     [default: 'gfortran']
        cc (str):             The C compiler to use              [default: 'gcc']
        ifmpi (bool):         Perform compilation/tests with MPI [default: False]
        source_root (str):    Path to Nek source directory;overridden by $SOURCE_ROOT env variable
                              [default: '$HOME/nek5_svn/trunk/nek']
        tools_root (str):     Path to Nek tools directory; overridden by $TOOLS_ROOT env variable
                              [default: '$HOME/nek5_svn/trunk/tools']
        examples_root (str):  Path to Nek examples directory; overridden by $EXAMPLES_ROOT env variable
                              [default: '$HOME/nek5_svn/examples']
        makenek (str):        Path to makenek                    [default: source_root/makenek]
        tools_bin (str):      Directory to place compiled tools  [default: tools_root/bin]

    Subclass attributes:
        These aren't meaningful in the base class.  They're intended for a subclass that represents
        a particular example problem.
        example_subdir (str): The subdirectory for the subclass' example.  Assumed that it's in example_root
        rea_file (str):       The .rea file for the subclass' example, minus the '.rea' extension.  Assumed
                              that it's in example_root/example_dir
        size_file (str):      The SIZE file for the subclass' example.  Assuemed that it's in
                              example_root/example_subdir
    """
    # Defined in subclasses only; declared here to make syntax checker happy
    example_subdir      = ""
    rea_file            = ""
    box_file            = ""
    serial_script       = ""
    parallel_script     = ""


    def __init__(self, *args, **kwargs):
        # These can be overridden by self.get_opts
        self.f77            = "gfortran"
        self.cc             = "gcc"
        self.ifmpi          = False
        self.source_root    = "{0}/nek5_svn/trunk/nek".format(os.environ.get('HOME', ""))
        self.examples_root  = "{0}/nek5_svn/examples".format(os.environ.get('HOME', ""))
        self.tools_root     = "{0}/nek5_svn/trunk/tools".format(os.environ.get('HOME', ""))
        self.log_root       = ''
        self.makenek        = ''
        self.tools_bin      = ''

        # These can be overridden by method decorators (pn_pn_serial, pn_pn_parallel,
        # pn_pn_2_serial, and pn_pn_2_parallel)
        self.log_suffix = ""
        self.mpi_procs  = 1

        # Empy list of delayed fails
        self._delayed_failures = []

        self.get_opts()

        unittest.TestCase.__init__(self, *args, **kwargs)

    def assertAlmostEqualDelayed(self, test_val, target_val, delta, label):
        if abs(test_val-target_val) <= delta:
            msg = '    SUCCESS: {0}: Test value {1} equals target value {2} +/- {3}'.format(label, test_val, target_val, delta)
        else:
            msg = '    FAILURE: {0}: Test value {1} exceeds target value {2} +/- {3}'.format(label, test_val, target_val, delta)
            self._delayed_failures.append(msg)
        print(msg)

    def assertIsNotNullDelayed(self, test_val, label):
        if test_val:
            msg = 'SUCCESS: Found phrase "{0}" in logfile.'.format(label)
        else:
            msg = 'FAILURE: Unexpectedly did not find phrase "{0}" in logfile'.format(label)
            self._delayed_failures.append(msg)
        print(msg)

    def assertDelayedFailures(self):
        if self._delayed_failures:
            report = [
                '\n\nFailed assertions:{0}\n'.format(len(self._delayed_failures))
            ]
            for i,failure in enumerate(self._delayed_failures, start=1):
                report.append('{0}: {1}'.format(i, failure))
            #self._delayed_failures = []
            self.fail('\n'.join(report))

    def get_opts(self):


        print("Getting setup options...")

        # Get compilers from env, default to GNU
        self.f77   = os.environ.get('F77',   self.f77)
        self.cc    = os.environ.get('CC',    self.cc)
        self.ifmpi = os.environ.get('IFMPI', self.ifmpi)

        # String/bool conversion
        ifmpi_str = str(self.ifmpi).lower()
        self.ifmpi = ifmpi_str == 'yes' or ifmpi_str == 'true'

        for name, val in (('F77', self.f77),
                          ('CC', self.cc),
                          ('IFMPI', str(self.ifmpi).lower())):
            print('    Using {0}="{1}"'.format(name, val))

        # Get Nek5000 dirs from env, if defined
        self.source_root   = os.environ.get('SOURCE_ROOT',   self.source_root)
        self.tools_root    = os.environ.get('TOOLS_ROOT',    self.tools_root)
        self.examples_root = os.environ.get('EXAMPLES_ROOT', self.examples_root)
        self.log_root      = os.environ.get('LOG_ROOT',      self.log_root)
        if not self.makenek:
            self.makenek   = os.path.join(self.source_root, 'makenek')
        if not self.tools_bin:
            self.tools_bin = os.path.join(self.tools_root, 'bin')

        # Raise error if source_, tools_, tests_, examples_root don't exist
        for val, name in ((self.source_root,   'SOURCE_ROOT'),
                          #(cls.tests_root,    'TESTS_ROOT'),
                          (self.examples_root, 'EXAMPLES_ROOT'),
                          (self.tools_root,    'TOOLS_ROOT')):
            if os.path.isdir(val):
                print('    Using {0} at "{1}"'.format(name, val))
            else:
                raise RuntimeError('The {0} directory, "{1}", does not exist. \
                Please set ${0} to a valid path.'.format(name, val))

        # Make tools_bin if it doesn't exist
        for val, name in ((self.tools_bin, 'TOOLS_BIN'),
                          (self.log_root,  'LOG_ROOT')):
            if val:
                if os.path.isdir(val):
                    print('    Using {0} at "{1}"'.format(name, val))
                else:
                    print('    The {0} directory, "{1}" does not exist.  It will be created'.format(name, val))
                    os.makedirs(val)

        print("Finished getting setup options!")

    def build_tools(self, targets=None, tools_root=None, tools_bin=None, f77=None, cc=None, bigmem=None):
        from tools.nekBinBuild import build_tools
        build_tools(
            targets    = targets    if targets    else ('clean', 'genmap'),
            tools_root = tools_root if tools_root else self.tools_root,
            tools_bin  = tools_bin  if tools_bin  else self.tools_bin,
            f77        = f77        if f77        else 'gfortran',
            cc         = cc         if cc         else 'gcc',
            bigmem     = bigmem     if bigmem     else 'false'
        )

    def config_size(self, infile=None, outfile=None, lx=None, ly=None, lz=None):
        from tools.nekFileConfig import config_size
        cls = self.__class__

        if not infile:
            infile = os.path.join(self.examples_root, cls.example_subdir, 'SIZE')
        if not outfile:
            outfile = os.path.join(self.examples_root, cls.example_subdir, 'SIZE')

        config_size(
            infile  = infile,
            outfile = outfile,
            lx2 = lx,
            ly2 = ly,
            lz2 = lz
        )

    def run_genmap(self, tol='0.5'):
        from tools.nekBinRun import run_meshgen
        cls = self.__class__
        run_meshgen(
            command = os.path.join(self.tools_bin, 'genmap'),
            stdin   = [cls.rea_file, tol],
            cwd     = os.path.join(self.examples_root, cls.example_subdir),
        )

    def run_genbox(self, box_file=None):
        from tools.nekBinRun import run_meshgen
        assert(box_file or self.__class__.box_file)

        if not box_file:
            box_file = self.__class__.box_file

        # Fix extension, in case user doesn't provide it
        root, ext = os.path.splitext(box_file)
        if ext != '.box':
            box_file = root + ext + '.box'

        run_meshgen(
            command = os.path.join(self.tools_bin, 'genbox'),
            stdin   = [box_file],
            cwd     = os.path.join(self.examples_root, self.__class__.example_subdir),
        )

    def build_nek(self):
        from tools.nekBinBuild import build_nek
        cls = self.__class__

        build_nek(
            source_root = self.source_root,
            rea_file    = cls.rea_file,
            cwd         = os.path.join(self.examples_root, cls.example_subdir),
            f77         = self.f77,
            cc          = self.cc,
            ifmpi       = str(self.ifmpi).lower()
        )

    def run_nek(self, mpi_procs=None):
        from tools.nekBinRun import run_nek_script
        cls = self.__class__

        # Serial run
        if not self.ifmpi:
            run_nek_script(
                script     = os.path.join(self.tools_root, 'scripts', cls.serial_script),
                rea_file   = cls.rea_file,
                cwd        = os.path.join(self.examples_root, cls.example_subdir),
                log_suffix = self.log_suffix,
                mpi_procs  = self.mpi_procs if not mpi_procs else mpi_procs
            )
        # Parallel run
        else:
            run_nek_script(
                script     = os.path.join(self.tools_root, 'scripts', cls.parallel_script),
                rea_file   = cls.rea_file,
                cwd        = os.path.join(self.examples_root, cls.example_subdir),
                log_suffix = self.log_suffix,
                mpi_procs  = self.mpi_procs if not mpi_procs else mpi_procs
            )

    def move_logs(self):
        cls = self.__class__
        if self.log_root:

            if not os.path.isdir(os.path.join(self.log_root, cls.example_subdir)):
                os.makedirs(os.path.join(self.log_root, cls.example_subdir))

            for f in os.listdir(os.path.join(self.examples_root, cls.example_subdir)):
                if f == 'compiler.out' or f == 'genmap.out' or 'log' in f:
                    os.rename(
                        os.path.join(self.examples_root, cls.example_subdir, f),
                        os.path.join(self.log_root, cls.example_subdir, f)
                    )

    def mvn(self, src_prefix, dest_prefix):
        from tools.nekBinRun import mvn
        cls = self.__class__
        mvn(src_prefix, dest_prefix,
            cwd = os.path.join(self.examples_root, cls.example_subdir)
        )


    def get_value_from_log(self, label, column, row=0, logfile=None):
        cls = self.__class__
        if not logfile:
            logfile = os.path.join(
                self.examples_root,
                cls.example_subdir,
                '{0}.log.{1}{2}'.format(cls.rea_file, self.mpi_procs, self.log_suffix)
            )
        # Get all lines with label
        with open(logfile, 'r') as f:
            line_list = [l for l in f if label in l]
        if not line_list:
            raise ValueError("Could not find label \"{0}\" in logfile \"{1}\".  The run may have failed.".format(label, logfile))
        try:
            value = float(line_list[row].split()[column])
        except ValueError:
            raise ValueError("Attempted to parse non-numerical value in logfile, \"{0}\".  Logfile may be malformatted or run may have failed".format(logfile))
        except IndexError:
            raise IndexError("Fewer rows and/or columns than expected in logfile, \"{0}\".  Logfile may be malformmated or run may have failed.".format(logfile))
        else:
            return value

    def get_phrase_from_log(self, label, logfile=None, row=0):
        cls = self.__class__
        if not logfile:
            logfile = os.path.join(
                self.examples_root,
                cls.example_subdir,
                '{0}.log.{1}{2}'.format(cls.rea_file, self.mpi_procs, self.log_suffix)
            )

        with open(logfile, 'r') as f:
            line_list = [l for l in f if label in l]

        try:
            line = line_list[row]
        except IndexError:
            return None
        else:
            return line

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
# class Blasius(NekTestCase):
#     example_subdir  = 'blasius'
#     rea_file        = 'blasius'
#     serial_script   = 'nek10s'
#     parallel_script = 'nek10steps'
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
# class ConjHt(NekTestCase):
#     example_subdir  = 'conj_ht'
#     rea_file        = 'conj_ht'
#     serial_script   = 'nekbb'
#     parallel_script = 'neklmpi'
#
# ####################################################################
# #  cyl_restart: ca.rea, cb.rea, pa.rea, pb.rea
# ####################################################################
#
# class CylRestart(NekTestCase):
#     # No rea_file here; defined in subclasses below
#     example_subdir  = 'cyl_restart'
#     serial_script   = 'nekbb'
#     parallel_script = 'neklmpi'
#
# class CylRestartCa(CylRestart):
#     rea_file = 'ca'
#
# class CylRestartCb(CylRestart):
#     rea_file = 'cb'
#
# class CylRestartPa(CylRestart):
#     rea_file = 'pa'
#
# class CylRestartPb(CylRestart):
#     rea_file = 'pb'
#
# ####################################################################
# #  eddy; eddy_uv.rea, amg_eddy.rea, htps_ed.rea
# ####################################################################
#
# # TODO: implement eddy for amg_eddy.rea, htps_ed.rea
#
# class EddyEddyUv(NekTestCase):
#
#     example_subdir  = 'eddy'
#     rea_file        = 'eddy_uv'
#     serial_script   = 'nekbb'
#     parallel_script = 'neklmpi'
#
#     @classmethod
#     def setUpClass(cls):
#         from re import sub
#
#         cls.get_opts()
#
#         build_tools(
#             targets    = ('clean', 'genmap'),
#             tools_root = cls.tools_root,
#             tools_bin  = cls.tools_bin,
#             f77='gfortran',
#
#             cc         = 'gcc',
#             bigmem     = 'false'
#         )
#         config_size(
#             infile  = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
#             outfile = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
#             lx2 = cls.lx2,
#             ly2 = cls.ly2,
#             lz2 = cls.lz2
#         )
#
#         # Tweak .rea
#         rea_path = os.path.join(cls.examples_root, cls.example_subdir, cls.rea_file+'.rea')
#         with open(rea_path, 'r') as f:
#             lines = [sub(r'^.*DIVERGENCE$', '      0.10000E-08', l) for l in f]
#         with open(rea_path, 'w') as f:
#             f.writelines(lines)
#
#         run_meshgen(
#             command = os.path.join(cls.tools_bin, 'genmap'),
#             stdin   = [cls.rea_file, '0.5'],
#             cwd     = os.path.join(cls.examples_root, cls.example_subdir),
#             )
#         build_nek(
#             source_root = cls.source_root,
#             rea_file    = cls.rea_file,
#             cwd         = os.path.join(cls.examples_root, cls.example_subdir),
#             f77         = cls.f77,
#             cc          = cls.cc,
#             ifmpi       = str(cls.ifmpi).lower()
#         )
#         # Serial run
#         if not cls.ifmpi:
#             run_nek_script(
#                 script     = os.path.join(cls.tools_root, 'scripts', cls.serial_script),
#                 rea_file   = cls.rea_file,
#                 cwd        = os.path.join(cls.examples_root, cls.example_subdir),
#                 log_suffix = cls.serial_log_suffix
#             )
#         # Parallel run
#         else:
#             run_nek_script(
#                 script     = os.path.join(cls.tools_root, 'scripts', cls.parallel_script),
#                 rea_file   = cls.rea_file,
#                 cwd        = os.path.join(cls.examples_root, cls.example_subdir),
#                 log_suffix = cls.parallel_log_suffix,
#                 mpi_procs  = ("1", "4")
#             )
#
# ####################################################################
# #  eddy_neknek: eddy_neknek.rea
# ####################################################################
#
# # TODO: implment eddy_neknek tests
#
# ####################################################################
# #  eddy_psi_omega; psi_omega.rea
# ####################################################################
#
# class EddyPsiOmega(NekTestCase):
#     example_subdir  = 'eddy_psi_omega'
#     rea_file        = 'psi_omega'
#     serial_script   = 'nek10s'
#     parallel_script = 'nek10steps'
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
# class ExtCyl(NekTestCase):
#     example_subdir  = 'ext_cyl'
#     rea_file        = 'ext_cyl'
#     serial_script   = 'nek1000s'
#     parallel_script = 'nek1000steps'
#
# ####################################################################
# #  fs_hydro; fs_hydro.rea
# ####################################################################
#
# class FsHydro(NekTestCase):
#     example_subdir  = 'fs_hydro'
#     rea_file        = 'fs_hydro'
#     serial_script   = 'nek1000s'
#     parallel_script = 'nek1000steps'
#
# ####################################################################
# #  hemi: hemi.rea
# ####################################################################
#
# class Hemi(NekTestCase):
#     example_subdir  = 'hemi'
#     rea_file        = 'hemi'
#     serial_script   = 'nek10s'
#     parallel_script = 'nek10steps'

