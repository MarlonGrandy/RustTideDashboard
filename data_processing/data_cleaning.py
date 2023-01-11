import pandas as pd
import os
import geopandas


cwd = os.getcwd()


def clean_DEM_data():
    DEM_data = pd.read_csv(os.path.join(
        cwd, "dashboard_data", "RIDEMCochlodiniumCounts.csv"))
    DEM_data = DEM_data[["Date", "Lat", "Long",
                         "Cochlodinium polykrikoides (cells/L)"]]
    DEM_data['Date'] = pd.to_datetime(DEM_data['Date'])
    DEM_data['Cochlodinium polykrikoides (cells/L)'] = DEM_data['Cochlodinium polykrikoides (cells/L)'].str.replace(
        ',', '').astype(float)

    DEM_data.rename(columns={
                    'Cochlodinium polykrikoides (cells/L)': 'Margalefidinium polykrikoides (Cells/L)'}, inplace=True)
    DEM_data = DEM_data.set_index('Date')
    return DEM_data


def clean_URI_data():
    xls = pd.ExcelFile(os.path.join(cwd, "dashboard_data",
                                    'Phytoplankton Count Data (.xls)'))
    URI_data = pd.read_excel(xls, 'Count data')
    URI_data = URI_data.drop(index=0)

    URI_data = URI_data[['DATE', 'Cochlodinium']]
    URI_data['DATE'] = pd.to_datetime(URI_data['DATE'])
    URI_data['Cochlodinium'] = URI_data['Cochlodinium'].astype(float)
    URI_data.rename(columns={
                    'Cochlodinium': 'Margalefidinium polykrikoides (Cells/L)', 'DATE': 'Date'}, inplace=True)
    URI_data = URI_data.set_index('Date')
    URI_data = URI_data.resample(
        'W').max()
    URI_data['Lat'] = 41.5722
    URI_data['Long'] = -71.3944
    return URI_data


def clean_WHOI_data():
    WHOI_data = pd.read_csv(os.path.join(
        cwd, "dashboard_data", "habhub_data.csv"))
    WHOI_data = WHOI_data[['DateTime', 'Margalefidinium polykrikoides']]
    WHOI_data['DateTime'] = pd.to_datetime(WHOI_data['DateTime'])
    WHOI_data['Margalefidinium polykrikoides'] = WHOI_data['Margalefidinium polykrikoides'].astype(
        float)
    WHOI_data.rename(columns={
        'DateTime': 'Date', "Margalefidinium polykrikoides": 'Margalefidinium polykrikoides (Cells/L)'}, inplace=True)

    WHOI_data = WHOI_data.set_index('Date')
    WHOI_data = WHOI_data.resample(
        'W').max()
    WHOI_data['Lat'] = 41.49224
    WHOI_data['Long'] = -71.41896
    return WHOI_data


def clean_met_data():
    met_data = pd.read_csv(os.path.join(
        cwd, 'dashboard_data', 'NARPCMET.csv'), skiprows=[0, 1])

    met_data = met_data[['DateTimeStamp', 'TotPrcp', 'MaxWSpd', 'WSpd']]
    met_data['DateTimeStamp'] = pd.to_datetime(met_data['DateTimeStamp'])
    met_data = met_data.set_index("DateTimeStamp")
    MaxWSpd = met_data['MaxWSpd'].resample(
        'W').max()
    WSpd = met_data['WSpd'].resample('W').mean()
    TotPrcp = met_data['TotPrcp'].resample('D').max().resample('W').sum()
    df = pd.concat([MaxWSpd, WSpd, TotPrcp], axis=1)
    df['Date'] = df.index.values
    df['Date'] = df['Date'] - pd.to_timedelta(
        df['Date'].dt.dayofweek, unit='d')
    df.reset_index(inplace=True, drop=True)
    df = df.rename({'DateTimeStamp': 'Date'})
    return df


def clean_WQ_data():
    WQ_data = pd.read_csv(
        '/Users/marlongrandy/Desktop/rust-tide-dashboard/dashboard_data/NARPCWQ.csv', skiprows=[0, 1])
    WQ_data = WQ_data[['DateTimeStamp', 'Temp']]
    WQ_data['DateTimeStamp'] = pd.to_datetime(WQ_data['DateTimeStamp'])
    WQ_data = WQ_data.set_index("DateTimeStamp")
    WQ_data = WQ_data.resample('W').mean()
    WQ_data['Date'] = WQ_data.index.values
    WQ_data['Date'] = WQ_data['Date'] - pd.to_timedelta(
        WQ_data['Date'].dt.dayofweek, unit='d')
    WQ_data.reset_index(inplace=True, drop=True)
    WQ_data['Temp'] = WQ_data['Temp'].apply(lambda x: x*1.8+32)

    WQ_data = WQ_data.rename({'Temp': 'WaterTemp', 'DateTimeStamp': 'Date'})
    return WQ_data


def dashbaord_df():
    df = pd.concat([clean_DEM_data(), clean_URI_data(),
                   clean_WHOI_data()]).sort_values(by='Date')
    df.dropna(inplace=True)
    df = df.loc['2016-01-01':]
    df = df[df['Margalefidinium polykrikoides (Cells/L)'] > 0]
    df['Date'] = df.index.values
    df['Date'] = df['Date'] - pd.to_timedelta(
        df['Date'].dt.dayofweek, unit='d')
    df.reset_index(inplace=True, drop=True)
    df = clean_WQ_data().merge(df, on='Date', how='left').merge(
        clean_met_data(), on='Date', how='left')

    return df


def main():
    df = dashbaord_df()
    print(df.to_striNG())


if __name__ == "__main__":
    main()
