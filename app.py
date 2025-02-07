# from flask import Flask, request, jsonify, session, render_template
# import os
# import logging
# from dotenv import load_dotenv
# from datetime import datetime
# import pandas as pd
# import uuid
# import threading
# from langchain.schema import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.messages import SystemMessage, HumanMessage

# load_dotenv()

# app = Flask(__name__)
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# csv_lock = threading.Lock()

# PROGRAMS = {
#     '1': 'Kids Program',
#     '2': 'Adults Program',
#     '3': 'Ladies-Only Aqua Fitness',
#     '4': 'Baby & Toddler Program',
#     '5': 'Special Needs Program'
# }

# uid = 'postgres'
# pwd = 'ahmed'
# server = "172.27.249.6"
# database = "sample"

# def get_main_menu():
#     return {
#         "text": "👋 Welcome to Aquasprint Swimming Academy!\n\nChoose an option:",
#         "options": [
#             {"value": "1", "label": "Book a Class"},
#             {"value": "2", "label": "Program Information"},
#             {"value": "3", "label": "Location & Hours"},
#             {"value": "4", "label": "Contact Us"},
#             {"value": "5", "label": "Talk to AI Agent"}
#         ]
#     }

# import psycopg2
# from psycopg2 import sql

# def save_inquiry(data):
#     """ Save inquiry data to PostgreSQL database """
#     conn = None
#     try:
#         conn = psycopg2.connect(
#             dbname=database,
#             user=uid,
#             password=pwd,
#             host=server
#         )
#         cur = conn.cursor()
        
#         query = sql.SQL("""
#             INSERT INTO inquiries (program, name, phone, email, timestamp)
#             VALUES (%s, %s, %s, %s, %s)
#         """)
        
#         cur.execute(query, (
#             data['program'],
#             data['name'],
#             data['phone'],
#             data['email'],
#             data['timestamp']
#         ))
        
#         conn.commit()
#         cur.close()
#     except Exception as e:
#         logger.error(f"Save failed: {str(e)}")
#         raise
#     finally:
#         if conn is not None:
#             conn.close()

# @app.route('/')
# def chat_interface():
#     session['session_id'] = str(uuid.uuid4())
#     session['state'] = 'MAIN_MENU'
#     return render_template('chat.html')

# @app.route('/send_message', methods=['POST'])
# def handle_message():
#     user_input = request.json.get('message', '').strip()
#     session_id = session.get('session_id')
#     current_state = session.get('state', 'MAIN_MENU')

#     response = process_message(user_input, current_state, session_id)

#     if response is None:
#         return jsonify({
#             "text": "⚠️ An error occurred while processing your request. Please try again or type 'menu'"
#         })

#     if "new_state" in response:
#         session['state'] = response.get('new_state', 'MAIN_MENU')

#     return jsonify(response)

# def process_message(message, current_state, session_id):
#     try:
#         logger.info(f"Processing message: {message}, Current state: {current_state}, Session ID: {session_id}")

#         if message.lower() == 'menu':
#             return {
#                 "text": get_main_menu()['text'],
#                 "options": get_main_menu()['options'],
#                 "new_state": 'MAIN_MENU'
#             }
            
#         if current_state == 'MAIN_MENU':
#             return handle_main_menu(message)
#         elif current_state == 'PROGRAM_SELECTION':
#             return handle_program_selection(message)
#         elif current_state == 'PROGRAM_INFO':
#             return handle_program_info(message)
#         elif current_state == 'BOOKING_PROGRAM':
#             return handle_booking(message)
#         elif current_state == 'AI_QUERY':
#             return handle_ai_query(message)
#         else:
#             logger.error(f"Unknown state: {current_state}")
#             return {"text": "⚠️ Unknown state. Please try again or type 'menu'"}
            
#     except Exception as e:
#         logger.error(f"Error processing message: {e}")
#         return {"text": "⚠️ An error occurred. Please try again or type 'menu'"}

