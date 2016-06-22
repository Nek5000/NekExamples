import os
import sys
from subprocess import call, check_call, PIPE, STDOUT, Popen, CalledProcessError

def run_meshgen(command, stdin, cwd):

    logfile = os.path.join(cwd, '{0}.out'.format(os.path.basename(command)))
    stdin_bytes   = bytes("\n".join(stdin))

    print('Running "{0}"...'.format(os.path.basename(command)))
    print('    Using command "{0}"'.format(command))
    print('    Using stdin "{0}"'.format(stdin))
    print('    Using working directory "{0}"'.format(cwd))

    try:
        with open(logfile, 'w') as f:
            Popen([command], stdin=PIPE, stderr=STDOUT, stdout=f, cwd=cwd).communicate(stdin_bytes)
    except (OSError, CalledProcessError) as E:
        # TODO: Change to warnings.warn()
        print('Could not complete {0}!  Caught error: "{1}".  Check "{2}" for details.'.format(command, E, logfile))
    else:
        print("Succefully finished {0}!".format(os.path.basename(command)))


def run_nek_script(script, rea_file, cwd, log_suffix='', mpi_procs='1'):
    try:
        logs = (os.path.join(cwd, "logfile"), os.path.join(cwd, "{0}.log.{1}".format(rea_file, mpi_procs)))

        # Remove old logs
        for l in logs:
            if os.path.exists(l):
                os.remove(l)

        # Running 'script' through shell since it doesn't have a shebang at the top.
        # Need to concatenate args into a string if shell=True
        cmd = " ".join([script, rea_file, str(mpi_procs)])
        print("Running nek5000...")
        print('    Using command "{0}"'.format(cmd))
        print('    Using working directory "{0}"'.format(cwd))
        try:
            # TODO: This doesn't work as intended.  If the nek executable fails, the nek script doesn't return the error.
            # Check doxygen to see what exit values there are (some succesful exit values there are!)
            check_call(cmd, cwd=cwd, shell=True)
        except Exception as E:
            # TODO: Change to warnings.warn()
            print('Could not successfully run nek5000! Caught error: {0}'.format(E))
        else:
            #print('Successfully ran nek5000!')
            print('Finished running nek5000!')

        # Rename logs
        if log_suffix:
            for l in logs:
                os.rename(l, l+log_suffix)

    # This are expected exceptions if 'check_call' or 'os.rename' fail.
    # We issue a warning, not error, so subsequent tests can continue
    except (OSError, CalledProcessError) as E:
        # TODO: Change to warnings.warn()
        print('Could not complete command: "{0}": {1}'.format(
            " ".join([script, rea_file, mpi_procs]), E))

def run_nek(cwd, rea_file, ifmpi, log_suffix='', n_procs=1, step_limit=None, verbose=False):
    # Paths to executables, files
    nek5000      = os.path.join(cwd, 'nek5000')
    logfile      = os.path.join(cwd, '{0}.log.{1}{2}'.format(rea_file, n_procs, log_suffix))
    session_name = os.path.join(cwd, 'SESSION.NAME')
    ioinfo       = os.path.join(cwd, 'ioinfo')
    sch_file     = os.path.join(cwd, '{0}.sch'.format(rea_file))
    if ifmpi:
        command = ['mpiexec', '-np', str(n_procs), nek5000]
    else:
        command = [nek5000]

    print("Running nek5000...")
    print('    Using command "{0}"'.format(' '.join(command)))
    print('    Using working directory "{0}"'.format(cwd))
    print('    Using .rea file "{0}"'.format(rea_file))

    # An OSError here can be expected
    # If the examples directory is clean, there will be no .sch file and
    # os.remove(sch_file) will be expected to fail.
    try:
        os.remove(sch_file)
    except OSError as E:
        # TODO: Change to warnings.warning
        print("    Could not remove {0}: {1}".format(sch_file, E))

    # Any error here is unexepected
    try:
        with open(session_name, 'w') as f:
            f.writelines([rea_file+"\n", cwd+'/\n'])

        if step_limit:
            with open(ioinfo, 'w') as f:
                f.writelines(['-{0}'.format(step_limit)])

        if verbose:
            with open(logfile, 'w') as f:
                proc =Popen(command, cwd=cwd, stderr=STDOUT, stdout=PIPE)
                for line in proc.stdout:
                    sys.stdout.write(line)
                    f.write(line)
        else:
            with open(logfile, 'w') as f:
                call(command, cwd=cwd, stdout=f)

    except Exception as E:
        # TODO: Change to warnings.warn()
        print('Could not successfully run nek5000! Caught error: {0}'.format(E))
    else:
        print('Finished running nek5000!')


def mvn(src_prefix, dst_prefix, cwd):
    exts = ('.box', '.rea', '.usr', '.map', '.sep', '.re2')
    print("Running mvn...")
    print('    Using working directory "{0}"'.format(cwd))
    for x in exts:
        src = os.path.join(cwd, src_prefix + x)
        dst = os.path.join(cwd, dst_prefix + x)
        try:
            os.rename(src, dst)
        except OSError as E:
            # TODO: Change to warnings.warn()
            print("    Could not move {0} to {1}: {2}".format(src, dst, E))
        else:
            print("    Successfully moved {0} to {1}".format(src, dst))
    print('Finished running mvn!')
