import logging
import config
from api import app

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run():
    try:
        app.run()
    except Exception as e:
        logging.error("An error occurred while running the app", exc_info=True)

if __name__ == "__main__":
    run()
