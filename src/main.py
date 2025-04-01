import os
import json
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from chat.llm import GeminiLLM
from chat.rag import GraphRAG
from chat.auto_extractor import AutoExtractor

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Domain-Specific FAQ Chatbot",
    description="A chatbot that combines knowledge graphs with LLM for enhanced FAQ responses",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize components
llm = GeminiLLM()
rag = GraphRAG()
extractor = AutoExtractor()

# Load knowledge base
@app.on_event("startup")
async def startup_event():
    """Load knowledge base on startup."""
    try:
        rag.load_knowledge_base(
            "src/knowledge_graph/schema.metta",
            "src/knowledge_graph/data.metta"
        )
    except Exception as e:
        print(f"Error loading knowledge base: {e}")

# Serve demo.html at the root
@app.get("/")
async def get_demo():
    return FileResponse("demo.html")

@app.get("/demo.html")
async def get_demo_html():
    return FileResponse("demo.html")

# Pydantic models for request/response validation
class Question(BaseModel):
    text: str
    history: Optional[List[Dict[str, str]]] = None

class Answer(BaseModel):
    text: str
    context: List[Dict]

class FAQEntry(BaseModel):
    question: str
    answer: str
    category: str
    concepts: Optional[str] = None

class PropertyValue(BaseModel):
    value: str
    metadata: str

class Entity(BaseModel):
    name: str
    entity_type: str
    properties: Optional[Dict[str, PropertyValue]] = None

class Relationship(BaseModel):
    from_entity: str
    relationship_type: str
    to_entity: str
    context: Optional[str] = ""

class DocumentExtraction(BaseModel):
    text: str

