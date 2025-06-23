# import os
# import openai
# import pdfplumber
# import requests
# import time
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.tools import Tool
# from langchain_core.documents import Document

# # ✅ Load environment variables
# load_dotenv()

# # ✅ Set OpenAI API Key
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # ✅ User-Agent Header to Avoid Bot Detection
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.google.com/",
#     "DNT": "1",
#     "Connection": "keep-alive"
# }

# # ✅ Website URLs (Zoopla Removed)
# urls = [
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ"
# ]

# # ✅ Function to Extract Text from a PDF
# def extract_text_from_pdf(pdf_path):
#     if not os.path.exists(pdf_path):
#         return "No PDF file found."

#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 extracted_text = page.extract_text()
#                 if extracted_text:
#                     text += extracted_text + "\n"
#     except Exception:
#         return "No text extracted from PDF."

#     return text.strip() if text else "No text extracted from PDF."

# # ✅ Set PDF Path
# pdf_path = r"C:\Users\STA\Desktop\KFV\AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # ✅ Function to Scrape Website Data
# def scrape_website(url):
#     try:
#         time.sleep(3)  # 🕒 Avoid bot detection
#         response = requests.get(url, headers=headers, timeout=10)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
#             return soup.get_text(separator=" ", strip=True)
#         return None
#     except Exception:
#         return None

# # ✅ Scrape Website Data
# docs = [scrape_website(url) for url in urls if scrape_website(url)]

# # ✅ Combine Scraped Web Content and PDF Content
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # ✅ Split Documents into Smaller Chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(all_docs)

# # ✅ Create FAISS Vector Store for Retrieval
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # ✅ Define Retriever Tool
# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: retriever.get_relevant_documents(query),
#     description="Useful for retrieving mortgage-related information."
# )

# # ✅ Initialize ChatOpenAI Model
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=2500, top_p=0.9)

# # ✅ Define Question Generation Prompt
# question_generation_prompt = ChatPromptTemplate.from_template(
#     """
#     The user is interested in mortgage-related information. Based on their responses so far, generate the next most relevant question from the following list:
    
#     1. Is this a single person application or are you in a partnership? (Married, Civil Partnership, Living Together)
#     2. Are you a first-time buyer?
#     3. Please provide your date of birth (and your partner's, if applicable).
#     4. Are you in employment?
#     5. If yes, are you employed or self-employed?
#     6. What is your annual gross income (before tax and deductions)?
#     7. Do you have any credit commitments? If yes, please list them.
#     8. How many dependents do you have?
#     9. If you have adverse credit, what is it?
#     10. Do you plan to sell an existing property to support your new mortgage?
#     11. What are your committed expenses? (e.g., maintenance, school fees, nursery costs)

#     Generate only one relevant question at a time based on the user's responses so far.
#     """
# )

# # ✅ Corrected Method for Generating Questions Dynamically
# llm_question_chain = question_generation_prompt | llm

# # ✅ Chatbot Interaction
# print("\n🚀 Welcome! How can I assist you today?")

# chat_active = True
# mortgage_interest_detected = False
# user_data = {}
# last_message = ""

# while chat_active:
#     user_input = input("\nYour message: ").strip()
    
#     if not user_input:
#         continue  # Skip empty input
    
#     if user_input.lower() in ["exit", "quit", "close"]:
#         print("✅ Thank you for chatting! Feel free to return anytime.")
#         break  # Exit the chat
    
#     # Prevent duplicate messages
#     if user_input == last_message:
#         continue
#     last_message = user_input

#     # Detect mortgage-related interest
#     if "mortgage" in user_input.lower() and not mortgage_interest_detected:
#         print("📢 Sure! Buying a mortgage involves multiple steps. Let's go through the process step by step.")
#         mortgage_interest_detected = True

#     elif mortgage_interest_detected:
#         # Generate next relevant question dynamically
#         generated_question = llm_question_chain.invoke({"previous_responses": user_data})
#         question_text = generated_question.content.strip()
        
#         print(f"\n🤖 AI: {question_text}")
#         answer = input("Your answer: ").strip()
        
