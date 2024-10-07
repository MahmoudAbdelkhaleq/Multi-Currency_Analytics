# Multi-Currency Analytics API

## Overview

The **Multi-Currency Analytics API** is a powerful tool designed to manage customer invoices in multiple currencies, providing detailed analytics such as total revenue, average invoice size, and revenue trends over time. The API automatically fetches current exchange rates to convert invoice amounts into a standard currency, facilitating consistent financial reporting and analysis.

## Features

- **CRUD Operations**: Full Create, Read, Update, and Delete operations for invoices.
- **Multi-Currency Support**: Handle invoices in various currencies and convert them into a standard currency.
- **Analytics**: 
  - Total revenue calculation.
  - Average invoice size analytics.
  - Revenue trends over time.
- **Automatic Currency Conversion**: Fetch current exchange rates upon recording new invoices for accurate conversions.
- **GraphQL Support**: Advanced querying capabilities to optimize data retrieval.

## Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Third-Party API**: ExchangeRate-API for currency conversion
- **GraphQL**: For enhanced data querying
- **Testing**: pytest

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MahmoudAbdelkhaleq/Multi-Currency_Analytics.git
    cd Multi-Currency_Analytics
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python -m venv .venv
    .venv/Scripts/Activate.ps1  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```plaintext
   DATABASE_URL=your_database_url
   EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
   EXCHANGE_RATE_VERSION = current_version_of_exchange_rate_api

5. **Run the database**:
   After setting up the `.env` file, We are ready to rund the database
   we pull a mysql docker image and run it using the command:
    ```bash
    docker-compose up
    ```
    nysql instance configuration can be found in the docker-compose file (user, password, ..etc)

5. **Run the server**:
   Make sure we are in the directory Multi_Currency_Analytics
   Run the command
    ```bash
    fastapi dev main.py
    ```

5. **Use the API**:
   In your browser navigate to 
   1-http://localhost:8000/docs in order to access the APIs.
   2-http://localhost:8000/graphql in order to call the server using GraphQL
    