import os
import sys
from subprocess import call, check_call, Popen, PIPE, STDOUT
from lib.nekFileConfig import config_makenek, config_maketools, config_basics_inc

def build_tools(tools_root, tools_bin, f77=None, cc=None, bigmem=None,
                targets=('clean', 'all'), verbose=False):

    print('Compiling tools... ')
    print('    Using source directory "{0}"'.format(tools_root))
    print('    Using output directory "{0}"'.format(tools_bin))
    print('    Using F77 "{0}"'.format(f77))
    print('    Using CC "{0}"'.format(cc))

    maketools_in  = os.path.join(tools_root, 'maketools')
    maketools_out = os.path.join(tools_root, 'maketools.tests')
    maketools_log = os.path.join(tools_root, 'maketools.out')

    try:

        config_maketools(
            infile  = maketools_in,
            outfile = maketools_out,
            f77     = f77,
            cc      = cc,
            bigmem  = bigmem
        )

        config_basics_inc(
            infile  = os.path.join(tools_root, 'prenek', 'basics.inc'),
            outfile = os.path.join(tools_root, 'prenek', 'basics.inc'),
            nelm    = '10 000'
        )

        with open(maketools_log, 'w') as f:
            for t in targets:
                if verbose:
                    proc = Popen(
                        [maketools_out, t, tools_bin],
                        cwd=tools_root,
                        stderr=STDOUT,
                        stdout=PIPE
                    )
                    for line in proc.stdout:
                        sys.stdout.write(line)
                        f.write(line)
                else:
                    check_call(
                        [maketools_out, t, tools_bin],
                        stderr=STDOUT,
                        stdout=f,
                        cwd=tools_root
                    )
    except:
        print('Could not compile tools! Check "{0}" for details.'.format(maketools_log))
        raise
    else:
        print('Successfully compiled tools!')

def build_nek(source_root, usr_file, cwd=None, f77=None, cc=None, ifmpi=None, pplist=None, verbose=False):

    print('Compiling nek5000...')
    print('    Using source directory "{0}"'.format(source_root))
    print('    Using working directory "{0}"'.format(cwd))
    print('    Using .usr file "{0}"'.format(usr_file))
    print('    Using F77 "{0}"'.format(f77))
    print('    Using CC "{0}"'.format(cc))
    print('    Using IFMPI "{0}"'.format(ifmpi))

    makenek_in  = os.path.join(source_root, 'bin', 'makenek')
    makenek_out = os.path.join(source_root, 'bin', 'makenek.tests')
    logfile     = os.path.join(cwd, 'compiler.out')
    try:
        config_makenek(
            infile      = makenek_in,
            outfile     = makenek_out,
            f77         = f77,
            cc          = cc,
            source_root = source_root,
            ifmpi       = ifmpi,
            pplist      = pplist,
        )

        call([makenek_out, 'clean'], cwd=cwd)
        if verbose:
            with open(logfile, 'w') as f:
                proc = Popen([makenek_out, usr_file], cwd=cwd, stderr=STDOUT, stdout=PIPE)
                for line in proc.stdout:
                    sys.stdout.write(line)
                    f.write(line)
        else:
            with open(logfile, 'w') as f:
                call([makenek_out, usr_file], cwd=cwd, stdout=f)

    except:
        print('Could not compile nek5000!')
        raise
    else:
        print('Successfully compiled nek5000!')


