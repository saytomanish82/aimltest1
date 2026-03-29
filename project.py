"""
main entry point for the Medical AI Assistant application.

Architecture: Modular Monolithic Design
- Data Module (data_module.py): Knowledge Base containing medical graph and disease info
- Medical Module (medical_module.py): Controller/Logic layer with DFS diagnosis engine
- UI Module (ui_module.py): View layer with Tkinter GUI components

This application uses a Rule-Based Expert System with DFS algorithm to navigate a symptom-disease Directed Acyclic Graph (DAG).
"""

import tkinter as tk
from ui_module import MedicalAIApp


def main():
    """
    initialize the MedicalAIApplication and start the Tkinter event loop.
    """
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Initialize the Medical AI Application
    app = MedicalAIApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
