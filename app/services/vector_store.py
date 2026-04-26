import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Global variables to hold the embedding model, FAISS index, and dataset.
# Kept global so they are only initialized once when the module loads.
model = None
index = None
resources_data = []

def _initialize_vector_store():
    global model, index, resources_data
    
    # 1. Initialize the embedding model (downloads the first time it runs)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # 2. Small dataset of learning resources across different skills
    resources_data = [
        # Python
        {
            "title": "Python for Beginners - Full Course",
            "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
            "description": "Learn the basics of Python programming in this comprehensive video tutorial.",
            "skill": "Python"
        },
        {
            "title": "Official Python Tutorial",
            "url": "https://docs.python.org/3/tutorial/index.html",
            "description": "The official documentation and tutorial for the Python programming language.",
            "skill": "Python"
        },
        {
            "title": "Real Python Tutorials",
            "url": "https://realpython.com/",
            "description": "In-depth articles, tutorials, and video courses for Python developers.",
            "skill": "Python"
        },
        {
            "title": "Automate the Boring Stuff with Python",
            "url": "https://automatetheboringstuff.com/",
            "description": "A practical programming book for total beginners.",
            "skill": "Python"
        },
        
        # SQL
        {
            "title": "SQL Tutorial - Full Database Course for Beginners",
            "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
            "description": "Learn SQL basics, database management, and queries in this full course.",
            "skill": "SQL"
        },
        {
            "title": "Mode SQL Tutorial",
            "url": "https://mode.com/sql-tutorial/",
            "description": "Interactive SQL tutorial ranging from basic to advanced analytical functions.",
            "skill": "SQL"
        },
        {
            "title": "PostgreSQL Official Documentation",
            "url": "https://www.postgresql.org/docs/",
            "description": "Complete reference manual and tutorial for PostgreSQL relational databases.",
            "skill": "SQL"
        },
        {
            "title": "SQLBolt",
            "url": "https://sqlbolt.com/",
            "description": "Learn SQL with simple, interactive exercises.",
            "skill": "SQL"
        },
        
        # System Design
        {
            "title": "System Design Primer",
            "url": "https://github.com/donnemartin/system-design-primer",
            "description": "Learn how to design large-scale systems. Prep for the system design interview.",
            "skill": "System Design"
        },
        {
            "title": "Grokking the System Design Interview",
            "url": "https://www.educative.io/courses/grokking-the-system-design-interview",
            "description": "A highly recommended course for understanding scalable architectures and design patterns.",
            "skill": "System Design"
        },
        {
            "title": "InfoQ System Architecture",
            "url": "https://www.infoq.com/architecture-design/",
            "description": "Articles, presentations, and interviews on modern software architecture.",
            "skill": "System Design"
        },
        {
            "title": "AWS Architecture Center",
            "url": "https://aws.amazon.com/architecture/",
            "description": "Reference architectures and best practices for building scalable systems on AWS.",
            "skill": "System Design"
        },
        
        # Machine Learning
        {
            "title": "Machine Learning by Andrew Ng",
            "url": "https://www.coursera.org/specializations/machine-learning-introduction",
            "description": "The definitive foundational course on machine learning, algorithms, and deep learning.",
            "skill": "Machine Learning"
        },
        {
            "title": "Fast.ai Practical Deep Learning",
            "url": "https://course.fast.ai/",
            "description": "A practical, top-down approach to deep learning using PyTorch.",
            "skill": "Machine Learning"
        },
        {
            "title": "Scikit-Learn Documentation",
            "url": "https://scikit-learn.org/stable/user_guide.html",
            "description": "Comprehensive guide for implementing machine learning algorithms in Python.",
            "skill": "Machine Learning"
        },
        {
            "title": "Hands-On Machine Learning with Scikit-Learn and TensorFlow",
            "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/",
            "description": "An excellent book focusing on practical ML implementation in Python.",
            "skill": "Machine Learning"
        }
    ]
    
    # 3. Convert descriptions into embeddings
    descriptions = [res["description"] for res in resources_data]
    embeddings = model.encode(descriptions)
    
    # SentenceTransformers returns a numpy array, ensure it's float32 for FAISS
    embeddings = np.array(embeddings).astype("float32")
    
    # 4. Store embeddings using FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

# Initialize everything immediately when the module is imported
print("Initializing RAG vector store... This may take a moment to download the model.")
_initialize_vector_store()
print("RAG vector store initialized successfully.")

def retrieve_resources(skill: str) -> List[Dict[str, str]]:
    """
    Retrieves the top 5 most relevant learning resources for a given skill.
    """
    if not skill or not skill.strip():
        raise ValueError("Skill input cannot be empty.")
        
    # Generate embedding for the requested skill
    skill_embedding = model.encode([skill]).astype("float32")
    
    # Perform similarity search in FAISS (k = top 5)
    k = min(5, len(resources_data))
    distances, indices = index.search(skill_embedding, k)
    
    # Check if we got any results
    if len(indices) == 0 or len(indices[0]) == 0:
        raise ValueError(f"No resources found for skill: {skill}")
        
    results = []
    for idx in indices[0]:
        # Handle cases where FAISS returns -1 (unlikely with IndexFlatL2 but good practice)
        if idx == -1:
            continue
            
        resource = resources_data[idx]
        
        # Format the output strictly as requested
        results.append({
            "title": resource["title"],
            "url": resource["url"],
            "description": resource["description"]
        })
        
    if not results:
        raise ValueError(f"No resources found for skill: {skill}")
        
    return results
