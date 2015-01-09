import logging
import sys

if __name__ == '__main__':

    logging.basicConfig(filename = 'MuxControl.log',
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',level = logging.DEBUG)
    logging.captureWarnings(True)

    try:
        import muxControl.MuxControl
        muxControl.MuxControl.main()
    except SystemExit as e:
        if e.code == 1:
            logging.info('First time dialog cancelled. Exiting')
        else:
            raise e
    except:
        logging.exception('Something went wrong')
        print 'Something went wrong - check the error log'
        logging.info('Exiting')

    logging.shutdown()
    sys.exit(0)