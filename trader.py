from argparse import ArgumentParser
from utils import Trader
start = "config.json"
current_state = "state_of_the_system.json"
history = "write.csv"
args = ArgumentParser()
args.add_argument("argument", type=str, nargs='?', default=None)
args.add_argument("argument_2", type=str, nargs='?', default=None)
args = vars(args.parse_args())
option = args['argument']
amount_of_currency = args['argument_2']
restart = Trader(start)
current_data = Trader(current_state)
if option == "RESTART":
    restart.write_json_file(current_state)
    restart.write_history_csv_file(history)
elif option == "RATE":
    print(current_data.current_exchange())
elif option == "AVAILABLE":
    print(f"UAH {current_data.uah()}")
    print(f"USD {current_data.usd()}")
elif option == "NEXT":
    current_data.next_current_exchange(current_state, history)
elif option == "BUY":
    current_data.buy_usd(amount_of_currency, current_state, history)
elif option == "SELL":
    current_data.sell_usd(amount_of_currency, current_state, history)