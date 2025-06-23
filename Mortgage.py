# # import pdfplumber
# # from langchain_community.document_loaders import WebBaseLoader
# # from langchain_community.vectorstores import FAISS
# # from langchain_openai import OpenAIEmbeddings  # Import OpenAIEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain.chains import LLMChain
# # from langchain.prompts import ChatPromptTemplate  # Use ChatPromptTemplate
# # from langchain_openai import ChatOpenAI
# # from langchain.agents import initialize_agent, AgentType
# # from langchain.tools import Tool
# # from langchain_core.documents import Document

# # import os
# # from dotenv import load_dotenv
# # load_dotenv()

# # # Set environment variables
# # os.environ["USER_AGENT"] = "MyMortgageBot/1.0"
# # os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # # Step 1: Define the web scraping and PDF data loading (Mortgage-specific content)
# # urls = [
# #     "https://askaboutmortgages.co.uk/",
# #     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
# #     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
# #     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
# #     "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
# #     "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
# #     "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
# #     "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
# #     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
# #     "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
# # ]

# # # Step 2: Use pdfplumber to load PDF file data
# # def extract_text_from_pdf(pdf_path):
# #     text = ""
# #     with pdfplumber.open(pdf_path) as pdf:
# #         for page in pdf.pages:
# #             text += page.extract_text() or ""  # Ensure text extraction even if some pages are empty
# #     return text.strip()  # Remove any extra spaces

# # # Path to the uploaded PDF file
# # pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# # pdf_docs_text = extract_text_from_pdf(pdf_path)

# # # Scraping data from the websites
# # docs = []
# # for url in urls:
# #     loader = WebBaseLoader(url)
# #     documents = loader.load()
# #     for doc in documents:
# #         if isinstance(doc, dict) and 'page_content' in doc:
# #             docs.append(doc['page_content'])

# # # Combine web scraped data and PDF data (from pdfplumber)
# # all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # # Step 3: Split the documents into chunks using RecursiveCharacterTextSplitter
# # documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)

# # # Step 4: Use OpenAI Embeddings to convert documents into vectors
# # vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# # retriever = vectordb.as_retriever()

# # # Define a custom retriever tool to fetch mortgage-related info
# # def retriever_tool(query: str) -> str:
# #     return f"Retrieved mortgage-related information for: {query}"

# # retriever_tool = Tool(
# #     name="Mortgage Information Retriever",
# #     func=retriever_tool,
# #     description="Useful for retrieving mortgage-related information."
# # )

# # # Step 5: Set up the LLM chain for personalized responses based on user inputs
# # llm = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=1000)# Increased max_tokens for detailed response

# # summary_prompt = ChatPromptTemplate.from_template(
# #     """
# #     🌟 **Personalized Mortgage Summary for {user_name}** 🌟

# #     Dear {user_name},

# #     Thank you for providing your mortgage details! Below is a **detailed** recommendation tailored to your requirements.

# #     ### **🏡 Loan Information:**
# #     - **Purpose:** {purpose}
# #     - **Credit Score:** {credit_score} ⭐
# #     - **Loan Amount:** ${loan_amount}
# #     - **Loan Term:** {loan_term} years 📆
# #     - **Interest Rate Type:** {interest_rate} 🔄
# #     - **Down Payment:** ${down_payment} 💰

# #     ### **🔍 Expert Recommendation:**
# #     Considering your **loan term** and **interest rate type**, I suggest the following options:

# #     **1️⃣ Best Loan Option:** Based on your details, a **{interest_rate}-rate mortgage** is suitable for you.
# #     **2️⃣ Potential Risks:** Since your **down payment is ${down_payment}**, you may require **Private Mortgage Insurance (PMI)**.
# #     **3️⃣ Financial Tips:** If you increase your down payment, you may qualify for **lower interest rates**.

# #     ### **📢 Next Steps:**
# #     - ✅ Speak with a mortgage advisor to discuss **pre-approval options**.
# #     - 📊 Use an **online mortgage calculator** to estimate your **monthly payments**.
# #     - 💡 Improve your **credit score** for better mortgage deals.

# #     Let me know if you need any further information.

# #     **Would you like to proceed with this mortgage option? (Yes/No)** ✨
# #     """
# # )