# def handle_main_menu(message):
#     if message == '1':
#         return {
#             "text": "Choose program:",
#             "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
#             "new_state": 'PROGRAM_SELECTION'
#         }
#     elif message == '2':
#         return {
#             "text": "Choose program for details:",
#             "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
#             "new_state": 'PROGRAM_INFO'
#         }
#     elif message == '3':
#         return {
#             "text": ("🏊‍♂️ Aquasprint Swimming Academy\n\n"
#                      "📍 Location: The Sustainable City, Dubai\n"
#                      "⏰ Hours: Daily 6AM-10PM\n"
#                      "📞 +971542502761\n"
#                      "📧 info@aquasprint.ae"),
#             "options": [{"value": "menu", "label": "Return to Menu"}]
#         }
#     elif message == '4':
#         return {
#             "text": ("📞 Contact Us:\n"
#                      "Call us at +971542502761\n"
#                      "Email: info@aquasprint.ae"),
#             "options": [{"value": "menu", "label": "Return to Menu"}]
#         }
#     elif message == '5':
#         return {
#             "text": "Ask me anything about our programs!",
#             "new_state": 'AI_QUERY'
#         }
#     else:
#         return get_main_menu()

# def handle_program_info(message):
#     """ Handles the display of program information based on user choice """
#     program = PROGRAMS.get(message)
#     if program:
#         details = {
#             '1': "👶 Kids Program (4-14 years)\n- 8 skill levels\n- Certified instructors",
#             '2': "🏊 Adults Program\n- Beginner to advanced\n- Flexible scheduling",
#             '3': "🚺 Ladies-Only Aqua Fitness\n- Women-only sessions\n- Full-body workout",
#             '4': "👶👨👩 Baby & Toddler\n- Parent-child classes\n- Water safety basics",
#             '5': "🌟 Special Needs Program\n- Adapted curriculum\n- Individual attention"
#         }.get(message, "Program details not available")
        
#         return {
#             "text": f"{program} Details:\n{details}",
#             "options": [{"value": "menu", "label": "Return to Menu"}],
#             "new_state": "MAIN_MENU"
#         }
#     else:
#         return {
#             "text": "Invalid choice. Please select 1-5",
#             "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
#             "new_state": 'PROGRAM_INFO'
#         }

# def handle_program_selection(message):
#     """ Prepares for booking by capturing the selected program """
#     program = PROGRAMS.get(message)
#     if program:
#         session['booking_data'] = {'program': program}
#         session['booking_step'] = 'GET_NAME'
#         return {
#             "text": f"Selected program: {program}\nWhat's your full name?",
#             "new_state": 'BOOKING_PROGRAM'
#         }
#     else:
#         return {
#             "text": "Invalid program selection. Please choose 1-5",
#             "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
#             "new_state": 'PROGRAM_SELECTION'
#         }

# def handle_booking(message):
#     """ Handles the multi-step booking process """
#     try:
#         current_step = session.get('booking_step', 'GET_NAME')
#         booking_data = session.get('booking_data', {})

#         logger.info(f"Booking Step: {current_step}, Message: {message}")

#         if current_step == 'GET_NAME':
#             booking_data['name'] = message
#             session['booking_step'] = 'GET_PHONE'
#             session['booking_data'] = booking_data
#             return {"text": "📱 What's your phone number?"}

#         elif current_step == 'GET_PHONE':
#             booking_data['phone'] = message
#             session['booking_step'] = 'GET_EMAIL'
#             session['booking_data'] = booking_data
#             return {"text": "📧 What's your email address?"}

#         elif current_step == 'GET_EMAIL':
#             booking_data['email'] = message
#             booking_data['timestamp'] = datetime.now().isoformat()

#             save_inquiry(booking_data)

#             confirmation = (
#                 "✅ Booking confirmed!\n"
#                 f"Program: {booking_data.get('program')}\n"
#                 f"Name: {booking_data.get('name')}\n"
#                 f"Phone: {booking_data.get('phone')}\n"
#                 f"Email: {booking_data.get('email')}\n\n"
#                 "We'll contact you soon!"
#             )

#             session.pop('booking_data', None)
#             session.pop('booking_step', None)

#             return {
#                 "text": confirmation,
#                 "options": [{"value": "menu", "label": "Return to Menu"}],
#                 "new_state": 'MAIN_MENU'
#             }

#         return {"text": "Invalid booking step. Type 'menu' to start over."}

