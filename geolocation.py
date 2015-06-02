from collections import Counter


def iso_convert(iso2c):
    """
    Takes a two character ISO country code and returns the corresponding 3
    character ISO country code.
    Parameters
    ----------
    iso2c: A two character ISO country code.
    Returns
    -------
    iso3c: A three character ISO country code.
    """

    iso_dict = {"AD": "AND", "AE": "ARE", "AF": "AFG", "AG": "ATG", "AI": "AIA",
                "AL": "ALB", "AM": "ARM", "AO": "AGO", "AQ": "ATA", "AR": "ARG",
                "AS": "ASM", "AT": "AUT", "AU": "AUS", "AW": "ABW", "AX": "ALA",
                "AZ": "AZE", "BA": "BIH", "BB": "BRB", "BD": "BGD", "BE": "BEL",
                "BF": "BFA", "BG": "BGR", "BH": "BHR", "BI": "BDI", "BJ": "BEN",
                "BL": "BLM", "BM": "BMU", "BN": "BRN", "BO": "BOL", "BQ": "BES",
                "BR": "BRA", "BS": "BHS", "BT": "BTN", "BV": "BVT", "BW": "BWA",
                "BY": "BLR", "BZ": "BLZ", "CA": "CAN", "CC": "CCK", "CD": "COD",
                "CF": "CAF", "CG": "COG", "CH": "CHE", "CI": "CIV", "CK": "COK",
                "CL": "CHL", "CM": "CMR", "CN": "CHN", "CO": "COL", "CR": "CRI",
                "CU": "CUB", "CV": "CPV", "CW": "CUW", "CX": "CXR", "CY": "CYP",
                "CZ": "CZE", "DE": "DEU", "DJ": "DJI", "DK": "DNK", "DM": "DMA",
                "DO": "DOM", "DZ": "DZA", "EC": "ECU", "EE": "EST", "EG": "EGY",
                "EH": "ESH", "ER": "ERI", "ES": "ESP", "ET": "ETH", "FI": "FIN",
                "FJ": "FJI", "FK": "FLK", "FM": "FSM", "FO": "FRO", "FR": "FRA",
                "GA": "GAB", "GB": "GBR", "GD": "GRD", "GE": "GEO", "GF": "GUF",
                "GG": "GGY", "GH": "GHA", "GI": "GIB", "GL": "GRL", "GM": "GMB",
                "GN": "GIN", "GP": "GLP", "GQ": "GNQ", "GR": "GRC", "GS": "SGS",
                "GT": "GTM", "GU": "GUM", "GW": "GNB", "GY": "GUY", "HK": "HKG",
                "HM": "HMD", "HN": "HND", "HR": "HRV", "HT": "HTI", "HU": "HUN",
                "ID": "IDN", "IE": "IRL", "IL": "ISR", "IM": "IMN", "IN": "IND",
                "IO": "IOT", "IQ": "IRQ", "IR": "IRN", "IS": "ISL", "IT": "ITA",
                "JE": "JEY", "JM": "JAM", "JO": "JOR", "JP": "JPN", "KE": "KEN",
                "KG": "KGZ", "KH": "KHM", "KI": "KIR", "KM": "COM", "KN": "KNA",
                "KP": "PRK", "KR": "KOR", "XK": "XKX", "KW": "KWT", "KY": "CYM",
                "KZ": "KAZ", "LA": "LAO", "LB": "LBN", "LC": "LCA", "LI": "LIE",
                "LK": "LKA", "LR": "LBR", "LS": "LSO", "LT": "LTU", "LU": "LUX",
                "LV": "LVA", "LY": "LBY", "MA": "MAR", "MC": "MCO", "MD": "MDA",
                "ME": "MNE", "MF": "MAF", "MG": "MDG", "MH": "MHL", "MK": "MKD",
                "ML": "MLI", "MM": "MMR", "MN": "MNG", "MO": "MAC", "MP": "MNP",
                "MQ": "MTQ", "MR": "MRT", "MS": "MSR", "MT": "MLT", "MU": "MUS",
                "MV": "MDV", "MW": "MWI", "MX": "MEX", "MY": "MYS", "MZ": "MOZ",
                "NA": "NAM", "NC": "NCL", "NE": "NER", "NF": "NFK", "NG": "NGA",
                "NI": "NIC", "NL": "NLD", "NO": "NOR", "NP": "NPL", "NR": "NRU",
                "NU": "NIU", "NZ": "NZL", "OM": "OMN", "PA": "PAN", "PE": "PER",
                "PF": "PYF", "PG": "PNG", "PH": "PHL", "PK": "PAK", "PL": "POL",
                "PM": "SPM", "PN": "PCN", "PR": "PRI", "PS": "PSE", "PT": "PRT",
                "PW": "PLW", "PY": "PRY", "QA": "QAT", "RE": "REU", "RO": "ROU",
                "RS": "SRB", "RU": "RUS", "RW": "RWA", "SA": "SAU", "SB": "SLB",
                "SC": "SYC", "SD": "SDN", "SS": "SSD", "SE": "SWE", "SG": "SGP",
                "SH": "SHN", "SI": "SVN", "SJ": "SJM", "SK": "SVK", "SL": "SLE",
                "SM": "SMR", "SN": "SEN", "SO": "SOM", "SR": "SUR", "ST": "STP",
                "SV": "SLV", "SX": "SXM", "SY": "SYR", "SZ": "SWZ", "TC": "TCA",
                "TD": "TCD", "TF": "ATF", "TG": "TGO", "TH": "THA", "TJ": "TJK",
                "TK": "TKL", "TL": "TLS", "TM": "TKM", "TN": "TUN", "TO": "TON",
                "TR": "TUR", "TT": "TTO", "TV": "TUV", "TW": "TWN", "TZ": "TZA",
                "UA": "UKR", "UG": "UGA", "UM": "UMI", "US": "USA", "UY": "URY",
                "UZ": "UZB", "VA": "VAT", "VC": "VCT", "VE": "VEN", "VG": "VGB",
                "VI": "VIR", "VN": "VNM", "VU": "VUT", "WF": "WLF", "WS": "WSM",
                "YE": "YEM", "YT": "MYT", "ZA": "ZAF", "ZM": "ZMB", "ZW": "ZWE",
                "CS": "SCG", "AN": "ANT"}

    try:
        iso3c = iso_dict[iso2c]
        return iso3c
    except KeyError:
        print('Bad code: ' + iso2c)
        iso3c = "NA"
        return iso3c


