from typing import List, Dict, Any, Optional, Tuple
import re
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AutoExtractor:
    """
    Automatic entity and relationship extraction from text and media.
    Uses Gemini to extract structured knowledge from unstructured data.
    """
    
    def __init__(self, model_name: str = 'gemini-2.0-flash'):
        """Initialize the extractor with the specified model."""
        self.model_name = model_name
    
    async def extract_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract entities and relationships from text.
        
        Args:
            text: The text to extract from
            
        Returns:
            Dict with extracted entities and relationships
        """
        prompt = f"""
        Extract structured knowledge from the following text. Identify entities, their properties, 
        and relationships between entities. Format the output as JSON.
        
        Text: {text}
        
        Output format:
        {{
            "entities": [
                {{
                    "name": "entity_name",
                    "type": "entity_type",
                    "properties": {{
                        "property_name": {{
                            "value": "property_value",
                            "metadata": "source: text confidence: 0.9"
                        }}
                    }}
                }}
            ],
            "relationships": [
                {{
                    "from_entity": "entity1_name",
                    "relationship_type": "relates_to",
                    "to_entity": "entity2_name",
                    "context": "relationship_context confidence: 0.85"
                }}
            ],
            "faq_entries": [
                {{
                    "question": "extracted_question",
                    "answer": "extracted_answer",
                    "category": "extracted_category",
                    "concepts": "space_separated_concepts"
                }}
            ]
        }}
        
        Only extract information that is explicitly stated or strongly implied in the text.
        Assign confidence scores based on how explicitly the information is stated.
        """
        
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        # Extract JSON from response
        json_str = self._extract_json(response.text)
        
        # Parse and validate the extracted data
        return self._parse_and_validate(json_str)
    
    async def extract_from_image(self, image_data: Any, mime_type: str = None) -> Dict[str, Any]:
        """
        Extract entities and relationships from an image.
        
        Args:
            image_data: The image data (bytes, path, or file-like object)
            mime_type: The MIME type of the image
            
        Returns:
            Dict with extracted entities and relationships
        """
        # Create image part
        import base64
        
        # Create image part directly instead of importing GeminiLLM
        if isinstance(image_data, bytes):
            image_bytes = image_data
        else:
            # If it's a file-like object, read it
            image_bytes = image_data.read()
        
        # Default to JPEG if mime_type not specified
        mime_type = mime_type or "image/jpeg"
        
        # Create image part
        image_part = {
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(image_bytes).decode('utf-8')
            }
        }
        
        prompt = """
        Analyze this image and extract structured knowledge from it. Identify entities, their properties, 
        and relationships between entities. Format the output as JSON.
        
        Output format:
        {
            "entities": [
                {
                    "name": "entity_name",
                    "type": "entity_type",
                    "properties": {
                        "property_name": {
                            "value": "property_value",
                            "metadata": "source: image confidence: 0.8"
                        }
                    }
                }
            ],
            "relationships": [
                {
                    "from_entity": "entity1_name",
                    "relationship_type": "relates_to",
                    "to_entity": "entity2_name",
                    "context": "relationship_context confidence: 0.75"
                }
            ]
        }
        
        Only extract information that is clearly visible or strongly implied in the image.
        Assign confidence scores based on how clearly the information is presented.
        """
        
        response = client.models.generate_content(
            model=self.model_name,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        image_part
                    ]
                }
            ]
        )
        
        # Extract JSON from response
        json_str = self._extract_json(response.text)
        
        # Parse and validate the extracted data
        return self._parse_and_validate(json_str)
    
    async def extract_from_document(self, document_text: str) -> Dict[str, Any]:
        """
        Extract entities, relationships, and FAQ entries from a document.
        Optimized for longer texts like articles, documentation, etc.
        
        Args:
            document_text: The document text
            
        Returns:
            Dict with extracted entities, relationships, and FAQ entries
        """
        # For longer documents, we need to chunk the text
        chunks = self._chunk_text(document_text, max_length=8000)
        
        all_entities = []
        all_relationships = []
        all_faq_entries = []
        
        # Process each chunk
        for chunk in chunks:
            chunk_result = await self.extract_from_text(chunk)
            
            if 'entities' in chunk_result:
                all_entities.extend(chunk_result['entities'])
            
            if 'relationships' in chunk_result:
                all_relationships.extend(chunk_result['relationships'])
            
            if 'faq_entries' in chunk_result:
                all_faq_entries.extend(chunk_result['faq_entries'])
        
        # Deduplicate entities
        unique_entities = self._deduplicate_entities(all_entities)
        
        # Deduplicate relationships
        unique_relationships = self._deduplicate_relationships(all_relationships)
        
        # Deduplicate FAQ entries
        unique_faq_entries = self._deduplicate_faq_entries(all_faq_entries)
        
        return {
            'entities': unique_entities,
            'relationships': unique_relationships,
            'faq_entries': unique_faq_entries
        }
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text."""
        # Look for JSON pattern
        json_match = re.search(r'({[\s\S]*})', text)
        if json_match:
            return json_match.group(1)
        return "{}"
    
    def _parse_and_validate(self, json_str: str) -> Dict[str, Any]:
        """Parse and validate the extracted JSON."""
        import json
        try:
            data = json.loads(json_str)
            # Ensure required fields are present
            if 'entities' not in data:
                data['entities'] = []
            if 'relationships' not in data:
                data['relationships'] = []
            return data
        except json.JSONDecodeError:
            # Return empty structure if JSON is invalid
            return {'entities': [], 'relationships': []}
    
    def _chunk_text(self, text: str, max_length: int = 8000) -> List[str]:
        """Split text into chunks of maximum length."""
        # Simple chunking by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 <= max_length:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate entities by name."""
        unique_entities = {}
        
        for entity in entities:
            name = entity.get('name', '')
            if name:
                if name not in unique_entities:
                    unique_entities[name] = entity
                else:
                    # Merge properties
                    existing_props = unique_entities[name].get('properties', {})
                    new_props = entity.get('properties', {})
                    
                    for prop_name, prop_value in new_props.items():
                        if prop_name not in existing_props:
                            existing_props[prop_name] = prop_value
                    
                    unique_entities[name]['properties'] = existing_props
        
        return list(unique_entities.values())
    
    def _deduplicate_relationships(self, relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate relationships."""
        unique_relationships = {}
        
        for rel in relationships:
            from_entity = rel.get('from_entity', '')
            rel_type = rel.get('relationship_type', '')
            to_entity = rel.get('to_entity', '')
            
            key = f"{from_entity}|{rel_type}|{to_entity}"
            
            if key and key not in unique_relationships:
                unique_relationships[key] = rel
        
        return list(unique_relationships.values())
    
    def _deduplicate_faq_entries(self, faq_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate FAQ entries by question."""
        unique_faqs = {}
        
        for faq in faq_entries:
            question = faq.get('question', '')
            
            if question and question not in unique_faqs:
                unique_faqs[question] = faq
        
        return list(unique_faqs.values()) 