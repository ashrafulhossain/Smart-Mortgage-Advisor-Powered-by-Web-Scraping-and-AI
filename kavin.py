# import os
# import pdfplumber
# import requests
# import time
# import json
# from dataclasses import dataclass, asdict
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# import cloudscraper
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from langchain.schema import HumanMessage

# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# @dataclass
# class MortgageApplicantInfo:
#     application_type: str = None
#     first_time_buyer: str = None
#     dob: str = None
#     employment_status: str = None
#     employment_type: str = None
#     income: str = None
#     credit_commitments: str = None
#     dependants: str = None
#     adverse_credit: str = None
#     property_sale_info: str = None
#     expenditure: str = None
#     email: str = None
#     phone_number: str = None
#     deposit: str = None

# class MortgageAdvisorBot:
#     def __init__(self):
#         self.applicant = MortgageApplicantInfo()
#         self.fields = list(asdict(self.applicant).keys())
#         self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
#         self.chat_memory = []
#         self.is_collecting_info = False
#         self.awaiting_continue_confirmation = False
#         self.asked_fields = set()
#         self.last_asked_field = None
#         self.last_query_type = None

#         self.retriever = self.load_or_create_vectorstore()

#     def load_or_create_vectorstore(self):
#         def extract_text_from_pdf(pdf_path): 
#             if not os.path.exists(pdf_path): return ""
#             text = ""
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     content = page.extract_text()
#                     if content:
#                         text += content + "\n"
#             return text.strip()

#         def scrape(url):
#             try:
#                 scraper = cloudscraper.create_scraper()
#                 headers = {
#                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#                 }
#                 res = scraper.get(url, headers=headers, timeout=10)
#                 print(f"DEBUG: Status code for {url}: {res.status_code}")
#                 if res.status_code == 200:
#                     soup = BeautifulSoup(res.text, "html.parser")
#                     for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
#                         tag.extract()
#                     return soup.get_text(separator=" ", strip=True)
#                 else:
#                     print(f"DEBUG: Failed with status code {res.status_code} for {url}")
#                     return ""
#             except Exception as e:
#                 print(f"DEBUG: Exception for {url}: {str(e)}")
#                 return ""

#         urls = [
#             "https://askaboutmortgages.co.uk/",
#             "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#             "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#             "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#             "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#             "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#             "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#             "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions",
#             "https://www.money.co.uk/mortgages/bank-of-england-base-rate",
#         ]

#         print("\U0001F4DA Building vectorstore...")
#         scraped = []
#         for u in urls:
#             content = scrape(u)
#             if content:
#                 print(f"✅ Scraped: {u}")
#                 scraped.append(Document(page_content=content))
#             else:
#                 print(f"❌ Failed: {u}")

#         pdf_text = extract_text_from_pdf("AI Mortgage Advisor Project-12345.pdf")
#         if pdf_text:
#             scraped.append(Document(page_content=pdf_text))

#         chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(scraped)

#         if os.path.exists("faiss_db"):
#             return FAISS.load_local("faiss_db", OpenAIEmbeddings(), allow_dangerous_deserialization=True).as_retriever(search_kwargs={"k": 3})
#         db = FAISS.from_documents(chunks, OpenAIEmbeddings())
#         db.save_local("faiss_db")
#         return db.as_retriever(search_kwargs={"k": 3})

#     def detect_query_type(self, user_input):
#         if user_input.strip().lower() in ["yes", "no"]:
#             return "application" if self.is_collecting_info else "general"

#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are an intelligent classifier for a mortgage assistant chatbot.

# Classify the following user input into one of these three types:
# - application → if the user is trying to apply or give their personal or financial details.
# - information → if the user is asking about mortgage concepts, terms, policies, or loan types.
# - general → if it's small talk, unrelated, or casual.

# Recent conversation history (for context):
# {recent_history}

# Just return one of: "application", "information", or "general". Respond with only one word.

# User input: "{user_input}"
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         classification = response.content.strip().lower()

#         print(f"DEBUG: Input '{user_input}' classified as: {classification}")
#         return classification if classification in ["application", "information", "general"] else "general"

#     def extract_info(self, user_input):
#         last_question = self.chat_memory[-2]["ai"] if len(self.chat_memory) >= 2 and "ai" in self.chat_memory[-2] else ""
#         prompt = f"""
# You are extracting information for a mortgage application. Based on the previous question and the user's response, identify the relevant field and value. The fields are: {', '.join(self.fields)}.

# Previous question: {last_question}
# Existing info:
# {json.dumps(asdict(self.applicant), indent=2)}

# User response: {user_input}

# If the response is "yes" or "no", translate it to boolean true/false.
# Output a JSON object with exactly two keys: \"field\" and \"value\".
# If no relevant information is found, return {{\"field\": null, \"value\": null}}.
# """
#         try:
#             response = self.llm.invoke([HumanMessage(content=prompt)])
#             parsed = json.loads(response.content.strip())
#             print(f"DEBUG: extract_info output: {parsed}")
#             return parsed.get("field"), parsed.get("value")
#         except:
#             print(f"DEBUG: extract_info failed to parse: {response.content}")
#             return None, None

#     def update_field(self, field, value):
#         if field in self.fields:
#             setattr(self.applicant, field, value)
#             self.asked_fields.add(field)
#             self.last_asked_field = field

#     def calculate_loan_and_property(self, deposit, income):
#         try:
#             deposit = float(deposit.replace("£", "").replace(",", "").strip())
#             income = float(income.replace("£", "").replace(",", "").strip())
#             max_loan = income * 4.5  # 4.5x income as maximum loan
#             max_property_value = max_loan + deposit
#             return max_loan, max_property_value
#         except (ValueError, AttributeError):
#             return None, None

#     def ask_next_question(self):
#         for field in self.fields:
#             if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
#                 self.last_asked_field = field
#                 return self.get_question(field)
#         return self.finalize_lead()

#     def get_question(self, field):
#         questions = {
#             "application_type": "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#             "first_time_buyer": "Are you a first-time buyer?",
#             "dob": "Please can you give me your date of birth and your partner's, if applicable.",
#             "employment_status": "Are you in employment?",
#             "employment_type": "If yes, please specify if you are employed or self-employed?",
#             "income": "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#             "credit_commitments": "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#             "dependants": "How many dependants do you have, if any?",
#             "adverse_credit": "If you have adverse credit, please tell me what it is?",
#             "property_sale_info": "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#             "expenditure": "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs.",
#             "email": "Please provide your email address for future updates.",
#             "phone_number": "Please provide your contact number.",
#             "deposit": "How much is your deposit for the property purchase?"
#         }
#         return questions.get(field, f"Please provide your {field}")

#     def finalize_lead(self):
#         self.save_lead()
#         response = ("Thank you for your response, I will now forward your information to one of our free, "
#                     "CEMAP qualified mortgage advisors who will take over from here. It’s been great speaking "
#                     "with you and good luck with your house buying journey. Goodbye.")
        
#         if self.applicant.income and self.applicant.deposit:
#             max_loan, max_property_value = self.calculate_loan_and_property(self.applicant.deposit, self.applicant.income)
#             if max_loan and max_property_value:
#                 response = (f"Based on your income of £{self.applicant.income} and deposit of £{self.applicant.deposit}, "
#                             f"you may be eligible for a maximum loan of £{max_loan:,.2f}, allowing you to purchase a property "
#                             f"up to £{max_property_value:,.2f}. Thank you for your response, I will now forward your information "
#                             f"to one of our free, CEMAP qualified mortgage advisors who will take over from here. It’s been great "
#                             f"speaking with you and good luck with your house buying journey. Goodbye.")
        
#         return response

#     def save_lead(self):
#         with open("leads.json", "a") as f:
#             json.dump(asdict(self.applicant), f)
#             f.write("\n")

#     def post_process_response(self, response):
#         response = response.replace("broker", "mortgage advisor")
#         response = response.replace("mortgage advisor", "one of our free, CEMAP qualified mortgage advisors")
#         response = response.replace("$", "£")
#         return response

#     def answer_info_question(self, user_input):
#         if "mortgage rate" in user_input.lower() or "interest rate" in user_input.lower():
#             return self.post_process_response(
#                 "For the most accurate and up-to-date information on current mortgage rates in the UK, "
#                 "I recommend raising this with one of our free, qualified mortgage advisors who will "
#                 "be contacting you shortly to tailor a personalised quote based on the information you have given me."
#             )

#         if "qualified mortgage advisors" in user_input.lower():
#             return self.post_process_response(
#                 "Yes, we have free, CEMAP qualified mortgage advisors on hand at any time. "
#                 "Please provide your email and phone number, and I will have them contact you. "
#                 "Alternatively, feel free to ask me anything related to mortgages."
#             )

#         context_docs = self.retriever.invoke(user_input)
#         context_text = "\n".join([doc.page_content for doc in context_docs])
        
