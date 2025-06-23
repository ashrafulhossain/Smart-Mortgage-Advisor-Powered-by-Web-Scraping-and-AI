# # import os
# # import openai
# # import pdfplumber
# # from dotenv import load_dotenv
# # from langchain_community.document_loaders import WebBaseLoader
# # from langchain_community.vectorstores import FAISS
# # from langchain_openai import OpenAIEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain.chains import LLMChain
# # from langchain.prompts import ChatPromptTemplate
# # from langchain_openai import ChatOpenAI
# # from langchain.tools import Tool
# # from langchain_core.documents import Document

# # # Load environment variables
# # load_dotenv()
# # os.environ.setdefault("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
# # os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # # Ensure OpenAI API Key is set
# # openai.api_key = os.getenv('OPENAI_API_KEY')

# # # Step 1: Define the web scraping and PDF data loading
# # urls = [
# #     "https://www.zoopla.co.uk/discover/buying/answers-to-your-most-common-mortgage-questions/",
# #     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
# #     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
# #     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
# #     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ"
# # ]

# # # Extract text from PDF
# # def extract_text_from_pdf(pdf_path):
# #     text = ""
# #     with pdfplumber.open(pdf_path) as pdf:
# #         for page in pdf.pages:
# #             text += page.extract_text()
# #     return text

# # # Path to the uploaded PDF file
# # pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# # pdf_docs_text = extract_text_from_pdf(pdf_path)

# # # Scrape data from the websites
# # docs = []
# # for url in urls:
# #     loader = WebBaseLoader(url)
# #     documents = loader.load()
# #     for doc in documents:
# #         if isinstance(doc, dict) and 'page_content' in doc:
# #             docs.append(doc['page_content'])

# # # Combine web scraped data and PDF data
# # all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # # Step 3: Split the documents into chunks
# # documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)

# # # Step 4: Use OpenAI Embeddings to convert documents into vectors
# # vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# # retriever = vectordb.as_retriever()

# # # Define a custom retriever tool
# # retriever_tool = Tool(
# #     name="Mortgage Information Retriever",
# #     func=lambda query: f"Retrieved mortgage-related information for: {query}",
# #     description="Useful for retrieving mortgage-related information."
# # )

# # # Step 5: Set up the LLM chain for personalized responses
# # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=2500, top_p=0.9)

# # # Define the prompt template for dynamically generating questions
# # question_generation_prompt = ChatPromptTemplate.from_template(
# #     """
# #     The user is interested in mortgage-related information. Based on their responses so far, generate the next most relevant question from the following list:
    
# #     1. Is this a single person application or are you in a partnership? (Married, Civil Partnership, Living Together)
# #     2. Are you a first-time buyer?
# #     3. Please can you give me your date of birth and your partner's, if applicable?
# #     4. Are you in employment?
# #     5. If yes, please specify if you are employed or self-employed?
# #     6. How much do you earn per year, gross pay before tax and NI, including any commission, bonus, overtime, and other income sources?
# #     7. Please can you tell me if you have any credit commitments, if yes please list them?
# #     8. How many dependents do you have, if any?
# #     9. If you have adverse credit, please tell me what it is?
# #     10. Do you have an existing property that you plan to sell to support your new mortgage?
# #     11. What is your committed expenditure? (e.g., maintenance, school fees, nursery costs)
    
# #     Generate only one relevant question at a time based on the context of previous responses.
# #     """
# # )

# # # Create LLMChain for question generation
# # llm_question_chain = question_generation_prompt | llm

# # # Step 6: User interaction
# # print("Welcome! How can I assist you today?")

# # chat_active = True
# # mortgage_interest_detected = False
# # user_data = {}
# # last_message = ""

# # while chat_active:
# #     user_input = input("Your message: ")
    
# #     if user_input == last_message:
# #         continue  # Prevent duplicate messages
# #     last_message = user_input
    
# #     if "mortgage" in user_input.lower() and not mortgage_interest_detected:
# #         print("Sure! Buying a mortgage involves multiple steps, such as checking your credit score, finding the right lender, and choosing a mortgage type. Let's go through the process step by step.")
# #         mortgage_interest_detected = True
    
