import os
from subprocess import check_call, PIPE, STDOUT, Popen, SubprocessError

def run_meshgen(command, stdin, cwd):

    logfile = os.path.join(cwd, '{0}.out'.format(os.path.basename(command)))
    stdin   = bytes("\n".join(stdin), 'ascii')

    print('Running "{0}"...'.format(os.path.basename(command)))
    print('    Using command "{0}"'.format(command))
    print('    Using stdin "{0}"'.format(stdin))
    print('    Using working directory "{0}"'.format(cwd))

    try:
        with open(logfile, 'w') as f:
            Popen([command], stdin=PIPE, stderr=STDOUT, stdout=f, cwd=cwd).communicate(stdin)
    except (OSError, SubprocessError) as E:
        # TODO: Change to warnings.warn()
        print('Could not complete {0}!  Caught error: "{1}".  Check "{2}" for details.'.format(command, E, logfile))

    print("Succefully finished {0}!".format(os.path.basename(command)))


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
            print('Could not complete command: "{0}": {1}'.format(
                " ".join([script, rea_file, p]), E))

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
