import json
from datetime import datetime
from csv import DictWriter
import random


def rounding(value: float):
    two_characters = int(value * 100) / 100
    return two_characters


class Trader:
    def __init__(self,filename):
        self.filename = filename
        self.data = self.read_json_file()

    def read_json_file(self) -> list:
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data

    def write_json_file(self, save_file):
        with open(save_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def write_history_csv_file(self, filename_csv):
        now = datetime.now()
        self.data['date'] = f'{now.strftime("%c")}'
        headers_csv = ['Exchange', 'UAH', 'USD', "delta", "date"]
        with open(filename_csv, 'a', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headers_csv)
            dictwriter_object.writeheader()
            dictwriter_object.writerow(self.data)

    def current_exchange(self):
        current_exchange_rate = self.data
        current_exchange = current_exchange_rate["Exchange"]
        return current_exchange

    def uah(self):
        current_exchange_uah = self.data
        current_uah = current_exchange_uah["UAH"]
        return current_uah

    def usd(self):
        current_exchange_usd = self.data
        current_usd = current_exchange_usd["USD"]
        return current_usd

    def next_current_exchange(self, save_file, filename_csv):
        initial_course = self.data
        current_exchange = initial_course["Exchange"]
        delta = initial_course["delta"]
        min_value = current_exchange - delta
        max_value = current_exchange + delta
        initial_course["Exchange"] = round(random.uniform(min_value, max_value), 2)
        self.write_json_file(save_file)
        self.write_history_csv_file(filename_csv)

    def buy_usd(self, value: str, save_file, filename_csv):
        current_exchange_rate = self.data
        if value == "ALL":
            usd_bay = self.uah()/self.current_exchange()
            current_exchange_rate["UAH"] = rounding(self.uah() - (usd_bay*self.current_exchange()))
            current_exchange_rate["USD"] = rounding(self.usd() + usd_bay)
        else:
            try:
                value = float(value)
                usd_bay = value*self.current_exchange()
                if usd_bay <= current_exchange_rate["UAH"]:
                    current_exchange_rate["UAH"] = rounding(self.uah() - (value * self.current_exchange()))
                    current_exchange_rate["USD"] = rounding(self.usd() + value)
                else:
                    available = rounding(value*self.current_exchange())
                    print(f"UNAVAILABLE, REQUIRED BALANCE UAH {available}, AVAILABLE {current_exchange_rate['UAH']}")
            except ValueError:
                print("Enter 'ALL' or 'amount of money'")
        self.write_json_file(save_file)
        self.write_history_csv_file(filename_csv)

    def sell_usd(self, value: str, save_file, filename_csv):
        current_exchange_rate = self.data
        if value == "ALL":
            usd_all_sell = self.usd()*self.current_exchange()
            current_exchange_rate["UAH"] = rounding(self.uah() + usd_all_sell)
            current_exchange_rate["USD"] = 0
        else:
            try:
                value = float(value)
                usd_sell = value * self.current_exchange()
                if value <= current_exchange_rate["USD"]:
                    current_exchange_rate["UAH"] = rounding(self.uah() + usd_sell)
                    current_exchange_rate["USD"] = rounding(self.usd() - value)
                else:
                    print(f"UNAVAILABLE, REQUIRED BALANCE USD {value}, AVAILABLE {current_exchange_rate['USD']}")
            except ValueError:
                print("Enter 'ALL' or 'amount of money'")
        self.write_json_file(save_file)
        self.write_history_csv_file(filename_csv)