# # # Create LLMChain using GPT-4 and the defined summary prompt
# # llm_summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# # # Step 6: Example use case - Mortgage-related user interaction
# # print("Welcome to our mortgage assistant service! I’m here to help with your mortgage questions.")
# # user_name = input("May I know your name to make this conversation more personal? ")

# # # Collect user inputs
# # print(f"Hello {user_name}, let’s get started! What is the purpose of your mortgage?")
# # purpose = input("Your response: ")

# # print("Got it! Now, could you share your credit score range? (e.g., Excellent, Good, Fair)")
# # credit_score = input("Your response: ")

# # print("What’s your estimated budget or loan amount?")
# # loan_amount = input("Your response: ")

# # print("How long do you plan to take the loan for? (15, 20, 30 years)")
# # loan_term = input("Your response: ")

# # print("Do you prefer a fixed or adjustable interest rate?")
# # interest_rate = input("Your response: ")

# # print("How much down payment can you afford?")
# # down_payment = input("Your response: ")

# # generated_summary = llm_summary_chain.invoke({
# #     "user_name": user_name,
# #     "purpose": purpose,
# #     "credit_score": credit_score,
# #     "loan_amount": loan_amount,
# #     "loan_term": loan_term,
# #     "interest_rate": interest_rate,
# #     "down_payment": down_payment
# # })

# # # ✅ আউটপুট থেকে সঠিক টেক্সট বের করা
# # if isinstance(generated_summary, dict):
# #     mortgage_summary_text = generated_summary.get("text") or generated_summary.get("content") or str(generated_summary)
# # else:
# #     mortgage_summary_text = str(generated_summary)

# # print("\nGenerated Mortgage Summary:")
# # print(mortgage_summary_text)  # ✅ এখন সম্পূর্ণ বিস্তারিত সারাংশ দেখাবে


# # # ✅ সঠিকভাবে "text" বা "content" ফিল্ড থেকে ডাটা বের করুন
# # if isinstance(generated_summary, dict):
# #     mortgage_summary_text = generated_summary.get("text") or generated_summary.get("content") or str(generated_summary)
# # else:
# #     mortgage_summary_text = str(generated_summary)

# # print("\nGenerated Mortgage Summary:")
# # print(mortgage_summary_text)  # ✅ এখন সঠিক সারাংশ দেখাবে


# # # Step 8: Ask if the user is interested in this mortgage option
# # interest = input("\nAre you interested in this mortgage option? (Yes/No) ")

# # if interest.lower() == "yes":
# #     print("Thank you! I will now send your details to a human mortgage advisor.")
# # else:
# #     print("Thank you for your time. Feel free to reach out if you have more questions!")










# import pdfplumber
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings  # Import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate  # Use ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.agents import initialize_agent, AgentType
# from langchain.tools import Tool
# from langchain_core.documents import Document

# import os
# from dotenv import load_dotenv
# load_dotenv()

# os.environ["USER_AGENT"] = "MyMortgageBot/1.0"


# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Step 1: Define the web scraping and PDF data loading (Mortgage-specific content)
# urls = [
#     "https://askaboutmortgages.co.uk/",
#     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#     "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
# ]

# # Step 2: Use pdfplumber to load PDF file data
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# # Path to the uploaded PDF file
# pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Scraping data from the websites
# docs = []
# for url in urls:
#     loader = WebBaseLoader(url)
#     documents = loader.load()
#     for doc in documents:
#         if isinstance(doc, dict) and 'page_content' in doc:
#             docs.append(doc['page_content'])

# # Combine web scraped data and PDF data (from pdfplumber)
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Step 3: Split the documents into chunks using RecursiveCharacterTextSplitter
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)

# # Step 4: Use OpenAI Embeddings to convert documents into vectors
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define a custom retriever tool to fetch mortgage-related info
# def retriever_tool(query: str) -> str:
#     return f"Retrieved mortgage-related information for: {query}"

# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=retriever_tool,
#     description="Useful for retrieving mortgage-related information."
# )

# # Step 5: Set up the LLM chain for personalized responses based on user inputs
# llm = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=1000)  # Fix this line


