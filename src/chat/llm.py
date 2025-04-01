from typing import List, Dict, Any, Optional, Union, BinaryIO
import os
import base64
from pathlib import Path
import mimetypes
from google import genai
from dotenv import load_dotenv
import re

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

class GeminiLLM:
    def __init__(self, model_name: str = 'gemini-2.0-flash'):
        """Initialize Gemini LLM with specified model."""
        self.model_name = model_name
        
    async def generate_response(self, 
                              question: str, 
                              context: List[Dict[str, Any]], 
                              history: Optional[List[Dict[str, str]]] = None,
                              media_files: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Generate a response using Gemini with context from the knowledge graph.
        
        Args:
            question: User's question
            context: Relevant context from knowledge graph
            history: Chat history for context
            media_files: List of media files (images, videos, etc.)
            
        Returns:
            str: Generated response
        """
        # Format context for the prompt
        context_str = self._format_context(context)
        
        # Format chat history if provided
        history_str = self._format_history(history) if history else ""
        
        # Create the prompt
        prompt = f"""You are a domain-specific FAQ chatbot with knowledge graph integration.
        
{history_str}

CONTEXT INFORMATION:
{context_str}

USER QUESTION: {question}

Please provide a comprehensive answer based on the context information provided. 
If the context doesn't contain relevant information, provide a general response based on your knowledge.

Format your response with HTML for rich presentation:
1. Use <h3> tags for section headings
2. Use <ul> and <li> for lists
3. Use <a href="URL">text</a> for links to relevant resources
4. Use <code> tags for code or technical terms
5. Use <b> and <i> for emphasis
6. Use <div class="definition"> for term definitions
7. Use <div class="example"> for examples
8. For diagrams or visualizations, describe them with [IMAGE: description of what to visualize] and they will be rendered as images
9. For interactive elements, use:
   - <div class="interactive-element">
       <div class="collapsible-header">Title <button class="toggle-button">Show</button></div>
       <div class="collapsible-content">Content goes here...</div>
     </div>

IMPORTANT: Return the HTML directly, NOT wrapped in markdown code blocks. Do not use ```html or ``` tags.

Your response should be informative, accurate, and helpful.
"""
        
        try:
            # Prepare contents for the API call
            contents = []
            
            # Add text prompt as the first part
            text_part = {"text": prompt}
            
            # Create the content structure
            content = {
                "role": "user",
                "parts": [text_part]
            }
            
            # Add media files if provided
            if media_files and len(media_files) > 0:
                for media_file in media_files:
                    if media_file['type'] == 'image':
                        # Add image part to the same content
                        image_part = self._create_image_part(media_file['data'], media_file['mime_type'])
                        content["parts"].append(image_part)
            
            # Add the content to contents
            contents.append(content)
            
            # Generate response using the client
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents
            )
            
            # Process the response to ensure it has proper HTML formatting
            formatted_response = self._ensure_html_formatting(response.text)
            
            return formatted_response
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"I'm sorry, I encountered an error processing your request: {str(e)}"
    
    def _ensure_html_formatting(self, text: str) -> str:
        """
        Ensure the response has proper HTML formatting.
        If the response doesn't contain HTML tags, add basic formatting.
        """
        # Remove markdown code block markers if present
        if text.startswith("```html") and text.endswith("```"):
            text = text[7:-3].strip()
        elif text.startswith("```") and text.endswith("```"):
            text = text[3:-3].strip()
        
        # Process image descriptions
        image_pattern = r'\[IMAGE:\s*(.*?)\]'
        
        def replace_with_image(match):
            description = match.group(1).strip()
            # For demo purposes, use placeholder images based on the description
            if "graph" in description.lower() or "network" in description.lower():
                return f'<img src="https://via.placeholder.com/600x400/4285F4/FFFFFF?text=Knowledge+Graph+Visualization" alt="{description}" />'
            elif "hierarchy" in description.lower() or "tree" in description.lower():
                return f'<img src="https://via.placeholder.com/600x400/34A853/FFFFFF?text=Hierarchy+Diagram" alt="{description}" />'
            elif "flow" in description.lower() or "process" in description.lower():
                return f'<img src="https://via.placeholder.com/600x400/FBBC05/FFFFFF?text=Process+Flow" alt="{description}" />'
            elif "comparison" in description.lower():
                return f'<img src="https://via.placeholder.com/600x400/EA4335/FFFFFF?text=Comparison+Chart" alt="{description}" />'
            else:
                return f'<img src="https://via.placeholder.com/600x400/9C27B0/FFFFFF?text=Visualization" alt="{description}" />'
        
        text = re.sub(image_pattern, replace_with_image, text)
        
        # Check if the response already has HTML
        if "<" in text and ">" in text:
            # Already has some HTML, return as is
            return text
        
        # Add basic HTML formatting
        formatted_text = text
        
        # Format definitions (terms followed by colon and explanation)
        definition_pattern = r'([A-Z][a-zA-Z\s]+):\s([^\.]+\.)'
        formatted_text = re.sub(definition_pattern, r'<div class="definition"><b>\1:</b> \2</div>', formatted_text)
        
        # Format technical terms
        tech_terms = ["MeTTa", "GraphRAG", "Knowledge Graph", "Gemini", "Neo4j", "Entity Extraction", 
                      "Multimodal", "LLM", "RAG", "API"]
        for term in tech_terms:
            formatted_text = re.sub(r'\b' + re.escape(term) + r'\b', r'<code>\g<0></code>', formatted_text)
        
        # Add paragraph breaks
        formatted_text = "<p>" + formatted_text.replace("\n\n", "</p><p>") + "</p>"
        
        # Add links for common references
        formatted_text = formatted_text.replace("MeTTa documentation", '<a href="https://github.com/trueagi-io/metta" target="_blank">MeTTa documentation</a>')
        formatted_text = formatted_text.replace("Gemini API", '<a href="https://ai.google.dev/gemini-api" target="_blank">Gemini API</a>')
        formatted_text = formatted_text.replace("Neo4j", '<a href="https://neo4j.com/" target="_blank">Neo4j</a>')
        
        return formatted_text
    
    def _create_image_part(self, image_data: Union[bytes, BinaryIO], mime_type: str = None) -> Dict:
        """Create an image part for the Gemini API."""
        try:
            # If image_data is already bytes, use it directly
            if isinstance(image_data, bytes):
                image_bytes = image_data
            else:
                # If it's a file-like object, read it
                image_bytes = image_data.read()
            
            # Default to JPEG if mime_type not specified
            mime_type = mime_type or "image/jpeg"

            print(f"Image MIME: {mime_type}")
            print(f"Image data length: {len(image_bytes)} bytes")
            print(f"Base64 sample: {base64.b64encode(image_bytes).decode('utf-8')[:20]}...")
            
            # Create image part using the Gemini API
            return {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": base64.b64encode(image_bytes).decode('utf-8')
                }
            }
        except Exception as e:
            print(f"Error creating image part: {str(e)}")
            raise
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """Format knowledge graph context into a structured string."""
        sections = []
        
        # Process FAQs
        faqs = [item['faq'] for item in context if 'faq' in item]
        if faqs:
            faq_section = "RELEVANT FAQs:\n" + "\n\n".join([
                f"Q: {faq['question']}\n"
                f"A: {faq['answer']}\n"
                f"Category: {faq.get('category', 'General')}\n"
                f"Match Type: {faq.get('match_type', 'direct')}"
                for faq in faqs
            ])
            sections.append(faq_section)
        
        # Process Entities
        entities = [item['entity'] for item in context if 'entity' in item]
        if entities:
            entity_section = "RELEVANT ENTITIES:\n" + "\n\n".join([
                f"Entity: {entity['name']} (Type: {entity['type']})\n"
                f"Properties:\n" + "\n".join([
                    f"- {key}: {value['value']} "
                    f"(Metadata: {value['metadata']})"
                    for key, value in entity['properties'].items()
                ]) + "\n"
                f"Relationships:\n" + "\n".join([
                    f"- {rel['to']} ({rel['type']}) "
                    f"Context: {rel['context']}"
                    for rel in entity['relations']
                ])
                for entity in entities
            ])
            sections.append(entity_section)
        
        # Process Category Hierarchies
        hierarchies = [item['category_hierarchy'] for item in context if 'category_hierarchy' in item]
        if hierarchies:
            hierarchy_section = "CATEGORY HIERARCHIES:\n" + "\n".join([
                f"Category: {h['category']}\n"
                f"Parent: {h['parent']}\n"
                f"Description: {h['description']}"
                for h in hierarchies
            ])
            sections.append(hierarchy_section)
        
        # Process Context Relationships
        context_rels = [item['context_relationship'] for item in context if 'context_relationship' in item]
        if context_rels:
            context_section = "CONTEXTUAL RELATIONSHIPS:\n" + "\n".join([
                f"- {rel['context']} (Weight: {rel['weight']})"
                for rel in context_rels
            ])
            sections.append(context_section)
        
        return "\n\n".join(sections)
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """Format chat history into a structured string."""
        if not history:
            return ""
            
        return "Previous conversation:\n" + "\n\n".join([
            f"User: {h['user']}\n"
            f"Assistant: {h['assistant']}"
            for h in history
        ]) 