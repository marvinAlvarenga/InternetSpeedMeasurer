import datetime
import json
import logging
import time

import schedule
import speedtest


settings = {
    'OUTPUT_PATH': 'C:/Users/Marvin Alvarenga/Documents/SpeedMeasuring/output.csv',
    'LOG_LEVEL': 'DEBUG',
    'LOG_OUTPUT': 'C:/Users/Marvin Alvarenga/Documents/SpeedMeasuring/logs.log',
}


def __get_logger():
    logger = logging.getLogger('SPEED_MEASURING_SCRIPT')

    level = settings['LOG_LEVEL']
    logger.setLevel(logging._nameToLevel[level])

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(settings['LOG_OUTPUT'], encoding='utf-8')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = __get_logger()


def measure():
    logger.info('Started measuring')
    s = speedtest.Speedtest()
    s.download()
    s.upload()
    logger.info('Finished measuring')

    result = s.results.dict()

    logger.debug(json.dumps(result))

    return result


def format(data):
    return '{},{},{},{},{}\n'.format(
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data['download'] / 1000000,
        data['upload'] / 1000000,
        data['ping'],
        data['server']['url'],
    )


def write_to_csv(row):
    logger.info('Writing to csv')
    output_path = settings['OUTPUT_PATH']
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(row)


def main():
    logger.info('Script Started')

    result = measure()
    formated_result = format(result)
    write_to_csv(formated_result)

    logger.info('Script Finished')
    logger.info('Waiting for the next execution...')


def run_job():
    schedule.every(10).minutes.do(main)
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    try:
        logger.info('Starting job')
        run_job()
    except Exception as e:
        logger.exception(e)
        logger.info('Closing job')
        schedule.clear()
    except KeyboardInterrupt:
        logger.info('Closing job')
        schedule.clear()