#     except Exception as e:
#         logger.error(f"Booking error: {str(e)}")
#         return {"text": "⚠️ Booking failed. Type 'menu' to restart."}

# def handle_ai_query(message):
#     """Uses RAG with Ollama API to handle AI queries about swimming programs"""
#     try:
#         embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
#         vector_store = Chroma(
#             collection_name="example_collection",
#             embedding_function=embeddings,
#             persist_directory="chroma_db"
#         )
#         retriever = vector_store.as_retriever(search_kwargs={'k': 100})

#         docs = retriever.invoke(message)
        
#         knowledge = "\n\n".join([doc.page_content.strip() for doc in docs])
#         knowledge += "\n\nEnd of knowledge base."

#         print(knowledge)

#         llm = ChatOpenAI(
#             model="deepseek-llm",
#             base_url="http://172.27.240.1:11434/v1",
#             verbose=True,
#             temperature=0.1
#         )

#         messages = [
#             SystemMessage(
#             content=f"""You're an expert assistant for Aquasprint Swimming Academy. Follow these rules:
#             1. Answer ONLY using the knowledge base below
#             2. Be concise and professional
#             3. If unsure, say "I don't have that information"
#             4. Never make up answers

#             Knowledge Base:
#             {knowledge}"""
#             ),
#             HumanMessage(content=message)
#         ]

#         ai_response = llm.invoke(messages)
#         response_text = ai_response.content

#         return {
#             "text": f"🤖 AI Agent:\n{response_text}",
#             "options": [{"value": "menu", "label": "Return to Menu"}]
#         }
    
#     except Exception as e:
#         logger.error(f"AI Query Failed: {e}")
#         return {"text": "Our AI agent is currently busy. Please try again later."}


# if __name__ == '__main__':
#     app.run(port=5000)




# from flask import Flask, request, jsonify, session, render_template
# import os
# import logging
# from dotenv import load_dotenv
# from datetime import datetime
# import psycopg2
# from psycopg2 import sql
# import threading
# import uuid
# from langgraph.graph import StateGraph
# from langchain_core.messages import SystemMessage, HumanMessage
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langgraph.checkpoint.sqlite import SqliteSaver
# from dataclasses import dataclass, field
# from langgraph.graph import StateGraph
# from pydantic import BaseModel
# from typing import Optional
# from langgraph.graph import StateGraph
# from pydantic import BaseModel
# from typing import Optional, TypedDict, Literal
# from dataclasses import dataclass, field

# load_dotenv()

# app = Flask(__name__)
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# csv_lock = threading.Lock()

# PROGRAMS = {
#     '1': 'Kids Program',
#     '2': 'Adults Program',
#     '3': 'Ladies-Only Aqua Fitness',
#     '4': 'Baby & Toddler Program',
#     '5': 'Special Needs Program'
# }

# DB_CREDENTIALS = {
#     'dbname': 'sample',
#     'user': 'postgres',
#     'password': 'ahmed',
#     'host': '172.27.249.6'
# }

# # Define valid next states
# class SupervisorOutput(TypedDict):
#     next_state: Literal["tool_agent", "rag_agent"]

# class AppState(BaseModel):
#     input: str
#     session_data: dict = field(default_factory=dict)
#     output: Optional[str] = None

# def supervisor(state: AppState) -> SupervisorOutput:
#     user_input = state.input
#     if "book" in user_input.lower() or "register" in user_input.lower():
#         return {"next_state": "tool_agent"}  # Return dictionary
#     return {"next_state": "rag_agent"}  # Return dictionary


# # RAG Agent Function
# def rag_agent(state: AppState):
#     user_input = state.input
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
#     vector_store = Chroma(collection_name="example_collection", embedding_function=embeddings, persist_directory="chroma_db")
#     retriever = vector_store.as_retriever(search_kwargs={'k': 100})
#     docs = retriever.invoke(user_input)
#     knowledge = "\n\n".join([doc.page_content.strip() for doc in docs]) + "\n\nEnd of knowledge base."

#     llm = ChatOpenAI(model="deepseek-llm", base_url="http://172.27.240.1:11434/v1", temperature=0.1)
#     messages = [
#         SystemMessage(content=f"""You're an expert assistant for Aquasprint Swimming Academy. Use ONLY the knowledge base below:
#         {knowledge}"""),
#         HumanMessage(content=user_input)
#     ]
#     response = llm.invoke(messages).content
#     return AppState(output=f"🤖 AI Agent: {response}", session_data=state.session_data)