#         if answer:
#             user_data[question_text] = answer

#     else:
#         response = llm.invoke(user_input)
#         print(f"🤖 AI: {response.content}")






# import os
# import openai
# import pdfplumber
# import requests
# import time
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.tools import Tool
# from langchain_core.documents import Document
# from langchain.schema import AIMessage, HumanMessage
# import random

# # Load environment variables
# load_dotenv()

# # Set OpenAI API Key
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # User-Agent Header to Avoid Bot Detection
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.google.com/",
#     "DNT": "1",
#     "Connection": "keep-alive"
# }

# # Website URLs (Zoopla Removed)
# urls = [
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ"
# ]

# # Function to Extract Text from a PDF
# def extract_text_from_pdf(pdf_path):
#     if not os.path.exists(pdf_path):
#         return "No PDF file found."
    
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 extracted_text = page.extract_text()
#                 if extracted_text:
#                     text += extracted_text + "\n"
#     except Exception:
#         return "No text extracted from PDF."
    
#     return text.strip() if text else "No text extracted from PDF."

# # Set PDF Path
# pdf_path = r"C:\Users\STA\Desktop\KFV\AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Function to Scrape and Clean Website Data
# def scrape_website(url):
#     try:
#         time.sleep(3)  # Avoid bot detection
#         response = requests.get(url, headers=headers, timeout=10)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Remove footer, navigation, and legal text
#             for tag in soup.find_all(["footer", "nav", "script", "style", "header", "aside"]):
#                 tag.extract()
            
#             text_content = soup.get_text(separator=" ", strip=True)
#             return text_content
#         return None
#     except Exception:
#         return None

# # Scrape and Clean Website Data
# docs = [scrape_website(url) for url in urls if scrape_website(url)]

# # Combine Scraped Web Content and PDF Content
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Split Documents into Smaller Chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(all_docs)

# # Create FAISS Vector Store for Retrieval
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define Retriever Tool
# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: retriever.invoke(query),  # Updated method
#     description="Useful for retrieving mortgage-related information."
# )

# # Initialize ChatOpenAI Model
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, max_tokens=2500, top_p=0.95)

# # Chat Memory Storage
# chat_history = []

# # Chatbot Interaction
# print("\n🚀 Welcome! Your AI Mortgage Advisor is ready. Ask me anything!")

# chat_active = True
# user_data = {}
# last_message = ""

# while chat_active:
#     user_input = input("\nYour message: ").strip()
    
#     if not user_input:
#         continue  # Skip empty input
    
#     if user_input.lower() in ["exit", "quit", "close"]:
#         print("✅ Thank you for chatting! It was great talking to you. Have a wonderful day! 😊")
#         break  # Exit the chat
    
#     # Prevent duplicate messages
#     if user_input == last_message:
#         continue
#     last_message = user_input
    
#     # Adding ChatGPT-like natural response behavior
#     human_like_prompt = f"You are a friendly and engaging assistant. Respond naturally and conversationally like a human. Here's the user's message: '{user_input}'"
#     general_response = llm.invoke([HumanMessage(content=human_like_prompt)])
#     response_text = general_response.content
    
#     chat_history.append(HumanMessage(content=user_input))
#     chat_history.append(AIMessage(content=response_text))
    
#     print(f"\n🤖 AI: {response_text}")





# import os
# import pdfplumber
# import requests
# import time
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.tools import Tool
# from langchain_core.documents import Document
# from langchain.schema import AIMessage, HumanMessage

# # Load environment variables
# load_dotenv()

# # Set OpenAI API Key
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # User-Agent Header to Avoid Bot Detection
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.google.com/",
#     "DNT": "1",
#     "Connection": "keep-alive"
# }

# # Website URLs
# urls = [
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ"
# ]

# # Function to Extract Text from a PDF
# def extract_text_from_pdf(pdf_path):
#     if not os.path.exists(pdf_path):
#         return "No PDF file found."
    
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 extracted_text = page.extract_text()
#                 if extracted_text:
#                     text += extracted_text + "\n"
#     except Exception:
#         return "No text extracted from PDF."
    
