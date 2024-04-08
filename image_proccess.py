
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import json
from langchain_core.messages import HumanMessage
import streamlit as st
from langchain_core.output_parsers import JsonOutputParser





def process_image(uploaded_front_image_path, uploaded_back_image_path):
    # Load environment variables (assuming .env file is in the same directory)
    parser = JsonOutputParser()
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        st.error("Please set the GOOGLE_API_KEY environment variable.")
        return

    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", api_key=google_api_key)

    hmessage = HumanMessage(
        content=[
            {
                "type": "text",
                "text": """These are images of a visiting card. 1st image is the front side and 2nd image is the back side of the card. Extract all information from the card and give it in a structured format. If you have any additional information about the details in the card, add them to the 'additional info'. give reposne into below given json 
                json format = {
                        "name": "",
                        "company_name": "",
                        "job_title": "",
                        "website": "",
                        "email": "",
                        "phone_number": "",
                        "office_phone_number": "",
                        "address": "",
                        "additional_info": ""
                        }
                if any feilds missing in card give cvalue none for them 
                
                """,
            },
            {"type": "image_url", "image_url": uploaded_front_image_path},
            {"type": "image_url", "image_url": uploaded_back_image_path},
        ]
    )
    response_message = llm.invoke([hmessage])
    message = response_message.content
    message = message.replace("```json", "").strip()
    message = message.replace("```", "").strip()
    temp_dir = "temp_files" 
    res_path = os.path.join(temp_dir, 'res.json')
    with open(res_path, "w") as json_file:
        json.dump(message, json_file, indent=4)
    print(message)
    return message

