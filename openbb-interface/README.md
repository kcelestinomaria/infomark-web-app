Here's the updated `README.md` with the username `kcelestinomaria`:

---

# Infomark Terminal Backend

![Infomark Logo](https://example.com/infomark-logo.svg)

Welcome to the Infomark Terminal backend! This project powers the Infomark Terminal, a comprehensive financial data terminal designed to provide robust financial insights and analytics. The backend leverages a diverse set of APIs and libraries to deliver real-time data and advanced analytics to our users.

## Overview

Infomark Terminal combines several leading financial data sources and libraries to offer a seamless experience for accessing and analyzing financial information. The backend integrates with APIs and libraries from:

- **Benzinga**: Real-time news and data on stocks, options, and crypto.
- **Intrinio**: High-quality financial data feeds and analytics.
- **Yahoo Finance**: Historical and real-time market data.
- **Financial Modeling Prep**: Financial statements and valuation data.
- **OpenBB**: Open-source financial data and analytics.
- **Alpha Vantage**: Provides equity, crypto, and forex data.
- **Benzinga**: Financial news and analysis.
- **BizToc**: Financial news aggregation.
- **CBOE**: Options market data.
- **ECB**: European Central Bank data.
- **EconDB**: Economic data.
- **FINRA**: Financial regulatory data.
- **FinViz**: Stock market data.
- **FMP**: Financial modeling prep data.
- **FRED**: Federal Reserve Economic Data.
- **World Bank**: Global economic data.
- **GDELT**: Global event data.
- **IEEE**: Financial research data.
- **Inflation API**: Inflation data.
- **NASDAQ**: Stock market data.
- **Yahoo Finance**: Financial news and data.
- **OpenBB Platform API**: OpenBB Open-source Platform API

Our goal is to provide a powerful backend using the above libraries that supports the Infomark web-based frontend developed using Streamlit, enabling users to interact with a user-friendly and visually appealing interface.

## Features

- **Comprehensive Data Integration**: Access a wide range of financial data from multiple sources.
- **Real-Time Analytics**: Up-to-date financial metrics and insights.
- **Customizable Data Views**: Tailor the data and analytics to fit your needs.
- **Open-Source Libraries**: Built with OpenBB libraries to enhance data handling and analysis.

## Installation

To get started with the Infomark Terminal backend, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kcelestinomaria/infomark-backend.git
   cd infomark-backend
   ```

2. **Install Dependencies**
   Make sure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   Create a `.env` file in the root directory and add your API keys for the following services:
   ```env
   BENZINGA_API_KEY=your_benzinga_api_key
   INTRINIO_API_KEY=your_intrinio_api_key
   YAHOO_FINANCE_API_KEY=your_yahoo_finance_api_key
   FINANCIAL_MODELING_PREP_API_KEY=your_fmp_api_key
   OPENBB_API_KEY=your_openbb_api_key
   ```

4. **Run the Backend**
   Start the backend server:
   ```bash
   python app.py
   ```

## Usage

Once the backend is running, you can connect it to the Infomark frontend. The backend provides a RESTful API that the frontend will use to fetch financial data and perform analyses.

**Endpoints:**

- **/api/stocks**: Fetch stock market data.
- **/api/options**: Retrieve options data.
- **/api/crypto**: Get cryptocurrency data.
- **/api/forex**: Access forex market information.
- **/api/economy**: Economic indicators and macro data.

For detailed API documentation, please refer to [API Documentation](https://example.com/api-docs).

## Contributing

We welcome contributions to enhance the Infomark Terminal backend! If you have suggestions or would like to help improve the project, please:

1. **Fork the Repository**
2. **Create a Feature Branch**
3. **Commit Your Changes**
4. **Push to the Branch**
5. **Open a Pull Request**

For detailed contributing guidelines, please see our [Contributing Guide](https://example.com/contributing).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For any questions or support, feel free to reach out:

- **Email**: support@infomark.co
- **Discord**: [Join our Discord](https://example.com/discord)
- **Twitter**: [Follow us](https://twitter.com/infomark)

Thank you for using Infomark Terminal!

---

Feel free to adjust any additional details as necessary!