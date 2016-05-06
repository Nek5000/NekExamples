import os
from subprocess import check_call, PIPE, STDOUT, Popen, SubprocessError

def run_genmap(tools_bin, cwd, rea_file, tolerance=".05"):
    """ Runs genmap, using the .rea file defined by cls.rea_file

        Not useful in base class.  Useful in subclass for a given example,
        where cls.rea_file is defined

    Params:
        tolerance (str): Mesh tolerance.
                         It's a string, not a float, since it's piped into stdin as a literal
    """

    genmap  = os.path.join(tools_bin, 'genmap')
    logfile = os.path.join(cwd, 'genmap.out')
    stdin   = bytes("{0}\n{1}".format(rea_file, tolerance), 'ascii')

    print('Running genmap...')
    print('    Using executable "{0}"'.format(genmap))
    print('    Using working directory "{0}"'.format(cwd))
    print('    Using .rea file "{0}"'.format(rea_file))

    try:
        with open(logfile, 'w') as f:
            Popen([genmap], stdin=PIPE, stderr=STDOUT, stdout=f, cwd=cwd).communicate(stdin)
    except (OSError, SubprocessError) as E:
        # TODO: Change to warnings.warn()
        print('Could not complete genmap!  Caught error: "{0}".  Check "{1}" for details.'.format(E, logfile))

    print("Succefully finished genmap!")

def run_nek_script(script, rea_file, cwd, log_suffix="", mpi_procs=("1",)):
    for p in mpi_procs:
        try:
            logs = (os.path.join(cwd, "logfile"), os.path.join(cwd, rea_file+".log."+p))

            # Remove old logs
            for l in logs:
                if os.path.exists(l):
                    os.remove(l)

            # Running 'script' through shell since it doesn't have a shebang at the top.
            # Need to concatenate args into a string if shell=True
            cmd = " ".join([script, rea_file, p])
            print("Running nek5000...")
            print('    Using command "{0}"'.format(cmd))
            print('    Using working directory "{0}"'.format(cwd))
            check_call(cmd, cwd=cwd, shell=True)

            # Rename logs
            if log_suffix:
                for l in logs:
                    os.rename(l, l+log_suffix)

        # This are expected exceptions if 'check_call' or 'os.rename' fail.
        # We issue a warning, not error, so subsequent tests can continue
        except (OSError, SubprocessError) as E:
            # TODO: Change to warnings.warn()
            print('Could not complete command: "{0}"!  Caught error: "{1}"'.format(
                " ".join([script, rea_file, p]), E))
