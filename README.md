# Domain-Specific FAQ Chatbot with Knowledge Graph Integration

A powerful FAQ chatbot that combines MeTTa knowledge graphs with Google's Gemini 2.0 LLM for enhanced, context-aware responses. Features multimodal capabilities, automatic knowledge extraction, and rich interactive responses.

##  Features

- **Knowledge Graph Integration**: Uses MeTTa for structured knowledge representation
- **LLM Integration**: Leverages Google Gemini 2.0 for natural language understanding
- **Graph RAG**: Retrieval-Augmented Generation for context-aware responses
- **Real-time Updates**: Support for adding new FAQs, entities, and relationships
- **Context-Aware Answers**: Understands relationships and hierarchies within the domain
- **Multimodal Support**: Process and respond to images with text
- **Rich Responses**: Provides text, images, links, and interactive elements
- **Automatic Knowledge Extraction**: Extract entities, relationships, and FAQs from text and images



## 🛠️ Manual Setup

### Prerequisites

- Python 3.9+
- Gemini API key from [Google AI Studio](https://ai.google.dev/)

### Installation

1. Clone the repository:
   ```
   bash(https://github.com/Khushi-Mahato/HackIndia-Spark-4-2025-HackHers.git)
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

##  Using the Chatbot

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

