import json, os, requests, logging
from time import sleep
from fake_useragent import UserAgent
from pystyle import Colors, Colorate, Center

logo = """
██╗  ██╗███████╗██╗   ██╗██████╗ ██████╗  ██████╗ ██████╗ 
██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
█████╔╝ █████╗   ╚████╔╝ ██║  ██║██████╔╝██║   ██║██████╔╝
██╔═██╗ ██╔══╝    ╚██╔╝  ██║  ██║██╔══██╗██║   ██║██╔═══╝ 
██║  ██╗███████╗   ██║   ██████╔╝██║  ██║╚██████╔╝██║     
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝"""

# Clear the console.
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")

# Set the console title.
os.system(f"title Keydrop Battle Bot - discord.gg/kws")

class CaseBattle:
    def __init__(self, token, sleep_interval=1, ticket_cost_threshold=4):
        self.session = requests.Session()
        self.user_agent = UserAgent()
        self.session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "kdrp2.com",
            "Origin": "https://key-drop.com",
            "Referer": "https://key-drop.com/",
            "authorization": f"Bearer {token}",
            "User-Agent": self.user_agent.random
        })
        self.base_url = "https://kdrp2.com/CaseBattle/"
        self.active_battles_url = f"{self.base_url}battle?type=active&page=0&priceFrom=0&priceTo=0.29&searchText=&sort=priceAscending&players=all&roundsCount=all"
        self.join_battle_url = f"{self.base_url}joinCaseBattle/"
        self.sleep_interval = sleep_interval
        self.ticket_cost_threshold = ticket_cost_threshold

    def print_logo(self):
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "────────────────────────────────────────────\n", 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "Starting...", 1)))

    def get_active_battles(self):
        try:
            response = self.session.get(self.active_battles_url)
            response.raise_for_status()
            return json.loads(response.text)["data"]
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
            return []

    def join_battle(self, battle_id):
        try:
            url = f"{self.join_battle_url}{battle_id}/1"
            response = self.session.post(url)
            response.raise_for_status()
            json = json.loads(response.text)
            if json["success"]:
                return True, response.text
            if json["errorCode"] == "slotUnavailable":
                return False, "Slot unavailable!"
            if json["errorCode"] == "rateLimited":
                return False, "Ratelimited!"
            return False, json["errorCode"]
        except requests.HTTPError as http_err:
            if "Unauthorized" in str(response.text):
                return False, "Invalid token!"
            logging.error(f"HTTP Error: {http_err}")
            return False, str(http_err)
        except Exception as err:
            logging.error(f"Error: {err}")
            return False, str(err)

    def monitor_battles(self):
        clear()
        self.print_logo()
        while True:
            battles = self.get_active_battles()
            for battle in battles:
                if self.is_joinable(battle):
                    logging.info(f"Trying to join battle {battle['id']}...")
                    success, message = self.join_battle(battle["id"])
                    if success:
                        logging.info(f"Successfully joined battle!")
                    elif message == "Invalid token!":
                        logging.error("Invalid bearer token!")
                        exit()
                    elif message == "Ratelimited!":
                        logging.error("Ratelimited! Consider increasing the sleep interval.")
                        sleep(60)
                    else:
                        logging.error(f"Failed to join battle! Error: {message}")
                        sleep(self.sleep_interval)
            sleep(self.sleep_interval)

    def is_joinable(self, battle):
        isFreeBattle = battle["isFreeBattle"]
        users = battle["users"]
        maxUserCount = battle["maxUserCount"]
        if isFreeBattle and len(users) != maxUserCount:
            if battle["freeBattleTicketCost"] > self.ticket_cost_threshold:
                return False
            elif battle["freeBattleTicketCost"] < self.ticket_cost_threshold:
                return True
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    token = "YOUR_TOKEN_HERE"
    cb = CaseBattle(token)
    cb.monitor_battles()
