import json
import requests
from time import sleep
import logging

class CaseBattle:
    def __init__(self, token, sleep_interval=1, ticket_cost_threshold=1000):
        self.session = requests.Session()
        self.session.headers.update({
            "authorization": f"Bearer {token}"
        })
        self.base_url = "https://kdrp2.com/CaseBattle/"
        self.active_battles_url = f"{self.base_url}battle?type=active&page=0&priceFrom=0&priceTo=0.29&searchText=&sort=priceAscending&players=all&roundsCount=all"
        self.join_battle_url = f"{self.base_url}joinCaseBattle/"
        self.sleep_interval = sleep_interval
        self.ticket_cost_threshold = ticket_cost_threshold

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
            return json.loads(response.text)["success"], response.text
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return False, str(http_err)
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
            return False, str(err)

    def monitor_battles(self):
        while True:
            battles = self.get_active_battles()
            for battle in battles:
                if self.is_joinable(battle):
                    success, message = self.join_battle(battle["id"])
                    if success:
                        logging.info(f"Successfully joined to {battle['name']}!")
                    else:
                        logging.error(f"Failed to join to {battle['name']}!")
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
    token = "your_token_here"
    cb = CaseBattle(token)
    cb.monitor_battles()
