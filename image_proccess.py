
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import json
from langchain_core.messages import HumanMessage
import streamlit as st




def process_image(uploaded_front_image, uploaded_back_image):
    # Load environment variables (assuming .env file is in the same directory)
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
                "text": """These are images of a visiting card. 1st image is the front side and 2nd image is the back side of the card. Extract all information from the card and give it in a structured format. If you have any additional information about the details in the card, add them to the 'additional info'.""",
            },
            {"type": "image_url", "image_url": uploaded_front_image},
            {"type": "image_url", "image_url": uploaded_back_image},
        ]
    )
    message = llm.invoke([hmessage])
    st.write(message)