#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are a helpful mortgage advisor for a UK-based company. Always use pounds (£) as the currency and refer to 'one of our free, CEMAP qualified mortgage advisors' instead of 'mortgage advisor' or 'broker.' Never suggest external advisors or brokers. Be concise and focus on the UK mortgage market.

# Knowledge from web sources:
# {context_text}

# Recent conversation history (for context):
# {recent_history}

# User asked:
# {user_input}

# Answer with context where possible. Be concise. If the input is vague or incomplete, ask for clarification.
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return self.post_process_response(response.content)

#     def process_input(self, user_input):
#         self.chat_memory.append({"user": user_input})
#         query_type = self.detect_query_type(user_input)

#         is_application_mode = (
#             len(self.chat_memory) > 1
#             and "ai" in self.chat_memory[-2]
#             and any(self.get_question(field) in self.chat_memory[-2]["ai"] for field in self.fields)
#         )

#         application_in_progress = any(getattr(self.applicant, field) for field in self.fields)

#         if self.awaiting_continue_confirmation:
#             if user_input.lower() in ["yes", "continue", "ok"]:
#                 self.is_collecting_info = True
#                 self.awaiting_continue_confirmation = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_continue_confirmation = False
#                 reply = "Okay! Let me know if you need anything else."
#         elif query_type == "application" and not self.is_collecting_info:
#             self.is_collecting_info = True
#             reply = self.ask_next_question()
#         elif query_type == "information":
#             self.is_collecting_info = False
#             reply = self.answer_info_question(user_input)
#             if application_in_progress and self.last_query_type != "information":
#                 reply += "\nWould you like to continue with your mortgage application?"
#                 self.awaiting_continue_confirmation = True
#         elif query_type == "application" or (query_type == "general" and is_application_mode):
#             field, value = self.extract_info(user_input)
#             print(f"DEBUG: process_input - field: {field}, value: {value}")
#             if field is not None and value is not None:
#                 self.update_field(field, value)
#                 reply = self.ask_next_question()
#             else:
#                 reply = f"Sorry, I didn't understand. Could you answer: {self.get_question(self.last_asked_field)}"
#         else:
#             self.is_collecting_info = False
#             prompt = f"""
# Be a helpful, friendly mortgage assistant for a UK-based company. Always use pounds (£) and refer to 'one of our free, CEMAP qualified mortgage advisors.' Answer this:
# {user_input}
# """
#             reply = self.post_process_response(self.llm.invoke([HumanMessage(content=prompt)]).content)

#         self.chat_memory.append({"ai": reply})
#         self.last_query_type = query_type
#         return reply

# if __name__ == '__main__':
#     bot = MortgageAdvisorBot()
#     print("\n\U0001F3E1 Welcome to the Unified AI Mortgage Advisor! Type 'exit' to quit.")
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("\n\U0001F44B Goodbye! Stay financially wise!")
#             break
#         response = bot.process_input(user_input)
#         print(f"\n\U0001F916 AI: {response}")









# import os
# import pdfplumber
# import requests
# import time
# import json
# from dataclasses import dataclass, asdict
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# import cloudscraper
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from langchain.schema import HumanMessage

# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# @dataclass
# class MortgageApplicantInfo:
#     application_type: str = None
#     first_time_buyer: str = None
#     dob: str = None
#     employment_status: str = None
#     employment_type: str = None
#     income: str = None
#     credit_commitments: str = None
#     dependants: str = None
#     adverse_credit: str = None
#     property_sale_info: str = None
#     expenditure: str = None
#     email: str = None
#     phone_number: str = None
#     deposit: str = None

# class MortgageAdvisorBot:
#     def __init__(self):
#         self.applicant = MortgageApplicantInfo()
#         self.fields = list(asdict(self.applicant).keys())
#         self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
#         self.chat_memory = []
#         self.is_collecting_info = False
#         self.awaiting_continue_confirmation = False
#         self.awaiting_permission = False
#         self.awaiting_relevant_response = False  # নতুন স্টেট ভ্যারিয়েবল
#         self.last_relevant_question = None  # প্রাসঙ্গিক প্রশ্ন সংরক্ষণ
#         self.asked_fields = set()
#         self.last_asked_field = None
#         self.last_query_type = None

#         self.retriever = self.load_or_create_vectorstore()

#     def load_or_create_vectorstore(self):
#         def extract_text_from_pdf(pdf_path): 
#             if not os.path.exists(pdf_path): return ""
#             text = ""
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     content = page.extract_text()
#                     if content:
#                         text += content + "\n"
#             return text.strip()

#         def scrape(url):
#             try:
#                 scraper = cloudscraper.create_scraper()
#                 headers = {
#                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#                 }
#                 res = scraper.get(url, headers=headers, timeout=10)
#                 print(f"DEBUG: Status code for {url}: {res.status_code}")
#                 if res.status_code == 200:
#                     soup = BeautifulSoup(res.text, "html.parser")
#                     for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
#                         tag.extract()
#                     return soup.get_text(separator=" ", strip=True)
#                 else:
#                     print(f"DEBUG: Failed with status code {res.status_code} for {url}")
#                     return ""
#             except Exception as e:
#                 print(f"DEBUG: Exception for {url}: {str(e)}")
#                 return ""

#         urls = [
#             "https://askaboutmortgages.co.uk/",
#             "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#             "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#             "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#             "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#             "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#             "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#             "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions",
#             "https://www.money.co.uk/mortgages/bank-of-england-base-rate",
#         ]

#         print("\U0001F4DA Building vectorstore...")
#         scraped = []
#         for u in urls:
#             content = scrape(u)
#             if content:
#                 print(f"✅ Scraped: {u}")
#                 scraped.append(Document(page_content=content))
#             else:
#                 print(f"❌ Failed: {u}")

#         pdf_text = extract_text_from_pdf("AI Mortgage Advisor Project-12345.pdf")
#         if pdf_text:
#             scraped.append(Document(page_content=pdf_text))

#         chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(scraped)

#         if os.path.exists("faiss_db"):
#             return FAISS.load_local("faiss_db", OpenAIEmbeddings(), allow_dangerous_deserialization=True).as_retriever(search_kwargs={"k": 3})
#         db = FAISS.from_documents(chunks, OpenAIEmbeddings())
#         db.save_local("faiss_db")
#         return db.as_retriever(search_kwargs={"k": 3})

#     def detect_query_type(self, user_input):
#         if user_input.strip().lower() in ["yes", "no"]:
#             return "application" if self.is_collecting_info or self.awaiting_permission else "general"

#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are an intelligent classifier for a mortgage assistant chatbot.

# Classify the following user input into one of these three types:
# - application → if the user is trying to apply or give their personal or financial details.
# - information → if the user is asking about mortgage concepts, terms, policies, or loan types.
# - general → if it's small talk, unrelated, or casual.

# Recent conversation history (for context):
# {recent_history}

# Just return one of: "application", "information", or "general". Respond with only one word.

# User input: "{user_input}"
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         classification = response.content.strip().lower()

#         print(f"DEBUG: Input '{user_input}' classified as: {classification}")
#         return classification if classification in ["application", "information", "general"] else "general"

#     def generate_relevant_question(self, user_input):
#         prompt = f"""
# You are a mortgage assistant chatbot. The user has provided an input related to a mortgage application: "{user_input}". Instead of asking a standard application question, generate a relevant, engaging question that aligns with their input to continue the conversation naturally. For example:
# - If the user says "I want to buy a house," ask something like "What type of house are you looking to buy?"
# - If the user says "I have £50,000 saved," ask something like "Is that your deposit, or are you planning to save more?"

# Ensure the question is concise, relevant to the UK mortgage market, and encourages the user to provide more details.

# Generated question: 
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def generate_response_to_relevant_question(self, user_input, question):
#         prompt = f"""
# You are a mortgage assistant chatbot. The user was asked: "{question}" and responded with: "{user_input}". Generate a concise, friendly response that acknowledges their answer and aligns with the UK mortgage market. For example:
# - If the user says "A flat" to "What type of house are you looking to buy?", respond with something like "Great, a flat sounds perfect! Are you looking in a specific area?"
# - If the user says "£50,000 deposit" to "Is that your deposit?", respond with something like "That's a solid deposit! Are you planning to buy soon?"

# Response: 
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def extract_info(self, user_input):
#         last_question = self.chat_memory[-2]["ai"] if len(self.chat_memory) >= 2 and "ai" in self.chat_memory[-2] else ""
#         prompt = f"""
# You are extracting information for a mortgage application. Based on the previous question and the user's response, identify the relevant field and value. The fields are: {', '.join(self.fields)}.

# Previous question: {last_question}
# Existing info:
# {json.dumps(asdict(self.applicant), indent=2)}

# User response: {user_input}

