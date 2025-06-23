# import os
# import openai
# import pdfplumber
# from dotenv import load_dotenv
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.tools import Tool
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ.setdefault("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Ensure OpenAI API Key is set
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Step 1: Define the web scraping and PDF data loading
# urls = [
#     "https://www.zoopla.co.uk/discover/buying/answers-to-your-most-common-mortgage-questions/",
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ"
# ]

# # Extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# # Path to the uploaded PDF file
# pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Scrape data from the websites
# docs = []
# for url in urls:
#     loader = WebBaseLoader(url)
#     documents = loader.load()
#     for doc in documents:
#         if isinstance(doc, dict) and 'page_content' in doc:
#             docs.append(doc['page_content'])

# # Combine web scraped data and PDF data
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Step 3: Split the documents into chunks
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)

# # Step 4: Use OpenAI Embeddings to convert documents into vectors
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define a custom retriever tool
# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: f"Retrieved mortgage-related information for: {query}",
#     description="Useful for retrieving mortgage-related information."
# )

# # Step 5: Set up the LLM chain for personalized responses
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=2500, top_p=0.9)

# # Define the prompt template
# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     Here is a summary regarding the mortgage inquiry:
#     - Partnership Status: {partnership_status}
#     - First-time Buyer: {first_time_buyer}
#     - Date of Birth: {dob}
#     - Employment Status: {employment_status}
#     - Annual Income: {annual_income}
#     - Credit Commitments: {credit_commitments}
#     - Dependents: {dependents}
#     - Adverse Credit: {adverse_credit}
#     - Existing Property for Mortgage Support: {existing_property}
#     - Committed Expenditure: {committed_expenditure}
    
#     Based on this information, please provide a personalized recommendation from the available mortgage options.
#     """
# )

# # Create LLMChain
# llm_summary_chain = summary_prompt | llm

# # Step 6: User interaction
# print("Welcome! How can I assist you today?")

# chat_active = True
# mortgage_interest_detected = False
# current_question = None
# questions = [
#     "Is this a single person application or are you in a partnership? (Married, Civil Partnership, Living Together)",
#     "Are you a first-time buyer? (Yes/No)",
#     "Please provide your date of birth and your partner's, if applicable:",
#     "Are you in employment? If yes, specify if you are employed or self-employed:",
#     "How much do you earn per year (gross), including any commission, bonuses, overtime, and other income sources:",
#     "Do you have any credit commitments (e.g., credit cards, loans, mortgage payments, pensions)? If yes, please list them:",
#     "How many dependents do you have, if any:",
#     "If you have adverse credit, please specify what it is:",
#     "Do you have an existing property that you plan to sell to support your new mortgage? If yes, provide details:",
#     "What is your committed expenditure? (e.g., maintenance, school fees, nursery costs)"
# ]

# user_data = {}
# question_index = 0
# last_message = ""

# while chat_active:
#     user_input = input("Your message: ")
    
#     if user_input == last_message:
#         continue  # Prevent duplicate messages
#     last_message = user_input
    
#     if "mortgage" in user_input.lower() and not mortgage_interest_detected:
#         print("Sure! Buying a mortgage involves multiple steps, such as checking your credit score, finding the right lender, and choosing a mortgage type. Would you like me to guide you through the process?")
#         mortgage_interest_detected = True
    
#     elif mortgage_interest_detected:
#         if question_index < len(questions):
#             current_question = questions[question_index]
#             print(current_question)
#             answer = input("Your response: ")
#             if answer.strip():
#                 user_data[current_question] = answer  # Store responses with cleaner keys
#                 question_index += 1
#             else:
#                 print("I understand that this might be confusing. Let me clarify before we move forward.")
#         else:
#             print("Generating your mortgage summary...")
#             missing_keys = [key for key in summary_prompt.input_variables if key not in user_data]
#             for key in missing_keys:
#                 user_data[key] = "Not Provided"
#             generated_summary = llm_summary_chain.invoke(user_data)
#             print("\nGenerated Mortgage Summary:")
#             print(generated_summary.content)
#             mortgage_interest_detected = False
#             question_index = 0
#             user_data = {}
#     else:
#         if "how are you" in user_input.lower():
#             print("AI: I'm doing great! Thanks for asking. How about you?")
#         else:
#             response = llm.invoke(user_input)
#             print("AI:", response.content)
    
#     if user_input.lower() in ["exit", "quit", "close"]:
#         chat_active = False
#         print("Thank you for chatting! Feel free to return anytime.")







# import os
# import pdfplumber
# import requests
# import time
# import json  
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
# retriever = vectordb.as_retriever(search_kwargs={"k": 3})  # Get top 5 most relevant chunks

# # Initialize ChatOpenAI Model
# llm = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=1200, top_p=0.9)

# # Mortgage-related keywords to detect mortgage questions
# mortgage_keywords = [
#     "mortgage", "home loan", "property", "house", "buy", "purchase", "interest rate", 
#     "down payment", "deposit", "first-time buyer", "fixed rate", "variable rate", 
#     "remortgage", "equity", "repayment", "loan-to-value", "ltv", "term", "lender",
#     "borrowing", "credit score", "affordability", "amortization", "foreclosure",
#     "capital", "conveyancing", "stamp duty", "equity release", "tracker", "offset"
# ]

# # Predefined Questions for detailed mortgage application
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

# # Trigger Phrases for full mortgage application
# trigger_phrases = [
#     "I want to buy a house",
#     "I need a home loan",
#     "I want to apply for a mortgage",
#     "Can you help me get a mortgage",
#     "I need a mortgage for my new property",
#     "help me apply for a mortgage"
# ]

