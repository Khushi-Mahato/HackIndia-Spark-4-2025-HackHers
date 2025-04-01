;; Define the basic entity types
(= (Entity $name $type) (HasType $name $type))

;; Define relationships between entities with context
(= (Relationship $from $type $to $context) 
   (HasRelation $from $type $to $context))

;; Define properties for entities with metadata
(= (Property $entity $key $value $metadata) 
   (HasProperty $entity $key $value $metadata))

;; Define FAQ entries with metadata and related concepts
(= (FAQ $question $answer $category $concepts)
   (HasFAQ $question $answer $category $concepts))

;; Define category hierarchies with descriptions
(= (Category $name $parent $description)
   (HasParent $name $parent $description))

;; Define synonyms and semantic equivalents
(= (Synonym $term $equivalent $confidence)
   (HasSynonym $term $equivalent $confidence))

;; Define context relationships with weights
(= (Context $entity $context $weight)
   (HasContext $entity $context $weight))

;; Helper function to get all properties of an entity with metadata
(= (GetPropertiesWithMetadata $entity)
   (match &self (Property $entity $key $value $metadata)
          (PropertyInfo $key $value $metadata)))

;; Helper function to get related entities with context
(= (GetRelatedWithContext $entity)
   (match &self (Relationship $entity $type $to $context)
          (RelatedInfo $to $type $context)))

;; Helper function to get FAQs by category
(= (GetFAQsByCategory $category)
   (match &self (FAQ $question $answer $category $concepts)
          (FAQEntry $question $answer)))

;; Helper function to find similar terms using synonyms
(= (FindSimilarTerms $term)
   (match &self (Synonym $term $equivalent $confidence)
          (SimilarTerm $equivalent $confidence)))

;; Helper function to get category hierarchy
(= (GetCategoryHierarchy $category)
   (match &self (Category $category $parent $description)
          (CategoryInfo $parent $description)))

;; Helper function to get weighted context
(= (GetWeightedContext $entity)
   (match &self (Context $entity $context $weight)
          (ContextInfo $context $weight)))

;; Helper function to search across all FAQs
(= (SearchFAQs $query)
   (match &self (FAQ $question $answer $category $concepts)
          (FAQMatch $question $answer $category))) 