# If the response is "yes" or "no", translate it to boolean true/false.
# Output a JSON object with exactly two keys: \"field\" and \"value\".
# If no relevant information is found, return {{\"field\": null, \"value\": null}}.
# """
#         try:
#             response = self.llm.invoke([HumanMessage(content=prompt)])
#             parsed = json.loads(response.content.strip())
#             print(f"DEBUG: extract_info output: {parsed}")
#             return parsed.get("field"), parsed.get("value")
#         except:
#             print(f"DEBUG: extract_info failed to parse: {response.content}")
#             return None, None

#     def update_field(self, field, value):
#         if field in self.fields:
#             setattr(self.applicant, field, value)
#             self.asked_fields.add(field)
#             self.last_asked_field = field

#     def calculate_loan_and_property(self, deposit, income):
#         try:
#             deposit = float(deposit.replace("£", "").replace(",", "").strip())
#             income = float(income.replace("£", "").replace(",", "").strip())
#             max_loan = income * 4.5  # 4.5x income as maximum loan
#             max_property_value = max_loan + deposit
#             return max_loan, max_property_value
#         except (ValueError, AttributeError):
#             return None, None

#     def ask_next_question(self):
#         for field in self.fields:
#             if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
#                 self.last_asked_field = field
#                 return self.get_question(field)
#         return self.finalize_lead()

#     def get_question(self, field):
#         questions = {
#             "application_type": "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#             "first_time_buyer": "Are you a first-time buyer?",
#             "dob": "Please can you give me your date of birth and your partner's, if applicable.",
#             "employment_status": "Are you in employment?",
#             "employment_type": "If yes, please specify if you are employed or self-employed?",
#             "income": "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#             "credit_commitments": "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#             "dependants": "How many dependants do you have, if any?",
#             "adverse_credit": "If you have adverse credit, please tell me what it is?",
#             "property_sale_info": "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#             "expenditure": "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs.",
#             "email": "Please provide your email address for future updates.",
#             "phone_number": "Please provide your contact number.",
#             "deposit": "How much is your deposit for the property purchase?"
#         }
#         return questions.get(field, f"Please provide your {field}")

#     def finalize_lead(self):
#         self.save_lead()
#         response = ("Thank you for your response, I will now forward your information to one of our free, "
#                     "CEMAP qualified mortgage advisors who will take over from here. It’s been great speaking "
#                     "with you and good luck with your house buying journey. Goodbye.")
        
#         if self.applicant.income and self.applicant.deposit:
#             max_loan, max_property_value = self.calculate_loan_and_property(self.applicant.deposit, self.applicant.income)
#             if max_loan and max_property_value:
#                 response = (f"Based on your income of £{self.applicant.income} and deposit of £{self.applicant.deposit}, "
#                             f"you may be eligible for a maximum loan of £{max_loan:,.2f}, allowing you to purchase a property "
#                             f"up to £{max_property_value:,.2f}. Thank you for your response, I will now forward your information "
#                             f"to one of our free, CEMAP qualified mortgage advisors who will take over from here. It’s been great "
#                             f"speaking with you and good luck with your house buying journey. Goodbye.")
        
#         return response

#     def save_lead(self):
#         with open("leads.json", "a") as f:
#             json.dump(asdict(self.applicant), f)
#             f.write("\n")

#     def post_process_response(self, response):
#         response = response.replace("broker", "mortgage advisor")
#         response = response.replace("mortgage advisor", "one of our free, CEMAP qualified mortgage advisors")
#         response = response.replace("$", "£")
#         return response

#     def answer_info_question(self, user_input):
#         if "mortgage rate" in user_input.lower() or "interest rate" in user_input.lower():
#             return self.post_process_response(
#                 "For the most accurate and up-to-date information on current mortgage rates in the UK, "
#                 "I recommend raising this with one of our free, qualified mortgage advisors who will "
#                 "be contacting you shortly to tailor a personalised quote based on the information you have given me."
#             )

#         if "qualified mortgage advisors" in user_input.lower():
#             return self.post_process_response(
#                 "Yes, we have free, CEMAP qualified mortgage advisors on hand at any time. "
#                 "Please provide your email and phone number, and I will have them contact you. "
#                 "Alternatively, feel free to ask me anything related to mortgages."
#             )

#         context_docs = self.retriever.invoke(user_input)
#         context_text = "\n".join([doc.page_content for doc in context_docs])
        
#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are a helpful mortgage advisor for a UK-based company. Always use pounds (£) as the currency and refer to 'one of our free, CEMAP qualified mortgage advisors' instead of 'mortgage advisor' or 'broker.' Never suggest external advisors or brokers. Be concise and focus on the UK mortgage market.

# Knowledge from web sources:
# {context_text}

# Recent conversation history (for context):
# {recent_history}

# User asked:
# {user_input}

# Answer with context where possible. Be concise. If the input is vague or incomplete, ask for clarification.
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return self.post_process_response(response.content)

#     def process_input(self, user_input):
#         self.chat_memory.append({"user": user_input})
#         query_type = self.detect_query_type(user_input)

#         is_application_mode = (
#             len(self.chat_memory) > 1
#             and "ai" in self.chat_memory[-2]
#             and any(self.get_question(field) in self.chat_memory[-2]["ai"] for field in self.fields)
#         )

#         application_in_progress = any(getattr(self.applicant, field) for field in self.fields)

#         if self.awaiting_permission:
#             if user_input.lower() in ["yes", "ok", "sure"]:
#                 self.is_collecting_info = True
#                 self.awaiting_permission = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_permission = False
#                 reply = "Okay, let me know when you're ready to provide more details or if you have other questions!"
#         elif self.awaiting_relevant_response:
#             # প্রাসঙ্গিক প্রশ্নের উত্তর প্রসেস করা
#             response = self.generate_response_to_relevant_question(user_input, self.last_relevant_question)
#             reply = f"{response} May I collect some information from you to assist with your mortgage application?"
#             self.awaiting_relevant_response = False
#             self.awaiting_permission = True
#         elif self.awaiting_continue_confirmation:
#             if user_input.lower() in ["yes", "continue", "ok"]:
#                 self.is_collecting_info = True
#                 self.awaiting_continue_confirmation = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_continue_confirmation = False
#                 reply = "Okay! Let me know if you need anything else."
#         elif query_type == "application" and not self.is_collecting_info and not application_in_progress:
#             # প্রথমবার অ্যাপ্লিকেশন টাইপ ইনপুট পেলে প্রাসঙ্গিক প্রশ্ন জিজ্ঞাসা করো
#             relevant_question = self.generate_relevant_question(user_input)
#             self.last_relevant_question = relevant_question
#             reply = relevant_question
#             self.awaiting_relevant_response = True
#         elif query_type == "information":
#             self.is_collecting_info = False
#             reply = self.answer_info_question(user_input)
#             if application_in_progress and self.last_query_type != "information":
#                 reply += "\nWould you like to continue with your mortgage application?"
#                 self.awaiting_continue_confirmation = True
#         elif query_type == "application" or (query_type == "general" and is_application_mode):
#             field, value = self.extract_info(user_input)
#             print(f"DEBUG: process_input - field: {field}, value: {value}")
#             if field is not None and value is not None:
#                 self.update_field(field, value)
#                 reply = self.ask_next_question()
#             else:
#                 reply = f"Sorry, I didn't understand. Could you answer: {self.get_question(self.last_asked_field)}"
#         else:
#             self.is_collecting_info = False
#             prompt = f"""
# Be a helpful, friendly mortgage assistant for a UK-based company. Always use pounds (£) and refer to 'one of our free, CEMAP qualified mortgage advisors.' Answer this:
# {user_input}
# """
#             reply = self.post_process_response(self.llm.invoke([HumanMessage(content=prompt)]).content)

#         self.chat_memory.append({"ai": reply})
#         self.last_query_type = query_type
#         return reply

# if __name__ == '__main__':
#     bot = MortgageAdvisorBot()
#     print("\n\U0001F3E1 Welcome to the Unified AI Mortgage Advisor! Type 'exit' to quit.")
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("\n\U0001F44B Goodbye! Stay financially wise!")
#             break
#         response = bot.process_input(user_input)
#         print(f"\n\U0001F916 AI: {response}")












# import os
# import pdfplumber
# import requests
# import time
# import json
# from dataclasses import dataclass, asdict
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# import cloudscraper
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from langchain.schema import HumanMessage

# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# @dataclass
# class MortgageApplicantInfo:
#     application_type: str = None
#     first_time_buyer: str = None
#     dob: str = None
#     employment_status: str = None
#     employment_type: str = None
#     income: str = None
#     credit_commitments: str = None
#     dependants: str = None
#     adverse_credit: str = None
#     property_sale_info: str = None
#     expenditure: str = None
#     email: str = None
#     phone_number: str = None

