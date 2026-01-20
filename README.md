# Financial Data Chatbot

A chatbot that answers questions about holdings and trades data using natural language.

## Features

- Query holdings data (portfolio positions, P&L, market values)
- Query trades data (buy/sell transactions, volumes)
- Natural language interface powered by GPT-4
- Web-based chat UI using Streamlit

## Prerequisites

- Python 3.10+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd property_loop
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key.

## Running Locally

```bash
streamlit run app.py
```

The application will open at http://localhost:8501

## Project Structure

```
property_loop/
├── data/
│   ├── holdings.csv
│   └── trades.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── prompts.py
│   └── agent.py
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Data Description

### Holdings Table (1,023 rows)
Current portfolio positions with columns for fund names, quantities, prices, market values, and profit/loss metrics (daily, monthly, quarterly, yearly).

Fund names: Garfield, Heather, MNC Inv, Ytum, Platpot, Opium, NorthPoint, etc.

### Trades Table (650 rows)
Historical buy/sell transactions with columns for trade type, quantities, prices, principal values, and counterparties.

Fund names: HoldCo 1, HoldCo 3, ClientA, UNC Investment Fund, Redfield Accu-Fund, etc.

### Important Notes
- Holdings and Trades have different fund naming conventions
- Tables can be joined on: SecurityId, CustodianName
- Tables cannot be joined on fund/portfolio names

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Add `OPENAI_API_KEY` in Secrets
5. Deploy

## License

MIT
