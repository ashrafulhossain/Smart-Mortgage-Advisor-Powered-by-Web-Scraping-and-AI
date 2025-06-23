# 🏡 Smart Mortgage Advisor Powered by Web Scraping and AI

Smart Mortgage Advisor is an AI-powered intelligent chatbot that guides users through mortgage-related queries and applications in the UK. It uses GPT-4 to generate dynamic responses based on user inputs, scraped web content, and parsed PDFs. The bot stores conversation context using FAISS vector search and can collect application details to be saved securely for advisor follow-up.

---

## 📌 Features

✅ Intelligent mortgage assistant powered by GPT-4

✅ Collects user details conversationally and generates summaries

✅ Scrapes top UK mortgage advice websites for real-time context

✅ Extracts content from both digital and scanned PDFs using OCR

✅ Stores and retrieves contextual info via FAISS vector database

✅ Handles application logic (name, income, property details, etc.)

✅ Summarizes the entire mortgage profile with AI

✅ Prevents secret leaks using .env and .gitignore


---

## 🧠 Tech Stack

| Technology                                | Purpose                                                             |
| ----------------------------------------- | ------------------------------------------------------------------- |
| **Python 3.10+**                          | Core programming language                                           |
| **OpenAI GPT-4 (via `langchain_openai`)** | LLM to classify, generate responses, and extract mortgage data      |
| **LangChain**                             | Framework to orchestrate LLM chains and manage conversation flow    |
| **FAISS**                                 | Local vector store for efficient semantic search                    |
| **PDFPlumber**                            | Extract text from native PDF documents                              |
| **cloudscraper**                          | Bypass Cloudflare and scrape content from mortgage-related websites |
| **BeautifulSoup4**                        | Parse and clean scraped HTML content                                |
| **dotenv (`python-dotenv`)**              | Securely load sensitive variables like API keys from `.env` files   |
| **dataclasses**                           | Manage applicant data as structured objects                         |
| **uuid / os / json / time / glob**        | Handle file operations, temporary storage, and data processing      |
| **RecursiveCharacterTextSplitter**        | Split long documents into chunks for embedding                      |
| **LangChain Community + Core**            | Support for custom document types and schemas                       |

---