# class MortgageAdvisorBot:
#     def __init__(self):
#         self.applicant = MortgageApplicantInfo()
#         self.fields = [
#             "application_type", "first_time_buyer", "dob", "employment_status",
#             "employment_type", "income", "credit_commitments", "dependants",
#             "adverse_credit", "property_sale_info", "expenditure"
#         ]
#         self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
#         self.chat_memory = []
#         self.is_collecting_info = False
#         self.awaiting_continue_confirmation = False
#         self.awaiting_permission = False
#         self.awaiting_relevant_response = False
#         self.awaiting_save_permission = False  # নতুন স্টেট: তথ্য সেভের অনুমতি
#         self.awaiting_contact_info = False  # নতুন স্টেট: ইমেইল এবং ফোন নম্বর
#         self.last_relevant_question = None
#         self.asked_fields = set()
#         self.last_asked_field = None
#         self.last_query_type = None

#         self.retriever = self.load_or_create_vectorstore()

#     def load_or_create_vectorstore(self):
#         def extract_text_from_pdf(pdf_path): 
#             if not os.path.exists(pdf_path): return ""
#             text = ""
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     content = page.extract_text()
#                     if content:
#                         text += content + "\n"
#             return text.strip()

#         def scrape(url):
#             try:
#                 scraper = cloudscraper.create_scraper()
#                 headers = {
#                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#                 }
#                 res = scraper.get(url, headers=headers, timeout=10)
#                 print(f"DEBUG: Status code for {url}: {res.status_code}")
#                 if res.status_code == 200:
#                     soup = BeautifulSoup(res.text, "html.parser")
#                     for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
#                         tag.extract()
#                     return soup.get_text(separator=" ", strip=True)
#                 else:
#                     print(f"DEBUG: Failed with status code {res.status_code} for {url}")
#                     return ""
#             except Exception as e:
#                 print(f"DEBUG: Exception for {url}: {str(e)}")
#                 return ""

#         urls = [
#             "https://askaboutmortgages.co.uk/",
#             "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#             "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#             "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#             "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#             "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#             "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#             "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions",
#             "https://www.money.co.uk/mortgages/bank-of-england-base-rate",
#         ]

#         print("\U0001F4DA Building vectorstore...")
#         scraped = []
#         for u in urls:
#             content = scrape(u)
#             if content:
#                 print(f"✅ Scraped: {u}")
#                 scraped.append(Document(page_content=content))
#             else:
#                 print(f"❌ Failed: {u}")

#         pdf_text = extract_text_from_pdf("AI Mortgage Advisor Project-12345.pdf")
#         if pdf_text:
#             scraped.append(Document(page_content=pdf_text))

#         chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(scraped)

#         if os.path.exists("faiss_db"):
#             return FAISS.load_local("faiss_db", OpenAIEmbeddings(), allow_dangerous_deserialization=True).as_retriever(search_kwargs={"k": 3})
#         db = FAISS.from_documents(chunks, OpenAIEmbeddings())
#         db.save_local("faiss_db")
#         return db.as_retriever(search_kwargs={"k": 3})

#     def detect_query_type(self, user_input):
#         if user_input.strip().lower() in ["yes", "no"]:
#             return "application" if self.is_collecting_info or self.awaiting_permission or self.awaiting_save_permission or self.awaiting_contact_info else "general"

#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are an intelligent classifier for a mortgage assistant chatbot.

# Classify the following user input into one of these three types:
# - application → if the user is trying to apply or give their personal or financial details.
# - information → if the user is asking about mortgage concepts, terms, policies, or loan types.
# - general → if it's small talk, unrelated, or casual.

# Recent conversation history (for context):
# {recent_history}

# Just return one of: "application", "information", or "general". Respond with only one word.

# User input: "{user_input}"
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         classification = response.content.strip().lower()

#         print(f"DEBUG: Input '{user_input}' classified as: {classification}")
#         return classification if classification in ["application", "information", "general"] else "general"

#     def generate_relevant_question(self, user_input):
#         prompt = f"""
# You are a mortgage assistant chatbot. The user has provided an input related to a mortgage application: "{user_input}". Instead of asking a standard application question, generate a relevant, engaging question that aligns with their input to continue the conversation naturally. For example:
# - If the user says "I want to buy a house," ask something like "What type of house are you looking to buy?"
# - If the user says "I have £50,000 saved," ask something like "Is that your deposit, or are you planning to save more?"

# Ensure the question is concise, relevant to the UK mortgage market, and encourages the user to provide more details.

# Generated question: 
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def generate_response_to_relevant_question(self, user_input, question):
#         prompt = f"""
# You are a mortgage assistant chatbot. The user was asked: "{question}" and responded with: "{user_input}". Generate a concise, friendly response that acknowledges their answer and aligns with the UK mortgage market. For example:
# - If the user says "A flat" to "What type of house are you looking to buy?", respond with something like "Great, a flat sounds perfect! Are you looking in a specific area?"
# - If the user says "£50,000 deposit" to "Is that your deposit?", respond with something like "That's a solid deposit! Are you planning to buy soon?"

# Response: 
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def extract_info(self, user_input):
#         last_question = self.chat_memory[-2]["ai"] if len(self.chat_memory) >= 2 and "ai" in self.chat_memory[-2] else ""
#         prompt = f"""
# You are extracting information for a mortgage application. Based on the previous question and the user's response, identify the relevant field and value. The fields are: {', '.join(self.fields + ['email', 'phone_number'])}.

# Previous question: {last_question}
# Existing info:
# {json.dumps(asdict(self.applicant), indent=2)}

# User response: {user_input}

# If the response is "yes" or "no", translate it to boolean true/false.
# Output a JSON object with exactly two keys: \"field\" and \"value\".
# If no relevant information is found, return {{\"field\": null, \"value\": null}}.
# """
#         try:
#             response = self.llm.invoke([HumanMessage(content=prompt)])
#             parsed = json.loads(response.content.strip())
#             print(f"DEBUG: extract_info output: {parsed}")
#             return parsed.get("field"), parsed.get("value")
#         except:
#             print(f"DEBUG: extract_info failed to parse: {response.content}")
#             return None, None

#     def update_field(self, field, value):
#         if field in asdict(self.applicant).keys():
#             setattr(self.applicant, field, value)
#             if field in self.fields:
#                 self.asked_fields.add(field)
#             self.last_asked_field = field

#     def generate_summary(self):
#         questions = self.get_questions()
#         applicant_info = asdict(self.applicant)
#         info_summary = "\n".join([f"{questions[field]}: {applicant_info[field]}" for field in self.fields if applicant_info[field]])

#         prompt = f"""
# You are a mortgage assistant chatbot. Below is the information collected from a user during a mortgage application, including the questions asked and their answers:

# {info_summary}

# Generate a concise summary of the user's mortgage application details in a professional tone, suitable for the UK mortgage market. The summary should include all provided details in a clear, structured format.

# Summary:
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def ask_next_question(self):
#         for field in self.fields:
#             if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
#                 self.last_asked_field = field
#                 return self.get_questions()[field]
#         return self.finalize_application()

#     def get_questions(self):
#         return {
#             "application_type": "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#             "first_time_buyer": "Are you a first-time buyer?",
#             "dob": "Please can you give me your date of birth and your partner's, if applicable.",
#             "employment_status": "Are you in employment?",
#             "employment_type": "If yes, please specify if you are employed or self-employed?",
#             "income": "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#             "credit_commitments": "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#             "dependants": "How many dependants do you have, if any?",
#             "adverse_credit": "If you have adverse credit, please tell me what it is?",
#             "property_sale_info": "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#             "expenditure": "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs.",
#             "email": "Please provide your email address for future updates.",
#             "phone_number": "Please provide your contact number."
#         }

#     def finalize_application(self):
#         summary = self.generate_summary()
#         self.awaiting_save_permission = True
#         return f"Here is a summary of your application:\n{summary}\n\nMay I save this information to proceed with your mortgage application?"

#     def save_lead(self):
#         with open("leads.json", "a") as f:
#             json.dump(asdict(self.applicant), f)
#             f.write("\n")

#     def post_process_response(self, response):
#         response = response.replace("broker", "mortgage advisor")
#         response = response.replace("mortgage advisor", "one of our free, CEMAP qualified mortgage advisors")
#         response = response.replace("$", "£")
#         return response

#     def answer_info_question(self, user_input):
#         if "mortgage rate" in user_input.lower() or "interest rate" in user_input.lower():
#             return self.post_process_response(
#                 "For the most accurate and up-to-date information on current mortgage rates in the UK, "
#                 "I recommend raising this with one of our free, qualified mortgage advisors who will "
#                 "be contacting you shortly to tailor a personalised quote based on the information you have given me."
#             )

#         if "qualified mortgage advisors" in user_input.lower():
#             return self.post_process_response(
#                 "Yes, we have free, CEMAP qualified mortgage advisors on hand at any time. "
#                 "Please provide your email and phone number, and I will have them contact you. "
#                 "Alternatively, feel free to ask me anything related to mortgages."
#             )

#         context_docs = self.retriever.invoke(user_input)
#         context_text = "\n".join([doc.page_content for doc in context_docs])
        
