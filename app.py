import streamlit as st
from kafka import KafkaProducer, KafkaConsumer
import json
import time
import threading

# Set up Kafka configuration
bootstrap_servers = 'localhost:9092'
producer_topic = 'llm_prompts'
consumer_topic = 'llm_responses'

# Initialize the Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to produce messages to Kafka
def produce_message(prompt):
    producer.send(producer_topic, value={'prompt': prompt})
    producer.flush()  # Ensure the message is sent

# Function to consume messages from Kafka
def consume_messages():
    consumer = KafkaConsumer(consumer_topic,
                             bootstrap_servers=bootstrap_servers,
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        response = message.value.get('response', 'No response received')
        st.session_state['response'] = response
        break  # Consume one message and stop (for simplicity)

# Streamlit app layout
st.title('AI-Powered Chat with Kafka')

# Prompt input
user_prompt = st.text_input("Enter your prompt:")

if st.button('Send'):
    if user_prompt:
        # Send the prompt to Kafka (producer)
        produce_message(user_prompt)
        st.write(f"Prompt sent: {user_prompt}")

        # Display a waiting message
        st.write("Waiting for response...")

        # Start a separate thread to consume the response (so UI doesn't block)
        threading.Thread(target=consume_messages).start()

# Display the AI's response
if 'response' in st.session_state:
    st.write(f"Response: {st.session_state['response']}")
