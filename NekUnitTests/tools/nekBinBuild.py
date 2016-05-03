import os
from subprocess import check_call
from NekUnitTests.tools.nekFileConfig import config_makenek, config_maketools, config_basics_inc

def build_tools(tools_root, tools_bin, f77=None, cc=None, bigmem=None):

    print('Compiling tools... ')
    print('    Using source directory "{0}"'.format(tools_root))
    print('    Using output directory "{0}"'.format(tools_bin))
    print('    Using F77 "{0}"'.format(f77))
    print('    Using CC "{0}"'.format(cc))

    maketools_in  = os.path.join(tools_root, 'maketools')
    maketools_out = os.path.join(tools_root, 'maketools.tests')

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

        # check_call([maketools_out, 'clean', cls.tools_bin], cwd=cls.tools_root)
        check_call([maketools_out, 'all', tools_bin], cwd=tools_root)

    except:
        print('Could not compile tools!')
        raise
    else:
        print('Successfully compiled tools!')

def build_nek(source_root, rea_file, cwd=None, f77=None, cc=None, ifmpi=None):

    print('Compiling nek5000...')
    print('    Using source directory "{0}"'.format(source_root))
    print('    Using working directory "{0}"'.format(cwd))
    print('    Using rea_file "{0}"'.format(rea_file))
    print('    Using F77 "{0}"'.format(f77))
    print('    Using CC "{0}"'.format(cc))
    print('    Using IFMPI "{0}"'.format(ifmpi))

    makenek_in  = os.path.join(source_root, 'makenek')
    makenek_out = os.path.join(source_root, 'makenek.tests')

    try:

        config_makenek(
            infile      = makenek_in,
            outfile     = makenek_out,
            f77         = f77,
            cc          = cc,
            ifmpi       = ifmpi
        )

        # check_call([makenek_out, 'clean', source_root], cwd=cwd)
        check_call([makenek_out, rea_file, source_root], cwd=cwd)

    except:
        print('Could not compile nek5000!')
        raise
    else:
        print('Successfully compiled nek5000!')