# # Define the prompt template for personalized mortgage responses
# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     Here is a summary for {user_name} regarding their mortgage inquiry:
#     - Purpose: {purpose}
#     - Credit Score: {credit_score}
#     - Estimated Loan Amount: {loan_amount}
#     - Loan Term: {loan_term} years
#     - Interest Rate: {interest_rate}
#     - Down Payment: {down_payment}

#     Based on this information, please provide a personalized recommendation from the available mortgage options.
#     """
# )

# # Create LLMChain using GPT-4 and the defined summary prompt
# llm_summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# # Step 6: Example use case - Mortgage-related user interaction
# print("Welcome to our mortgage assistant service! I’m here to help with your mortgage questions.")
# user_name = input("May I know your name to make this conversation more personal? ")

# # Collect user inputs
# print(f"Hello {user_name}, let’s get started! What is the purpose of your mortgage?")
# purpose = input("Your response: ")

# print("Got it! Now, could you share your credit score range? (e.g., Excellent, Good, Fair)")
# credit_score = input("Your response: ")

# print("What’s your estimated budget or loan amount?")
# loan_amount = input("Your response: ")

# print("How long do you plan to take the loan for? (15, 20, 30 years)")
# loan_term = input("Your response: ")

# print("Do you prefer a fixed or adjustable interest rate?")
# interest_rate = input("Your response: ")

# print("How much down payment can you afford?")
# down_payment = input("Your response: ")

# # Step 7: Generate the personalized summary using LLMChain
# generated_summary = llm_summary_chain.invoke({
#     "user_name": user_name,
#     "purpose": purpose,
#     "credit_score": credit_score,
#     "loan_amount": loan_amount,
#     "loan_term": loan_term,
#     "interest_rate": interest_rate,
#     "down_payment": down_payment
# })


# print("\nGenerated Mortgage Summary:")
# print(generated_summary)

# # Step 8: Ask if the user is interested in this mortgage option
# interest = input("\nAre you interested in this mortgage option? (Yes/No) ")

# if interest.lower() == "yes":
#     print("Thank you! I will now send your details to a human mortgage advisor.")
# else:
#     print("Thank you for your time. Feel free to reach out if you have more questions!")



# import pdfplumber
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings  # Import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate  # Use ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.agents import initialize_agent, AgentType
# from langchain.tools import Tool
# from langchain_core.documents import Document

# import os
# from dotenv import load_dotenv
# load_dotenv()

# # Set environment variables
# os.environ["USER_AGENT"] = "MyMortgageBot/1.0"
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Step 1: Define the web scraping and PDF data loading (Mortgage-specific content)
# urls = [
#     "https://askaboutmortgages.co.uk/",
#     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#     "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
# ]

# # Step 2: Use pdfplumber to load PDF file data
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""  # Ensure text extraction even if some pages are empty
#     return text.strip()  # Remove any extra spaces

# # Path to the uploaded PDF file
# pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Scraping data from the websites
# docs = []
# for url in urls:
#     loader = WebBaseLoader(url)
#     documents = loader.load()
#     for doc in documents:
#         if isinstance(doc, dict) and 'page_content' in doc:
#             docs.append(doc['page_content'])

# # Combine web scraped data and PDF data (from pdfplumber)
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Step 3: Split the documents into chunks using RecursiveCharacterTextSplitter
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)

# # Step 4: Use OpenAI Embeddings to convert documents into vectors
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define a custom retriever tool to fetch mortgage-related info
# def retriever_tool(query: str) -> str:
#     return f"Retrieved mortgage-related information for: {query}"

# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=retriever_tool,
#     description="Useful for retrieving mortgage-related information."
# )

# # Step 5: Set up the LLM chain for personalized responses based on user inputs
# llm = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=1000)# Increased max_tokens for detailed response

# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     🌟 **Personalized Mortgage Summary for {user_name}** 🌟

#     Dear {user_name},

#     Thank you for providing your mortgage details! Below is a **detailed** recommendation tailored to your requirements.

#     ### **🏡 Loan Information:**
#     - **Purpose:** {purpose}
#     - **Credit Score:** {credit_score} ⭐
#     - **Loan Amount:** ${loan_amount}
#     - **Loan Term:** {loan_term} years 📆
#     - **Interest Rate Type:** {interest_rate} 🔄
#     - **Down Payment:** ${down_payment} 💰

