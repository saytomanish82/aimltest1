"""
Data Module - Knowledge Base
Contains the medical symptom-disease graph and disease information database.
This module serves as the data layer for the Medical AI Assistant.
"""

# Symptom-Disease Graph (Directed Acyclic Graph)
# Structure: Each key maps to possible sub-symptoms or final diseases
medical_graph = {
    "Start": ["Fever", "Cough", "Skin Rash"],
    "Fever": ["High Grade", "Low Grade"],
    "High Grade": ["Malaria"],
    "Low Grade": ["Common Cold"],
    "Cough": ["Persistent", "Short-term"],
    "Persistent": ["Tuberculosis"],
    "Short-term": ["Bronchitis"],
    "Skin Rash": ["Itchy", "Non-itchy"],
    "Itchy": ["Chickenpox"],
    "Non-itchy": ["Measles"]
}

# Disease Information Database
# Contains symptoms and precautions for each diagnosed disease
disease_info = {
    "Malaria": {
        "symptoms": "High fever, chills, sweating, headache, and nausea.",
        "precautions": "Use mosquito nets, wear long sleeves, and use insect repellent."
    },
    "Common Cold": {
        "symptoms": "Runny nose, sneezing, sore throat, and mild cough.",
        "precautions": "Rest, stay hydrated, and wash hands frequently."
    },
    "Tuberculosis": {
        "symptoms": "Chronic cough (often with blood), chest pain, weight loss, and fatigue.",
        "precautions": "Wear a mask, ensure good ventilation, and complete the full antibiotic course."
    },
    "Bronchitis": {
        "symptoms": "Cough with mucus, shortness of breath, and chest discomfort.",
        "precautions": "Avoid smoke and air pollutants, use a humidifier, and get plenty of rest."
    },
    "Chickenpox": {
        "symptoms": "Itchy red blisters, fever, and tiredness.",
        "precautions": "Avoid scratching, stay isolated to prevent spread, and use calamine lotion."
    },
    "Measles": {
        "symptoms": "High fever, dry cough, runny nose, and a characteristic skin rash.",
        "precautions": "Isolate from others, stay hydrated, and ensure vitamin A intake."
    }
}


def get_disease_info(disease_name):
    """
    Retrieves disease information from the database.
    
    Args:
        disease_name (str): Name of the disease to look up
        
    Returns:
        dict: Dictionary containing symptoms and precautions, or empty dict if not found
    """
    return disease_info.get(disease_name, {})


def get_options(node):
    """
    Gets the next options/symptoms available from a given node in the graph.
    
    Args:
        node (str): Current node in the symptom graph
        
    Returns:
        list: List of available options from the current node
    """
    return medical_graph.get(node, [])


def is_leaf_node(node):
    """
    Checks if a node is a leaf node (disease/final diagnosis).
    
    Args:
        node (str): Node to check
        
    Returns:
        bool: True if node is a leaf node, False otherwise
    """
    return node not in medical_graph
