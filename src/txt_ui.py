from src.webscrape import YahooWebScrapeInstance, YahooWebScrapeException


class BasicTextUI:
    def __init__(self):
        self.curr_instance = None

    def run(self):
        print("Welcome to the Basic Yahoo Webscraping Tool. \nWith this tool you can look at recent daily prices for a "
              "given stock symbol.\n")
        running = True
        while running:
            init_menu_sel = input("What would you like to do?\n\tL - Lookup Recent Stock History\n\tQ - Quit\n")
            while init_menu_sel.lower() != 'q' and init_menu_sel.lower() != 'l':
                init_menu_sel = input("Incorrect Input:\n\tL - Lookup Recent Stock History\n\tQ - Quit\n")
            if init_menu_sel.lower() == 'q':
                running = False
                continue
            elif init_menu_sel.lower() == 'l':
                try:
                    stock_selection = input("Input a Stock Symbol: \n")
                    self.curr_instance = YahooWebScrapeInstance(stock_selection)
                    successful_instance_created = True
                except YahooWebScrapeException as ywse:
                    print(ywse.default_msg)
                    successful_instance_created = False
                    status_code = ywse.status_code
                    if not successful_instance_created and (status_code is 404 or status_code is -1):
                        while not successful_instance_created and (status_code is 404 or status_code is -1):
                            try:
                                stock_selection = input("Either Incorrect Stock Symbol or no Information Available.  "
                                                        "\nInput Correct symbol: \n")
                                self.curr_instance = YahooWebScrapeInstance(stock_selection)
                                successful_instance_created = True
                            except YahooWebScrapeException as ywse:
                                print(ywse.default_msg)
                                successful_instance_created = False
                                status_code = ywse.status_code
                    if not successful_instance_created and status_code is not 404:
                        print("Refer to error given.  Stopping application and would recommend restarting or checking "
                              "internet/firewall.\n")
                        running = False
                        continue
                if successful_instance_created:
                    in_curr_instance = True
                    while in_curr_instance:
                        data_selection = input("How many open days back of data would you like to see?  "
                                               "\nInput 'any' if you would like to see all 100 days available.\n"
                                               "If you would like to go back to main menu, type 'q'\n")
                        if data_selection.lower() == 'any':
                            print(str(self.curr_instance.dataframe_table)  + "\n" + str(self.curr_instance.footnotes) + "\n")
                        elif data_selection.lower() == 'q':
                            in_curr_instance = False
                            continue
                        else:
                            try:
                                print(self.curr_instance.get_days_back(int(data_selection)))
                            except ValueError:
                                print("Invalid Integer Input.\n")
                            except IndexError:
                                print("Invalid Index Input: Must be 0-" + str(len(self.curr_instance.dataframe_table.index) - 1) + "(Inclusive)\n")