#     ### **🔍 Expert Recommendation:**
#     Considering your **loan term** and **interest rate type**, I suggest the following options:

#     **1️⃣ Best Loan Option:** Based on your details, a **{interest_rate}-rate mortgage** is suitable for you.
#     **2️⃣ Potential Risks:** Since your **down payment is ${down_payment}**, you may require **Private Mortgage Insurance (PMI)**.
#     **3️⃣ Financial Tips:** If you increase your down payment, you may qualify for **lower interest rates**.

#     ### **📢 Next Steps:**
#     - ✅ Speak with a mortgage advisor to discuss **pre-approval options**.
#     - 📊 Use an **online mortgage calculator** to estimate your **monthly payments**.
#     - 💡 Improve your **credit score** for better mortgage deals.

#     Let me know if you need any further information.

#     **Would you like to proceed with this mortgage option? (Yes/No)** ✨
#     """
# )



# # Create LLMChain using GPT-4 and the defined summary prompt
# llm_summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# # Step 6: Example use case - Mortgage-related user interaction
# print("Welcome to our mortgage assistant service! I’m here to help with your mortgage questions.")
# user_name = input("May I know your name to make this conversation more personal? ")

# # Collect user inputs
# print(f"Hello {user_name}, let’s get started! What is the purpose of your mortgage?")
# purpose = input("Your response: ")

# print("Got it! Now, could you share your credit score range? (e.g., Excellent, Good, Fair)")
# credit_score = input("Your response: ")

# print("What’s your estimated budget or loan amount?")
# loan_amount = input("Your response: ")

# print("How long do you plan to take the loan for? (15, 20, 30 years)")
# loan_term = input("Your response: ")

# print("Do you prefer a fixed or adjustable interest rate?")
# interest_rate = input("Your response: ")

# print("How much down payment can you afford?")
# down_payment = input("Your response: ")

# generated_summary = llm_summary_chain.invoke({
#     "user_name": user_name,
#     "purpose": purpose,
#     "credit_score": credit_score,
#     "loan_amount": loan_amount,
#     "loan_term": loan_term,
#     "interest_rate": interest_rate,
#     "down_payment": down_payment
# })

# # ✅ আউটপুট থেকে সঠিক টেক্সট বের করা
# if isinstance(generated_summary, dict):
#     mortgage_summary_text = generated_summary.get("text") or generated_summary.get("content") or str(generated_summary)
# else:
#     mortgage_summary_text = str(generated_summary)

# print("\nGenerated Mortgage Summary:")
# print(mortgage_summary_text)  # ✅ এখন সম্পূর্ণ বিস্তারিত সারাংশ দেখাবে


# # ✅ সঠিকভাবে "text" বা "content" ফিল্ড থেকে ডাটা বের করুন
# if isinstance(generated_summary, dict):
#     mortgage_summary_text = generated_summary.get("text") or generated_summary.get("content") or str(generated_summary)
# else:
#     mortgage_summary_text = str(generated_summary)

# print("\nGenerated Mortgage Summary:")
# print(mortgage_summary_text)  # ✅ এখন সঠিক সারাংশ দেখাবে


# # Step 8: Ask if the user is interested in this mortgage option
# interest = input("\nAre you interested in this mortgage option? (Yes/No) ")

# if interest.lower() == "yes":
#     print("Thank you! I will now send your details to a human mortgage advisor.")
# else:
#     print("Thank you for your time. Feel free to reach out if you have more questions!")








# import pdfplumber
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings  # Import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate  # Use ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.agents import initialize_agent, AgentType
# from langchain.tools import Tool
# from langchain_core.documents import Document

# import os
# from dotenv import load_dotenv
# load_dotenv()

# os.environ.setdefault("USER_AGENT", "MyMortgageBot/1.0")


# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Step 1: Define the web scraping and PDF data loading (Mortgage-specific content)
# urls = [
#     "https://askaboutmortgages.co.uk/",
#     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#     "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
# ]

