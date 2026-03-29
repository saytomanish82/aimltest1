"""
Medical Information Module - Controller/Logic Layer
Contains the diagnosis engine using DFS (Depth-First Search) algorithm.
This module handles the medical reasoning and navigation logic.
"""

from data_module import medical_graph, disease_info, get_options, is_leaf_node, get_disease_info


class DiagnosisEngine:
    """
    Diagnosis Engine using DFS algorithm to navigate the symptom-disease graph.
    Handles the core medical reasoning logic.
    """
    
    def __init__(self):
        self.current_node = "Start"
        self.diagnosis_path = []  # Track the path taken for diagnosis
    
    def reset(self):
        self.current_node = "Start"
        self.diagnosis_path = []
    
    def get_current_options(self):
        """
        Get available options from current node.
        
        Returns:
            list: List of available symptom/disease options
        """
        return get_options(self.current_node)
    
    def dfs_search(self, choice):
        """
        Perform DFS traversal based on user's symptom choice.
        
        Args:
            choice (str): User's selected symptom/option
            
        Returns:
            tuple: (is_diagnosis_complete, result)
                - If diagnosis complete: (True, disease_name)
                - If more options needed: (False, None)
        """
        # Add choice to the diagnosis path
        self.diagnosis_path.append(choice)
        
        # Check if choice is a leaf node (disease)
        if is_leaf_node(choice):
            return (True, choice)
        
        # Get next options from the chosen node
        next_options = get_options(choice)
        
        # If only one option and it's a disease (leaf node), return diagnosis
        if len(next_options) == 1 and is_leaf_node(next_options[0]):
            self.diagnosis_path.append(next_options[0])
            return (True, next_options[0])
        
        # Continue traversal - update current node
        self.current_node = choice
        return (False, None)
    
    def get_diagnosis_path(self):
        """
        Get the path taken during diagnosis.
        
        Returns:
            list: List of nodes visited during diagnosis
        """
        return self.diagnosis_path.copy()
    
    def get_disease_details(self, disease_name):
        """
        Get detailed information about a disease.
        
        Args:
            disease_name (str): Name of the diagnosed disease
            
        Returns:
            dict: Dictionary containing symptoms and precautions
        """
        return get_disease_info(disease_name)


class PatientSession:
    """
    Manages patient session information.
    Handles user data and session state.
    """
    
    def __init__(self):
        self.user_name = ""
        self.diagnosis_engine = DiagnosisEngine()
    
    def set_user_name(self, name):
        """
        Set the patient's name.
        
        Args:
            name (str): Patient's name
        """
        self.user_name = name
    
    def get_user_name(self):
        return self.user_name
    
    def is_valid_name(self, name):
        return name and name.strip() != ""
    
    def reset_session(self):
        """Reset the diagnosis while keeping user name."""
        self.diagnosis_engine.reset()
    
    def full_reset(self):
        """Completely reset the session including user name."""
        self.user_name = ""
        self.diagnosis_engine.reset()
