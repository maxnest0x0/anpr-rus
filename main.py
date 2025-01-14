import multiprocessing
from api.app import run_api
from bot.app import run_bot

def main():
    api_thread = multiprocessing.Process(target=run_api)
    bot_thread = multiprocessing.Process(target=run_bot)

    api_thread.start()
    bot_thread.start()

    api_thread.join()
    bot_thread.join()

if __name__ == '__main__':
    main()