# # Step 2: Use pdfplumber to load PDF file data
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# # Path to the uploaded PDF file
# pdf_path = "C:/KFV/AI Mortgage Advisor Project-12345.pdf"
# pdf_docs_text = extract_text_from_pdf(pdf_path)

# # Scraping data from the websites
# docs = []
# for url in urls:
#     loader = WebBaseLoader(url)
#     documents = loader.load()
#     for doc in documents:
#         if isinstance(doc, dict) and 'page_content' in doc:
#             docs.append(doc['page_content'])

# # Combine web scraped data and PDF data (from pdfplumber)
# all_docs = [Document(page_content=doc) for doc in docs] + [Document(page_content=pdf_docs_text)]

# # Step 3: Split the documents into chunks using RecursiveCharacterTextSplitter
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)

# # Step 4: Use OpenAI Embeddings to convert documents into vectors
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define a custom retriever tool to fetch mortgage-related info
# def retriever_tool(query: str) -> str:
#     return f"Retrieved mortgage-related information for: {query}"

# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=retriever_tool,
#     description="Useful for retrieving mortgage-related information."
# )

# # Step 5: Set up the LLM chain for personalized responses based on user inputs
# llm = ChatOpenAI(model="gpt-4", temperature=0.5, max_tokens=1000)  # Fix this line


# # Define the prompt template for personalized mortgage responses
# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     Here is a summary for {user_name} regarding their mortgage inquiry:
#     - Purpose: {purpose}
#     - Credit Score: {credit_score}
#     - Estimated Loan Amount: {loan_amount}
#     - Loan Term: {loan_term} years
#     - Interest Rate: {interest_rate}
#     - Down Payment: {down_payment}

#     Based on this information, please provide a personalized recommendation from the available mortgage options.
#     """
# )

# # Create LLMChain using GPT-4 and the defined summary prompt
# llm_summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# # Step 6: Example use case - Mortgage-related user interaction
# print("Welcome to our mortgage assistant service! I’m here to help with your mortgage questions.")
# user_name = input("May I know your name to make this conversation more personal? ")

# # Collect user inputs
# print(f"Hello {user_name}, let’s get started! What is the purpose of your mortgage?")
# purpose = input("Your response: ")

# print("Got it! Now, could you share your credit score range? (e.g., Excellent, Good, Fair)")
# credit_score = input("Your response: ")

# print("What’s your estimated budget or loan amount?")
# loan_amount = input("Your response: ")

# print("How long do you plan to take the loan for? (15, 20, 30 years)")
# loan_term = input("Your response: ")

# print("Do you prefer a fixed or adjustable interest rate?")
# interest_rate = input("Your response: ")

# print("How much down payment can you afford?")
# down_payment = input("Your response: ")

# # Step 7: Generate the personalized summary using LLMChain
# generated_summary = llm_summary_chain.invoke({
#     "user_name": user_name,
#     "purpose": purpose,
#     "credit_score": credit_score,
#     "loan_amount": loan_amount,
#     "loan_term": loan_term,
#     "interest_rate": interest_rate,
#     "down_payment": down_payment
# })


# print("\nGenerated Mortgage Summary:")
# print(generated_summary)

# # Step 8: Ask if the user is interested in this mortgage option
# interest = input("\nAre you interested in this mortgage option? (Yes/No) ")

# if interest.lower() == "yes":
#     print("Thank you! I will now send your details to a human mortgage advisor.")
# else:
#     print("Thank you for your time. Feel free to reach out if you have more questions!")






# import pdfplumber
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.tools import Tool
# from langchain_core.documents import Document

# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# os.environ.setdefault("USER_AGENT", "MyMortgageBot/1.0")
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# # Step 1: Define the web scraping and PDF data loading
# urls = [
#     "https://askaboutmortgages.co.uk/",
#     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#     "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
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
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=1.0, max_tokens=2500, top_p=0.9)

# # Define the prompt template
# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     Here is a summary for {user_name} regarding their mortgage inquiry:
#     - Purpose: {purpose}
#     - Credit Score: {credit_score}
#     - Estimated Loan Amount: {loan_amount}
#     - Loan Term: {loan_term} years
#     - Interest Rate: {interest_rate}
#     - Down Payment: {down_payment}

#     Based on this information, please provide a personalized recommendation from the available mortgage options.
#     """
# )

