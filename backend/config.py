"""
All static configuration for the FOMC sentiment pipeline: the economic
n-gram lists and the include/exclude adjustment dictionaries (Aruoba-Drechsel methodology) 
"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads  .env file and makes its values available via os.getenv()

# --- Paths ---
PDF_FOLDER = os.getenv("PDF_FOLDER", "backend/data/pdfs")
LEXICON_PATH = os.getenv("LEXICON_PATH", "backend/data/lexicon/Loughran-McDonald_MasterDictionary_1993-2023.csv")
DATABASE_PATH = os.getenv("DATABASE_PATH", "backend/data/fomc.db")

DATE_PATTERN = r"\d{4}_\d{2}_\d{2}"

# Lists of singles, doubles, and triples (unigrams, bigrams, and trigrams).
SINGLES = [('borrowing',), ('brazil',), ('banks',), ('canada',), ('credit',), ('china',), ('consumption',), ('construction',), ('currencies',), ('deposits',), ('employment',), ('equipment',), ('euro',), ('exports',), ('germany',), ('hiring',), ('hours',), ('housing',), ('imports',), ('inflation',), ('inventories',), ('investment',), ('japan',), ('liquidity',), ('loans',), ('leasing',), ('lending',), ('machinery',), ('mexico',), ('mortgage',), ('output',), ('productivity',), ('profits',), ('recovery',), ('reserves',), ('savings',), ('spread',), ('structures',), ('tourism',), ('unemployment',), ('utilization',), ('wages',), ('weather',), ('yield',), ('income',), ('gdp',), ('cpi',), ('nairu',), ('services',), ('bonds',), ('economy',), ('outlays',), ('financing',), ('assets',), ('finance',), ('shipments',), ('capacity',), ('office',), ('computers',), ('industries',), ('producers',), ('supply',), ('homes',), ('sectors',), ('agriculture',), ('merchandise',), ('investors',), ('aircraft',), ('stocks',), ('buildings',), ('cash',), ('trucks',), ('semiconductors',), ('farm',), ('uncertainty',), ('households',), ('crop',), ('apparel',), ('steel',), ('automotive',), ('metals',), ('permits',), ('commerce',), ('transportation',), ('municipal',), ('commodities',), ('corporations',), ('liabilities',), ('consumers',), ('firms',), ('trading',), ('corn',), ('asia',), ('taxes',), ('software',), ('mining',), ('losses',), ('jobs',), ('cars',), ('depreciation',), ('recession',), ('france',), ('korea',), ('italy',), ('lumber',), ('volatility',), ('wheat',), ('livestock',), ('rents',), ('petroleum',), ('traffic',), ('fuel',), ('plants',), ('technology',), ('argentina',), ('cattle',), ('crisis',), ('utilities',), ('travel',), ('payrolls',), ('factory',), ('transfers',), ('drought',), ('gold',), ('salaries',), ('cotton',), ('coal',), ('philippines',), ('singapore',), ('taiwan',), ('thailand',), ('soybean',), ('swaps',), ('harvest',), ('environment',), ('deflator',), ('delinquencies',), ('chemicals',), ('mergers',), ('rigs',), ('indonesia',), ('political',), ('peso',), ('retirement',), ('tobacco',), ('hurricane',), ('equities',), ('russia',), ('workers',), ('contractors',), ('borrowers',), ('brazilian',), ('bank',), ('banking',), ('bankers',), ('canadian',), ('chinese',), ('export',), ('german',), ('hires',), ('houses',), ('import',), ('inventory',), ('investments',), ('japanese',), ('loan',), ('lenders',), ('mortgages',), ('profit',), ('saving',), ('spreads',), ('wage',), ('yields',), ('durables',), ('manufacturers',), ('manufacturer',), ('treasuries',), ('gnp',), ('service',), ('asset',), ('computer',), ('building',), ('builders',), ('truck',), ('semiconductor',), ('farmers',), ('autos',), ('automobile',), ('metal',), ('soybeans',), ('christmas',)
 ]

DOUBLES = [('employment', 'cost'), ('aggregate, demand'), ('auto', 'sales'), ('bond', 'issuance'), ('budget', 'deficit'), ('business', 'activity'), ('business', 'confidence'), ('business', 'spending'), ('capital', 'expenditures'), ('consumer', 'confidence'), ('current', 'account'), ('debt', 'growth'), ('defense', 'spending'), ('delinquency', 'rates'), ('developing', 'countries'), ('domestic', 'demand'), ('drilling', 'activity'), ('durable', 'goods'), ('economic', 'growth'), ('energy', 'prices'), ('equity', 'issuance'), ('equity', 'prices'), ('euro', 'area'), ('exchange', 'rate'), ('federal', 'debt'), ('financial', 'conditions'), ('financial', 'developments'), ('fiscal', 'policy'), ('fiscal', 'stimulus'), ('food', 'prices'), ('foreign', 'economies'), ('gas', 'prices'), ('gasoline', 'prices'), ('government', 'purchases'), ('home', 'prices'), ('home', 'sales'), ('hourly', 'compensation'), ('household', 'debt'), ('household', 'spending'), ('import', 'prices'), ('industrial', 'production'), ('industrial', 'supplies'), ('inflation', 'compensation'), ('inflation', 'expectations'), ('initial', 'claims'), ('input', 'prices'), ('intermediate', 'materials'), ('international', 'developments'), ('labor', 'market'), ('manufacturing', 'activity'), ('manufacturing', 'firms'), ('monetary', 'aggregates'), ('mortgage', 'interest'), ('natural', 'rate'), ('net', 'exports'), ('new', 'orders'), ('nondefense', 'capital'), ('oil', 'prices'), ('output', 'gap'), ('potential', 'output'), ('price', 'pressures'), ('producer', 'prices'), ('refinancing', 'activity'), ('residential', 'investment'), ('retail', 'prices'), ('retail', 'sales'), ('retail', 'trade'), ('share', 'prices'), ('social', 'security'), ('stock', 'market'), ('trade', 'balance'), ('trade', 'deficit'), ('trade', 'surplus'), ('treasury', 'securities'), ('treasury', 'yield'), ('vacancy', 'rates'), ('wholesale', 'prices'), ('wholesale', 'trade'), ('yield', 'curve'), ('foreign', 'exchange'), ('nominal', 'gdp'), ('core', 'inflation'), ('motor', 'vehicles'), ('financial', 'institutions'), ('depository', 'institutions'), ('credit', 'standards'), ('consumer', 'prices'), ('crude', 'oil'), ('loan', 'demand'), ('united', 'kingdom'), ('money', 'market'), ('market', 'participants'), ('commercial', 'paper'), ('housing', 'starts'), ('housing', 'activity'), ('natural', 'gas'), ('consumer', 'goods'), ('balance', 'sheet'), ('financial', 'markets'), ('economic', 'indicators'), ('final', 'sales'), ('credit', 'quality'), ('international', 'transactions'), ('finished', 'goods'), ('latin', 'america'), ('economic', 'outlook'), ('domestic', 'developments'), ('oil', 'imports'), ('home', 'equity'), ('headline', 'inflation'), ('raw', 'materials'), ('holiday', 'season'), ('inflationary', 'pressures'), ('loan', 'officer'), ('health', 'care'), ('economic', 'expansion'), ('economic', 'data'), ('canadian', 'dollar'), ('corporate', 'profits'), ('insurance', 'companies'), ('wage', 'pressures'), ('market', 'expectations'), ('consumer', 'spending'), ('car', 'sales'), ('vehicle', 'sales'), ('real', 'activity'), ('business', 'conditions',), ('economic', 'conditions'), ('capital', 'spending'), ('consumer', 'sentiment'), ('durable', 'equipment'), ('energy', 'price'), ('equity', 'price'), ('stock', 'prices'), ('stock', 'price'), ('exchange', 'rates'), ('food', 'price'), ('gas', 'price'), ('gasoline', 'price'), ('home', 'price'), ('house', 'prices'), ('house', 'price'), ('hourly', 'earnings'), ('import', 'price'), ('input', 'price'), ('labor', 'markets'), ('manufacturing', 'sector'), ('mortgage', 'rates'), ('oil', 'price'), ('potential', 'gdp'), ('producer', 'price'), ('retail', 'price'), ('share', 'price'), ('treasury', 'bills'), ('treasury', 'security'), ('treasury', 'yields'), ('vacancy', 'rate'), ('wholesale', 'price'), ('nominal', 'gnp'), ('thrift', 'institutions'), ('lending', 'standards'), ('consumer', 'price'), ('imported', 'oil'), ('crude', 'materials'), ('district', 'banks'), ('import', 'prices'), ('inflation', 'expectations'), ('inflation', 'compensation'), ('core', 'inflation'), ('headline', 'inflation'), ('loan', 'rates'), ('mortgage', 'rate'), ('unemployment', 'insurance'), ('national', 'income'), ('income', 'tax',), ('foreign', 'gdp'), ('asset', 'purchases'), ('oil', 'price'), ('oil', 'prices'), ('commodity', 'prices'), ('commodity', 'price')

]

TRIPLES = [('advanced', 'foreign', 'economies'), ('commercial', 'real', 'estate'), ('compensation', 'per', 'hour'), ('domestic', 'final', 'purchases'), ('domestic', 'financial', 'developments'), ('emerging', 'market', 'economies'), ('foreign', 'industrial', 'countries'), ('gross', 'domestic', 'purchases'), ('household', 'net', 'worth'), ('international', 'financial', 'transactions'), ('labor', 'force', 'participation'), ('major', 'industrial', 'countries'), ('market', 'interest', 'rates'), ('nondefense', 'capital', 'goods'), ('output', 'per', 'hour'), ('real', 'estate', 'activity'), ('real', 'estate', 'market'), ('real', 'interest', 'rate'), ('real', 'interest', 'rates'), ('residential', 'real', 'estate'), ('unit', 'labor', 'cost'), ('unit', 'labor', 'costs'), ('money', 'market', 'mutual'), ('foreign', 'net', 'purchases'), ('real', 'estate', 'markets'), ('gross', 'domestic', 'product'), ('gross', 'national', 'product'), ('foreign', 'direct', 'investment'), ('money', 'market', 'mutual')
]

ALL_NGRAMS = {1: SINGLES, 2: DOUBLES, 3: TRIPLES}

# Define n-grams to include and exclude as dictionaries.
INCLUDE_DICT = {
    "borrowing": ["borrowers"],
    "brazil": ["brazilian"],
    "banks": ["bank", "banking", "bankers"],
    "canada": ["canadian"],
    "china": ["chinese"],
    "consumption": [("consumer", "spending")],
    "exports": ["export"],
    "germany": ["german"],
    "hiring": ["hires"],
    "housing": ["houses"],
    "imports": ["import"],
    "inventories": ["inventory"],
    "investment": ["investments"],
    "japan": ["japanese"],
    "loans": ["loan"],
    "lending": ["lenders"],
    "mortgage": ["mortgages"],
    "profits": ["profit"],
    "savings": ["saving"],
    "spread": ["spreads"],
    "wages": ["wage"],
    "yield": ["yields"],
    ("auto", "sales"): [("car", "sales"), ("vehicle", "sales")],
    ("business", "activity"): [("business", "activity"), ("real", "activity"), ("business", "conditions"), ("economic", "conditions")],
    ("capital", "expenditures"): [("capital", "spending")],
    ("commodity", "prices"): [("commodity", "price")],
    ("consumer", "confidence"): [("consumer", "sentiment")],
    ("durable", "goods"): ["durables", ("durable", "equipment")],
    ("energy", "prices"): [("energy", "price")],
    ("equity", "prices"): [("equity", "price"), ("stock", "prices"), ("stock", "price")],
    ("exchange", "rate"): [("exchange", "rates")],
    ("food", "prices"): [("food", "price")],
    ("gas", "prices"): [("gas", "price")],
    ("gasoline", "prices"): [("gasoline", "price")],
    ("home", "prices"): [("home", "price"), ("house", "prices"), ("house", "price")],
    ("hourly", "compensation"): [("hourly", "earnings")],
    ("import", "prices"): [("import", "price")],
    ("input", "prices"): [("input", "price")],
    ("labor", "market"): [("labor", "markets")],
    ("manufacturing", "firms"): ["manufacturers", "manufacturer",("manufacturing", "sector")],
    ("mortgage", "interest"): [("mortgage", "rate"), ("mortgage", "rates")],
    ("oil", "prices"): [("oil", "price")],
    ("potential", "output"): [("potential", "gdp")],
    ("producer", "prices"): [("producer", "price")],
    ("retail", "prices"): [("retail", "price")],
    ("share", "prices"): [("share", "price")],
    ("treasury", "securities"): ["treasuries", ("treasury", "bills"), ("treasury", "security")],
    ("treasury", "yield"): [("treasury", "yields")],
    ("vacancy", "rates"): [("vacancy", "rate")],
    ("wholesale", "prices"): [("wholesale", "price")],
    ("real", "estate", "market"): [("real", "estate", "markets")],
    ("real", "interest", "rate"): [("real", "interest", "rates")],
    ("unit", "labor", "cost"): [("unit", "labor", "costs")],
    "gdp": [("gross", "domestic", "product"), "gnp", ("gross", "national", "product")],
    ("nominal", "gdp"): [("nominal", "gnp")],
    "services": ["service"],
    ("depository", "institutions"): [("thrift", "institutions")],
    "assets": ["asset"],
    ("credit", "standards"): [("lending", "standards")],
    "computers": ["computer"],
    "buildings": ["building", "builders"],
    ("consumer", "prices"): [("consumer", "price")],
    "trucks": ["truck"],
    "semiconductors": ["semiconductor"],
    "farm": ["farmers"],
    "automotive": ["autos", "cars", "automobile"],
    "metals": ["metal"],
    ("oil", "imports"): [("imported", "oil")],
    "soybean": ["soybeans"],
    ("raw", "materials"): [("crude", "materials")],
    ("holiday", "season"): ["christmas"]
}

EXCLUDE_DICT = {
    "banks": [("district", "banks")],
    "credit": [("credit", "standards"), ("credit", "quality")],
    "employment": [("employment", "cost")],
    "euro": [("euro", "area")],
    "exports": [("net", "exports")],
    "housing": [("housing", "starts"), ("housing", "activity")],
    "imports": [("import", "prices")],
    "inflation": [("inflation", "expectations"), ("inflation", "compensation"), ("core", "inflation"), ("headline", "inflation")],
    "investment": [("residential", "investment"), ("foreign", "direct", "investment")],
    "loans": [("loan", "demand"), ("loan", "officer"), ("loan", "rates")],
    "mortgage": [("mortgage", "interest"), ("mortgage", "rates"), ("mortgage", "rate")],
    "output": [("output", "gap"), ("potential", "output"), ("output", "per", "hour")],
    "unemployment": [("unemployment", "insurance")],
    "wages": [("wage", "pressures")],
    "yield": [("yield", "curve"), ("treasury", "yield")],
    "income": [("national", "income"), ("income", "tax")],
    ("treasury", "yield"): [("yield", "curve")],
    ("advanced", "foreign", "economies"): [("foreign", "economies")],
    "gdp": [("nominal", "gdp"), ("potential", "gdp"), ("nominal", "gnp"), ("foreign", "gdp")],
    "assets": [("asset", "purchases")],
    ("crude", "oil"): [("oil", "price"), ("oil", "prices")],
    ("money", "market"): [("money", "market", "mutual")],
    ("natural", "gas"): [("gas", "price"), ("gas", "prices")],
    "commodities": [("commodity", "prices"), ("commodity", "price")],
    "firms": [("manufacturing", "firms")]
}

# OCR Normlization dictionary for common OCR errors in FOMC transcripts.
COMMON_FIXES = {
        'devel': 'development',
        'reserv': 'reserves',
        'dom': 'domestic',
        'purch': 'purchases',
        'prod': 'product',
        'cons': 'consumption',
        'prices3': 'prices',
        'econ': 'economic',
        'int': 'international',
        'pe': 'percent'
    }