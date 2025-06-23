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

| Technology              | Purpose                                                |
| ----------------------- | ------------------------------------------------------ |
| **Python 3.10+**        | Core programming language                              |
| **OpenAI GPT-4**        | Generate personalized health recommendations           |
| **Pinecone**            | Vector database to store and query document embeddings |
| **FAISS**               | Perform fast local similarity search over embeddings   |
| **LangChain**           | Chunk and format long text documents                   |
| **PDFPlumber**          | Extract text from native PDFs                          |
| **PDF2Image + EasyOCR** | Extract text from scanned PDFs using OCR               |
| **dotenv**              | Securely load API keys from `.env`                     |
| **Pickle + JSON**       | Local cache and metadata storage                       |
| **uuid, glob, os**      | File handling and cleanup utilities                    |

---

