from tools.nekTestCase import *

class TurbChannelPnPn(NekTestCase):

    example_subdir = 'turbChannel'
    rea_file       = 'turbChannel'

    serial_script     = 'nek10s'
    serial_log_suffix = '.pn-pn.serial'

    parallel_script     = 'nek10steps'
    parallel_log_suffix = '.pn-pn.parallel'

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1'

    def test_GmresSerial(self):
        """ Greps gmres from logs """
        cls = self.__class__
        if not cls.ifmpi:
            self.check_value(
                logfile      = cls.serial_log,
                label        = 'gmres: ',
                target_value = 0.,
                delta        = 95.,
                column       = 7
            )
        else:
            self.check_value(
                logfile      = cls.parallel_logs["1"],
                label        = 'gmres: ',
                target_value = 0.,
                delta        = 95.,
                column       = 7
            )

    @skip_unless_mpi
    def test_GmresParallel(self):
        """ Greps gmres from logs """
        cls = self.__class__
        self.check_value(
            logfile      = cls.parallel_logs["4"],
            label        = 'gmres: ',
            target_value = 0.,
            delta        = 95.,
            column       = 7
        )


class TurbChannelPnPn2(NekTestCase):

    example_subdir = "turbChannel"
    rea_file       = 'turbChannel'

    serial_script     = 'nek10s'
    serial_log_suffix = '.pn-pn-2.serial'

    parallel_script     = 'nek10steps'
    parallel_log_suffix = '.pn-pn-2.parallel'

    lx2 = 'lx1'
    ly2 = 'ly1'
    lz2 = 'lz1-2'

    def test_GmresSerial(self):
        """ Greps gmres from logs """
        cls = self.__class__
        if not cls.ifmpi:
            self.check_value(
                logfile      =  cls.serial_log,
                label        = 'gmres: ',
                target_value = 0.,
                delta        = 26.,
                column       = 6
            )
        else:
            self.check_value(
                logfile      =  cls.parallel_logs["1"],
                label        = 'gmres: ',
                target_value = 0.,
                delta        = 26.,
                column       = 6
            )

    @skip_unless_mpi
    def test_GmresParallel(self):
        cls = self.__class__
        self.check_value(
            logfile      =  cls.parallel_logs["4"],
            label        = 'gmres: ',
            target_value = 0.,
            delta        = 26.,
            column       = 6
        )


if __name__ == '__main__':
    unittest.main()