# #     elif mortgage_interest_detected:
# #         generated_question = llm_question_chain.invoke(user_data)
# #         question_text = generated_question.content.strip()
# #         print(question_text)
# #         answer = input()
# #         if answer.strip():
# #             user_data[question_text] = answer
# #         else:
# #             print("I understand that this might be confusing. Let me clarify before we move forward.")
# #     else:
# #         if "how are you" in user_input.lower():
# #             print("AI: I'm doing great! Thanks for asking. How about you?")
# #         else:
# #             response = llm.invoke(user_input)
# #             print("AI:", response.content)
    
# #     if user_input.lower() in ["exit", "quit", "close"]:
# #         chat_active = False
# #         print("Thank you for chatting! Feel free to return anytime.")









# import os
# import openai
# import pdfplumber
# from dotenv import load_dotenv
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQA
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()
# os.environ.setdefault("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Ensure OpenAI API Key is set
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Step 1: Load Mortgage Knowledge Base (PDF + Websites)
# urls = [
#     "https://money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage-explained"
# ]

# # Extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""  # Avoid NoneType errors
#     return text

# pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Scrape data from websites
# docs = []
# for url in urls:
#     loader = WebBaseLoader(url)
#     documents = loader.load()
#     for doc in documents:
#         if isinstance(doc, dict) and 'page_content' in doc:
#             docs.append(doc['page_content'])

# # Combine web scraped data and PDF data
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Step 2: Vector Database for Information Retrieval
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Step 3: Define Mortgage Questions
# mortgage_questions = [
#     "Is this a single person application or are you in a partnership? (Married, Civil Partnership, Living Together)",
#     "Are you a first-time buyer?",
#     "Please can you give me your date of birth and your partner's, if applicable?",
#     "Are you in employment?",
#     "If yes, please specify if you are employed or self-employed?",
#     "How much do you earn per year, gross pay before tax and NI, including any commission, bonus, overtime, and other income sources?",
#     "Please can you tell me if you have any credit commitments, if yes please list them?",
#     "How many dependents do you have, if any?",
#     "If you have adverse credit, please tell me what it is?",
#     "Do you have an existing property that you plan to sell to support your new mortgage?",
#     "What is your committed expenditure? (e.g., maintenance, school fees, nursery costs)"
# ]

# # Step 4: Initialize Chat LLM
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=2500, top_p=0.9)

# # Step 5: Define a Retrieval-based Question Answering Chain
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm, retriever=retriever, return_source_documents=True
# )

# # Step 6: User Interaction Loop
# print("Welcome! How can I assist you today?")

# chat_active = True
# mortgage_interest_detected = False
# user_data = {}  # Store user responses
# current_question_index = 0  # Track the current mortgage question
# awaiting_clarification = False  # Handle clarification

# while chat_active:
#     user_input = input("Your message: ").strip().lower()

#     # Ignore empty messages
#     if not user_input:
#         continue

#     # Exit condition
#     if user_input in ["exit", "quit", "close"]:
#         chat_active = False
#         print("\nThank you for chatting! Feel free to return anytime.")
#         break

#     # Detect mortgage interest and start the process
#     if "mortgage" in user_input and not mortgage_interest_detected:
#         print("\nSure! Buying a mortgage involves multiple steps, such as checking your credit score, finding the right lender, and choosing a mortgage type.")
#         print("Let's go through the process step by step.\n")
#         mortgage_interest_detected = True
#         print(mortgage_questions[current_question_index])  # Ask first question
#         continue

#     # Handle "I don't understand" cases
#     if awaiting_clarification:
#         print("\nI understand. Let me clarify:")
#         clarification_response = qa_chain.run(mortgage_questions[current_question_index])
#         print(clarification_response)  # Provide an answer from knowledge base
#         print("\n" + mortgage_questions[current_question_index])  # Re-ask the same question
#         awaiting_clarification = False  # Reset clarification flag
#         continue

#     # Mortgage Q&A Flow
#     if mortgage_interest_detected:
#         if user_input in ["i don't understand", "can you clarify?", "explain"]:
#             awaiting_clarification = True  # Flag that clarification is needed
#             continue

#         # Store user response
#         user_data[mortgage_questions[current_question_index]] = user_input

#         # Move to the next question
#         current_question_index += 1

#         # If there are more questions, ask the next one
#         if current_question_index < len(mortgage_questions):
#             print("\n" + mortgage_questions[current_question_index])
#         else:
#             print("\nThank you! I have all the necessary mortgage information. Let me process this and provide insights.")
#             mortgage_interest_detected = False  # End mortgage questioning
#         continue

#     # Use AI + Knowledge Base to answer other mortgage-related queries
#     response = qa_chain.run(user_input)
#     print("AI:", response)






