from kafka import KafkaProducer
import json
import time

# Replace with your Kafka broker address (if running locally)
bootstrap_servers = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    try:
        # Allow user to input their prompt
        prompt = input("Enter your prompt (or type 'exit' to quit): ")

        # Break the loop if the user types 'exit'
        if prompt.lower() == 'exit':
            print("Exiting...")
            break

        # Send the user's input to the 'llm_prompts' topic
        print(f"Producing: {prompt}")
        producer.send('llm_prompts', value={'prompt': prompt})
        producer.flush()  # Ensure the message is actually sent

    except Exception as e:
        print(f"Error while producing message: {e}")