# # Create LLMChain
# llm_summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# # Step 6: User interaction
# print("Welcome to our mortgage assistant service! I’m here to help with your mortgage questions.")
# user_name = input("May I know your name to make this conversation more personal? ")

# print(f"Hello {user_name}, let’s get started! What is the purpose of your mortgage?")
# purpose = input("Your response: ")

# print("Got it! Now, could you share your credit score range? (e.g., Excellent, Good, Fair)")
# credit_score = input("Your response: ")

# print("What’s your estimated budget or loan amount?")
# loan_amount = input("Your response: ")

# print("How long do you plan to take the loan for? (15, 20, 30 years)")
# loan_term = input("Your response: ")

# print("Do you prefer a fixed or adjustable interest rate?")
# interest_rate = input("Your response: ")

# print("How much down payment can you afford?")
# down_payment = input("Your response: ")

# # Step 7: Generate the mortgage summary
# generated_summary = llm_summary_chain.invoke({
#     "user_name": user_name,
#     "purpose": purpose,
#     "credit_score": credit_score,
#     "loan_amount": loan_amount,
#     "loan_term": loan_term,
#     "interest_rate": interest_rate,
#     "down_payment": down_payment
# })

# # Extract only the necessary text and clean it
# summary_text = generated_summary["text"]
# clean_summary = summary_text.replace("\n\n", " ")

# # Display the cleaned mortgage summary
# print("\nGenerated Mortgage Summary:")
# print(clean_summary)

# # Step 8: Ask if the user is interested in the mortgage option
# interest = input("\nAre you interested in this mortgage option? (Yes/No) ")

# if interest.lower() == "yes":
#     print("Thank you! I will now send your details to a human mortgage advisor.")
# else:
#     print("Thank you for your time. Feel free to reach out if you have more questions!")








# import os
# from dotenv import load_dotenv
# from playwright.sync_api import sync_playwright
# import requests
# from bs4 import BeautifulSoup
# import pdfplumber
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_core.documents import Document
# from langchain.tools import Tool

# # Step 1: Load environment variables
# load_dotenv()

# # Ensure USER_AGENT is set properly
# os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "MyMortgageBot/1.0")

# # Debugging: Check if USER_AGENT is set correctly
# #print(f"User-Agent Set: {os.environ.get('USER_AGENT')}")

# # Step 2: Define the web scraping URLs
# urls = [
#     "https://askaboutmortgages.co.uk/",
#     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#     "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#     "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#     "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#     "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#     "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
# ]

# # Step 3: Function to scrape websites using Playwright (for JavaScript rendering)
# def scrape_with_playwright(url):
#     """ Scrape JavaScript-heavy websites using Playwright """
#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=True)
#             page = browser.new_page()
#             page.set_extra_http_headers({"User-Agent": os.getenv("USER_AGENT")})
#             page.goto(url, timeout=60000)  # 60 seconds timeout
#             page.wait_for_load_state("networkidle")
#             content = page.content()
#             browser.close()
#             return content
#     except Exception as e:
#         print(f"Error loading {url} with Playwright: {e}")
#         return None

# # Step 4: Function to scrape websites using requests (for simple websites)
# def scrape_with_requests(url):
#     """ Fetch content from a website using requests and BeautifulSoup """
#     headers = {"User-Agent": os.getenv("USER_AGENT")}
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
#             return soup.get_text()
#         else:
#             print(f"Failed to fetch {url}, Status Code: {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"Error loading {url} with requests: {e}")
#         return None

# # Step 5: Scrape all URLs using Playwright first, then fallback to requests
# docs = []

# for url in urls:
#     #print(f"Scraping {url}...")
    
#     # Try Playwright first for JavaScript-heavy websites
#     content = scrape_with_playwright(url)
    
#     # If Playwright fails, fallback to requests
#     if not content:
#         print(f"Falling back to requests for {url}...")
#         content = scrape_with_requests(url)
    
#     # Append scraped content
#     if content:
#         docs.append(Document(page_content=content[:1000]))  # Store first 1000 characters only for preview

# # Step 6: Extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 text += page.extract_text() or ""  # Avoid NoneType error
#     except Exception as e:
#         print(f"Error opening PDF: {e}")
#     return text

