# 🛒 Thelawala Search

### A Smart Product Search Engine Built with Python

Thelawala Search is a Python-based product search application that helps users find grocery products using simple text queries. It supports typo correction, keyword matching, price filtering, and stock-aware product ranking.

## 🚀 Features

- Smart product search
- Typo correction for misspelled queries
- Keyword-based product matching
- Price filtering (e.g., oil under 200)
- Stock availability handling
- Relevance-based product ranking
- Batch query processing
- JSONL result generation

## 🛠️ Technologies Used

- Python
- CSV
- JSON
- Regular Expressions
- Difflib
- IDF-based Ranking

## 📂 Project Structure

    thelawala-search/
    │
    ├── search.py
    ├── catalog.csv
    ├── inventory.csv
    ├── sample_queries.txt
    ├── results.jsonl
    ├── AI_USAGE.md
    ├── README.md
    └── .gitignore

## ⚙️ Installation

**1. Clone the repository**

    git clone https://github.com/saikumarbulasala/thelawala-search.git

**2. Navigate to the project folder**

    cd thelawala-search

**3. Check Python version**

    python --version

No external Python packages are required.

## ▶️ Usage

**Search for a product**

    python search.py "milk"

**Search with a price filter**

    python search.py "oil under 200"

**Test typo correction**

    python search.py "bisuit"

**Run batch queries**

    python search.py --batch sample_queries.txt

## 🧠 How It Works

1. Query Processing – Normalizes and tokenizes user search queries.
2. Typo Correction – Identifies and corrects spelling mistakes.
3. Product Matching – Matches search terms with product information.
4. Relevance Ranking – Ranks products based on matching relevance.
5. Price Filtering – Filters products based on specified price limits.
6. Stock Handling – Considers product availability when ranking results.
7. Result Generation – Produces search results in JSONL format.

## 💡 Sample Search Queries

| Query | Description |
|---|---|
| milk | Search for milk products |
| oil under 200 | Find oil below ₹200 |
| bisuit | Test spelling correction |
| doodh | Search using a synonym |
| thela select ghee | Search for a specific brand |

## 🔮 Future Enhancements

- Telugu and Hindi language support
- Improved search accuracy
- Web-based user interface
- Advanced product recommendations
- Search performance optimization

## 👨‍💻 Author

**Sai Kumar Bulasala**

GitHub: [@saikumarbulasala](https://github.com/saikumarbulasala)

---

⭐ If you like this project, consider giving it a star!