#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are a helpful mortgage advisor for a UK-based company. Always use pounds (£) as the currency and refer to 'one of our free, CEMAP qualified mortgage advisors' instead of 'mortgage advisor' or 'broker.' Never suggest external advisors or brokers. Be concise and focus on the UK mortgage market.

# Knowledge from web sources:
# {context_text}

# Recent conversation history (for context):
# {recent_history}

# User asked:
# {user_input}

# Answer with context where possible. Be concise. If the input is vague or incomplete, ask for clarification.
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return self.post_process_response(response.content)

#     def process_input(self, user_input):
#         self.chat_memory.append({"user": user_input})
#         query_type = self.detect_query_type(user_input)

#         is_application_mode = (
#             len(self.chat_memory) > 1
#             and "ai" in self.chat_memory[-2]
#             and any(self.get_questions()[field] in self.chat_memory[-2]["ai"] for field in self.fields + ["email", "phone_number"])
#         )

#         application_in_progress = any(getattr(self.applicant, field) for field in self.fields)

#         if self.awaiting_save_permission:
#             if user_input.lower() in ["yes", "ok", "sure"]:
#                 self.awaiting_save_permission = False
#                 self.awaiting_contact_info = True
#                 self.last_asked_field = "email"
#                 reply = self.get_questions()["email"]
#             else:
#                 self.awaiting_save_permission = False
#                 reply = "Thank you for your application. If you have any more questions or wish to proceed later, feel free to let me know!"
#         elif self.awaiting_contact_info:
#             field, value = self.extract_info(user_input)
#             if field == "email" and value:
#                 self.update_field(field, value)
#                 self.last_asked_field = "phone_number"
#                 reply = self.get_questions()["phone_number"]
#             elif field == "phone_number" and value:
#                 self.update_field(field, value)
#                 self.save_lead()
#                 self.awaiting_contact_info = False
#                 reply = ("Thank you for providing your contact details. Your information has been saved, and one of our free, "
#                          "CEMAP qualified mortgage advisors will contact you soon. If you have any more questions, feel free to ask!")
#             else:
#                 reply = f"Sorry, I didn't understand. Could you answer: {self.get_questions()[self.last_asked_field]}"
#         elif self.awaiting_permission:
#             if user_input.lower() in ["yes", "ok", "sure"]:
#                 self.is_collecting_info = True
#                 self.awaiting_permission = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_permission = False
#                 reply = "Okay, let me know when you're ready to provide more details or if you have other questions!"
#         elif self.awaiting_relevant_response:
#             response = self.generate_response_to_relevant_question(user_input, self.last_relevant_question)
#             reply = f"{response} May I collect some information from you to assist with your mortgage application?"
#             self.awaiting_relevant_response = False
#             self.awaiting_permission = True
#         elif self.awaiting_continue_confirmation:
#             if user_input.lower() in ["yes", "continue", "ok"]:
#                 self.is_collecting_info = True
#                 self.awaiting_continue_confirmation = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_continue_confirmation = False
#                 reply = "Okay! Let me know if you need anything else."
#         elif query_type == "application" and not self.is_collecting_info and not application_in_progress:
#             relevant_question = self.generate_relevant_question(user_input)
#             self.last_relevant_question = relevant_question
#             reply = relevant_question
#             self.awaiting_relevant_response = True
#         elif query_type == "information":
#             self.is_collecting_info = False
#             reply = self.answer_info_question(user_input)
#             if application_in_progress and self.last_query_type != "information":
#                 reply += "\nWould you like to continue with your mortgage application?"
#                 self.awaiting_continue_confirmation = True
#         elif query_type == "application" or (query_type == "general" and is_application_mode):
#             field, value = self.extract_info(user_input)
#             print(f"DEBUG: process_input - field: {field}, value: {value}")
#             if field is not None and value is not None:
#                 self.update_field(field, value)
#                 reply = self.ask_next_question()
#             else:
#                 reply = f"Sorry, I didn't understand. Could you answer: {self.get_questions()[self.last_asked_field]}"
#         else:
#             self.is_collecting_info = False
#             prompt = f"""
# Be a helpful, friendly mortgage assistant for a UK-based company. Always use pounds (£) and refer to 'one of our free, CEMAP qualified mortgage advisors.' Answer this:
# {user_input}
# """
#             reply = self.post_process_response(self.llm.invoke([HumanMessage(content=prompt)]).content)

#         self.chat_memory.append({"ai": reply})
#         self.last_query_type = query_type
#         return reply

# if __name__ == '__main__':
#     bot = MortgageAdvisorBot()
#     print("\n\U0001F3E1 Welcome to the Unified AI Mortgage Advisor! Type 'exit' to quit.")
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("\n\U0001F44B Goodbye! Stay financially wise!")
#             break
#         response = bot.process_input(user_input)
#         print(f"\n\U0001F916 AI: {response}")














# import os
# import pdfplumber
# import requests
# import time
# import json
# from dataclasses import dataclass, asdict
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# import cloudscraper
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from langchain.schema import HumanMessage

# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# @dataclass
# class MortgageApplicantInfo:
#     application_type: str = None
#     first_time_buyer: str = None
#     dob: str = None
#     employment_status: str = None
#     employment_type: str = None
#     income: str = None
#     credit_commitments: str = None
#     dependants: str = None
#     adverse_credit: str = None
#     property_sale_info: str = None
#     expenditure: str = None
#     email: str = None
#     phone_number: str = None

# class MortgageAdvisorBot:
#     def __init__(self):
#         self.applicant = MortgageApplicantInfo()
#         self.fields = [
#             "application_type", "first_time_buyer", "dob", "employment_status",
#             "employment_type", "income", "credit_commitments", "dependants",
#             "adverse_credit", "property_sale_info", "expenditure"
#         ]
#         self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
#         self.chat_memory = []
#         self.is_collecting_info = False
#         self.awaiting_continue_confirmation = False
#         self.awaiting_permission = False
#         self.awaiting_relevant_response = False
#         self.awaiting_save_permission = False
#         self.awaiting_contact_info = False
#         self.last_relevant_question = None
#         self.asked_fields = set()
#         self.last_asked_field = None
#         self.last_query_type = None

#         self.retriever = self.load_or_create_vectorstore()

#     def load_or_create_vectorstore(self):
#         def extract_text_from_pdf(pdf_path): 
#             if not os.path.exists(pdf_path): return ""
#             text = ""
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     content = page.extract_text()
#                     if content:
#                         text += content + "\n"
#             return text.strip()

#         def scrape(url):
#             try:
#                 scraper = cloudscraper.create_scraper()
#                 headers = {
#                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#                 }
#                 res = scraper.get(url, headers=headers, timeout=10)
#                 print(f"DEBUG: Status code for {url}: {res.status_code}")
#                 if res.status_code == 200:
#                     soup = BeautifulSoup(res.text, "html.parser")
#                     for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
#                         tag.extract()
#                     return soup.get_text(separator=" ", strip=True)
#                 else:
#                     print(f"DEBUG: Failed with status code {res.status_code} for {url}")
#                     return ""
#             except Exception as e:
#                 print(f"DEBUG: Exception for {url}: {str(e)}")
#                 return ""

#         urls = [
#             "https://askaboutmortgages.co.uk/",
#             "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
#             "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
#             "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
#             "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
#             "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
#             "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
#             "https://www.which.co.uk/money/mortgages-and-property/mortgages",
#             "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions",
#             "https://www.money.co.uk/mortgages/bank-of-england-base-rate",
#         ]

#         print("\U0001F4DA Building vectorstore...")
#         scraped = []
#         for u in urls:
#             content = scrape(u)
#             if content:
#                 print(f"✅ Scraped: {u}")
#                 scraped.append(Document(page_content=content))
#             else:
#                 print(f"❌ Failed: {u}")

#         pdf_text = extract_text_from_pdf("AI Mortgage Advisor Project-12345.pdf")
#         if pdf_text:
#             scraped.append(Document(page_content=pdf_text))

#         chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(scraped)

#         if os.path.exists("faiss_db"):
#             return FAISS.load_local("faiss_db", OpenAIEmbeddings(), allow_dangerous_deserialization=True).as_retriever(search_kwargs={"k": 3})
#         db = FAISS.from_documents(chunks, OpenAIEmbeddings())
#         db.save_local("faiss_db")
#         return db.as_retriever(search_kwargs={"k": 3})

#     def detect_query_type(self, user_input):
#         if user_input.strip().lower() in ["yes", "no"]:
#             return "application" if self.is_collecting_info or self.awaiting_permission or self.awaiting_save_permission or self.awaiting_contact_info else "general"

#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are an intelligent classifier for a mortgage assistant chatbot.

# Classify the following user input into one of these three types:
# - application → if the user is trying to apply or give their personal or financial details.
# - information → if the user is asking about mortgage concepts, terms, policies, or loan types.
# - general → if it's small talk, unrelated, or casual.

# Recent conversation history (for context):
# {recent_history}

