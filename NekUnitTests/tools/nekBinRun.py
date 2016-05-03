import os
from subprocess import check_call, PIPE, Popen

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

def run_nek10s(rea_file, cwd, logfile):

    nek5000      = os.path.join(cwd, "nek5000")
    session_name = os.path.join(cwd, "SESSION_NAME")
    ioinfo       = os.path.join(cwd, "ioinfo")

    print('Running nek10s...')
    print('    Using executable "{0}"'.format(nek5000))
    print('    Using working directory "{0}"'.format(cwd))
    print('    Using logfile "{0}"'.format(logfile))

    with open(session_name, "w") as f:
        f.write(rea_file)
        f.write(cwd)

    with open(ioinfo, "w") as f:
        f.write("-10")

    with open(logfile, 'w') as f:
        check_call([nek5000], cwd=cwd,  stdout=f)