#     return text.strip() if text else "No text extracted from PDF."

# # Set PDF Path
# pdf_path = r"C:\Users\STA\Desktop\KFV\AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Function to Scrape and Clean Website Data
# def scrape_website(url):
#     try:
#         time.sleep(3)  # Avoid bot detection
#         response = requests.get(url, headers=headers, timeout=10)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Remove footer, navigation, and legal text
#             for tag in soup.find_all(["footer", "nav", "script", "style", "header", "aside"]):
#                 tag.extract()
            
#             text_content = soup.get_text(separator=" ", strip=True)
#             return text_content
#         return None
#     except Exception:
#         return None

# # Scrape and Clean Website Data
# docs = [scrape_website(url) for url in urls if scrape_website(url)]

# # Combine Scraped Web Content and PDF Content
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Split Documents into Smaller Chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(all_docs)

# # Create FAISS Vector Store for Retrieval
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define Retriever Tool
# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: retriever.invoke(query),
#     description="Useful for retrieving mortgage-related information."
# )

# # Initialize ChatOpenAI Model
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=4000, top_p=0.9)

# # Predefined Questions
# predefined_questions = [
#     "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#     "Are you a first-time buyer?",
#     "Please can you give me your date of birth and your partner's, if applicable.",
#     "Are you in employment?",
#     "If yes, please specify if you are employed or self-employed?",
#     "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#     "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#     "How many dependants do you have, if any?",
#     "If you have adverse credit, please tell me what it is?",
#     "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#     "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs."
# ]

# # Trigger Phrases
# trigger_phrases = [
#     "I want to buy a house",
#     "I need a home loan",
#     "I want to apply for a mortgage",
#     "Can you help me get a mortgage",
#     "I need a mortgage for my new property"
# ]

# # Function to Check if User Input Matches Trigger Phrases
# def is_mortgage_related(input_text):
#     input_text = input_text.lower()
#     for phrase in trigger_phrases:
#         if phrase.lower() in input_text:
#             return True
#     return False

# # Function to Ask Predefined Questions
# def ask_predefined_questions():
#     user_responses = {}
#     for question in predefined_questions:
#         print(f"\n🤖 AI: {question}")
#         user_response = input("Your answer: ").strip()
#         user_responses[question] = user_response
#     return user_responses

# # Function to Generate Summary Using the Model
# def generate_summary(user_responses):
#     # Combine questions and answers into a single string
#     qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in user_responses.items()])
    
#     # Prompt for the model to generate a summary
#     summary_prompt = f"""
#     You are a helpful mortgage advisor. Below are the questions and answers provided by the user. 
#     Please summarize the information in a clear and concise way, and provide any relevant advice or next steps.

#     Questions and Answers:
#     {qa_pairs}

#     Summary:
#     """
    
#     # Generate summary using the model
#     summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
#     return summary_response.content

# # Chat Memory Storage
# chat_history = []

# # Chatbot Interaction
# print("\n🚀 Welcome! Your AI Mortgage Advisor is ready. Ask me anything!")

# chat_active = True
# user_data = {}
# last_message = ""

# while chat_active:
#     user_input = input("\nYour message: ").strip()
    
#     if not user_input:
#         continue  # Skip empty input
    
#     if user_input.lower() in ["exit", "quit", "close"]:
#         print("✅ Thank you for chatting! It was great talking to you. Have a wonderful day! 😊")
#         break  # Exit the chat
    
#     # Prevent duplicate messages
#     if user_input == last_message:
#         continue
#     last_message = user_input
    
#     # Check if User Input Matches Trigger Phrases
#     if is_mortgage_related(user_input):
#         print("\n🤖 AI: Sure! I can help you with that. Let me ask you a few questions to get started.")
#         user_data = ask_predefined_questions()
        
#         # Generate Summary Using the Model
#         print("\n🤖 AI: Thank you for providing the information! Generating a summary for you...")
#         summary = generate_summary(user_data)
        