# Examples:
# - "I have £75,000 saved" → application
# - "What is a mortgage?" → information
# - "Hello, how are you?" → general
# - "How much can I borrow?" → application
# - "Tell me about fixed-rate mortgages" → information
# - "My name is Kevin" → application
# - "What are current interest rates?" → information

# Just return one of: "application", "information", or "general". Respond with only one word.

# User input: "{user_input}"
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         classification = response.content.strip().lower()

#         print(f"DEBUG: Input '{user_input}' classified as: {classification}")
#         return classification if classification in ["application", "information", "general"] else "general"

#     def generate_relevant     def generate_relevant_question(self, user_input):
#         prompt = f"""
# You are a mortgage assistant chatbot. The user has provided an input related to a mortgage application: "{user_input}". Instead of asking a standard application question, generate a relevant, engaging question that aligns with their input to continue the conversation naturally. For example:
# - If the user says "I want to buy a house," ask something like "What type of house are you looking to buy?"
# - If the user says "I have £50,000 saved," ask something like "Is that your deposit, or are you planning to save more?"

# Ensure the question is concise, relevant to the UK mortgage market, and encourages the user to provide more details.

# Generated question: 
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def generate_response_to_relevant_question(self, user_input, question):
#         prompt = f"""
# You are a mortgage assistant chatbot. The user was asked: "{question}" and responded with: "{user_input}". Generate a concise, friendly response that acknowledges their answer and aligns with the UK mortgage market. For example:
# - If the user says "A flat" to "What type of house are you looking to buy?", respond with something like "Great, a flat sounds perfect! Are you looking in a specific area?"
# - If the user says "£50,000 deposit" to "Is that your deposit?", respond with something like "That's a solid deposit! Are you planning to buy soon?"

# Response: 
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def extract_info(self, user_input):
#         last_question = self.chat_memory[-2]["ai"] if len(self.chat_memory) >= 2 and "ai" in self.chat_memory[-2] else ""
#         prompt = f"""
# You are extracting information for a mortgage application. Based on the previous question and the user's response, identify the relevant field and value. The fields are: {', '.join(self.fields + ['email', 'phone_number'])}.

# Previous question: {last_question}
# Existing info:
# {json.dumps(asdict(self.applicant), indent=2)}

# User response: {user_input}

# If the response is "yes" or "no", translate it to boolean true/false.
# Output a JSON object with exactly two keys: \"field\" and \"value\".
# If no relevant information is found, return {{\"field\": null, \"value\": null}}.
# """
#         try:
#             response = self.llm.invoke([HumanMessage(content=prompt)])
#             parsed = json.loads(response.content.strip())
#             print(f"DEBUG: extract_info output: {parsed}")
#             return parsed.get("field"), parsed.get("value")
#         except:
#             print(f"DEBUG: extract_info failed to parse: {response.content}")
#             return None, None

#     def update_field(self, field, value):
#         if field in asdict(self.applicant).keys():
#             setattr(self.applicant, field, value)
#             if field in self.fields:
#                 self.asked_fields.add(field)
#             self.last_asked_field = field

#     def generate_summary(self):
#         questions = self.get_questions()
#         applicant_info = asdict(self.applicant)
#         info_summary = "\n".join([f"{questions[field]}: {applicant_info[field]}" for field in self.fields if applicant_info[field]])

#         prompt = f"""
# You are a mortgage assistant chatbot. Below is the information collected from a user during a mortgage application, including the questions asked and their answers:

# {info_summary}

# Generate a concise summary of the user's mortgage application details in a professional tone, suitable for the UK mortgage market. The summary should include all provided details in a clear, structured format.

# Summary:
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()

#     def ask_next_question(self):
#         for field in self.fields:
#             if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
#                 self.last_asked_field = field
#                 return self.get_questions()[field]
#         return self.finalize_application()

#     def get_questions(self):
#         return {
#             "application_type": "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
#             "first_time_buyer": "Are you a first-time buyer?",
#             "dob": "Please can you give me your date of birth and your partner's, if applicable.",
#             "employment_status": "Are you in employment?",
#             "employment_type": "If yes, please specify if you are employed or self-employed?",
#             "income": "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
#             "credit_commitments": "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
#             "dependants": "How many dependants do you have, if any?",
#             "adverse_credit": "If you have adverse credit, please tell me what it is?",
#             "property_sale_info": "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
#             "expenditure": "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs.",
#             "email": "Please provide your email address for future updates.",
#             "phone_number": "Please provide your contact number."
#         }

#     def finalize_application(self):
#         summary = self.generate_summary()
#         self.awaiting_save_permission = True
#         return f"Here is a summary of your application:\n{summary}\n\nMay I save this information to proceed with your mortgage application?"

#     def save_lead(self):
#         with open("leads.json", "a") as f:
#             json.dump(asdict(self.applicant), f)
#             f.write("\n")

#     def post_process_response(self, response):
#         response = response.replace("broker", "mortgage advisor")
#         response = response.replace("mortgage advisor", "one of our free, CEMAP qualified mortgage advisors")
#         response = response.replace("$", "£")
#         return response

#     def answer_info_question(self, user_input):
#         if "mortgage rate" in user_input.lower() or "interest rate" in user_input.lower():
#             return self.post_process_response(
#                 "For the most accurate and up-to-date information on current mortgage rates in the UK, "
#                 "I recommend raising this with one of our free, qualified mortgage advisors who will "
#                 "be contacting you shortly to tailor a personalised quote based on the information you have given me."
#             )

#         if "qualified mortgage advisors" in user_input.lower():
#             return self.post_process_response(
#                 "Yes, we have free, CEMAP qualified mortgage advisors on hand at any time. "
#                 "Please provide your email and phone number, and I will have them contact you. "
#                 "Alternatively, feel free to ask me anything related to mortgages."
#             )

#         if "how much can I borrow" in user_input.lower():
#             return self.post_process_response(
#                 "To provide an accurate estimate of how much you can borrow, I’ll need to collect some additional information. "
#                 "May I ask a few questions to assist you further?"
#             )

#         context_docs = self.retriever.invoke(user_input)
#         context_text = "\n".join([doc.page_content for doc in context_docs])
        
#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are a helpful mortgage advisor for a UK-based company. Always use pounds (£) as the currency and refer to 'one of our free, CEMAP qualified mortgage advisors' instead of 'mortgage advisor' or 'broker.' 
# Never suggest external advisors, brokers, or lenders. Be concise and focus on the UK mortgage market.

# Knowledge from web sources:
# {context_text}

# Recent conversation history (for context):
# {recent_history}

# User asked:
# {user_input}

# Answer with context where possible. Be concise. If the input is vague or incomplete, ask for clarification.
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         reply = self.post_process_response(response.content)

#         # If application is in progress, prompt to continue collecting information
#         application_in_progress = any(getattr(self.applicant, field) for field in self.fields)
#         if application_in_progress:
#             self.awaiting_continue_confirmation = True
#             reply += "\nWould you like to continue with your mortgage application?"

#         return reply

#     def process_input(self, user_input):
#         self.chat_memory.append({"user": user_input})
#         query_type = self.detect_query_type(user_input)

#         is_application_mode = (
#             len(self.chat_memory) > 1
#             and "ai" in self.chat_memory[-2]
#             and any(self.get_questions()[field] in self.chat_memory[-2]["ai"] for field in self.fields + ["email", "phone_number"])
#         )

#         application_in_progress = any(getattr(self.applicant, field) for field in self.fields)

