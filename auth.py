# easy4us/auth.py  
import requests  
from bs4 import BeautifulSoup  
import logging  

class Authenticator:  
    def __init__(self, username, password):  
        self.username = username  
        self.password = password  
        self.base_url = "https://easytoyou.eu"  
        self.headers = {  
            "Connection": "keep-alive",  
            "Cache-Control": "max-age=0",  
            "Upgrade-Insecure-Requests": "1",  
            "User-Agent": "Mozilla/5.0",  
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  
            "Accept-Encoding": "gzip, deflate, br",  
            "Accept-Language": "en-US,en;q=0.9"  
        }  

    def login(self):  
        session = requests.Session()  
        login_url = f"{self.base_url}/login"  
        login_data = {"loginname": self.username, "password": self.password}  
        try:  
            resp = session.post(login_url, headers={**self.headers, "Content-Type": "application/x-www-form-urlencoded"}, data=login_data, allow_redirects=True)  
            logging.debug(f"Login response URL: {resp.url}")  

            if "/account" in resp.url:  
                logging.info("Login successful.")  
                return session  

            logging.error("Login failed.")  
        except requests.RequestException as e:  
            logging.error(f"Login failed: {str(e)}")  
            
        return False  

    def get_membership_details(self, session):  
        try:  
            response = session.get(f"{self.base_url}/user/account.php", headers=self.headers)  
            soup = BeautifulSoup(response.content, 'html.parser')  
            table = soup.find('table', {'class': 'myTable'})  
            if not table:  
                logging.error("Membership table not found.")  
                return None  

            row = table.find('tbody').find('tr', {'class': 'odd'})  
            if not row:  
                logging.error("Membership details row not found.")  
                return None  

            cells = row.find_all('td')  
            if len(cells) >= 2:  
                membership_type = cells[0].get_text(strip=True)  
                valid_until = cells[1].get_text(strip=True)  
                return membership_type, valid_until  

        except requests.RequestException as e:  
            logging.error(f"Failed to fetch account details: {str(e)}")  
        
        return None