#         # Display Summary to the User
#         print(f"\n🤖 AI: Here's a summary based on your answers:\n{summary}")
#         break  # Exit after generating the summary
#     else:
#         # Normal Chatbot Interaction
#         human_like_prompt = f"You are a friendly and engaging assistant. Respond naturally and conversationally like a human. Here's the user's message: '{user_input}'"
#         general_response = llm.invoke([HumanMessage(content=human_like_prompt)])
#         response_text = general_response.content
        
#         chat_history.append(HumanMessage(content=user_input))
#         chat_history.append(AIMessage(content=response_text))
        
#         print(f"\n🤖 AI: {response_text}")











# import os
# import pdfplumber
# import requests
# import time
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.tools import Tool
# from langchain_core.documents import Document
# from langchain.schema import AIMessage, HumanMessage

# # Load environment variables
# load_dotenv()

# # Set OpenAI API Key
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # User-Agent Header to Avoid Bot Detection
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.google.com/",
#     "DNT": "1",
#     "Connection": "keep-alive"
# }

# # Website URLs
# urls = [
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://www.hsbc.co.uk/mortgages/our-rates/", 
#     "https://www.nerdwallet.com/"  
# ]

# # Function to Extract Text from a PDF
# def extract_text_from_pdf(pdf_path):
#     if not os.path.exists(pdf_path):
#         return "No PDF file found."
    
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 extracted_text = page.extract_text()
#                 if extracted_text:
#                     text += extracted_text + "\n"
#     except Exception:
#         return "No text extracted from PDF."
    
#     return text.strip() if text else "No text extracted from PDF."

# # Set PDF Path
# pdf_path = r"C:\Users\STA\Desktop\KFV\AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Function to Scrape and Clean Website Data
# def scrape_website(url):
#     try:
#         time.sleep(3)  # Avoid bot detection
#         response = requests.get(url, headers=headers, timeout=10)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Remove footer, navigation, and legal text
#             for tag in soup.find_all(["footer", "nav", "script", "style", "header", "aside"]):
#                 tag.extract()
            
#             text_content = soup.get_text(separator=" ", strip=True)
#             return text_content
#         return None
#     except Exception:
#         return None

# # Scrape and Clean Website Data
# docs = [scrape_website(url) for url in urls if scrape_website(url)]

# # Combine Scraped Web Content and PDF Content
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Split Documents into Smaller Chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(all_docs)

# # Create FAISS Vector Store for Retrieval
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define Retriever Tool
# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: retriever.invoke(query),
#     description="Useful for retrieving mortgage-related information."
# )

# # Initialize ChatOpenAI Model
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=4000, top_p=0.9)

# # Predefined Questions
# predefined_questions = [
#     "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#     "Are you a first-time buyer?",
#     "Please can you give me your date of birth and your partner's, if applicable.",
#     "Are you in employment?",
#     "If yes, please specify if you are employed or self-employed?",
#     "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#     "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#     "How many dependants do you have, if any?",
#     "If you have adverse credit, please tell me what it is?",
#     "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#     "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs."
# ]

# # Trigger Phrases
# trigger_phrases = [
#     "I want to buy a house",
#     "I need a home loan",
#     "I want to apply for a mortgage",
#     "Can you help me get a mortgage",
#     "I need a mortgage for my new property"
# ]

# # Function to Check if User Input Matches Trigger Phrases
# def is_mortgage_related(input_text):
#     input_text = input_text.lower()
#     for phrase in trigger_phrases:
#         if phrase.lower() in input_text:
#             return True
#     return False

# # Function to Ask Predefined Questions
# def ask_predefined_questions():
#     user_responses = {}
#     for question in predefined_questions:
#         print(f"\n🤖 AI: {question}")
#         user_response = input("Your answer: ").strip()
#         user_responses[question] = user_response
#     return user_responses

# # Function to Generate Summary Using the Model
# def generate_summary(user_responses):
#     # Combine questions and answers into a single string
#     qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in user_responses.items()])
    
#     # Prompt for the model to generate a summary
#     summary_prompt = f"""
#     You are a helpful mortgage advisor. Below are the questions and answers provided by the user. 
#     Please summarize the information in a clear and concise way, and provide any relevant advice or next steps.