# # Path to the uploaded PDF file
# pdf_path = "C:\KFV\AI Mortgage Advisor Project-12345.pdf"

# # Check if the file exists
# if os.path.exists(pdf_path):
#     pdf_docs_text = extract_text_from_pdf(pdf_path)
#     docs.append(Document(page_content=pdf_docs_text))  # Append extracted text from PDF
# else:
#     print(f"Warning: PDF file not found at {pdf_path}")

# # Step 7: Split the documents into chunks
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

# # Step 8: Use OpenAI Embeddings to convert documents into vectors
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# # Define a custom retriever tool
# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: f"Retrieved mortgage-related information for: {query}",
#     description="Useful for retrieving mortgage-related information."
# )

# # Step 9: Set up the LLM chain for personalized responses
# llm = ChatOpenAI(model="gpt-4", temperature=1.0, max_tokens=2500, top_p=0.9)

# # Define the prompt template
# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     Here is a summary for {user_name} regarding their mortgage inquiry:
#     - Purpose: {purpose}
#     - Credit Score: {credit_score}
#     - Estimated Loan Amount: {loan_amount}
#     - Loan Term: {loan_term} years
#     - Interest Rate: {interest_rate}
#     - Down Payment: {down_payment}

#     Based on this information, please provide a personalized recommendation from the available mortgage options.
#     """
# )

# # Create LLMChain
# llm_summary_chain = summary_prompt | llm

# # Step 10: User interaction
# print("Welcome to our mortgage assistant service! I’m here to help with your mortgage questions.")
# user_name = input("May I know your name to make this conversation more personal? ")

# print(f"Hello {user_name}, let’s get started! What is the purpose of your mortgage?")
# purpose = input("Your response: ")

# print("Got it! Now, could you share your credit score range? (e.g., Excellent, Good, Fair)")
# credit_score = input("Your response: ")

# print("What’s your estimated budget or loan amount?")
# loan_amount = input("Your response: ")

# print("How long do you plan to take the loan for? (15, 20, 30 years)")
# loan_term = input("Your response: ")

# print("Do you prefer a fixed or adjustable interest rate?")
# interest_rate = input("Your response: ")

# print("How much down payment can you afford?")
# down_payment = input("Your response: ")

# # Step 11: Generate the mortgage summary
# generated_summary = llm_summary_chain.invoke({
#     "user_name": user_name,
#     "purpose": purpose,
#     "credit_score": credit_score,
#     "loan_amount": loan_amount,
#     "loan_term": loan_term,
#     "interest_rate": interest_rate,
#     "down_payment": down_payment
# })

# # Extract only the necessary text and clean it
# summary_text = generated_summary.content
# clean_summary = summary_text.replace("\n\n", " ")

# # Display the cleaned mortgage summary
# print("\nGenerated Mortgage Summary:")
# print(clean_summary)

# # Step 12: Ask if the user is interested in the mortgage option
# interest = input("\nAre you interested in this mortgage option? (Yes/No) ")

# if interest.lower() == "yes":
#     print("Thank you! I will now send your details to a human mortgage advisor.")
# else:
#     print("Thank you for your time. Feel free to reach out if you have more questions!")







# import os
# import asyncio
# import logging
# from dotenv import load_dotenv
# from playwright.async_api import async_playwright
# import aiohttp
# from bs4 import BeautifulSoup
# import pdfplumber
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_core.documents import Document
# from langchain.tools import Tool

# # Load environment variables
# load_dotenv()
# USER_AGENT = os.getenv("USER_AGENT", "MyMortgageBot/1.0")

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # URLs to scrape
# urls = [
#     "https://askaboutmortgages.co.uk/",
#     "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#     "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#     "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
# ]

# async def scrape_with_playwright(url):
#     """Scrape JavaScript-heavy websites using Playwright (async)."""
#     try:
#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=True)
#             page = await browser.new_page()
#             await page.set_extra_http_headers({"User-Agent": USER_AGENT})
#             await page.goto(url, timeout=60000)
#             await page.wait_for_load_state("networkidle")
#             content = await page.content()
#             await browser.close()
#             return content
#     except Exception as e:
#         logging.error(f"Playwright Error loading {url}: {e}")
#         return None

