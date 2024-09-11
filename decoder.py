# easy4us/decoder.py  
import os  
import codecs  
import zipfile  
from io import BytesIO  
import requests  
from bs4 import BeautifulSoup  
import shutil  
import logging  
from .utils import batch  

class Decoder:  
    def __init__(self, session, decoder, source, destination, overwrite):  
        self.session = session  
        self.base_url = "https://easytoyou.eu"  
        self.decoder = decoder  
        self.source = source  
        self.destination = destination  
        self.overwrite = overwrite  
        self.headers = {  
            "Connection": "keep-alive",  
            "Cache-Control": "max-age=0",  
            "Upgrade-Insecure-Requests": "1",  
            "User-Agent": "Mozilla/5.0",  
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  
            "Accept-Encoding": "gzip, deflate, br",  
            "Accept-Language": "en-US,en;q=0.9"  
        }  
        self.not_decoded = []  

    def clear(self):  
        logging.info("Clearing page...")  
        while True:  
            try:  
                res = self.session.get(f"{self.base_url}/decoder/{self.decoder}/1", headers=self.headers)  
                s = BeautifulSoup(res.content, "lxml")  
                inputs = s.find_all(attrs={"name": "file[]"})  
                if not inputs:  
                    break  
                final = "".join([f"{urllib.parse.urlencode({i['name']: i.get('value', '')})}&" for i in inputs])  
                self.session.post(f"{self.base_url}/decoder/{self.decoder}/1", data=final, headers={**self.headers, "Content-Type": "application/x-www-form-urlencoded"})  
            except requests.RequestException as e:  
                logging.error(f"Error clearing page: {str(e)}")  
                break  

    def upload(self, dir, files):  
        logging.info(f"Preparing to upload files from directory: {dir}")  
        upload = []  
        upload_url = f"{self.base_url}/decoder/{self.decoder}"  
        for file in files:  
            full_path = os.path.join(dir, file)  
            if file.endswith(".php"):  
                logging.info(f"Adding file to upload list: {full_path}")  
                with codecs.open(full_path, 'rb') as f:  
                    upload.append(('file[]', (file, f, 'application/x-php')))  

        if upload:  
            logging.info(f"Uploading {len(upload)} files...")  
            try:  
                res = self.session.post(upload_url, headers=self.headers, files=upload)  
                return self.parse_upload_result(res)  
            except requests.RequestException as e:  
                logging.error(f"Error uploading files: {str(e)}")  
        else:  
            logging.warning("No files to upload.")  
        return [], []  

    def parse_upload_result(self, response):  
        try:  
            s = BeautifulSoup(response.content, "lxml")  
            success = [el.text.split()[1] for el in s.find_all("div", {"class": "alert-success"})]  
            failure = [el.text.split()[3] for el in s.find_all("div", {"class": "alert-danger"})]  
            return success, failure  
        except Exception as e:  
            logging.error(f"Error parsing upload result: {str(e)}")  
            return [], []  

    def download_zip(self):  
        if not os.path.exists(self.destination):  
            os.makedirs(self.destination)  
        try:  
            res = self.session.get(f"{self.base_url}/download.php?id=all", headers=self.headers)  
            with zipfile.ZipFile(BytesIO(res.content)) as zf:  
                for name in zf.namelist():  
                    data = zf.read(name)  
                    dest = os.path.join(self.destination, os.path.basename(name))  
                    with open(dest, 'wb') as f:  
                        f.write(data)  
                    logging.info(f"Wrote {len(data)} bytes to {dest}")  
            return True  
        except Exception as e:  
            logging.error(f"Download failed: {str(e)}")  
            return False  

    def copy(self, src, dest, files):  
        for file in files:  
            csrc = os.path.join(src, file)  
            cdest = os.path.join(dest, file)  
            shutil.copyfile(csrc, cdest)  
            logging.info(f"Copied {file} to {dest}")  

    def process_files(self, dir, phpfiles):  
        logging.info(f"Uploading {len(phpfiles)} files...")  
        success, failure = self.upload(dir, phpfiles)  
        self.not_decoded.extend([os.path.join(dir, f) for f in failure])  
        if success:  
            if not self.download_zip():  
                logging.warning("Couldn't download. Copying originals and continuing")  
                self.not_decoded.extend([os.path.join(dir, f) for f in phpfiles])  
            self.clear()  

        logging.info(f"Checking contents of directory: {self.destination}")  
        for filename in phpfiles:  
            src_file = os.path.join(dir, filename)  
            dst_file = os.path.join(self.destination, filename)  
            if os.path.exists(dst_file):  
                logging.info(f"File {filename} decoded and saved successfully in {self.destination}")  
            else:  
                logging.error(f"Decoding failed for file {filename}, it's missing in destination")  

    def process(self):  
        self.clear()  
        for dir, _, filenames in os.walk(self.source):  
            logging.info(f"Descended into {dir}")  
            rel = os.path.relpath(dir, self.source)  
            dest = os.path.join(self.destination, rel).strip(".")  

            if not os.path.exists(dest):  
                os.makedirs(dest)  

            phpfiles = [f for f in filenames if f.endswith(".php") and b"ionCube Loader" in open(os.path.join(dir, f), "rb").read()]  
            otherfiles = [f for f in filenames if f not in phpfiles]  

            self.copy(dir, dest, otherfiles)  
            if not self.overwrite:  
                phpfiles = [f for f in phpfiles if not os.path.exists(os.path.join(dest, f))]  

            if phpfiles:  
                for f in batch(phpfiles, 25):  
                    self.process_files(dir, f)  
        logging.info("Finished. IonCube files that failed to decode:")  
        for f in self.not_decoded:  
            logging.info(f)