def process_cliff(located):

    cliff_people = []
    cliff_orgs = []
    focus_cities = []
    focus_states = []
    focus_countries = []
    state_vec = []
    country_vec = []
    big_json = {"cliff_people": cliff_people, "cliff_orgs": cliff_orgs,
                "focus_cities": focus_cities, "focus_states": focus_states,
                "focus_countries": focus_countries, "country_vec": country_vec,
                "stateVec": state_vec}

    for p in located['results']['people']:
        cliff_people.append(p['name'])
    for o in located['results']['organizations']:
        cliff_orgs.append(o['name'])
    try:
        focus = located['results']['places']['focus']

        for c in focus['states']:
            countryCode = iso_convert(c['countryCode'])
            state = {"name": c['name'], "countryCode": countryCode,
                     "lon": c['lon'], "lat": c['lat'],
                     "stateCode": c['stateCode']}
            focus_states.append(state)
            state_vec.append(state['name'])
            country_vec.append(state['countryCode'])
    except:
        pass
    try:
        tmp_state_dict = {}
        for item in focus_states:
            code = item['stateCode']
            tmp_state_dict[code] = item['name']
    except:
        pass
    try:
        for c in focus['cities']:
            stateCode = c['stateCode']
            countryCode = iso_convert(c['countryCode'])
            stateName = tmp_state_dict[stateCode]
            city = {"name": c['name'], "countryCode": countryCode,
                    "lon": c['lon'], "lat": c['lat'], "stateName": stateName}
            focus_cities.append(city)
            country_vec.append(city['countryCode'])
    except:
        pass
    try:
        for c in focus['countries']:
            countryCode = iso_convert(c['countryCode'])
            country = {'name': c['name'], 'countryCode': countryCode,
                       'lon': c['lon'], 'lat': c['lat']}
            focus_countries.append(country)
            country_vec.append(country['countryCode'])
    except:
        pass
    try:
        cv = list(set(country_vec))
        big_json = {"cliff_people": cliff_people, "cliff_orgs": cliff_orgs,
                    "focus_cities": focus_cities, "focus_states": focus_states,
                    "focus_countries": focus_countries, "country_vec": cv,
                    "stateVec": state_vec}
        return big_json

    except:
        return big_json


def process_mordecai(located):
    country_vec = []
    for loc in located:
        country_vec.append(loc['countrycode'])
    focus_countries = Counter(country_vec)

    out = {'country_vec': country_vec, 'locations': located,
           'focus_countries': focus_countries}
    return out
