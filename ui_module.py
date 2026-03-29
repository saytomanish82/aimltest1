"""
UI Module :- 
	- This module contains the Tkinter GUI components for the Medical AI Assistant.
	- This module handles all user interface elements and interactions.
"""

import tkinter as tk
from tkinter import messagebox
from medical_module import PatientSession


class UIConfig:
    """Configuration class for UI colors and styling."""
    
    # Color palette - warm and stress-reducing
    BG_WARM = "#FFF5E1"          # Cream background
    BTN_WARM = "#FF6B6B"          # Coral buttons
    TEXT_COLOR = "#4A4A4A"        # Dark gray text
    ACCENT_COLOR = "#E67E22"      # Orange accent
    CARD_BG = "#FFF9F0"           # Light cream for cards
    CARD_BORDER = "#FFD8A8"       # Light orange border
    DISCLAIMER_COLOR = "#C0392B"  # Red for disclaimer
    
    # Window settings
    WINDOW_TITLE = "AI Medical Assistant"
    WINDOW_SIZE = "500x620"
    
    # Font settings
    TITLE_FONT = ("Arial", 18, "bold")
    HEADING_FONT = ("Arial", 16, "bold")
    LABEL_FONT = ("Arial", 12, "bold")
    NORMAL_FONT = ("Arial", 11)
    BUTTON_FONT = ("Arial", 10, "bold")
    SMALL_FONT = ("Arial", 10)
    DISCLAIMER_FONT = ("Arial", 9, "bold italic")


