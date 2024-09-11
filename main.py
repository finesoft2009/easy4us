# main.py  
import os  # Импортируем os для использования os.path.basename  
import logging  
import argparse  
from easy4us.auth import Authenticator  
from easy4us.decoder import Decoder  

# Настройка логирования  
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')  

# Парсер аргументов  
parser = argparse.ArgumentParser(usage="easy4us", description="decode directories with easytoyou.eu")  
parser.add_argument("-u", "--username", required=True, help="easytoyou.eu username")  
parser.add_argument("-p", "--password", required=True, help="easytoyou.eu password")  
parser.add_argument("-s", "--source", required=True, help="source directory")  
parser.add_argument("-o", "--destination", required=True, help="destination directory", default="")  
parser.add_argument("-d", "--decoder", help="decoder (default: ic11php72)", default="ic11php72")  
parser.add_argument("-w", "--overwrite", help="overwrite files", action='store_true', default=False)  
parser.add_argument("--account", help="fetch account membership details", action='store_true')  
args = parser.parse_args()  

def main():  
    if not args.destination:  
        args.destination = f"{os.path.basename(args.source)}_decoded"  
    
    auth = Authenticator(args.username, args.password)  
    session = auth.login()  
    
    if session:  
        if args.account:  
            details = auth.get_membership_details(session)  
            if details:  
                membership_type, valid_until = details  
                logging.info(f"Account valid until {valid_until}.")  
            else:  
                logging.error("Could not retrieve membership details.")  

        decoder = Decoder(session, args.decoder, args.source, args.destination, args.overwrite)  
        decoder.process()  

if __name__ == '__main__':  
    main()