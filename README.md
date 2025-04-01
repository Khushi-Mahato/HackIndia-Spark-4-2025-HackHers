# Domain-Specific FAQ Chatbot with Knowledge Graph Integration

A powerful FAQ chatbot that combines MeTTa knowledge graphs with Google's Gemini 2.0 LLM for enhanced, context-aware responses. Features multimodal capabilities, automatic knowledge extraction, and rich interactive responses.

## 🌟 Features

- **Knowledge Graph Integration**: Uses MeTTa for structured knowledge representation
- **LLM Integration**: Leverages Google Gemini 2.0 for natural language understanding
- **Graph RAG**: Retrieval-Augmented Generation for context-aware responses
- **Real-time Updates**: Support for adding new FAQs, entities, and relationships
- **Context-Aware Answers**: Understands relationships and hierarchies within the domain
- **Multimodal Support**: Process and respond to images with text
- **Rich Responses**: Provides text, images, links, and interactive elements
- **Automatic Knowledge Extraction**: Extract entities, relationships, and FAQs from text and images

## 🚀 Quick Start

### Option 1: Using the Start Script (Recommended for Unix/Mac)

```bash
# Make the script executable (if not already)
chmod +x start.sh

# Run the start script
./start.sh
```

The script will:
1. Create a virtual environment if it doesn't exist
2. Install all dependencies
3. Check for a `.env` file with your Gemini API key
4. Start the server

### Option 2: Using the Demo Script (Recommended for All Platforms)

```bash
# Activate your virtual environment first
# On Unix/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Run the demo script
python start_demo.py
```

This script will:
1. Start the server
2. Open the demo interface in your default web browser
3. Handle server shutdown when you're done


## 📜 Project Scripts

The project includes several scripts to simplify setup, running, and testing:

### `start.sh` - Unix/Mac Startup Script

A Bash script that handles the complete setup and startup process:

```bash
./start.sh
```
for documentations -> `http://localhost:8000/docs`

- Creates a Python virtual environment if it doesn't exist
- Activates the virtual environment
- Installs all dependencies from requirements.txt
- Checks for a .env file and prompts for Gemini API key if needed
- Starts the FastAPI server

### `start.bat` - Windows Startup Script

A Windows batch file that performs the same functions as start.sh but for Windows:

```bash
start.bat
```
for documentations -> `http://localhost:8000/docs`

- Creates a Python virtual environment if it doesn't exist
- Activates the virtual environment
- Installs all dependencies from requirements.txt
- Checks for a .env file and prompts for Gemini API key if needed
- Starts the FastAPI server

### `start_demo.py` - Cross-Platform Demo Launcher

A Python script that provides a more interactive startup experience:

```bash
python start_demo.py
```
for documentations -> `http://localhost:8000/docs`


- Checks if the server is already running
- Starts the server if needed
- Opens the demo interface in your default web browser
- Handles graceful shutdown of the server when you're done

<!-- ### `test_multimodal.py` - Multimodal Testing Script

A Python script for testing the multimodal capabilities:

```bash
python test_multimodal.py path/to/image.jpg "What is in this image?"
```

- Sends an image and a question to the chatbot API
- Displays the formatted response
- Useful for testing the image analysis capabilities -->

## 🛠️ Manual Setup

### Prerequisites