@app.post("/chat", response_model=Answer)
async def chat(question: Question):
    """
    Get an answer to a question using the knowledge graph and LLM.
    """
    try:
        # Query knowledge graph for context
        context = rag.query_context(question.text)
        
        # Generate response using LLM with context
        response = await llm.generate_response(
            question=question.text,
            context=context,
            history=question.history
        )
        
        return Answer(text=response, context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/multimodal")
async def chat_multimodal(
    text: str = Form(...),
    files: List[UploadFile] = File(None),
    history: str = Form(None)
):
    """
    Get an answer to a question with attached media files.
    Extracts entities from images and integrates with knowledge graph.
    """
    try:
        # Parse history if provided
        history_list = json.loads(history) if history else []
        
        # Process uploaded files
        media_files = []
        extracted_entities = []
        
        # Check if files is not None and not empty before iterating
        if files:
            for file in files:
                if file is None:
                    continue
                    
                content_type = file.content_type
                file_data = await file.read()
                
                if content_type.startswith('image/'):
                    # Add to media files for LLM processing
                    media_files.append({
                        'type': 'image',
                        'data': file_data,
                        'mime_type': content_type
                    })
                    
                    # Extract entities from image in background
                    # We'll use the file data we already read
                    try:
                        # Extract entities from the image
                        image_entities = await extractor.extract_from_image(file_data, content_type)
                        extracted_entities.extend(image_entities.get('entities', []))
                        # image_entities = {'entities': []}  # Fake empty result
# Skip background task
                        # Add extracted entities to the knowledge graph asynchronously
                        # This won't block the response
                        background_tasks = BackgroundTasks()
                        background_tasks.add_task(add_extracted_data_to_graph, image_entities)
                    except Exception as extraction_error:
                        print(f"Entity extraction error (non-blocking): {str(extraction_error)}")
                        # Continue processing even if extraction fails
                
                elif content_type.startswith('video/'):
                    # For videos, we'd need to extract frames or thumbnails
                    # This is a simplified approach
                    media_files.append({
                        'type': 'video',
                        'data': file_data,
                        'mime_type': content_type
                    })
        
        # Enhance the query with extracted entities if any
        enhanced_query = text
        if extracted_entities:
            entity_names = [entity.get('name', '') for entity in extracted_entities if entity.get('name')]
            if entity_names:
                enhanced_query = f"{text} (Considering these entities: {', '.join(entity_names)})"
        
        # Query knowledge graph for context
        context = rag.query_context(enhanced_query)
        
        # Add extracted entities to context if they're not already included
        for entity in extracted_entities:
            entity_in_context = False
            for ctx in context:
                if 'entity' in ctx and ctx['entity'].get('name') == entity.get('name'):
                    entity_in_context = True
                    break
            
            if not entity_in_context and entity.get('name'):
                # Convert to the format expected by the context
                formatted_entity = {
                    'name': entity.get('name', ''),
                    'type': entity.get('entity_type', 'Unknown'),
                    'properties': entity.get('properties', {}),
                    'relations': entity.get('relations', [])
                }
                context.append({'entity': formatted_entity, 'score': 0.9, 'source': 'image_extraction'})
        
        # Generate response using LLM with context and media
        response = await llm.generate_response(
            question=enhanced_query,
            context=context,
            history=history_list,
            media_files=media_files
        )
        
        # Update history with this interaction
        history_list.append({
            "user": text,
            "assistant": response
        })
        
        return JSONResponse(content={
            "text": response, 
            "context": context,
            "history": history_list,
            "extracted_entities": extracted_entities
        })
    except Exception as e:
        print(f"Multimodal chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/faq")
async def add_faq(faq: FAQEntry):
    """Add a new FAQ entry to the knowledge graph."""
    try:
        concepts_list = faq.concepts.split() if faq.concepts else None
        rag.add_faq(faq.question, faq.answer, faq.category, concepts_list)
        return {"message": "FAQ added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/entity")
async def add_entity(entity: Entity):
    """Add a new entity to the knowledge graph."""
    try:
        properties_dict = {
            key: {"value": prop.value, "metadata": prop.metadata}
            for key, prop in entity.properties.items()
        } if entity.properties else None
        
        rag.add_entity(entity.name, entity.entity_type, properties_dict)
        return {"message": "Entity added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/relationship")
async def add_relationship(relationship: Relationship):
    """Add a new relationship between entities."""
    try:
        rag.add_relationship(
            relationship.from_entity,
            relationship.relationship_type,
            relationship.to_entity,
            relationship.context
        )
        return {"message": "Relationship added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/text")
async def extract_from_text(document: DocumentExtraction, background_tasks: BackgroundTasks):
    """
    Extract entities, relationships, and FAQs from text and add them to the knowledge graph.
    """
    try:
        # Extract knowledge from text
        extracted_data = await extractor.extract_from_text(document.text)
        
        # Add extracted data to knowledge graph in the background
        background_tasks.add_task(add_extracted_data_to_graph, extracted_data)
        
        return {
            "message": "Extraction started. Data will be added to the knowledge graph.",
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/document")
async def extract_from_document(document: DocumentExtraction, background_tasks: BackgroundTasks):
    """
    Extract entities, relationships, and FAQs from a document and add them to the knowledge graph.
    Optimized for longer texts.
    """
    try:
        # Extract knowledge from document
        extracted_data = await extractor.extract_from_document(document.text)
        
        # Add extracted data to knowledge graph in the background
        background_tasks.add_task(add_extracted_data_to_graph, extracted_data)
        
        return {
            "message": "Extraction started. Data will be added to the knowledge graph.",
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/image")
async def extract_from_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Extract entities and relationships from an image and add them to the knowledge graph.
    """
    try:
        # Read image data
        image_data = await file.read()
        content_type = file.content_type
        
        # Extract knowledge from image
        extracted_data = await extractor.extract_from_image(image_data, content_type)
        
        # Add extracted data to knowledge graph in the background
        if background_tasks:
            background_tasks.add_task(add_extracted_data_to_graph, extracted_data)
        
        return {
            "message": "Extraction completed. Data will be added to the knowledge graph.",
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_extracted_data_to_graph(data: Dict[str, Any]):
    """
    Add extracted data to the knowledge graph.
    
    Args:
        data: Dictionary containing entities, relationships, and FAQ entries
    """
    # Add entities
    for entity in data.get('entities', []):
        try:
            rag.add_entity(
                name=entity['name'],
                entity_type=entity['type'],
                properties=entity.get('properties', {})
            )
        except Exception as e:
            print(f"Error adding entity {entity['name']}: {e}")
    
    # Add relationships
    for rel in data.get('relationships', []):
        try:
            rag.add_relationship(
                from_entity=rel['from_entity'],
                relationship_type=rel['relationship_type'],
                to_entity=rel['to_entity'],
                context=rel.get('context', '')
            )
        except Exception as e:
            print(f"Error adding relationship: {e}")
    
    # Add FAQ entries
    for faq in data.get('faq_entries', []):
        try:
            concepts = faq.get('concepts', '').split() if 'concepts' in faq else None
            rag.add_faq(
                question=faq['question'],
                answer=faq['answer'],
                category=faq.get('category', 'General'),
                concepts=concepts
            )
        except Exception as e:
            print(f"Error adding FAQ: {e}")

if __name__ == "__main__":
    import uvicorn
    
    # Mount static files after all routes are defined
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 