#         if self.awaiting_save_permission:
#             if user_input.lower() in ["yes", "ok", "sure"]:
#                 self.awaiting_save_permission = False
#                 self.awaiting_contact_info = True
#                 self.last_asked_field = "email"
#                 reply = self.get_questions()["email"]
#             else:
#                 self.awaiting_save_permission = False
#                 reply = "Thank you for your application. If you have any more questions or wish to proceed later, feel free to let me know!"
#         elif self.awaiting_contact_info:
#             field, value = self.extract_info(user_input)
#             if field == "email" and value:
#                 self.update_field(field, value)
#                 self.last_asked_field = "phone_number"
#                 reply = self.get_questions()["phone_number"]
#             elif field == "phone_number" and value:
#                 self.update_field(field, value)
#                 self.save_lead()
#                 self.awaiting_contact_info = False
#                 reply = ("Thank you for your response, I will now forward your information to one of our free, CEMAP qualified mortgage advisors "
#                          "who will take over from here. It’s been great speaking with you and good luck with your house buying journey. Goodbye")
#             else:
#                 reply = f"Sorry, I didn't understand. Could you answer: {self.get_questions()[self.last_asked_field]}"
#         elif self.awaiting_permission:
#             if user_input.lower() in ["yes", "ok", "sure"]:
#                 self.is_collecting_info = True
#                 self.awaiting_permission = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_permission = False
#                 reply = "Okay, let me know when you're ready to provide more details or if you have other questions!"
#         elif self.awaiting_relevant_response:
#             response = self.generate_response_to_relevant_question(user_input, self.last_relevant_question)
#             reply = f"{response} May I collect some information from you to assist with your mortgage application?"
#             self.awaiting_relevant_response = False
#             self.awaiting_permission = True
#         elif self.awaiting_continue_confirmation:
#             if user_input.lower() in ["yes", "continue", "ok"]:
#                 self.is_collecting_info = True
#                 self.awaiting_continue_confirmation = False
#                 reply = self.ask_next_question()
#             else:
#                 self.awaiting_continue_confirmation = False
#                 reply = "Okay! Let me know if you need anything else."
#         elif query_type == "application" and not self.is_collecting_info and not application_in_progress:
#             relevant_question = self.generate_relevant_question(user_input)
#             self.last_relevant_question = relevant_question
#             reply = relevant_question
#             self.awaiting_relevant_response = True
#         elif query_type == "information":
#             self.is_collecting_info = False
#             reply = self.answer_info_question(user_input)
#         elif query_type == "application" or (query_type == "general" and is_application_mode):
#             field, value = self.extract_info(user_input)
#             print(f"DEBUG: process_input - field: {field}, value: {value}")
#             if field is not None and value is not None:
#                 self.update_field(field, value)
#                 reply = self.ask_next_question()
#             else:
#                 reply = f"Sorry, I didn't understand. Could you answer: {self.get_questions()[self.last_asked_field]}"
#         else:
#             self.is_collecting_info = False
#             prompt = f"""
# Be a helpful, friendly mortgage assistant for a UK-based company. Always use pounds (£) and refer to 'one of our free, CEMAP qualified mortgage advisors.' Answer this:
# {user_input}
# """
#             reply = self.post_process_response(self.llm.invoke([HumanMessage(content=prompt)]).content)

#         self.chat_memory.append({"ai": reply})
#         self.last_query_type = query_type
#         return reply

# if __name__ == '__main__':
#     bot = MortgageAdvisorBot()
#     print("\n\U0001F3E1 Welcome to the Unified AI Mortgage Advisor! Type 'exit' to quit.")
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("\n\U0001F44B Goodbye! Stay financially wise!")
#             break
#         response = bot.process_input(user_input)
#         print(f"\n\U0001F916 AI: {response}")













import os
import pdfplumber
import requests
import time
import json
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import cloudscraper
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.schema import HumanMessage

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

@dataclass
class MortgageApplicantInfo:
    application_type: str = None
    first_time_buyer: str = None
    dob: str = None
    employment_status: str = None
    employment_type: str = None
    income: str = None
    credit_commitments: str = None
    dependants: str = None
    adverse_credit: str = None
    property_sale_info: str = None
    expenditure: str = None
    email: str = None
    phone_number: str = None