#     Questions and Answers:
#     {qa_pairs}

#     Summary:
#     """
    
#     # Generate summary using the model
#     summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
#     return summary_response.content

# # Chat Memory Storage
# chat_history = []

# # Chatbot Interaction
# print("\n🚀 Welcome! Your AI Mortgage Advisor is ready. Ask me anything!")

# chat_active = True
# user_data = {}
# last_message = ""

# while chat_active:
#     user_input = input("\nYour message: ").strip()
    
#     if not user_input:
#         continue  # Skip empty input
    
#     if user_input.lower() in ["exit", "quit", "close"]:
#         print("✅ Thank you for chatting! It was great talking to you. Have a wonderful day! 😊")
#         break  # Exit the chat
    
#     # Prevent duplicate messages
#     if user_input == last_message:
#         continue
#     last_message = user_input
    
#     # Check if User Input Matches Trigger Phrases
#     if is_mortgage_related(user_input):
#         print("\n🤖 AI: Sure! I can help you with that. Let me ask you a few questions to get started.")
#         user_data = ask_predefined_questions()
        
#         # Generate Summary Using the Model
#         print("\n🤖 AI: Thank you for providing the information! Generating a summary for you...")
#         summary = generate_summary(user_data)
        
#         # Display Summary to the User
#         print(f"\n🤖 AI: Here's a summary based on your answers:\n{summary}")
#         break  # Exit after generating the summary
#     else:
#         # Normal Chatbot Interaction
#         human_like_prompt = f"You are a friendly and engaging assistant. Respond naturally and conversationally like a human. Here's the user's message: '{user_input}'"
#         general_response = llm.invoke([HumanMessage(content=human_like_prompt)])
#         response_text = general_response.content
        
#         chat_history.append(HumanMessage(content=user_input))
#         chat_history.append(AIMessage(content=response_text))
        
#         print(f"\n🤖 AI: {response_text}")















# import os
# import pdfplumber
# import requests
# import time
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()

# # Set OpenAI API Key
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # User-Agent Header to Avoid Bot Detection
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.google.com/",
#     "DNT": "1",
#     "Connection": "keep-alive"
# }

# # Website URLs
# urls = [
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://www.hsbc.co.uk/mortgages/our-rates/", 
#     "https://www.nerdwallet.com/"  
# ]

# # Function to Extract Text from a PDF
# def extract_text_from_pdf(pdf_path):
#     if not os.path.exists(pdf_path):
#         return "No PDF file found."
    
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 extracted_text = page.extract_text()
#                 if extracted_text:
#                     text += extracted_text + "\n"
#     except Exception:
#         return "No text extracted from PDF."
    
#     return text.strip() if text else "No text extracted from PDF."

# # Set PDF Path
# pdf_path = r"C:\Users\STA\Desktop\KFV\AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Function to Scrape and Clean Website Data
# def scrape_website(url):
#     try:
#         time.sleep(3)  # Avoid bot detection
#         response = requests.get(url, headers=headers, timeout=10)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Remove footer, navigation, and legal text
#             for tag in soup.find_all(["footer", "nav", "script", "style", "header", "aside"]):
#                 tag.extract()
            
#             text_content = soup.get_text(separator=" ", strip=True)
#             return text_content
#         return None
#     except Exception:
#         return None

# # Scrape and Clean Website Data
# docs = [scrape_website(url) for url in urls if scrape_website(url)]

# # Combine Scraped Web Content and PDF Content
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Split Documents into Smaller Chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(all_docs)

# # Create FAISS Vector Store for Retrieval
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Initialize ChatOpenAI Model
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=4000, top_p=0.9)

# # Trigger Phrases
# trigger_phrases = [
#     "I want to buy a house",
#     "I need a home loan",
#     "I want to apply for a mortgage",
#     "Can you help me get a mortgage",
#     "I need a mortgage for my new property"
# ]