class MedicalAIApp:
    """
    This class module handles the GUI and user interactions.
    """
    
    def __init__(self, root):
        """
        Initialize the Medical AI Application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(UIConfig.WINDOW_TITLE)
        self.root.geometry(UIConfig.WINDOW_SIZE)
        self.root.configure(bg=UIConfig.BG_WARM)
        
        # Initialize patient session (contains diagnosis engine)
        self.patient_session = PatientSession()
        
        # Main container
        self.main_container = tk.Frame(self.root, bg=UIConfig.BG_WARM)
        self.main_container.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Button frame for symptom options
        self.button_frame = None
        
        # Start with name screen
        self.setup_name_screen()
    
    def clear_container(self):
        """Clear all widgets from the main container."""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def create_label(self, parent, text, font=None, fg=None, **kwargs):
        """
        Create a styled label.
        
        Args:
            parent: Parent widget
            text: Label text
            font: Font tuple (optional)
            fg: Foreground color (optional)
            **kwargs: Additional label options
            
        Returns:
            tk.Label: Created label widget
        """
        return tk.Label(parent, text=text, font=font or UIConfig.NORMAL_FONT, bg=kwargs.pop('bg', UIConfig.BG_WARM), fg=fg or UIConfig.TEXT_COLOR, **kwargs
        )
    
    def create_button(self, parent, text, command, width=25, **kwargs):
        """
        Create a styled button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command callback
            width: Button width (default 25)
            **kwargs: Additional button options
            
        Returns:
            tk.Button: Created button widget
        """
        return tk.Button(parent, text=text, width=width, font=UIConfig.BUTTON_FONT, bg=UIConfig.BTN_WARM, fg="white",
            activebackground="#FF8787", relief="flat", cursor="hand2", command=command,
            **kwargs
        )
    
    def setup_name_screen(self):
        """Setup the initial name entry screen."""
        self.clear_container()
        
        # Title
        self.create_label(self.main_container, "Medical AI Assistant", font=UIConfig.TITLE_FONT, fg=UIConfig.BTN_WARM).pack(pady=30)
        
        # Instructions
        self.create_label(self.main_container, "Please enter your name to begin:", font=UIConfig.NORMAL_FONT).pack(pady=10)
        
        # Name entry
        self.name_entry = tk.Entry(self.main_container, font=UIConfig.LABEL_FONT, width=25, justify='center')
        self.name_entry.pack(pady=10)
        
        # Start button
        start_btn = self.create_button(self.main_container, "Start Diagnosis", self.start_app)
        start_btn.pack(pady=20, ipady=8, ipadx=15)
    
    def start_app(self):
        """Handle the start diagnosis button click."""
        name = self.name_entry.get().strip()
        
        if not self.patient_session.is_valid_name(name):
            messagebox.showwarning("Input Required", "Please enter your name.")
            return
        
        self.patient_session.set_user_name(name)
        self.show_symptom_screen()
    
    def show_symptom_screen(self):
        """Display the symptom selection screen."""
        self.clear_container()
        
        # Patient name display
        self.create_label(self.main_container, "Patient: {self.patient_session.get_user_name()}", font=UIConfig.LABEL_FONT).pack(pady=5)
        
        # Instructions
        self.create_label(self.main_container, "Select your current symptom:", font=UIConfig.NORMAL_FONT, wraplength=400).pack(pady=15)
        
        # Button frame for options
        self.button_frame = tk.Frame(self.main_container, bg=UIConfig.BG_WARM)
        self.button_frame.pack(pady=10)
        
        self.update_options()
    
    def update_options(self):
        """Update the symptom option buttons based on current state."""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Get current options from diagnosis engine
        options = self.patient_session.diagnosis_engine.get_current_options()
        
        # Create button for each option
        for opt in options:
            btn = self.create_button(self.button_frame, opt, lambda o=opt: self.handle_symptom_selection(o))
            btn.pack(pady=8, ipady=5)
    
    def handle_symptom_selection(self, choice):
        """
        Handle symptom selection by user.
        
        Args:
            choice: Selected symptom/option
        """
        is_complete, disease = self.patient_session.diagnosis_engine.dfs_search(choice)
        
        if is_complete:
            self.display_final_result(disease)
        else:
            self.update_options()
    
    def display_final_result(self, disease):
        """
        Display the final diagnosis result.
        
        Args:
            disease: Diagnosed disease name
        """
        self.clear_container()
        
        # Get disease information
        info = self.patient_session.diagnosis_engine.get_disease_details(disease)
        user_name = self.patient_session.get_user_name()
        
        # Title
        self.create_label(self.main_container, "Assessment Complete", font=UIConfig.HEADING_FONT, fg=UIConfig.ACCENT_COLOR).pack(pady=10)
        
        # Greeting
        self.create_label(self.main_container, "Hello {user_name},", font=UIConfig.LABEL_FONT).pack(anchor="w")
        
        # Result message
        self.create_label(self.main_container, "Based on your symptoms, it is possible you have:", font=UIConfig.NORMAL_FONT).pack(anchor="w", pady=(0, 5))
        
        # Disease name
        self.create_label(self.main_container, disease.upper(), font=("Arial", 20, "bold"), fg=UIConfig.BTN_WARM).pack(pady=15)
        
        # Detail card
        detail_card = tk.Frame(self.main_container, bg=UIConfig.CARD_BG, padx=15, pady=15, highlightbackground=UIConfig.CARD_BORDER, highlightthickness=1)
        detail_card.pack(fill="x", pady=10)
        
        # Symptoms section
        tk.Label(detail_card, text="TYPICAL SYMPTOMS:", font=UIConfig.BUTTON_FONT, bg=UIConfig.CARD_BG, fg=UIConfig.TEXT_COLOR).pack(anchor="w")
        
        tk.Label(detail_card, text=info.get('symptoms', 'Information not available'),
            font=UIConfig.SMALL_FONT, bg=UIConfig.CARD_BG, fg=UIConfig.TEXT_COLOR, wraplength=380, justify="left"
        ).pack(anchor="w", pady=(0, 10))
        
        # Precautions section
        tk.Label(detail_card, text="PRECAUTIONS:",
            font=UIConfig.BUTTON_FONT, bg=UIConfig.CARD_BG, fg=UIConfig.TEXT_COLOR
        ).pack(anchor="w")
        
        tk.Label(detail_card,
            text=info.get('precautions', 'Information not available'),
            font=UIConfig.SMALL_FONT, bg=UIConfig.CARD_BG, fg=UIConfig.TEXT_COLOR,
            wraplength=380,justify="left"
        ).pack(anchor="w")
        
        # Disclaimer
        disclaimer_text = ("MEDICAL ADVICE: Please consult a doctor if your health "
                          "deteriorates further. This is for information only.")
        self.create_label(self.main_container, disclaimer_text,
            font=UIConfig.DISCLAIMER_FONT, fg=UIConfig.DISCLAIMER_COLOR, wraplength=400, pady=20
        ).pack()
        
        # Restart button
        restart_btn = self.create_button(
            self.main_container,
            "Restart Analysis",
            self.reset_app
        )
        restart_btn.pack(pady=10, ipady=8, ipadx=15)
    
    def reset_app(self):
        """Reset the application to start a new diagnosis."""
        self.patient_session.reset_session()
        self.show_symptom_screen()
