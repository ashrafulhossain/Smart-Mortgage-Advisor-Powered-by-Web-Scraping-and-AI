
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
#     income: str = None
#     credit_commitments: str = None
#     dependants: str = None
#     adverse_credit: str = None
#     property_sale_info: str = None
#     expenditure: str = None

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
#             "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
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

#         prompt = f"""
# You are an intelligent classifier for a mortgage assistant chatbot.

# Classify the following user input into one of these three types:
# - application → if the user is trying to apply or give their personal or financial details.
# - information → if the user is asking about mortgage concepts, terms, policies, or loan types.
# - general → if it's small talk, unrelated, or casual.

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
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         try:
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

#     def ask_next_question(self):
#         for field in self.fields:
#             if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
#                 self.last_asked_field = field
#                 return self.get_question(field)
#         return self.generate_summary()

#     def get_question(self, field):
#         questions = {
#             "application_type": "Is this a single person application or joint (married, etc.)?",
#             "first_time_buyer": "Are you a first-time buyer?",
#             "dob": "What is your date of birth (and partner's if applicable)?",
#             "employment_status": "Are you employed or self-employed?",
#             "income": "What is your annual income before tax (include bonuses, commission etc.)?",
#             "credit_commitments": "List any credit commitments (loans, cards, etc.)",
#             "dependants": "How many dependants do you have?",
#             "adverse_credit": "Do you have any adverse credit history?",
#             "property_sale_info": "Are you selling a property? What's it worth and what is outstanding?",
#             "expenditure": "Any fixed monthly expenses (school, maintenance etc.)?",
#         }
#         return questions.get(field, f"Please provide your {field}")

#     def generate_summary(self):
#         prompt = f"""
# Summarize this applicant's mortgage profile:
# {json.dumps(asdict(self.applicant), indent=2)}
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content

#     def answer_info_question(self, user_input):
#         context_docs = self.retriever.invoke(user_input)
#         context_text = "\n".join([doc.page_content for doc in context_docs])
#         prompt = f"""
# You are a helpful mortgage advisor.
# Knowledge:
# {context_text}

# User asked:
# {user_input}

# Answer with context where possible. Be concise.
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content

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
#             if application_in_progress:
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
# Be a helpful, friendly mortgage assistant. Answer this:
# {user_input}
# """
#             reply = self.llm.invoke([HumanMessage(content=prompt)]).content

#         self.chat_memory.append({"ai": reply})
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
#     income: str = None
#     credit_commitments: str = None
#     dependants: str = None
#     adverse_credit: str = None
#     property_sale_info: str = None
#     expenditure: str = None

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
#             "https://moneytothemasses.com/owning-a-home/mortgages/the-10-most-popular-mortgage-questions"
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
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         try:
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

#     def ask_next_question(self):
#         for field in self.fields:
#             if getattr(self.applicant, field) in (None, "") and field not in self.asked_fields:
#                 self.last_asked_field = field
#                 return self.get_question(field)
#         return self.generate_summary()

#     def get_question(self, field):
#         questions = {
#             "application_type": "Is this a single person application or joint (married, etc.)?",
#             "first_time_buyer": "Are you a first-time buyer?",
#             "dob": "What is your date of birth (and partner's if applicable)?",
#             "employment_status": "Are you employed or self-employed?",
#             "income": "What is your annual income before tax (include bonuses, commission etc.)?",
#             "credit_commitments": "List any credit commitments (loans, cards, etc.)",
#             "dependants": "How many dependants do you have?",
#             "adverse_credit": "Do you have any adverse credit history?",
#             "property_sale_info": "Are you selling a property? What's it worth and what is outstanding?",
#             "expenditure": "Any fixed monthly expenses (school, maintenance etc.)?",
#         }
#         return questions.get(field, f"Please provide your {field}")

#     def generate_summary(self):
#         prompt = f"""
# Summarize this applicant's mortgage profile:
# {json.dumps(asdict(self.applicant), indent=2)}
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content

#     def answer_info_question(self, user_input):
#         context_docs = self.retriever.invoke(user_input)
#         context_text = "\n".join([doc.page_content for doc in context_docs])
        
#         recent_history = "\n".join(
#             [f"User: {m['user']}\nAI: {m['ai']}" for m in self.chat_memory[-4:] if "user" in m and "ai" in m]
#         ) if self.chat_memory else ""

#         prompt = f"""
# You are a helpful mortgage advisor.
# Knowledge from web sources:
# {context_text}

# Recent conversation history (for context):
# {recent_history}

# User asked:
# {user_input}

# Answer with context where possible. Be concise. If the input is vague or incomplete, ask for clarification.
# """
#         response = self.llm.invoke([HumanMessage(content=prompt)])
#         return response.content

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
# Be a helpful, friendly mortgage assistant. Answer this:
# {user_input}
# """
#             reply = self.llm.invoke([HumanMessage(content=prompt)]).content

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