# # Predefined Questions for Mortgage Application
# predefined_questions = [
#     "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#     "Are you a first-time buyer?",
#     "Please can you give me your date of birth and your partner's, if applicable.",
#     "Are you in employment?",
#     "If yes, please specify if you are employed or self-employed?",
#     "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#     "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#     "How many dependants do you have, if any?",
#     "If you have adverse credit, please tell me what it is?",
#     "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#     "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs."
# ]

# # Function to Check if User Input Matches Trigger Phrases
# def is_mortgage_related(input_text):
#     input_text = input_text.lower()
#     for phrase in trigger_phrases:
#         if phrase.lower() in input_text:
#             return True
#     return False

# # Function to Retrieve Relevant Information Using FAISS
# def retrieve_relevant_information(user_input):
#     relevant_docs = retriever.invoke(user_input)
#     relevant_info = "\n".join([doc.page_content for doc in relevant_docs])
#     return relevant_info

# # Function to Generate Dynamic Response Using ChatOpenAI
# def generate_dynamic_response(user_input):
#     # Retrieve Relevant Information
#     relevant_info = retrieve_relevant_information(user_input)
    
#     # Dynamic Prompt for AI Model
#     prompt = f"""
#     You are a helpful mortgage advisor. The user has asked the following question: 
#     "{user_input}"
    
#     Here is some relevant information that might help you answer the question:
#     {relevant_info}
    
#     Provide a detailed and informative response based on this information.
#     """
#     # Generate Response Using ChatOpenAI
#     response = llm.invoke([{"role": "user", "content": prompt}])
#     return response.content

# # Function to Ask Predefined Questions
# def ask_predefined_questions():
#     user_responses = {}
#     print("\n🤖 AI: Let's gather some information for your mortgage application.")
#     for question in predefined_questions:
#         print(f"\n🤖 AI: {question}")
#         user_response = input("Your answer: ").strip()
#         user_responses[question] = user_response
#     return user_responses

# # Function to Generate Summary Using the Model
# def generate_summary(user_responses):
#     # Combine questions and answers into a single string
#     qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in user_responses.items()])
    
#     # Prompt for the model to generate a summary
#     summary_prompt = f"""
#     You are a helpful mortgage advisor. Below are the questions and answers provided by the user. 
#     Please summarize the information in a clear and concise way, and provide any relevant advice or next steps.

#     Questions and Answers:
#     {qa_pairs}

#     Summary:
#     """
    
#     # Generate summary using the model
#     summary_response = llm.invoke([{"role": "user", "content": summary_prompt}])
#     return summary_response.content

# # Chatbot Interaction
# print("\n🚀 Welcome! Your AI Mortgage Advisor is ready. Ask me anything!")

# chat_active = True
# while chat_active:
#     user_input = input("\nYour message: ").strip()
    
#     if not user_input:
#         continue  # Skip empty input
    
#     if user_input.lower() in ["exit", "quit", "close"]:
#         print("✅ Thank you for chatting! It was great talking to you. Have a wonderful day! 😊")
#         break  # Exit the chat
    
#     # Check if Input is Mortgage Related
#     if is_mortgage_related(user_input):
#         if "apply" in user_input.lower():
#             # Start Mortgage Application Process
#             print("\n🤖 AI: Sure! Let's start your mortgage application process.")
#             user_data = ask_predefined_questions()
            
#             # Generate Summary Using the Model
#             print("\n🤖 AI: Thank you for providing the information! Generating a summary for you...")
#             summary = generate_summary(user_data)
            
#             # Display Summary to the User
#             print(f"\n🤖 AI: Here's a summary based on your answers:\n{summary}")
#         else:
#             # Generate Informed Response
#             response = generate_dynamic_response(user_input)
#             print(f"\n🤖 AI: {response}")
#     else:
#         # Normal Chatbot Interaction
#         human_like_prompt = f"You are a friendly and engaging assistant. Respond naturally and conversationally like a human. Here's the user's message: '{user_input}'"
#         general_response = llm.invoke([{"role": "user", "content": human_like_prompt}])
#         response_text = general_response.content
        
#         print(f"\n🤖 AI: {response_text}")




















