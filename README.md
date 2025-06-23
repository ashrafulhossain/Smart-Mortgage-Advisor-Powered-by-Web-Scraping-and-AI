# 🏡 Smart Mortgage Advisor Powered by Web Scraping and AI

Smart Mortgage Advisor is an AI-powered intelligent chatbot that guides users through mortgage-related queries and applications in the UK. It uses GPT-4 to generate dynamic responses based on user inputs, scraped web content, and parsed PDFs. The bot stores conversation context using FAISS vector search and can collect application details to be saved securely for advisor follow-up.

---


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

## 🚀Features

📄 Processes PDF DocumentsExtracts text from local PDF guides and resources using pdfplumber.

🌐 Scrapes Real-Time Mortgage ContentGathers information from top UK mortgage websites using cloudscraper and BeautifulSoup.

🧠 Classifies User Queries SmartlyUses GPT-4 to classify user input into types: application, information, or general.

🗣️ Conversational AI with MemoryChatbot remembers past messages and responds in context using LangChain + GPT-4.

🔍 Semantic Search with FAISSScraped and PDF content is chunked and embedded, then stored in FAISS for fast retrieval.

🧬 Embeddings with OpenAIText chunks are embedded using OpenAI’s embedding model to match user questions.

📚 Real-Time Recommendation GenerationGPT-4 generates answers using retrieved knowledge and chat history.

🧾 Dynamic Mortgage Application CollectionAutomatically collects user mortgage data step-by-step and generates summaries.

🔐 Environment-Safe ConfigurationLoads API keys and configs from .env using python-dotenv.

💾 Lead Storage for Further Follow-UpStores collected applicant info into a local JSON file (leads.json).

