import streamlit as st
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Webhook URL
WEBHOOK_URL = "https://n8n.nikkuv.site/webhook/e32837d2-e23f-4deb-8d91-c79cf092b8b5"

st.title("SHL catalogue AI search")

# User input
user_query = st.text_input("Enter your query:")

if st.button("Submit"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        try:
            # Send POST request to the webhook
            response = requests.get(
                WEBHOOK_URL,
                json={"query": user_query}
            )
            response.raise_for_status()

            # Parse the webhook response
            webhook_data = response.json()

            # Use GPT-4o Mini to refine the response
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that refines and clarifies responses."},
                    {"role": "user", "content": f"Please refine the following response for better clarity:\n\n{webhook_data}"}
                ],
                temperature=0.7,
                max_tokens=500
            )

            refined_answer = completion.choices[0].message.content.strip()

            st.success("Refined Answer:")
            st.write(refined_answer)

        except requests.exceptions.RequestException as e:
            st.error(f"Webhook request failed: {e}")
        except ValueError:
            st.error("Failed to parse JSON response.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