class MortgageAdvisorBot:
    def __init__(self):
        self.applicant = MortgageApplicantInfo()
        self.fields = [
            "application_type", "first_time_buyer", "dob", "employment_status",
            "employment_type", "income", "credit_commitments", "dependants",
            "adverse_credit", "property_sale_info", "expenditure"
        ]
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        self.chat_memory = []
        self.is_collecting_info = False
        self.awaiting_continue_confirmation = False
        self.awaiting_permission = False
        self.awaiting_relevant_response = False
        self.awaiting_save_permission = False
        self.awaiting_contact_info = False
        self.last_relevant_question = None
        self.asked_fields = set()
        self.last_asked_field = None
        self.last_query_type = None

        self.retriever = self.load_or_create_vectorstore()

    def load_or_create_vectorstore(self):
        def extract_text_from_pdf(pdf_path): 
            if not os.path.exists(pdf_path): return ""
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"
            return text.strip()

        def scrape(url):
            try:
                scraper = cloudscraper.create_scraper()
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                }
                res = scraper.get(url, headers=headers, timeout=10)
                print(f"DEBUG: Status code for {url}: {res.status_code}")
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    for tag in soup(["script", "style", "footer", "nav", "header", "aside"]):
                        tag.extract()
                    return soup.get_text(separator=" ", strip=True)
                else:
                    print(f"DEBUG: Failed with status code {res.status_code} for {url}")
                    return ""
            except Exception as e:
                print(f"DEBUG: Exception for {url}: {str(e)}")
                return ""

        urls = [
            "https://askaboutmortgages.co.uk/",
            "https://www.money.co.uk/mortgages/a-complete-guide-to-mortgages",
            "https://moneysavingguru.co.uk/info/what-will-a-mortgage-advisor-ask-me/",
            "https://www.citizensadvice.org.uk/debt-and-money/mortgage-problems/",
            "https://www.propertymark.co.uk/professional-standards/consumer-guides/buying-selling-houses/mortgage-guide.html",
            "https://www.experian.co.uk/consumer/mortgages/guides/what-is-a-mortgage.html",
            "https://www.which.co.uk/money/mortgages-and-property/mortgages/types-of-mortgage/mortgage-types-explained-aIGHA3F2WqyQ",
            "https://getmymortgage.co.uk/pre/2/remortgage-calculator",
            "https://www.which.co.uk/money/mortgages-and-property/mortgages",
            "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions",
            "https://www.money.co.uk/mortgages/bank-of-england-base-rate",
        ]

        print("\U0001F4DA Building vectorstore...")
        scraped = []
        for u in urls:
            content = scrape(u)
            if content:
                print(f"✅ Scraped: {u}")
                scraped.append(Document(page_content=content))
            else:
                print(f"❌ Failed: {u}")

        pdf_text = extract_text_from_pdf("AI Mortgage Advisor Project-12345.pdf")
        if pdf_text:
            scraped.append(Document(page_content=pdf_text))

        chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(scraped)

        if os.path.exists("faiss_db"):
            return FAISS.load_local("faiss_db", OpenAIEmbeddings(), allow_dangerous_deserialization=True).as_retriever(search_kwargs={"k": 3})
        db = FAISS.from_documents(chunks, OpenAIEmbeddings())
        db.save_local("faiss_db")
        return db.as_retriever(search_kwargs={"k": 3})

    def detect_query_type(self, user_input):
        if user_input.strip().lower() in ["yes", "no"]:
            return "application" if self.is_collecting_info or self.awaiting_permission or self.awaiting_save_permission or self.awaiting_contact_info else "general"

        recent_history = "\n".join(
            [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
        ) if self.chat_memory else ""

        prompt = f"""
You are an intelligent classifier for a mortgage assistant chatbot.

Classify the following user input into one of these three types:
- application → if the user is trying to apply or give their personal or financial details.
- information → if the user is asking about mortgage concepts, terms, policies, or loan types.
- general → if it's small talk, unrelated, or casual.

Recent conversation history (for context):
{recent_history}

Examples:
- "I have £75,000 saved" → application
- "What is a mortgage?" → information
- "Hello, how are you?" → general
- "How much can I borrow?" → application
- "Tell me about fixed-rate mortgages" → information
- "My name is Kevin" → application
- "What are current interest rates?" → information

Just return one of: "application", "information", or "general". Respond with only one word.

User input: "{user_input}"
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        classification = response.content.strip().lower()

        print(f"DEBUG: Input '{user_input}' classified as: {classification}")
        return classification if classification in ["application", "information", "general"] else "general"

    def generate_relevant_question(self, user_input):
        prompt = f"""
You are a mortgage assistant chatbot. The user has provided an input related to a mortgage application: "{user_input}". Instead of asking a standard application question, generate a relevant, engaging question that aligns with their input to continue the conversation naturally. For example:
- If the user says "I want to buy a house," ask something like "What type of house are you looking to buy?"
- If the user says "I have £50,000 saved," ask something like "Is that your deposit, or are you planning to save more?"

Ensure the question is concise, relevant to the UK mortgage market, and encourages the user to provide more details.

Generated question: 
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()

    def generate_response_to_relevant_question(self, user_input, question):
        prompt = f"""
You are a mortgage assistant chatbot. The user was asked: "{question}" and responded with: "{user_input}". Generate a concise, friendly response that acknowledges their answer and aligns with the UK mortgage market. For example:
- If the user says "A flat" to "What type of house are you looking to buy?", respond with something like "Great, a flat sounds perfect! Are you looking in a specific area?"
- If the user says "£50,000 deposit" to "Is that your deposit?", respond with something like "That's a solid deposit! Are you planning to buy soon?"

Response: 
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()

    def extract_info(self, user_input):
        last_question = self.chat_memory[-2]["ai"] if len(self.chat_memory) >= 2 and "ai" in self.chat_memory[-2] else ""
        prompt = f"""
You are extracting information for a mortgage application. Based on the previous question and the user's response, identify the relevant field and value. The fields are: {', '.join(self.fields + ['email', 'phone_number'])}.

Previous question: {last_question}
Existing info:
{json.dumps(asdict(self.applicant), indent=2)}

User response: {user_input}

If the response is "yes" or "no", translate it to boolean true/false.
Output a JSON object with exactly two keys: \"field\" and \"value\".
If no relevant information is found, return {{\"field\": null, \"value\": null}}.
"""
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            parsed = json.loads(response.content.strip())
            print(f"DEBUG: extract_info output: {parsed}")
            return parsed.get("field"), parsed.get("value")
        except:
            print(f"DEBUG: extract_info failed to parse: {response.content}")
            return None, None

    def update_field(self, field, value):
        if field in asdict(self.applicant).keys():
            setattr(self.applicant, field, value)
            if field in self.fields:
                self.asked_fields.add(field)
            self.last_asked_field = field

    def generate_summary(self):
        questions = self.get_questions()
        applicant_info = asdict(self.applicant)
        info_summary = "\n".join([f"{questions[field]}: {applicant_info[field]}" for field in self.fields if applicant_info[field]])

        prompt = f"""
You are a mortgage assistant chatbot. Below is the information collected from a user during a mortgage application, including the questions asked and their answers:

{info_summary}

Generate a concise summary of the user's mortgage application details in a professional tone, suitable for the UK mortgage market. The summary should include all provided details in a clear, structured format.

Summary:
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()

    def ask_next_question(self):
        for field in self.fields:
            if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
                self.last_asked_field = field
                return self.get_questions()[field]
        return self.finalize_application()

    def get_questions(self):
        return {
            "application_type": "Is this a single person application or are you a partnership? i.e married, civil partnership or living together.",
            "first_time_buyer": "Are you a first-time buyer?",
            "dob": "Please can you give me your date of birth and your partner's, if applicable.",
            "employment_status": "Are you in employment?",
            "employment_type": "If yes, please specify if you are employed or self-employed?",
            "income": "How much do you earn per year, gross pay before tax and NI, also include any commission, bonus, overtime and any other income sources.",
            "credit_commitments": "Please can you tell me if you have any credit commitments, if yes please list them, examples are credit cards, loans or even other mortgage payments and pensions.",
            "dependants": "How many dependants do you have, if any?",
            "adverse_credit": "If you have adverse credit, please tell me what it is?",
            "property_sale_info": "Do you have an existing property that you plan to sell to support your new mortgage? If yes – what is it worth, how much do you have outstanding on the mortgage and what do you hope to sell it for?",
            "expenditure": "Finally, what is your committed expenditure. Examples are maintenance, school fees & nursery costs.",
            "email": "Please provide your email address for future updates.",
            "phone_number": "Please provide your contact number."
        }

    def finalize_application(self):
        summary = self.generate_summary()
        self.awaiting_save_permission = True
        return f"Here is a summary of your application:\n{summary}\n\nMay I save this information to proceed with your mortgage application?"

    def save_lead(self):
        with open("leads.json", "a") as f:
            json.dump(asdict(self.applicant), f)
            f.write("\n")

    def post_process_response(self, response):
        response = response.replace("broker", "mortgage advisor")
        response = response.replace("mortgage advisor", "one of our free, CEMAP qualified mortgage advisors")
        response = response.replace("$", "£")
        return response

    def answer_info_question(self, user_input):
        if "mortgage rate" in user_input.lower() or "interest rate" in user_input.lower():
            return self.post_process_response(
                "For the most accurate and up-to-date information on current mortgage rates in the UK, "
                "I recommend raising this with one of our free, qualified mortgage advisors who will "
                "be contacting you shortly to tailor a personalised quote based on the information you have given me."
            )

        if "qualified mortgage advisors" in user_input.lower():
            return self.post_process_response(
                "Yes, we have free, CEMAP qualified mortgage advisors on hand at any time. "
                "Please provide your email and phone number, and I will have them contact you. "
                "Alternatively, feel free to ask me anything related to mortgages."
            )

        if "how much can I borrow" in user_input.lower():
            return self.post_process_response(
                "To provide an accurate estimate of how much you can borrow, I’ll need to collect some additional information. "
                "May I ask a few questions to assist you further?"
            )

        context_docs = self.retriever.invoke(user_input)
        context_text = "\n".join([doc.page_content for doc in context_docs])
        
        recent_history = "\n".join(
            [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
        ) if self.chat_memory else ""

        prompt = f"""
You are a helpful mortgage advisor for a UK-based company. Always use pounds (£) as the currency and refer to 'one of our free, CEMAP qualified mortgage advisors' instead of 'mortgage advisor' or 'broker.' 
Never suggest external advisors, brokers, or lenders. Be concise and focus on the UK mortgage market.

Knowledge from web sources:
{context_text}

Recent conversation history (for context):
{recent_history}

User asked:
{user_input}

Answer with context where possible. Be concise. If the input is vague or incomplete, ask for clarification.
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        reply = self.post_process_response(response.content)

        # If application is in progress, prompt to continue collecting information
        application_in_progress = any(getattr(self.applicant, field) for field in self.fields)
        if application_in_progress:
            self.awaiting_continue_confirmation = True
            reply += "\nWould you like to continue with your mortgage application?"

        return reply

    def process_input(self, user_input):
        self.chat_memory.append({"user": user_input})
        query_type = self.detect_query_type(user_input)

        is_application_mode = (
            len(self.chat_memory) > 1
            and "ai" in self.chat_memory[-2]
            and any(self.get_questions()[field] in self.chat_memory[-2]["ai"] for field in self.fields + ["email", "phone_number"])
        )

        application_in_progress = any(getattr(self.applicant, field) for field in self.fields)

        if self.awaiting_save_permission:
            if user_input.lower() in ["yes", "ok", "sure"]:
                self.awaiting_save_permission = False
                self.awaiting_contact_info = True
                self.last_asked_field = "email"
                reply = self.get_questions()["email"]
            else:
                self.awaiting_save_permission = False
                reply = "Thank you for your application. If you have any more questions or wish to proceed later, feel free to let me know!"
        elif self.awaiting_contact_info:
            field, value = self.extract_info(user_input)
            if field == "email" and value:
                self.update_field(field, value)
                self.last_asked_field = "phone_number"
                reply = self.get_questions()["phone_number"]
            elif field == "phone_number" and value:
                self.update_field(field, value)
                self.save_lead()
                self.awaiting_contact_info = False
                reply = ("Thank you for your response, I will now forward your information to one of our free, CEMAP qualified mortgage advisors "
                         "who will take over from here. It’s been great speaking with you and good luck with your house buying journey. Goodbye")
            else:
                reply = f"Sorry, I didn't understand. Could you answer: {self.get_questions()[self.last_asked_field]}"
        elif self.awaiting_permission:
            if user_input.lower() in ["yes", "ok", "sure"]:
                self.is_collecting_info = True
                self.awaiting_permission = False
                reply = self.ask_next_question()
            else:
                self.awaiting_permission = False
                reply = "Okay, let me know when you're ready to provide more details or if you have other questions!"
        elif self.awaiting_relevant_response:
            response = self.generate_response_to_relevant_question(user_input, self.last_relevant_question)
            reply = f"{response} May I collect some information from you to assist with your mortgage application?"
            self.awaiting_relevant_response = False
            self.awaiting_permission = True
        elif self.awaiting_continue_confirmation:
            if user_input.lower() in ["yes", "continue", "ok"]:
                self.is_collecting_info = True
                self.awaiting_continue_confirmation = False
                reply = self.ask_next_question()
            else:
                self.awaiting_continue_confirmation = False
                reply = "Okay! Let me know if you need anything else."
        elif query_type == "application" and not self.is_collecting_info and not application_in_progress:
            relevant_question = self.generate_relevant_question(user_input)
            self.last_relevant_question = relevant_question
            reply = relevant_question
            self.awaiting_relevant_response = True
        elif query_type == "information":
            self.is_collecting_info = False
            reply = self.answer_info_question(user_input)
        elif query_type == "application" or (query_type == "general" and is_application_mode):
            field, value = self.extract_info(user_input)
            print(f"DEBUG: process_input - field: {field}, value: {value}")
            if field is not None and value is not None:
                self.update_field(field, value)
                reply = self.ask_next_question()
            else:
                reply = f"Sorry, I didn't understand. Could you answer: {self.get_questions()[self.last_asked_field]}"
        else:
            self.is_collecting_info = False
            prompt = f"""
Be a helpful, friendly mortgage assistant for a UK-based company. Always use pounds (£) and refer to 'one of our free, CEMAP qualified mortgage advisors.' Answer this:
{user_input}
"""
            reply = self.post_process_response(self.llm.invoke([HumanMessage(content=prompt)]).content)

        self.chat_memory.append({"ai": reply})
        self.last_query_type = query_type
        return reply

if __name__ == '__main__':
    bot = MortgageAdvisorBot()
    print("\n\U0001F3E1 Welcome to the Unified AI Mortgage Advisor! Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\n\U0001F44B Goodbye! Stay financially wise!")
            break
        response = bot.process_input(user_input)
        print(f"\n\U0001F916 AI: {response}")
















