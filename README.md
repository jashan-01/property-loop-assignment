# Financial Data Chatbot

Chat with your portfolio data. Ask questions in plain English, get answers from your holdings and trades.

Built with LangChain + Streamlit.

## What it does

You can ask things like:
- "What's my total portfolio value?"
- "Show me all trades from last month"
- "Which fund has the highest P&L?"
- "List all buy transactions for HoldCo 1"

The agent reads from two CSV files (holdings + trades) and uses GPT-4 to figure out how to answer your question.

## Setup

```bash
# clone and enter the project
git clone <repo-url>
cd property_loop

# create venv and install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# add your openai key
echo "OPENAI_API_KEY=sk-..." > .env
```

## Run

```bash
streamlit run app.py
```

Opens at http://localhost:8501

## Project layout

```
├── app.py              # streamlit frontend
├── src/
│   ├── agent.py        # langchain agent setup
│   ├── data_loader.py  # loads the csvs
│   └── prompts.py      # system prompts
├── data/
│   ├── holdings.csv    # ~1k rows of portfolio positions
│   └── trades.csv      # ~650 rows of transactions
└── requirements.txt
```

## About the data

**Holdings** - current positions with market values, quantities, and P&L (daily/monthly/quarterly/yearly). Funds include Garfield, Heather, MNC Inv, Ytum, etc.

**Trades** - historical buy/sell records with prices, quantities, and counterparties. Funds include HoldCo 1, ClientA, UNC Investment Fund, etc.

Note: the two tables use different naming for funds. They can be joined on `SecurityId` or `CustodianName`, but not on fund names directly.

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Connect repo at streamlit.io/cloud
3. Add `OPENAI_API_KEY` to Secrets
4. Done

## License

MIT
