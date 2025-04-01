from typing import List, Dict, Any, Optional
from hyperon import MeTTa, E, S, V, G
import re

class GraphRAG:
    def __init__(self):
        """Initialize MeTTa engine and load knowledge graph."""
        self.metta = MeTTa()
        
    def load_knowledge_base(self, schema_file: str, data_file: str):
        """Load knowledge graph schema and data."""
        # Load schema
        with open(schema_file, 'r') as f:
            self.metta.run(f.read())
            
        # Load data
        with open(data_file, 'r') as f:
            self.metta.run(f.read())
    
    def query_context(self, question: str) -> List[Dict[str, Any]]:
        """
        Query the knowledge graph for relevant context based on the question.
        Uses multiple strategies to find relevant information.
        """
        context = []
        
        # 1. Direct FAQ matches
        faq_matches = self._query_faqs(question)
        context.extend(faq_matches)
        
        # 2. Entity and concept matches
        entity_matches = self._query_entities(question)
        context.extend(entity_matches)
        
        # 3. Find related concepts through synonyms
        synonym_matches = self._query_synonyms(question)
        for synonym in synonym_matches:
            # Query entities and FAQs using synonyms
            context.extend(self._query_entities(synonym['term']))
        
        # 4. Get category hierarchies for relevant concepts
        categories = self._extract_categories(context)
        for category in categories:
            hierarchy = self._query_category_hierarchy(category)
            if hierarchy:
                context.append({'category_hierarchy': hierarchy})
        
        # 5. Get weighted context relationships
        context_relationships = self._query_context_relationships(question)
        context.extend(context_relationships)
        
        return context
    
    def _query_faqs(self, query: str) -> List[Dict[str, Any]]:
        """Query FAQs using direct matching."""
        results = []
        
        # Get all FAQs
        faq_matches = self.metta.run(f'''
            ! (match &self (FAQ $question $answer $category $concepts)
                (FAQEntry $question $answer $category))
        ''')[0]
        
        # Filter FAQs based on relevance to query
        for match in faq_matches:
            question = str(match.get_children()[0])
            answer = str(match.get_children()[1])
            category = str(match.get_children()[2])
            
            # Simple relevance check - if query terms appear in question or answer
            if self._is_relevant(query, question) or self._is_relevant(query, answer):
                results.append({
                    'faq': {
                        'question': question,
                        'answer': answer,
                        'category': category,
                        'match_type': 'direct'
                    }
                })
        
        # Get FAQs by category if any terms match category names
        terms = self._extract_terms(query)
        for term in terms:
            category_matches = self.metta.run(f'''
                ! (GetFAQsByCategory "{term}")
            ''')[0]
            
            for match in category_matches:
                results.append({
                    'faq': {
                        'question': str(match.get_children()[0]),
                        'answer': str(match.get_children()[1]),
                        'match_type': 'category'
                    }
                })
        
        return results
    
    def _is_relevant(self, query: str, text: str) -> bool:
        """Check if query is relevant to text using simple term matching."""
        query_terms = self._extract_terms(query.lower())
        text_lower = text.lower()
        
        for term in query_terms:
            if term in text_lower:
                return True
        return False
    
    def _query_entities(self, query: str) -> List[Dict[str, Any]]:
        """Query entities and their relationships."""
        results = []
        
        # Extract terms for entity matching
        terms = self._extract_terms(query)
        for term in terms:
            # Query entities
            entity_matches = self.metta.run(f'''
                ! (match &self 
                    (Entity "{term}" $type)
                    (EntityInfo "{term}" $type))
            ''')[0]
            
            for match in entity_matches:
                entity_name = str(match.get_children()[0])
                
                # Get entity properties with metadata
                properties = self.metta.run(f'''
                    ! (GetPropertiesWithMetadata "{entity_name}")
                ''')[0]
                
                # Get related entities with context
                relations = self.metta.run(f'''
                    ! (GetRelatedWithContext "{entity_name}")
                ''')[0]
                
                results.append({
                    'entity': {
                        'name': entity_name,
                        'type': str(match.get_children()[1]),
                        'properties': {
                            str(prop.get_children()[0]): {
                                'value': str(prop.get_children()[1]),
                                'metadata': str(prop.get_children()[2])
                            }
                            for prop in properties
                        },
                        'relations': [
                            {
                                'to': str(rel.get_children()[0]),
                                'type': str(rel.get_children()[1]),
                                'context': str(rel.get_children()[2])
                            }
                            for rel in relations
                        ]
                    }
                })
        
        return results
    
    def _query_synonyms(self, query: str) -> List[Dict[str, Any]]:
        """Find synonyms and semantic equivalents."""
        results = []
        terms = self._extract_terms(query)
        
        for term in terms:
            synonym_matches = self.metta.run(f'''
                ! (FindSimilarTerms "{term}")
            ''')[0]
            
            for match in synonym_matches:
                results.append({
                    'term': str(match.get_children()[0]),
                    'confidence': float(match.get_children()[1])
                })
        
        return results
    
    def _query_category_hierarchy(self, category: str) -> Optional[Dict[str, Any]]:
        """Get category hierarchy information."""
        hierarchy_matches = self.metta.run(f'''
            ! (GetCategoryHierarchy "{category}")
        ''')[0]
        
        if hierarchy_matches:
            match = hierarchy_matches[0]
            return {
                'category': category,
                'parent': str(match.get_children()[0]),
                'description': str(match.get_children()[1])
            }
        return None
    
    def _query_context_relationships(self, query: str) -> List[Dict[str, Any]]:
        """Get weighted context relationships."""
        results = []
        terms = self._extract_terms(query)
        
        for term in terms:
            context_matches = self.metta.run(f'''
                ! (GetWeightedContext "{term}")
            ''')[0]
            
            for match in context_matches:
                results.append({
                    'context_relationship': {
                        'context': str(match.get_children()[0]),
                        'weight': float(match.get_children()[1])
                    }
                })
        
        return results
    
    def _extract_terms(self, text: str) -> List[str]:
        """Extract key terms from text for entity matching."""
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Split into words and filter
        words = text.split()
        return [word for word in words if len(word) > 3]  # Filter out short words
    
    def _extract_categories(self, context: List[Dict[str, Any]]) -> List[str]:
        """Extract unique categories from context."""
        categories = set()
        
        for item in context:
            if 'faq' in item and 'category' in item['faq']:
                categories.add(item['faq']['category'])
            elif 'entity' in item and 'type' in item['entity']:
                categories.add(item['entity']['type'])
        
        return list(categories)
    
    def add_faq(self, question: str, answer: str, category: str, concepts: List[str] = None):
        """Add a new FAQ entry to the knowledge graph."""
        concepts_str = f'"{" ".join(concepts)}"' if concepts else '""'
        self.metta.run(f'''
            (FAQ "{question}" "{answer}" "{category}" {concepts_str})
        ''')
    
    def add_entity(self, name: str, entity_type: str, properties: Dict[str, Dict[str, str]] = None):
        """Add a new entity with metadata to the knowledge graph."""
        self.metta.run(f'''
            (Entity "{name}" "{entity_type}")
        ''')
        
        if properties:
            for key, value_data in properties.items():
                value = value_data.get('value', '')
                metadata = value_data.get('metadata', '')
                self.metta.run(f'''
                    (Property "{name}" "{key}" "{value}" "{metadata}")
                ''')
    
    def add_relationship(self, from_entity: str, relationship_type: str, to_entity: str, context: str = ""):
        """Add a new relationship with context between entities."""
        self.metta.run(f'''
            (Relationship "{from_entity}" "{relationship_type}" "{to_entity}" "{context}")
        ''') 