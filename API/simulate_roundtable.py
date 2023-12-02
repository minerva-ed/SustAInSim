#### RUN THIS TO INSTALL PKGS ########
# This comment indicates that the following line is a shell command to install necessary packages
# python -m pip install semantic-kernel
######################################

# Import necessary packages
import semantic_kernel as sk  # Import the semantic_kernel library
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion  # Import OpenAIChatCompletion from the semantic_kernel library
from semantic_kernel import PromptTemplateConfig, PromptTemplate, SemanticFunctionConfig  # Import additional classes from semantic_kernel
from sklearn.feature_extraction.text import TfidfVectorizer  # Import TfidfVectorizer for text vectorization
from sklearn.metrics.pairwise import cosine_similarity  # Import cosine_similarity for computing similarity between texts
import random  # Import random module for generating random numbers
import time  # Import time module for time-related tasks
import asyncio
import pdfplumber
import xlrd
from textblob import TextBlob
import os
import asyncio

# Data Ingestion: Function to read data from PDF and Excel files
def load(file_paths):
    data = ""
    for file_path in file_paths:
        temp_data = f"{file_path} has the following data"
        if file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                data = data +temp_data + '\n'.join([page.extract_text() for page in pdf.pages])
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            workbook = xlrd.open_workbook(file_path)
            sheet = workbook.sheet_by_index(0)
            data = data + temp_data + '\n'.join([' '.join(map(str, sheet.row_values(row))) for row in range(sheet.nrows)])
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf8') as txt_file:
                data += temp_data + '\n'+ txt_file.readlines()
        else:
            data.append(temp_data + "This Data Cannot be parsed")
    return data

# Prepare OpenAI service using credentials stored in the `.env` file
api_key, org_id = sk.openai_settings_from_dot_env()  # Retrieve API key and organization ID from a .env file

# Define a function to calculate cosine similarity between two texts
def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()  # Initialize a TfidfVectorizer
    tfidf_matrix = vectorizer.fit_transform([text1, text2])  # Transform the texts into TF-IDF matrix
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]  # Return the cosine similarity score

# Define a class to represent an Admin Agent that is part of the discussion
class AdminDiscussionAgent:
    def __init__(self, department):
        self.notes = None  # Initialize notes attribute to None
        self.kernel = sk.Kernel()  # Initialize a semantic kernel
        self.kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))  # Add OpenAI chat service to the kernel
        self.department = department
        
    # Method to upload notes
    def upload_notes(self, notes):
        self.notes = notes  # Set the notes attribute

    # Async method to answer a question
    async def discuss(self, comment):
        # Create and execute a semantic function to provide an answer
        return self.kernel.create_semantic_function(f"""You are the Director of {self.department} Provide your opinion or take to the following comment received following the summary of {self.notes}: {comment}? Answer concisely.""", temperature=0.8)()

# Define a class to represent an Admin Agent that is part of the discussion
class ProfessorDiscussionAgent:
    def __init__(self, department, track):
        self.notes = None  # Initialize notes attribute to None
        self.kernel = sk.Kernel()  # Initialize a semantic kernel
        self.kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))  # Add OpenAI chat service to the kernel
        self.department = department
        self.track = track
        
    # Method to upload notes
    def upload_notes(self, notes):
        self.notes = notes  # Set the notes attribute

    # Async method to answer a question
    async def discuss(self, comment):
        # Create and execute a semantic function to provide an answer
        return self.kernel.create_semantic_function(f"""You are the professor of {self.department} on track of {self.track}. Provide your opinion or take to the following comment received following the summary of {self.notes}: {comment}? Answer concisely.""", temperature=0.8)()

# Define a class to represent an Admin Agent that is part of the discussion
class EnvironmentalistDiscussionAgent:
    def __init__(self):
        self.notes = None  # Initialize notes attribute to None
        self.kernel = sk.Kernel()  # Initialize a semantic kernel
        self.kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))  # Add OpenAI chat service to the kernel
        
    # Method to upload notes
    def upload_notes(self, notes):
        self.notes = notes  # Set the notes attribute

    # Async method to answer a question
    async def discuss(self, comment):
        # Create and execute a semantic function to provide an answer
        return self.kernel.create_semantic_function(f"""You are an Environmentalist with legal background, and nature's best interests are your best interests. Represent Mountains, lakes, and forests nearby as appropriate to the ongoing discussion. Provide your opinion or take to the following comment received following the summary of {self.notes}: {comment}? Answer concisely.""", temperature=0.8)()

