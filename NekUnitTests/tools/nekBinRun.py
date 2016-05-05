import os
from subprocess import check_call, PIPE, Popen, SubprocessError

def run_genmap(tools_bin, cwd, rea_file, tolerance=".05"):
    """ Runs genmap, using the .rea file defined by cls.rea_file

        Not useful in base class.  Useful in subclass for a given example,
        where cls.rea_file is defined

    Params:
        tolerance (str): Mesh tolerance.
                         It's a string, not a float, since it's piped into stdin as a literal
    """

    genmap = os.path.join(tools_bin, 'genmap')
    stdin  = bytes("{0}\n{1}".format(rea_file, tolerance), 'ascii')

    print('Running genmap...')
    print('    Using executable "{0}"'.format(genmap))
    print('    Using working directory "{0}"'.format(cwd))
    print('    Using .rea file "{0}"'.format(rea_file))

    try:
        Popen([genmap], stdin=PIPE, cwd=cwd).communicate(stdin)
    except:
        print("Could not complete genmap!")
        raise
    print("Succefully finished genmap!")

def run_nek_script(script, rea_file, cwd, log_suffix="", mpi_procs=tuple("1")):
    for p in mpi_procs:
        try:
            # Running 'script' through shell since it doesn't have a shebang at the top.
            # Need to concatenate args into a string if shell=True
            check_call(" ".join([script, rea_file, p]), cwd=cwd, shell=True)
            logs = (os.path.join(cwd, "logfile"), os.path.join(cwd, rea_file+".log."+p))
            if log_suffix:
                for l in logs:
                    os.rename(l, l+log_suffix)
        # This are expected exceptions if 'check_call' or 'os.rename' fail.
        # We issue a warning, not error, so subsequent tests can continue
        except (OSError, SubprocessError) as E:
            # TODO: Change to warnings.warn()
            print('Could not complete command: "{0}"!  Caught error: "{1}"'.format(
                " ".join([script, rea_file, p]), E))
