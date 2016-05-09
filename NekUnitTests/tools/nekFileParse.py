def get_value(label, column, logfile):
    with open(logfile, 'r') as f:
        for line in f:
            if label in line:
                try:
                    value = float(line.split()[-column])
                except ValueError:
                    raise ValueError("Attempted to parse non-numerical value in logfile, \"{0}\".  The logfile may be malformatted".format(logfile))
                except IndexError:
                    raise IndexError("Fewer columns than expected in logfile, \"{0}\".  Logfile may be malformmated.".format(logfile))
                else:
                    return value
    return None
