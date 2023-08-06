def fetch_all_currencies(instruments):
    import pandas as pd
    import yfinance as yf

    data_frames = []

    for instrument in instruments:
        try:
            data = yf.download(instrument, start="2000-01-01", end="2023-04-27")
            data_frames.append(data["Close"].rename(instrument))
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")

    df_currencies = pd.concat(data_frames, axis=1, join="outer")
    return df_currencies

instruments = ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X", "GBPJPY=X", "EURGBP=X", "EURCAD=X", "EURSEK=X", "EURCHF=X", "EURHUF=X", "CNY=X", "HKD=X", "SGD=X", "INR=X", "MXN=X", "PHP=X", "IDR=X", "THB=X", "MYR=X", "ZAR=X", "RUB=X"]

df_currencies = fetch_all_data(instruments)
print(df_currencies.head())


def fetch_all_indexes(instruments):
    import pandas as pd
    import yfinance as yf

    data_frames = []

    for instrument in instruments:
        try:
            data = yf.download(instrument, start="2000-01-01", end="today")
            data_frames.append(data["Close"].rename(instrument))
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")

    df_indexes = pd.concat(data_frames, axis=1, join="outer")
    return df_indexes

instruments = ["^GSPC", "^DJI", "^IXIC", "^NYA", "^XAX", "^BUK100P", "^RUT", "^VIX", "^FTSE", "^GDAXI", "^FCHI", "^STOXX50E", "^N100", "^BFX", "IMOEX.ME", "^N225", "^HSI", "000001.SS", "399001.SZ", "^STI", "^AXJO", "^AORD", "^BSESN", "^JKSE", "^KLSE", "^NZ50", "^KS11", "^TWII", "^GSPTSE", "^BVSP", "^MXX", "^IPSA", "^MERV", "^TA125.TA", "^CASE30", "^JN0U.JO"]
df_indexes = fetch_all_data(instruments)
print(df_indexes.head())



def fetch_all_futures(instruments):
    import pandas as pd
    import yfinance as yf

    data_frames = []

    for instrument in instruments:
        try:
            data = yf.download(instrument, start="2000-01-01", end="today")
            data_frames.append(data["Close"].rename(instrument))
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")

    df_instruments = pd.concat(data_frames, axis=1, join="outer")
    return df_instruments

instruments = ["ES=F", "YM=F", "NQ=F", "RTY=F", "ZB=F", "ZN=F", "ZF=F", "ZT=F", "GC=F", "MGC=F", "SI=F", "SIL=F", "PL=F", "HG=F", "PA=F", "CL=F", "HO=F", "NG=F", "RB=F", "BZ=F", "B0=F", "ZC=F", "ZO=F", "KE=F", "ZR=F", "ZM=F", "ZL=F", "ZS=F", "GF=F", "HE=F", "LE=F", "CC=F", "KC=F", "CT=F", "LBS=F", "OJ=F", "SB=F"]
df_instruments = fetch_all_data(instruments)
print(df_instruments.head())


def update_currencies_csv(csv_file, instruments):
    import pandas as pd
    import yfinance as yf

    # Load existing CSV file
    try:
        df_currencies = pd.read_csv(csv_file)
    except FileNotFoundError:
        # If the file does not exist, create an empty DataFrame with the right columns
        df_currencies = pd.DataFrame(columns=['Date'] + instruments)
    
    # Fetch latest data
    data_frames = []
    for instrument in instruments:
        try:
            data = yf.download(instrument, start="2000-01-01", end="today")
            data_frames.append(data["Close"].rename(instrument))
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")
    new_data = pd.concat(data_frames, axis=1, join="outer")

    # Merge with existing data
    df_currencies = pd.concat([df_currencies, new_data], ignore_index=True)
    df_currencies = df_currencies.drop_duplicates(subset='Date', keep='last')

    # Save to CSV file
    df_currencies.to_csv("df_currencies.csv", index=False)

def update_indexes_csv(csv_file, instruments):
    import pandas as pd
    import yfinance as yf

    # Load existing CSV file
    try:
        df_indexes = pd.read_csv(csv_file)
    except FileNotFoundError:
        # If the file does not exist, create an empty DataFrame with the right columns
        df_indexes = pd.DataFrame(columns=['Date'] + instruments)
    
    # Fetch latest data
    data_frames = []
    for instrument in instruments:
        try:
            data = yf.download(instrument, start="2000-01-01", end="today")
            data_frames.append(data["Close"].rename(instrument))
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")
    new_data = pd.concat(data_frames, axis=1, join="outer")

    # Merge with existing data
    df_indexes = pd.concat([df_indexes, new_data], ignore_index=True)
    df_indexes = df_indexes.drop_duplicates(subset='Date', keep='last')

    # Save to CSV file
    df_indexes.to_csv("df_indexes.csv", index=False)
	

def update_futures_csv(csv_file, instruments):
    import pandas as pd
    import yfinance as yf

    # Load existing CSV file
    try:
        df_instruments = pd.read_csv(csv_file)
    except FileNotFoundError:
        # If the file does not exist, create an empty DataFrame with the right columns
        df_instruments = pd.DataFrame(columns=['Date'] + instruments)
    
    # Fetch latest data
    data_frames = []
    for instrument in instruments:
        try:
            data = yf.download(instrument, start="2000-01-01", end="today")
            data_frames.append(data["Close"].rename(instrument))
        except Exception as e:
            print(f"Error fetching data for {instrument}: {e}")
    new_data = pd.concat(data_frames, axis=1, join="outer")

    # Merge with existing data
    df_instruments = pd.concat([df_instruments, new_data], ignore_index=True)
    df_instruments = df_instruments.drop_duplicates(subset='Date', keep='last')

    # Save to CSV file
    df_instruments.to_csv("df_instruments.csv", index=False)


