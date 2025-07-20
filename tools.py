import logging
import requests
from livekit.agents import function_tool
from langchain_community.tools import DuckDuckGoSearchRun
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@function_tool()
async def get_weather(
    city: str,
) -> str:
    """Fetches the current weather for a given location."""
    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather data for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to fetch weather data for {city}: {response.status_code}")
            return f"Could not retrieve weather data for {city}."
    except Exception as e:
        logging.error(f"Error fetching weather data for {city}: {e}")
        return f"An error occurred while retrieving weather data for {city}."


@function_tool()
async def search_web(
    query: str,
) -> str:
    """Searches the web for a given query using DuckDuckGo."""
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."


@function_tool()
async def send_email(to: str, subject: str, message: str) -> str:
    """Sends an email to the given recipient."""
    try:
        sender_email = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("EMAIL_SMTP_PORT", 587))

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to, msg.as_string())

        return f"Email sent successfully to {to}."

    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"Failed to send email: {e}"