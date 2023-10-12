# Rust Tide Data Dashboard
![image](https://github.com/MarlonGrandy/rust-tide-dashboard/assets/106160715/04693ba5-2465-427a-8546-15d671d42b39)

Welcome to the HAB rust tide Dashboard repository! This dashboard displays data on the harmful algal bloom 'Margalefidinium polykrikoides' also known as rust tide. It also includes information on environmental variables such as water temperature and salinity from reporting stations in the area.

## Getting Started

To get started, clone the repository, cd to the 'rust-tide-dashboard' folder and run the app.py file in the 'dashboard' folder. The app will run on a locally hosted Dash server.

## Data Sources

Rust tide observations were collected from [The Narragansett Bay Long-Term Plankton Time Series](https://web.uri.edu/gso/research/plankton/data/), [WHOI HABHub data protal](https://habhub.whoi.edu), and samples taken by Rhode Island Department of Environmental Monitoring. Environemtnal data was collected from meteorological and water quality monitoring stations in Potters Cove provided by the [National Estuarine Research Reserve System](https://cdmo.baruch.sc.edu/get/landing.cfm).

## Features

- Script to scrape data from HTML based sources.
- Script to clean and aggregate all data into a single dataframe
- App.py file to run the Dash application
- Interactive map displaying data from rust tide samples
- Information on environmental variables such as water temperature and rainfall quantities displayed in a scatterplot

## Contributing

We welcome contributions to this project! If you would like to make a change, please fork the repository and submit a pull request.

## Contact

If you have any questions or feedback, please contact us at magran24@colby.edu.

## Disclaimer

The current data on rust tide is limited and the dashboard only presents avalible data. As more data becomes accessible, the dashboard will be updated.
