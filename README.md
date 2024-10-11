# Investment Simulation API

This repository contains the code for an **Investment Simulation API** that processes participants' choices from Google Forms, calculates the results based on their inputs and randomness introduced to simulate the stochastic nature of the market, and provides the final investment results.

## Project Overview

Participants make choices at n different times using Google Forms. Each choice influences the outcome of their investment, taking into account previous choices and simulated market randomness. The API:

- Retrieves participant data from Google Spreadsheets linked to Google Forms, using a secret key *(password)* that will be provided during the in-person session.
- Processes participant choices and calculates investment outcomes.
- Provides endpoints to access the final results and handle various requests.

## Repository Structure

```
├── LICENSE
├── README.md
├── requirements.txt
└── src
    ├── data
    │   ├── __init__.py
    │   └── credentials.json
    ├── main.py
    ├── models
    │   ├── __init__.py
    │   └── participant.py
    ├── routes
    │   ├── __init__.py
    │   └── broker_routes.py
    ├── services
    │   ├── __init__.py
    │   └── data_processing.py
    └── utils
        └── __init__.py
```

### Root Directory

- **LICENSE**: Contains the project's license information.
- **README.md**: Documentation and overview of the project.
- **requirements.txt**: Lists the Python dependencies required for the project.

### src/

The main application code resides in the `src` directory.

#### src/data/

- **\_\_init\_\_.py**: Initializes the `data` module.
- **credentials.json**: Google API credentials file required to access Google Sheets.

#### src/main.py

The entry point of the application. It initializes the API and starts the server.

#### src/models/

- **\_\_init\_\_.py**: Initializes the `models` module.
- **participant.py**: Defines the `Participant` class, representing a participant in the simulation, including their choices and methods to calculate results.

#### src/routes/

- **\_\_init\_\_.py**: Initializes the `routes` module.
- **broker_routes.py**: Contains the API endpoints related to the investment simulation, such as processing data and retrieving results. This allows handling requests beyond the investment simulation, facilitating scalability.

#### src/services/

- **\_\_init\_\_.py**: Initializes the `services` module.
- **data_processing.py**: Implements the logic for retrieving data from Google Sheets, processing participant choices, and calculating investment results considering previous choices and market randomness.

#### src/utils/

- **\_\_init\_\_.py**: Initializes the `utils` module.

Utility functions and helpers (e.g., randomness generation, common queries) are managed here to support the main application logic.