import subprocess
import logging


class CommandController:

    @staticmethod
    def run_command(argv):
        logging.debug('COMMAND RUN: ' + ' '.join(argv))

        output = subprocess.run(argv, stdout=subprocess.PIPE).stdout.decode('utf-8')

        if len(output) != 0:
            logging.debug('COMMAND OUTPUT: ' + output)

        return output
