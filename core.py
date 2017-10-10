import multiprocessing,time,logging
from config import  *
from generator import WeiboCookieGenerator
from checker import WeiboCookieChecker
from api import app

#核心调度器
logging.basicConfig(level=logging.DEBUG)
class Scheduler(object):

    @staticmethod
    def check_cookie(inteval=CHECK_INTERVAL):
        logging.debug('start to check cookie')
        checkers = []
        for name, cls in CHECKER_MAP.items():
            checker = eval('{}()'.format(cls))
            checkers.append(checker)
        while True and checkers:
            try:
                    for c in checkers:
                        c.run()
                        logging.debug('checker {} run complete'.format(c.__class__))
                    time.sleep(inteval)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(inteval=GEN_INTERVAL):
        logging.debug('start to generate cookie')
        generators = []
        for name, cls in GENERATOR_MAP.items():
            generator = eval('{}()'.format(cls))
            generators.append(generator)

        while True and generators:
            try:
                    for g in generators:
                        g.run()
                        logging.debug('generator {} run complete'.format(g.__class__))
                    time.sleep(inteval)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        app.run(host='0.0.0.0')


if __name__ == '__main__':
    if CHECKER_RUN:
        p1 = multiprocessing.Process(target=Scheduler.check_cookie)
        p1.start()
    if GENERATOR_RUN:
        p2 = multiprocessing.Process(target=Scheduler.generate_cookie)
        p2.start()
    if API_RUN:
        p3 = multiprocessing.Process(target=Scheduler.api)
        p3.start()