# # Tool Agent (Booking Handler)
# def tool_agent(state: AppState):
#     user_input = state.input
#     session_data = state.session_data
#     booking_step = session_data.get("booking_step", "GET_NAME")

#     if booking_step == "GET_NAME":
#         session_data["name"] = user_input
#         session_data["booking_step"] = "GET_PHONE"
#         return AppState(output="📱 What's your phone number?", session_data=session_data)
    
#     elif booking_step == "GET_PHONE":
#         session_data["phone"] = user_input
#         session_data["booking_step"] = "GET_EMAIL"
#         return AppState(output="📧 What's your email address?", session_data=session_data)
    
#     elif booking_step == "GET_EMAIL":
#         session_data["email"] = user_input
#         session_data["timestamp"] = datetime.now().isoformat()
        
#         try:
#             conn = psycopg2.connect(**DB_CREDENTIALS)
#             cur = conn.cursor()
#             cur.execute(
#                 sql.SQL("""
#                     INSERT INTO inquiries (program, name, phone, email, timestamp)
#                     VALUES (%s, %s, %s, %s, %s)
#                 """),
#                 (session_data.get('program', 'General Inquiry'), session_data['name'], session_data['phone'], session_data['email'], session_data['timestamp'])
#             )
#             conn.commit()
#             cur.close()
#             conn.close()
#         except Exception as e:
#             logger.error(f"Database error: {e}")
#             return AppState(output="⚠️ Booking failed. Please try again.", session_data=session_data)
        
#         session_data.clear()
#         return AppState(output="✅ Booking confirmed! We'll contact you soon.", session_data=session_data)
    
#     return AppState(output="Invalid booking step. Type 'menu' to restart.", session_data=session_data)


# # Define LangGraph Workflow
# graph = StateGraph(AppState)
# graph.add_node("supervisor", supervisor)
# graph.add_node("rag_agent", rag_agent)
# graph.add_node("tool_agent", tool_agent)

# # Add edges without conditional logic since supervisor returns literal strings
# graph.add_edge("supervisor", "tool_agent")
# graph.add_edge("supervisor", "rag_agent")

# graph.set_entry_point("supervisor")
# graph.set_finish_point("rag_agent")
# graph.set_finish_point("tool_agent")

# graph.checkpoint_manager = SqliteSaver("chat_history.db")
# workflow = graph.compile()

# @app.route('/')
# def chat_interface():
#     session['session_id'] = str(uuid.uuid4())
#     return render_template('chat.html')

# @app.route('/send_message', methods=['POST'])
# def handle_message():
#     user_input = request.json.get('message', '').strip()
#     session_data = session.get('session_data', {})
    
#     result = workflow.invoke(AppState(
#         input=user_input,
#         session_data=session_data
#     ))
    
#     session['session_data'] = result.session_data
#     return jsonify({"text": result.output})

# if __name__ == '__main__':
#     app.run(port=5000)
























from flask import Flask, request, jsonify, session, render_template
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import uuid
import threading
from pydantic import BaseModel
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import psycopg2
from psycopg2 import sql
from typing import Optional, Dict, List
from langchain_core.messages import SystemMessage, HumanMessage



from flask import Flask, request, jsonify, session, render_template
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import uuid
import threading
import re
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

csv_lock = threading.Lock()

PROGRAMS = {
    '1': 'Kids Program',
    '2': 'Adults Program',
    '3': 'Ladies-Only Aqua Fitness',
    '4': 'Baby & Toddler Program',
    '5': 'Special Needs Program'
}

uid = 'postgres'
pwd = 'ahmed'
server = "172.27.249.6"
database = "sample"

def get_main_menu():
    return {
        "text": "👋 Welcome to Aquasprint Swimming Academy!\n\nChoose an option:",
        "options": [
            {"value": "1", "label": "Book a Class"},
            {"value": "2", "label": "Program Information"},
            {"value": "3", "label": "Location & Hours"},
            {"value": "4", "label": "Contact Us"},
            {"value": "5", "label": "Talk to AI Agent"}
        ]
    }