- Python 3.9+
- Gemini API key from [Google AI Studio](https://ai.google.dev/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CryptoMaN-Rahul/metta
   cd metta
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Gemini API key:
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

### Running the Project

1. Start the server:
   ```bash
   python src/main.py
   ```

2. Access the demo interface:
   - Navigate to `http://localhost:8000/demo.html` in your browser
   
   > **Important**: Always access the demo through the server at `http://localhost:8000/demo.html`. Opening the HTML file directly will not work as it needs to connect to the server API.

## 🧠 Using the Chatbot

### Interactive Demo Interface

The demo interface (`demo.html`) provides a complete experience:

1. **Chat Interface**: Ask questions and get rich, formatted responses
2. **Image Upload**: Upload images for multimodal analysis
3. **Knowledge Graph Visualization**: See the knowledge graph grow in real-time
4. **Knowledge Management**: Add new FAQs, entities, and relationships
5. **Knowledge Extraction**: Extract knowledge from text and images

To use the demo:
1. Start the server using one of the methods above
2. Open `http://localhost:8000/demo.html` in your browser
3. Type questions in the chat input or upload images
4. View the knowledge graph visualization to see connections

### API Endpoints Reference

#### Chat Endpoints

1. **Text-only Chat**
```http
POST /chat
Content-Type: application/json

{
    "text": "What is a knowledge graph?",
    "history": [{"user": "Previous question", "assistant": "Previous answer"}]
}
```

2. **Multimodal Chat (Text + Images)**
```http
POST /chat/multimodal
Content-Type: multipart/form-data

text: What is in this image?
files: [image.jpg]
history: [{"user": "Previous question", "assistant": "Previous answer"}]
```

#### Knowledge Management Endpoints

1. **Add FAQ**
```http
POST /faq
Content-Type: application/json

{
    "question": "What is a knowledge graph?",
    "answer": "A knowledge graph is a network of entities, their semantic types, properties, and relationships between entities.",
    "category": "Knowledge Representation",
    "concepts": "knowledge graph semantic network ontology"
}
```

2. **Add Entity**
```http
POST /entity
Content-Type: application/json

{
    "name": "Knowledge Graph",
    "entity_type": "Concept",
    "properties": {
        "definition": {
            "value": "A knowledge graph is a network of entities, their semantic types, properties, and relationships.",
            "metadata": "source: documentation confidence: 0.9"
        },
        "created_by": {
            "value": "Google",
            "metadata": "year: 2012"
        }
    }
}
```

3. **Add Relationship**
```http
POST /relationship
Content-Type: application/json

{
    "from_entity": "Knowledge Graph",
    "relationship_type": "is_a",
    "to_entity": "Semantic Network",
    "context": "confidence: 0.85"
}
```

#### Knowledge Extraction Endpoints

1. **Extract from Text**
```http
POST /extract/text
Content-Type: application/json

{
    "text": "Knowledge graphs are a type of semantic network used to store interlinked descriptions of entities."
}
```

2. **Extract from Document**
```http
POST /extract/document
Content-Type: application/json

{
    "text": "Long document text with multiple paragraphs..."
}
```

3. **Extract from Image**
```http
POST /extract/image
Content-Type: multipart/form-data

file: image.jpg
```

## 📁 Project Structure

```
domain-specific-faq-chatbot/
├── src/
│   ├── main.py                 # FastAPI server and API endpoints
│   ├── chat/
│   │   ├── llm.py              # Gemini LLM integration
│   │   ├── rag.py              # Graph RAG implementation
│   │   └── auto_extractor.py   # Automatic entity extraction
│   └── knowledge_graph/
│       ├── schema.metta        # MeTTa schema definition
│       └── data.metta          # Knowledge graph data
├── static/                     # Static assets (CSS, JS, images)
├── demo.html                   # Interactive demo interface
├── start_demo.py               # Script to start demo and open browser
├── start.sh                    # Unix/Mac startup script
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (create this)
```

## 🔧 Technical Details

### Knowledge Graph

The knowledge graph is implemented using MeTTa, a knowledge representation language that combines functional and logical programming paradigms. The graph stores:

- Entities with properties and metadata
- Relationships between entities with context
- FAQs with categories and related concepts
- Category hierarchies and synonyms

### Graph RAG

The Graph RAG (Retrieval-Augmented Generation) system:

1. Analyzes the user's question
2. Queries the knowledge graph for relevant context
3. Formats the context for the LLM
4. Generates a response using the LLM with the context

### Multimodal Processing

The system can process images along with text:

1. Images are analyzed to extract entities and concepts
2. Extracted entities are added to the knowledge graph
3. The LLM generates responses considering both the text and image content

