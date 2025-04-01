;; Sample FAQ entries with related concepts
(FAQ "What is a knowledge graph?" 
     "A knowledge graph is a network of entities, their properties, and relationships between them. It helps organize and connect information in a structured way."
     "Basics"
     "knowledge_representation data_structure graph_database semantic_web")

(FAQ "How does the chatbot use the knowledge graph?"
     "The chatbot uses the knowledge graph to understand relationships between concepts, find relevant context, and provide more accurate and detailed answers by leveraging connected information."
     "Usage"
     "chatbot knowledge_graph context_awareness semantic_search")

(FAQ "Can I add new information to the knowledge graph?"
     "Yes, you can add new FAQs, entities, and relationships through the API endpoints. The knowledge graph updates in real-time to incorporate new information."
     "Usage"
     "api knowledge_management real_time_updates data_entry")

(FAQ "What is MeTTa?"
     "MeTTa is a knowledge representation language designed for graph-based knowledge storage and querying. It combines functional and logical programming paradigms to represent and manipulate knowledge in a structured way."
     "Technical"
     "metta programming_language knowledge_representation graph_processing")

(FAQ "How does MeTTa differ from other knowledge representation languages?"
     "MeTTa differs from other knowledge representation languages by combining functional and logical programming paradigms, providing a flexible way to represent and query knowledge graphs. It has a bracket-based syntax similar to Lisp and supports pattern matching through its match function."
     "Technical"
     "metta programming_language comparison functional_programming logical_programming")

(FAQ "What is Graph RAG?"
     "Graph RAG (Retrieval-Augmented Generation) is an approach that enhances language model responses by retrieving relevant information from a knowledge graph. It combines the structured knowledge of graphs with the natural language capabilities of LLMs for more accurate and contextual responses."
     "Technical"
     "rag retrieval_augmented_generation knowledge_graph llm")

(FAQ "What are the advantages of using a knowledge graph with an LLM?"
     "Using a knowledge graph with an LLM provides several advantages: more accurate and factual responses, better handling of complex relationships, improved context awareness, reduced hallucinations, and the ability to incorporate domain-specific knowledge that may not be in the LLM's training data."
     "Basics"
     "knowledge_graph llm advantages context_awareness factuality")

(FAQ "How can I extract entities from text and add them to the knowledge graph?"
     "You can extract entities from text using the /extract/text or /extract/document API endpoints. These use AI to identify entities, their properties, and relationships, then automatically add them to the knowledge graph. You can also manually add entities using the /entity endpoint."
     "Usage"
     "entity_extraction api knowledge_management")

(FAQ "What is multimodal understanding in chatbots?"
     "Multimodal understanding refers to a chatbot's ability to process and understand multiple types of input, such as text and images. This allows the chatbot to analyze images, extract information from them, and combine this with textual context to provide more comprehensive responses."
     "Technical"
     "multimodal image_processing computer_vision text_analysis")

;; Sample entities with metadata
(Entity "KnowledgeGraph" "Concept")
(Property "KnowledgeGraph" "definition" 
         "A structured representation of knowledge" 
         "source: academic_literature confidence: 0.95")
(Property "KnowledgeGraph" "purpose" 
         "To organize and connect information" 
         "source: technical_documentation confidence: 0.9")

(Entity "ChatbotSystem" "System")
(Property "ChatbotSystem" "type" 
         "FAQ Assistant" 
         "version: 1.0 status: active")
(Property "ChatbotSystem" "capability" 
         "Natural language understanding" 
         "framework: gemini confidence: 0.85")

(Entity "MeTTa" "Technology")
(Property "MeTTa" "type" 
         "Knowledge representation language" 
         "version: latest source: official_docs")
(Property "MeTTa" "purpose" 
         "Graph-based knowledge storage and querying" 
         "source: technical_spec confidence: 0.9")
(Property "MeTTa" "syntax" 
         "Bracket-based, similar to Lisp" 
         "source: documentation confidence: 0.95")
(Property "MeTTa" "paradigm" 
         "Combines functional and logical programming" 
         "source: technical_spec confidence: 0.9")
(Property "MeTTa" "key_feature" 
         "Pattern matching through match function" 
         "source: documentation confidence: 0.95")

(Entity "Gemini" "Technology")
(Property "Gemini" "type" 
         "Large Language Model" 
         "version: 2.0 provider: Google")
(Property "Gemini" "version" 
         "2.0" 
         "release_date: 2024 status: active")
(Property "Gemini" "provider" 
         "Google" 
         "source: official reliability: high")
(Property "Gemini" "capability" 
         "Multimodal understanding (text, images, video)" 
         "source: official documentation confidence: 0.95")
(Property "Gemini" "use_case" 
         "Natural language understanding and generation" 
         "source: technical_documentation confidence: 0.9")

(Entity "GraphRAG" "Concept")
(Property "GraphRAG" "definition" 
         "Retrieval-Augmented Generation using knowledge graphs" 
         "source: research_papers confidence: 0.9")
(Property "GraphRAG" "purpose" 
         "Enhance LLM responses with structured knowledge" 
         "source: technical_documentation confidence: 0.85")
(Property "GraphRAG" "advantage" 
         "Improved factuality and context awareness" 
         "source: research_papers confidence: 0.9")

(Entity "EntityExtraction" "Concept")
(Property "EntityExtraction" "definition" 
         "Process of identifying entities and relationships from unstructured data" 
         "source: technical_documentation confidence: 0.9")
(Property "EntityExtraction" "method" 
         "AI-based analysis of text and images" 
         "source: implementation_details confidence: 0.85")
