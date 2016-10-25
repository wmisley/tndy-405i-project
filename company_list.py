import csv


class CompanyRecord:
    symbol = ""
    name = ""
    last_sale = ""
    market_cap = ""
    ipo_year = ""
    sector = ""
    industry = ""
    summary_quote = ""

    def __init__(self):
        self.symbol = ""
        self.name = ""
        self.last_sale = ""
        self.market_cap = ""
        self.ipo_year = ""
        self.sector = ""
        self.industry = ""
        self.summary_quote = ""


class CompanyStockRecord:
    company = CompanyRecord()
    adj_close = "0.0"
    close = "0.0"
    high = "0.0"
    low = "0.0"
    open = "0.0"
    volume = "0"

    def __init__(self):
        self.init_values()

    def __init__(self, comp, ystock_dict):
        self.init_values()
        self.company = comp
        if not (ystock_dict is None):
            self.adj_close = ystock_dict.get("Adj Close")
            self.close = ystock_dict.get("Close")
            self.high = ystock_dict.get("High")
            self.low = ystock_dict.get("Low")
            self.open = ystock_dict.get("Open")
            self.volume = ystock_dict.get("Volume")

    def init_values(self):
        self.company = CompanyRecord()
        self.adj_close = "0.0"
        self.close = "0.0"
        self.high = "0.0"
        self.low = "0.0"
        self.open = "0.0"
        self.volume = "0"


class CompanyFileReader:
    __file_path = ""

    def __init__(self, file_path):
        self.__file_path = file_path

    def parse(self):
        company_dict = {}
        with open(self.__file_path, 'r') as f:
            next(f)
            reader = csv.reader(filter(lambda row: row[0] != '#', f), delimiter=',')

            for symbol, long_name, last_sale, market_cap, ipo_year, sector, industry, summary_quote in reader:
                company_dict[symbol] = CompanyRecord()
                company_dict[symbol].symbol = symbol
                company_dict[symbol].name = long_name
                company_dict[symbol].last_sale = last_sale
                company_dict[symbol].market_cap = market_cap
                company_dict[symbol].ipo_year = ipo_year
                company_dict[symbol].sector = sector
                company_dict[symbol].industry = industry
                company_dict[symbol].summary_quote = summary_quote

        return company_dict

    def trim_name(self, long_name):
        # if comma, drop everything after the comma
        # if "Corp." drop
        # if "L.P." drop
        # if "Inc" or "Inc." drop
        # if "ETF" drop
        # if "Limited" drop
        # if "Comporation" drop
        # if "Incorporated"
        return long_name.split(",")[0]
