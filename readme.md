# Vanilla RAG - Movie Search POC

## Overview

This project is a  **Vanilla RAG (Retrieval Augmented Generation)** proof of concept.

The application allows users to ask movie-related questions in natural language.

Weaviate is our retrieval engine only but RAG is the architecture that connects retrieved knowledge to an LLM so the LLM can produce a more relevant ,more accurate response in natural-language.

The system uses:

- **Grok (xAI)** - LLM
- **Pydantic** - Structured query validation
- **Weaviate** - Vector database and retrieval
- **Python** - Application logic

---

## Project Structure

```text
vanilla_rag/
│
├── config.ini
├── llm.py
├── logging_config.py
├── movie_metadata.csv
├── query_parser.py
├── rag.py
├── weaviate_client.py
├── check.ipynb
└── .gitignore
```

### File Responsibilities

- `llm.py` - Handles communication with Grok.
- `query_parser.py` - Converts the user's natural-language query into structured filters using Grok and Pydantic.
- `weaviate_client.py` - Connects to Weaviate and retrieves relevant movie data.
- `rag.py` - Orchestrates the complete RAG pipeline.
- `logging_config.py` - Configures application logging.
- `movie_metadata.csv` - Movie metadata used by the application.
- `config.ini` - Stores application configuration.

---

## RAG Flow

```text
User Query
    ↓
MovieRAG
    ↓
QueryParser
    ↓
Grok + Pydantic
    ↓
Structured Query Filters
    ↓
WeaviateClient
    ↓
Weaviate
    ↓
Relevant Movie Data
    ↓
MovieRAG
    ↓
Grok
    ↓
Final Answer
    ↓
User
```

---

## Example

### User Query

```text
Which action movie between 2012 and 2014 had the highest IMDb rating?
```

### Step 1 - Query Parsing

Grok converts the natural-language query into structured data:

```json
{
    "genre": "action",
    "start_year": 2012,
    "end_year": 2014
}
```

Pydantic validates this structured response.

### Step 2 - Retrieval

The structured filters are passed to Weaviate.

Weaviate performs:

- Semantic search
- Metadata filtering

and returns relevant movie records.

Example:

```text
The Amazing Spider-Man       2012    IMDb 7.0
A Most Violent Year           2014    IMDb 7.0
Act of Valor                  2012    IMDb 6.5
Red Tails                     2012    IMDb 5.9
```

### Step 3 - Generation

The retrieved movie data is provided to Grok along with the original question.

Grok generates the final answer using the retrieved context.

Example:

```text
The Amazing Spider-Man (2012) and A Most Violent Year (2014)
had the highest IMDb rating, with a score of 7.0.
```

---

## Why RAG?

Weaviate is responsible for **retrieving relevant information**.

Grok is responsible for:

- Understanding natural-language questions
- Converting user intent into structured filters
- Interpreting retrieved information
- Generating a natural-language response

Therefore, the basic RAG pattern is:

```text
User Question
     ↓
Understand
     ↓
Retrieve
     ↓
Provide Context
     ↓
Generate Answer
```

The LLM does not need to rely only on its pretrained knowledge.

Relevant information is retrieved from the external movie dataset at runtime and provided to the LLM.

---

## Technologies

- Python
- Grok / xAI
- OpenAI Python SDK
- Pydantic
- Weaviate
- ConfigParser
- Python Logging

---

## Running the POC

Activate the Python environment and run:

```bash
python rag.py
```

The application will:

1. Initialize the LLM client.
2. Initialize the query parser.
3. Connect to Weaviate.
4. Parse the user query.
5. Retrieve relevant movie data.
6. Send the retrieved context to the LLM.
7. Generate the final answer.
8. Close the Weaviate connection.

---

## POC Goal

The purpose of this POC is to demonstrate the fundamental **Vanilla RAG architecture**:

```text
Natural Language
       ↓
Structured Query
       ↓
Retrieval
       ↓
External Knowledge
       ↓
LLM Generation
       ↓
Natural Language Answer
```