# async def scrape_with_aiohttp(url):
#     """Scrape simple websites using aiohttp and BeautifulSoup."""
#     headers = {"User-Agent": USER_AGENT}
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=headers, timeout=10) as response:
#                 if response.status == 200:
#                     text = await response.text()
#                     soup = BeautifulSoup(text, "html.parser")
#                     return soup.get_text()
#                 else:
#                     logging.warning(f"Failed to fetch {url}, Status Code: {response.status}")
#                     return None
#     except Exception as e:
#         logging.error(f"Aiohttp Error loading {url}: {e}")
#         return None

# async def scrape_all_urls():
#     """Scrape all URLs concurrently."""
#     tasks = [scrape_with_playwright(url) for url in urls]
#     results = await asyncio.gather(*tasks)
#     return [Document(page_content=res[:1000]) for res in results if res]

# def extract_text_from_pdf(pdf_path):
#     """Extract text from a PDF file."""
#     text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 text += page.extract_text() or ""
#     except Exception as e:
#         logging.error(f"Error opening PDF: {e}")
#     return text

# # Dynamically handle PDF path
# pdf_path = os.path.join("C:\KFV\AI Mortgage Advisor Project-12345.pdf")
# if os.path.exists(pdf_path):
#     pdf_text = extract_text_from_pdf(pdf_path)
#     pdf_doc = Document(page_content=pdf_text)
# else:
#     logging.warning(f"PDF file not found at {pdf_path}")
#     pdf_doc = None

# # Run scraping
# docs = asyncio.run(scrape_all_urls())
# if pdf_doc:
#     docs.append(pdf_doc)

# # Split documents into smaller chunks
# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = splitter.split_documents(docs)

# # Convert to vector embeddings
# vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
# retriever = vectordb.as_retriever()

# retriever_tool = Tool(
#     name="Mortgage Information Retriever",
#     func=lambda query: f"Retrieved mortgage-related information for: {query}",
#     description="Useful for retrieving mortgage-related information."
# )

# # LLM setup
# llm = ChatOpenAI(model="gpt-4", temperature=1.0, max_tokens=2500, top_p=0.9)
# summary_prompt = ChatPromptTemplate.from_template(
#     """
#     Here is a summary for {user_name} regarding their mortgage inquiry:
#     - Purpose: {purpose}
#     - Credit Score: {credit_score}
#     - Estimated Loan Amount: {loan_amount}
#     - Loan Term: {loan_term} years
#     - Interest Rate: {interest_rate}
#     - Down Payment: {down_payment}
    
#     Based on this information, please provide a personalized recommendation.
#     """
# )
# llm_summary_chain = summary_prompt | llm

# def get_user_input():
#     """Securely get and validate user input."""
#     user_name = input("May I know your name? ").strip()
#     purpose = input("What is the purpose of your mortgage? ").strip()
#     credit_score = input("Your credit score range? (Excellent, Good, Fair) ").strip()
    
#     while True:
#         try:
#             loan_amount = float(input("Estimated loan amount: "))
#             if loan_amount > 0:
#                 break
#             else:
#                 print("Please enter a valid loan amount.")
#         except ValueError:
#             print("Invalid number. Please enter a valid amount.")
    
#     loan_term = input("Loan term (15, 20, 30 years): ").strip()
#     interest_rate = input("Fixed or adjustable interest rate? ").strip()
#     down_payment = input("Down payment amount: ").strip()
    
#     return {
#         "user_name": user_name,
#         "purpose": purpose,
#         "credit_score": credit_score,
#         "loan_amount": loan_amount,
#         "loan_term": loan_term,
#         "interest_rate": interest_rate,
#         "down_payment": down_payment,
#     }

# # Generate mortgage summary
# user_data = get_user_input()
# generated_summary = llm_summary_chain.invoke(user_data)

# # Display final output
# print("\nGenerated Mortgage Summary:")
# print(generated_summary.content.replace("\n\n", " "))

# interest = input("\nAre you interested in this mortgage option? (Yes/No) ")
# if interest.lower() == "yes":
#     print("Thank you! A human mortgage advisor will contact you.")
# else:
#     print("Thank you! Feel free to ask more questions.")

