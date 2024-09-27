from kafka import KafkaConsumer
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key for the SDK
genai.configure(api_key=os.getenv('API_KEY'))

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-exp-0827",
    generation_config=generation_config
)

# Replace with your Kafka broker address
bootstrap_servers = 'localhost:9092'

# Set up Kafka consumer
consumer = KafkaConsumer('llm_prompts',
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Process Kafka messages
for message in consumer:
    try:
        prompt = message.value['prompt']
        print(f"Consuming: {prompt}")

        # Start a chat session
        chat_session = model.start_chat(history=[])

        # Send the prompt to the model
        response = chat_session.send_message(prompt)

        # Print the model's response
        print(f"Response from Gemini: {response.text}")

    except Exception as e:
        print(f"Error while consuming message: {e}")