def save_inquiry(data):
    """ Save inquiry data to PostgreSQL database """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=uid,
            password=pwd,
            host=server
        )
        cur = conn.cursor()
        
        query = sql.SQL("""
            INSERT INTO inquiries (program, name, phone, email, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """)
        
        cur.execute(query, (
            data['program'],
            data['name'],
            data['phone'],
            data['email'],
            data['timestamp']
        ))
        
        conn.commit()
        cur.close()
    except Exception as e:
        logger.error(f"Save failed: {str(e)}")
        raise
    finally:
        if conn is not None:
            conn.close()


class BookingInfo(BaseModel):
    program: Optional[str] = Field(None, description="The swimming program name")
    name: Optional[str] = Field(None, description="Customer's full name")
    phone: Optional[str] = Field(None, description="Customer's phone number")
    email: Optional[str] = Field(None, description="Customer's email address")

def extract_booking_info(query: str) -> BookingInfo:
    """Extract booking information from a natural language query using LangChain"""
    llm = ChatOpenAI(
        model="deepseek-llm",
        base_url="http://172.27.240.1:11434/v1",
        temperature=0.1
    )
    
    parser = PydanticOutputParser(pydantic_object=BookingInfo)
    
    prompt = f"""
    Extract booking information from the following query. If information is not present, return null for that field.
    
    Query: {query}
    
    Extract these fields:
    - Program name (match to: Kids Program, Adults Program, Ladies-Only Aqua Fitness, Baby & Toddler Program, Special Needs Program), if they are unsure about its name or they have a typo, try being smart and figure out which program from the predefined list they mean.
    - Full name
    - Phone number
    - Email address
    
    {parser.get_format_instructions()}
    """
    
    messages = [
        SystemMessage(content="You are a helpful assistant that extracts booking information from text."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return parser.parse(response.content)

def get_missing_info(booking_info: BookingInfo) -> list:
    """Identify missing required booking information"""
    missing = []
    if not booking_info.program:
        missing.append('program')
    if not booking_info.name:
        missing.append('name')
    if not booking_info.phone:
        missing.append('phone')
    if not booking_info.email:
        missing.append('email')
    return missing


@app.route('/')
def chat_interface():
    session['session_id'] = str(uuid.uuid4())
    session['state'] = 'MAIN_MENU'
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def handle_message():
    user_input = request.json.get('message', '').strip()
    session_id = session.get('session_id')
    current_state = session.get('state', 'MAIN_MENU')

    response = process_message(user_input, current_state, session_id)

    if response is None:
        return jsonify({
            "text": "⚠️ An error occurred while processing your request. Please try again or type 'menu'"
        })

    if "new_state" in response:
        session['state'] = response.get('new_state', 'MAIN_MENU')

    return jsonify(response)

def process_message(message, current_state, session_id):
    try:
        logger.info(f"Processing message: {message}, Current state: {current_state}, Session ID: {session_id}")

        if message.lower() == 'menu':
            return {
                "text": get_main_menu()['text'],
                "options": get_main_menu()['options'],
                "new_state": 'MAIN_MENU'
            }
            
        if current_state == 'MAIN_MENU':
            return handle_main_menu(message)
        elif current_state == 'PROGRAM_SELECTION':
            return handle_program_selection(message)
        elif current_state == 'PROGRAM_INFO':
            return handle_program_info(message)
        elif current_state == 'BOOKING_PROGRAM':
            return handle_booking(message)
        elif current_state == 'AI_QUERY':
            return handle_ai_query(message)
        else:
            logger.error(f"Unknown state: {current_state}")
            return {"text": "⚠️ Unknown state. Please try again or type 'menu'"}
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {"text": "⚠️ An error occurred. Please try again or type 'menu'"}

def handle_main_menu(message):
    if message == '1':
        return {
            "text": "Choose program:",
            "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
            "new_state": 'PROGRAM_SELECTION'
        }
    elif message == '2':
        return {
            "text": "Choose program for details:",
            "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
            "new_state": 'PROGRAM_INFO'
        }
    elif message == '3':
        return {
            "text": ("🏊‍♂️ Aquasprint Swimming Academy\n\n"
                     "📍 Location: The Sustainable City, Dubai\n"
                     "⏰ Hours: Daily 6AM-10PM\n"
                     "📞 +971542502761\n"
                     "📧 info@aquasprint.ae"),
            "options": [{"value": "menu", "label": "Return to Menu"}]
        }
    elif message == '4':
        return {
            "text": ("📞 Contact Us:\n"
                     "Call us at +971542502761\n"
                     "Email: info@aquasprint.ae"),
            "options": [{"value": "menu", "label": "Return to Menu"}]
        }
    elif message == '5':
        return {
            "text": "Ask me anything about our programs!",
            "new_state": 'AI_QUERY'
        }
    else:
        return get_main_menu()

def handle_program_info(message):
    """ Handles the display of program information based on user choice """
    program = PROGRAMS.get(message)
    if program:
        details = {
            '1': "👶 Kids Program (4-14 years)\n- 8 skill levels\n- Certified instructors",
            '2': "🏊 Adults Program\n- Beginner to advanced\n- Flexible scheduling",
            '3': "🚺 Ladies-Only Aqua Fitness\n- Women-only sessions\n- Full-body workout",
            '4': "👶👨👩 Baby & Toddler\n- Parent-child classes\n- Water safety basics",
            '5': "🌟 Special Needs Program\n- Adapted curriculum\n- Individual attention"
        }.get(message, "Program details not available")
        
        return {
            "text": f"{program} Details:\n{details}",
            "options": [{"value": "menu", "label": "Return to Menu"}],
            "new_state": "MAIN_MENU"
        }
    else:
        return {
            "text": "Invalid choice. Please select 1-5",
            "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
            "new_state": 'PROGRAM_INFO'
        }

def handle_program_selection(message):
    """ Prepares for booking by capturing the selected program """
    program = PROGRAMS.get(message)
    if program:
        session['booking_data'] = {'program': program}
        session['booking_step'] = 'GET_NAME'
        return {
            "text": f"Selected program: {program}\nWhat's your full name?",
            "new_state": 'BOOKING_PROGRAM'
        }
    else:
        return {
            "text": "Invalid program selection. Please choose 1-5",
            "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
            "new_state": 'PROGRAM_SELECTION'
        }

def handle_booking(message: str) -> dict:
    """Handle individual booking steps"""
    try:
        current_step = session.get('booking_step')
        booking_data = session.get('booking_data', {})
        
        if not current_step:
            return {"text": "⚠️ Booking session expired. Please start over.", "new_state": 'MAIN_MENU'}
        
        field = current_step.split('_')[1].lower()
        booking_data[field] = message
        session['booking_data'] = booking_data
        
        next_missing = get_next_missing_field(booking_data)
        
        if next_missing:
            session['booking_step'] = f'GET_{next_missing.upper()}'
            prompts = {
                'program': "Which program would you like to join?",
                'name': "What's your full name?",
                'phone': "📱 What's your phone number?",
                'email': "📧 What's your email address?"
            }
            return {"text": prompts[next_missing]}
        else:
            # All information collected
            booking_data['timestamp'] = datetime.now().isoformat()
            save_inquiry(booking_data)
            
            confirmation = (
                "✅ Booking confirmed!\n"
                f"Program: {booking_data['program']}\n"
                f"Name: {booking_data['name']}\n"
                f"Phone: {booking_data['phone']}\n"
                f"Email: {booking_data['email']}\n\n"
                "We'll contact you soon!"
            )
            
            session.pop('booking_data', None)
            session.pop('booking_step', None)
            
            return {
                "text": confirmation,
                "options": [{"value": "menu", "label": "Return to Menu"}],
                "new_state": 'MAIN_MENU'
            }
            
    except Exception as e:
        logger.error(f"Booking error: {str(e)}")
        return {"text": "⚠️ Booking failed. Type 'menu' to restart."}

def extract_email(text: str) -> Optional[str]:
    """Extract email using regex pattern"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number using regex pattern"""
    phone_pattern = r'(?:\+?\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}'
    matches = re.findall(phone_pattern, text)
    return matches[0] if matches else None

def extract_program(text: str) -> Optional[str]:
    """Extract program by matching against known program names"""
    text_lower = text.lower()
    for program_id, program_name in PROGRAMS.items():
        if program_name.lower() in text_lower:
            return program_name
    return None

def get_next_missing_field(booking_data: dict) -> Optional[str]:
    """Return the next missing required field"""
    required_fields = ['program', 'name', 'phone', 'email']
    for field in required_fields:
        if not booking_data.get(field):
            return field
    return None

def handle_ai_query(message: str) -> dict:
    """Enhanced AI query handler with booking capabilities"""
    try:
        booking_keywords = ['book', 'register', 'sign up', 'enroll', 'join']
        is_booking_request = any(keyword in message.lower() for keyword in booking_keywords)
        
        if is_booking_request:
            # Extract booking information
            extracted_data = {
                'email': extract_email(message),
                'phone': extract_phone(message),
                'program': extract_program(message),
                'name': None
            }
            
            # Get or initialize booking data from session
            booking_data = session.get('booking_data', {})
            
            # Update with any new extracted information
            booking_data.update({k: v for k, v in extracted_data.items() if v is not None})
            
            # Store in session
            session['booking_data'] = booking_data
            
            # Get next missing field
            next_missing = get_next_missing_field(booking_data)
            
            if next_missing:
                # Prepare response showing what we got
                confirmed_info = []
                if booking_data.get('program'):
                    confirmed_info.append(f"Program: {booking_data['program']}")
                if booking_data.get('name'):
                    confirmed_info.append(f"Name: {booking_data['name']}")
                if booking_data.get('phone'):
                    confirmed_info.append(f"Phone: {booking_data['phone']}")
                if booking_data.get('email'):
                    confirmed_info.append(f"Email: {booking_data['email']}")
                
                info_text = "\n".join(confirmed_info) if confirmed_info else ""
                
                session['booking_step'] = f'GET_{next_missing.upper()}'
                
                prompts = {
                    'program': "Which program would you like to join?",
                    'name': "What's your full name?",
                    'phone': "📱 What's your phone number?",
                    'email': "📧 What's your email address?"
                }
                
                response_text = "Let me help you with the booking.\n\n"
                if info_text:
                    response_text += f"I've got this information:\n{info_text}\n\n"
                response_text += f"Please provide: {prompts[next_missing]}"
                
                if next_missing == 'program':
                    return {
                        "text": response_text,
                        "options": [{"value": k, "label": v} for k, v in PROGRAMS.items()],
                        "new_state": 'BOOKING_PROGRAM'
                    }
                else:
                    return {
                        "text": response_text,
                        "new_state": 'BOOKING_PROGRAM'
                    }
            else:
                # All information collected, proceed with booking
                booking_data['timestamp'] = datetime.now().isoformat()
                save_inquiry(booking_data)
                
                confirmation = (
                    "✅ Booking confirmed!\n"
                    f"Program: {booking_data['program']}\n"
                    f"Name: {booking_data['name']}\n"
                    f"Phone: {booking_data['phone']}\n"
                    f"Email: {booking_data['email']}\n\n"
                    "We'll contact you soon!"
                )
                
                session.pop('booking_data', None)
                session.pop('booking_step', None)
                
                return {
                    "text": confirmation,
                    "options": [{"value": "menu", "label": "Return to Menu"}],
                    "new_state": 'MAIN_MENU'
                }
            
        # Regular AI query handling remains the same
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=embeddings,
            persist_directory="chroma_db"
        )
        retriever = vector_store.as_retriever(search_kwargs={'k': 100})
        docs = retriever.invoke(message)
        knowledge = "\n\n".join([doc.page_content.strip() for doc in docs])
        
        llm = ChatOpenAI(
            model="deepseek-llm",
            base_url="http://172.27.240.1:11434/v1",
            temperature=0.1
        )
        
        messages = [SystemMessage(content=f"""You're an expert assistant for Aquasprint Swimming Academy. Follow these rules:
            1. Answer ONLY using the knowledge base below
            2. Be concise and professional
            3. If unsure, say "I don't have that information"
            4. Never make up answers
            5. If the user shows interest in booking, remind them they can book directly by saying something like 
               "Would you like to book a class? Just tell me your preferred program and contact details!"

            Knowledge Base:
            {knowledge}"""),
            HumanMessage(content=message)
        ]
        
        ai_response = llm.invoke(messages)
        return {
            "text": f"🤖 AI Agent:\n{ai_response.content}",
            "options": [{"value": "menu", "label": "Return to Menu"}]
        }
    
    except Exception as e:
        logger.error(f"AI Query Failed: {e}")
        return {"text": "Our AI agent is currently busy. Please try again later."}


# def handle_ai_query(message):
#     """Enhanced AI query handler with booking capabilities"""
#     try:
#         # First, check if this looks like a booking request
#         booking_keywords = ['book', 'register', 'sign up', 'enroll', 'join']
#         is_booking_request = any(keyword in message.lower() for keyword in booking_keywords)
        
#         if is_booking_request:
#             # Extract booking information from the query
#             booking_info = extract_booking_info(message)
#             missing_info = get_missing_info(booking_info)
            
#             if not missing_info:
#                 # All information is present, proceed with booking
#                 save_inquiry({
#                     'program': booking_info.program,
#                     'name': booking_info.name,
#                     'phone': booking_info.phone,
#                     'email': booking_info.email,
#                     'timestamp': datetime.now().isoformat()
#                 })
                
#                 confirmation = (
#                     "✅ Booking confirmed!\n"
#                     f"Program: {booking_info.program}\n"
#                     f"Name: {booking_info.name}\n"
#                     f"Phone: {booking_info.phone}\n"
#                     f"Email: {booking_info.email}\n\n"
#                     "We'll contact you soon!"
#                 )
                
#                 return {
#                     "text": confirmation,
#                     "options": [{"value": "menu", "label": "Return to Menu"}],
#                     "new_state": 'MAIN_MENU'
#                 }
#             else:
#                 # Some information is missing, start interactive booking
#                 session['booking_data'] = {
#                     'program': booking_info.program,
#                     'name': booking_info.name,
#                     'phone': booking_info.phone,
#                     'email': booking_info.email
#                 }
                
#                 # Determine the first missing field
#                 first_missing = missing_info[0]
#                 session['booking_step'] = f'GET_{first_missing.upper()}'
                
#                 prompts = {
#                     'program': "Which program would you like to join?\n" + "\n".join([f"{k}: {v}" for k, v in PROGRAMS.items()]),
#                     'name': "What's your full name?",
#                     'phone': "📱 What's your phone number?",
#                     'email': "📧 What's your email address?"
#                 }
                
#                 return {
#                     "text": f"I got some of your information, but I need a few more details.\n\n{prompts[first_missing]}",
#                     "new_state": 'BOOKING_PROGRAM'
#                 }
        
#         # If not a booking request, proceed with regular AI query handling
#         embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
#         vector_store = Chroma(
#             collection_name="example_collection",
#             embedding_function=embeddings,
#             persist_directory="chroma_db"
#         )
#         retriever = vector_store.as_retriever(search_kwargs={'k': 100})
        
#         docs = retriever.invoke(message)
#         knowledge = "\n\n".join([doc.page_content.strip() for doc in docs])
        
#         llm = ChatOpenAI(
#             model="deepseek-llm",
#             base_url="http://172.27.240.1:11434/v1",
#             temperature=0.1
#         )
        
#         messages = [
#             SystemMessage(
#                 content=f"""You're an expert assistant for Aquasprint Swimming Academy. Follow these rules:
#                 1. Answer ONLY using the knowledge base below
#                 2. Be concise and professional
#                 3. If unsure, say "I don't have that information"
#                 4. Never make up answers
#                 5. If the user shows interest in booking, remind them they can book directly by saying something like 
#                    "Would you like to book a class? Just tell me your preferred program and contact details!"

#                 Knowledge Base:
#                 {knowledge}"""
#             ),
#             HumanMessage(content=message)
#         ]
        
#         ai_response = llm.invoke(messages)
#         return {
#             "text": f"🤖 AI Agent:\n{ai_response.content}",
#             "options": [{"value": "menu", "label": "Return to Menu"}]
#         }
    
#     except Exception as e:
#         logger.error(f"AI Query Failed: {e}")
#         return {"text": "Our AI agent is currently busy. Please try again later."}


if __name__ == '__main__':
    app.run(port=5000)