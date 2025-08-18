import os
import logging
def setup_logger(file_name='poe.log'):     
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s', filename=f'logs/{file_name}', 
        filemode='a'
        )