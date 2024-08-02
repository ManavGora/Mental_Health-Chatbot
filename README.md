# FastAPI Chatbot with FastUI and MistralAI

This is a simple chatbot built with FastAPI, FastUI, and MistralAI. The chatbot leverages the FastUI framework for the frontend and MistralAI for generating chat responses.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Testing](#testing)
- [License](#license)

## Project Description

This project demonstrates how to build a chatbot using FastAPI for the backend, FastUI for the frontend, and MistralAI for the AI-driven chat responses. The chatbot maintains a history of messages and can reset the chat history.

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 3.10 or higher
- Virtual environment (optional but recommended)

### Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-chatbot.git
cd fastapi-chatbot
```

### Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables
Create a .env file in the root of your project directory and add your MistralAI API key:

```bash
MISTRAL_API_KEY=your_actual_mistral_api_key_here
```

### Running the App
Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000
