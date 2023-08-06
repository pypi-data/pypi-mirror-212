import argparse
import sys
from multiprocessing import Queue
from threading import Thread, Timer

sys.path.append('../')
from metalayer.consumer import CaptureConsumer
from metalayer.producer import CaptureProducer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-E', '--disable-embeddings', action='store_true',
                        help='Disable the embeddings, only valid if matching is enabled')
    parser.add_argument('-S', '--skip-sites', action='store_true',
                        help='Whether to fetch the url and favicon for visited sites in supported browsers. '
                             'Setting this flag will disable this feature. ')
    parser.add_argument('-I', '--capture-interval', type=float, default=1.,
                        help='Interval after no keyboard or mouse activity to capture a screenshot')
    parser.add_argument('-P', '--wait-for-power', action='store_true',
                        help='Wait until connected to external power before running OCR')
    parser.add_argument('-T', type=int, default=None,
                        help='Stop after T seconds. If not set, will run indefinitely.')
    parser.add_argument('-v', '--vault-path', type=str, default=None,
                        help='Path to the Obsidian vault to store indexed knowledge.')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    buffer = Queue()
    backend = 'macos' if sys.platform == 'darwin' else 'easyocr'
    producer = CaptureProducer(args.capture_interval, buffer,
                               save_sites=not args.skip_sites)
    consumer = CaptureConsumer(buffer, backend,
                               obsidian_vault_path=args.vault_path,
                               embeddings_enabled=not args.disable_embeddings,
                               wait_for_power=args.wait_for_power)

    # Soft-stop: finish OCR before exiting program
    def soft_stop():
        producer.stop()
        consumer.wait_for_power = False

    def wait_for_quit():
        while input() != 'q':
            pass
        soft_stop()

    stop_thread = Thread(target=wait_for_quit, daemon=True)

    producer.start()
    consumer.start()

    stop_thread.start()
    if args.T:
        timer = Timer(args.T, soft_stop)
        timer.start()

    producer.join()
    consumer.join()

    if args.T:
        timer.cancel()


if __name__ == '__main__':
    main()