(Property "EntityExtraction" "purpose" 
         "Populate knowledge graphs from unstructured sources" 
         "source: technical_documentation confidence: 0.9")

(Entity "MultimodalUnderstanding" "Concept")
(Property "MultimodalUnderstanding" "definition" 
         "Ability to process and understand multiple types of input (text, images, etc.)" 
         "source: research_papers confidence: 0.9")
(Property "MultimodalUnderstanding" "application" 
         "Enhanced chatbot capabilities with visual context" 
         "source: implementation_details confidence: 0.85")
(Property "MultimodalUnderstanding" "challenge" 
         "Aligning information across different modalities" 
         "source: research_papers confidence: 0.8")

(Entity "GraphDatabase" "Technology")
(Property "GraphDatabase" "definition" 
         "Database designed to store and query graph-structured data" 
         "source: technical_documentation confidence: 0.95")
(Property "GraphDatabase" "example" 
         "Neo4j, Amazon Neptune, JanusGraph" 
         "source: industry_survey confidence: 0.9")
(Property "GraphDatabase" "query_language" 
         "Cypher, Gremlin, SPARQL" 
         "source: technical_documentation confidence: 0.9")

(Entity "Neo4j" "Technology")
(Property "Neo4j" "type" 
         "Graph database management system" 
         "source: official_documentation confidence: 0.95")
(Property "Neo4j" "query_language" 
         "Cypher" 
         "source: official_documentation confidence: 0.95")
(Property "Neo4j" "use_case" 
         "Knowledge graphs, recommendation systems, fraud detection" 
         "source: case_studies confidence: 0.9")

;; Sample relationships with context
(Relationship "ChatbotSystem" "uses" "KnowledgeGraph" 
             "core_component integration_level: high")
(Relationship "ChatbotSystem" "uses" "MeTTa" 
             "for_knowledge_representation confidence: 0.9")
(Relationship "ChatbotSystem" "uses" "Gemini" 
             "for_natural_language_understanding confidence: 0.95")
(Relationship "KnowledgeGraph" "implementedIn" "MeTTa" 
             "primary_implementation confidence: 0.9")
(Relationship "ChatbotSystem" "implements" "GraphRAG" 
             "for_enhanced_responses confidence: 0.9")
(Relationship "ChatbotSystem" "uses" "EntityExtraction" 
             "for_knowledge_acquisition confidence: 0.85")
(Relationship "ChatbotSystem" "implements" "MultimodalUnderstanding" 
             "for_image_and_text_processing confidence: 0.9")
(Relationship "GraphRAG" "uses" "KnowledgeGraph" 
             "as_knowledge_source confidence: 0.95")
(Relationship "GraphRAG" "enhances" "Gemini" 
             "with_structured_knowledge confidence: 0.9")
(Relationship "EntityExtraction" "populates" "KnowledgeGraph" 
             "from_unstructured_data confidence: 0.9")
(Relationship "MultimodalUnderstanding" "enhances" "EntityExtraction" 
             "with_visual_information confidence: 0.85")
(Relationship "KnowledgeGraph" "storedIn" "GraphDatabase" 
             "for_efficient_querying confidence: 0.9")
(Relationship "Neo4j" "isA" "GraphDatabase" 
             "popular_implementation confidence: 0.95")

;; Sample categories with descriptions
(Category "Basics" "Root" 
         "Fundamental concepts and definitions")
(Category "Usage" "Root" 
         "How to use and interact with the system")
(Category "Technical" "Root" 
         "Technical details and implementation specifics")
(Category "Implementation" "Technical" 
         "Specific implementation details and technologies")
(Category "Concepts" "Basics" 
         "Theoretical concepts and principles")
(Category "Features" "Usage" 
         "Specific features and capabilities of the system")

;; Sample synonyms with confidence scores
(Synonym "KnowledgeGraph" "KG" 0.95)
(Synonym "KnowledgeGraph" "Knowledge Base" 0.85)
(Synonym "ChatbotSystem" "FAQ Assistant" 0.9)
(Synonym "MeTTa" "Meta Language" 0.8)
(Synonym "GraphRAG" "Graph-based RAG" 0.9)
(Synonym "GraphRAG" "Knowledge Graph RAG" 0.85)
(Synonym "EntityExtraction" "Entity Recognition" 0.9)
(Synonym "EntityExtraction" "Information Extraction" 0.8)
(Synonym "MultimodalUnderstanding" "Multimodal AI" 0.9)
(Synonym "MultimodalUnderstanding" "Cross-modal Understanding" 0.8)
(Synonym "GraphDatabase" "Graph DB" 0.95)
(Synonym "Neo4j" "Neo4j Graph Database" 0.9)

;; Sample context relationships with weights
(Context "KnowledgeGraph" "semantic_search" 0.9)
(Context "KnowledgeGraph" "data_storage" 0.8)
(Context "ChatbotSystem" "user_interaction" 0.95)
(Context "MeTTa" "graph_processing" 0.9)
(Context "Gemini" "natural_language_processing" 0.95)
(Context "Gemini" "image_understanding" 0.9)
(Context "GraphRAG" "information_retrieval" 0.9)
(Context "GraphRAG" "context_awareness" 0.85)
(Context "EntityExtraction" "natural_language_processing" 0.9)
(Context "EntityExtraction" "computer_vision" 0.8)
(Context "MultimodalUnderstanding" "computer_vision" 0.9)
(Context "MultimodalUnderstanding" "natural_language_processing" 0.9)
(Context "GraphDatabase" "data_management" 0.9)
(Context "Neo4j" "graph_query" 0.95) 