# Define a class to represent a Student Agent
class StudentDiscussionAgent:
    def __init__(self, socioeconomic_background, politicial_background, educational_background):
        self.socioeconomic_background = socioeconomic_background
        self.politicial_background = politicial_background
        self.educational_background = educational_background  # Set the educational background (e.g., Liberal Arts, Engineering, Pure Researcher)
        self.notes = None
        self.kernel = sk.Kernel()  # Initialize a semantic kernel
        self.kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))  # Add OpenAI chat service to the kernel

    # Method to upload notes
    def upload_notes(self, notes):
        self.notes = notes  # Set the notes attribute
        
    # Async method to generate questions from a lecture content
    async def discuss(self, comment):
        # Create and execute a semantic function to generate questions
        return self.kernel.create_semantic_function(f"""As a student, you went through the following {self.notes}: Pretend that you are a student with educational background of {self.educational_background}, political background of {self.political_background}, and socio-economic background of {self.socioeconomic_background}. Pretend to be the student described above learning from this discussion, and someone just made this comment {comment}. State one succinct comment/opinion/question you have about this lecture and explain to the audience where your confusion originated from, and make sure it is concise though. If you do not want to say anything respond by saying -1""", max_tokens=200, temperature=0.5)()

# Define a class to represent a General Agent
class GeneralAgent:
    def __init__(self):
        self.kernel = sk.Kernel()  # Initialize a semantic kernel
        self.kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-4-1106-preview", api_key, org_id))  # Add OpenAI chat service to the kernel
    
    # Async method to generate a summary of discussion
    async def generate_summary(self, discussion_notes):
        # Create and execute a semantic function to generate a summary
        return self.kernel.create_semantic_function(f"""Give a succinct summary of overall discussion so far at the round table and how does each others' contributions shaped it: {discussion_notes}.""")()

# Coroutine to simulate a roundtable discussion session
async def simulate_roundtable_discussion(agents, general_agent):
    content = load(["./project_summary.pdf"])
    for agent in agents:
        agent.upload_notes(f"""Here are some key resources for the discussion at hand: {content}""")  # Upload content

    discussion_notes = []  # Initialize an array to store discussion notes
    for agent in agents:
        response = await agent.discuss(str(discussion_notes))
        discussion_notes.append({"agent": str(agent), "response": response.result})
    
    # General Agent provides a summary
    summary = await general_agent.generate_summary(discussion_notes)
    discussion_notes.append({"agent": "General Summarizer", "comment": "Summary of the discussion so far is:", "response": summary.result})

    return discussion_notes  # Return the discussion notes

# Coroutine to simulate a classroom-style discussion environment
async def simulate_room():
    start_time = time.time()  # Record the start time

    # Instantiate Agents
    agents = [AdminDiscussionAgent("Office of Financial Planning and Operating Budget"),
              StudentDiscussionAgent("Middle-Class", "Liberal", "English and Political Science"),
              StudentDiscussionAgent("High-Income", "Conservative", "Economics, Math, CS, and Statistics"),
              StudentDiscussionAgent("Low-Income", "Conservative", "Environmental Studies and Law"),
              ProfessorDiscussionAgent("CS an Math", "Tenured"),
              ProfessorDiscussionAgent("LJST", "Lecturer"),
              EnvironmentalistDiscussionAgent()]

    general_agent = GeneralAgent()

    # Simulate the roundtable discussion
    roundtable_discussion_notes = await simulate_roundtable_discussion(agents, general_agent)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    return roundtable_discussion_notes  # Return the discussion notes


# Execute the main function if this script is run as the main module
if __name__ == "__main__":
    import asyncio  # Import asyncio for asynchronous execution
    asyncio.run(simulate_room())  # Run the simulate_classroom coroutine