# # Function to Check if User Input Contains Mortgage Keywords
# def is_mortgage_related(input_text):
#     input_text = input_text.lower()
    
#     # Check for trigger phrases (full application)
#     for phrase in trigger_phrases:
#         if phrase.lower() in input_text:
#             return "application"
    
#     # Check for mortgage keywords (informational)
#     for keyword in mortgage_keywords:
#         if keyword.lower() in input_text:
#             return "information"
            
#     return "general"

# # Function to Retrieve Relevant Information from Vector Database
# def get_relevant_info(query):
#     try:
#         # Get relevant documents from vector database
#         relevant_docs = retriever.invoke(query)
        
#         # Extract and format the content
#         retrieved_info = "\n\n".join([doc.page_content for doc in relevant_docs])
#         return retrieved_info
#     except Exception as e:
#         print(f"Error retrieving information: {e}")
#         return ""

# # Function to Ask Predefined Questions
# def ask_predefined_questions():
#     user_responses = {}
#     for question in predefined_questions:
#         print(f"\n🤖 AI: {question}")
#         user_response = input("Your answer: ").strip()
#         user_responses[question] = user_response
#     return user_responses

# # Function to Generate Response Using Retrieval-Augmented Generation
# def generate_rag_response(user_input):
#     # Get relevant information from vector database
#     relevant_info = get_relevant_info(user_input)
    
#     # Create a prompt that includes the retrieved information
#     rag_prompt = f"""
#     You are a knowledgeable mortgage advisor with expertise in UK mortgages, home loans, and property financing.
    
#     Relevant information from our knowledge base:
#     {relevant_info}
    
#     User's question: {user_input}
    
#     Based on the relevant information provided above, please give a comprehensive, detailed, and informative answer to the user's question.
#     Include specific details like typical interest rates, down payment percentages, loan terms, or requirements when relevant.
#     Avoid using markdown symbols like ** or *. Provide the answer in plain text.
#     If the information is not available in the knowledge base, provide general mortgage advice but be honest about limitations.
#     """
    
#     # Generate response using the model with RAG
#     response = llm.invoke([HumanMessage(content=rag_prompt)])
#     return response.content

# # Function to Generate Summary Using the Model
# def generate_summary(user_responses):
#     # Combine questions and answers into a prompt for the model
#     qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in user_responses.items()])
    
#     # Prompt for the model to generate a summary
#     summary_prompt = f"""
#     You are a helpful mortgage advisor. Below are the questions and answers provided by the user. 
#     Please summarize the information in a clear, concise, and conversational way. Avoid repeating the same information multiple times.
#     Provide any relevant advice or next steps.

#     Questions and Answers:
#     {qa_pairs}

#     Summary:
#     """
    
#     # Generate summary using the model
#     summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
#     return summary_response.content

# # Function to Save User Data to a JSON File
# def save_user_data(user_responses, summary, contact_info):
#     user_data = {
#         "user_responses": user_responses,  
#         "summary": summary,  
#         "contact_info": contact_info  
#     }
    
#     # Save the data to a JSON file
#     with open("user_data.json", "w") as file:
#         json.dump(user_data, file, indent=4)
    
#     print("✅ Your information has been saved successfully!")

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
    
#     # Check what type of query this is
#     query_type = is_mortgage_related(user_input)
    
#     # Handle based on query type
#     if query_type == "application":
#         # Full mortgage application process
#         print("\n🤖 AI: Sure! I can help you with your mortgage application. Let me ask you a few questions to get started.")
#         user_data = ask_predefined_questions()
        
#         # Generate Summary Using the Model
#         print("\n🤖 AI: Thank you for providing the information! Generating a summary for you...")
#         summary = generate_summary(user_data)
        
#         # Display Summary to the User
#         print(f"\n🤖 AI: Here's a summary based on your answers:\n{summary}")
        
#         # Ask if they want to save their information
#         print("\n🤖 AI: Would you like to save your information for future contact regarding mortgage offers or advice? (Type 'yes' or 'no')")
#         save_choice = input("Your choice: ").strip().lower()
        
#         if save_choice == "yes":
#             # Collect contact information
#             print("\n🤖 AI: Please provide your contact information for future updates.")
#             email = input("Your email: ").strip()
#             phone = input("Your phone number: ").strip()
            
#             # Save user data to a JSON file
#             contact_info = {"email": email, "phone": phone}
#             save_user_data(user_data, summary, contact_info)
        
#         # Ask if they want to continue or exit
#         print("\n🤖 AI: Would you like to continue chatting or exit? (Type 'continue' or 'exit')")
#         continue_choice = input("Your choice: ").strip().lower()
#         if continue_choice == "exit":
#             print("✅ Thank you for chatting! It was great talking to you. Have a wonderful day! 😊")
#             break
    
#     elif query_type == "information":
#         # Mortgage information query - use RAG
#         response_text = generate_rag_response(user_input)
        
#         chat_history.append(HumanMessage(content=user_input))
#         chat_history.append(AIMessage(content=response_text))
        
#         print(f"\n🤖 AI: {response_text}")
    
#     else:
#         # General chatbot interaction
#         general_prompt = f"""
#         You are a friendly and engaging mortgage advisor. Respond naturally and conversationally like a human. 
#         Avoid using markdown symbols or unnecessary formatting. Provide the answer in plain text.
#         Here's the user's message: '{user_input}'
#         """
#         general_response = llm.invoke([HumanMessage(content=general_prompt)])
#         response_text = general_response.content
        
#         chat_history.append(HumanMessage(content=user_input))
#         chat_history.append(AIMessage(content=response_text))
        
#         print(f"\n🤖 AI: {response_text}")
