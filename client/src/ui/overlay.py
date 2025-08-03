"""Sci-fi transparent overlay UI for displaying AI responses."""

import tkinter as tk
from tkinter import scrolledtext
import threading
import time


class SciFiOverlay:
    """Beautiful sci-fi aesthetic overlay window for AI responses."""
    
    def __init__(self):
        self.window = None
        self.text_widget = None
        self.status_label = None  # Initialize status_label
        self.is_visible = False
        
        # Sci-fi color scheme (Claude Code inspired)
        self.bg_color = "#0d1117"  # Dark background
        self.fg_color = "#f0f6fc"  # Light text
        self.accent_color = "#58a6ff"  # Blue accent
        self.border_color = "#30363d"  # Border
        self.success_color = "#56d364"  # Green for success
        self.warning_color = "#f85149"  # Red for errors
        
    def create_window(self):
        """Create the overlay window with sci-fi aesthetics."""
        if self.window is not None:
            return
            
        # Create the main window
        self.window = tk.Toplevel()
        self.window.title("AI Gaming Assistant")
        self.window.configure(bg=self.bg_color)
        
        # Window properties
        self.window.geometry("400x300+100+100")  # ~5cm x 10cm at standard DPI
        self.window.resizable(True, True)
        self.window.attributes("-topmost", True)  # Always on top
        self.window.attributes("-alpha", 0.9)  # Slight transparency
        
        # Create the frame with sci-fi border
        main_frame = tk.Frame(
            self.window,
            bg=self.bg_color,
            highlightbackground=self.border_color,
            highlightthickness=2,
            relief="solid"
        )
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Title bar with ASCII art styling
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill="x", pady=(5, 10))
        
        title_label = tk.Label(
            title_frame,
            text="╔══ AI GAMING ASSISTANT ══╗",
            bg=self.bg_color,
            fg=self.accent_color,
            font=("Consolas", 10, "bold")
        )
        title_label.pack()
        
        # Status indicator
        self.status_label = tk.Label(
            title_frame,
            text="║ Status: Ready           ║",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Consolas", 8)
        )
        self.status_label.pack()
        
        # Separator
        separator_label = tk.Label(
            title_frame,
            text="╚═════════════════════════╝",
            bg=self.bg_color,
            fg=self.accent_color,
            font=("Consolas", 10, "bold")
        )
        separator_label.pack()
        
        # Text display area with scrollbar
        text_frame = tk.Frame(main_frame, bg=self.bg_color)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_widget = scrolledtext.ScrolledText(
            text_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.accent_color,
            selectbackground=self.accent_color,
            selectforeground=self.bg_color,
            font=("Consolas", 9),
            wrap=tk.WORD,
            relief="flat",
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground=self.border_color
        )
        self.text_widget.pack(fill="both", expand=True)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill="x", pady=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="✕ Close",
            bg=self.warning_color,
            fg=self.bg_color,
            font=("Consolas", 8, "bold"),
            relief="flat",
            command=self.hide_window,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="○ Clear",
            bg=self.border_color,
            fg=self.fg_color,
            font=("Consolas", 8, "bold"),
            relief="flat",
            command=self.clear_text,
            cursor="hand2"
        )
        clear_btn.pack(side="right", padx=5)
        
        # Initially hide the window
        self.window.withdraw()
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
    def show_window(self):
        """Show the overlay window."""
        if self.window is None:
            self.create_window()
        
        self.window.deiconify()
        self.window.lift()
        self.window.attributes("-topmost", True)
        self.is_visible = True
        
    def hide_window(self):
        """Hide the overlay window."""
        if self.window is not None:
            self.window.withdraw()
        self.is_visible = False
        
    def update_status(self, status: str, color: str = None):
        """Update the status indicator."""
        if self.status_label is None:
            return
            
        if color is None:
            color = self.fg_color
            
        # Format status with padding
        formatted_status = f"║ Status: {status:<15} ║"
        self.status_label.config(text=formatted_status, fg=color)
        
    def display_response(self, response: str, show_window: bool = True):
        """Display AI response in the overlay."""
        if show_window:
            self.show_window()
            
        if self.text_widget is None:
            return
            
        # Clear previous content
        self.text_widget.delete(1.0, tk.END)
        
        # Add timestamp header
        timestamp = time.strftime("%H:%M:%S")
        header = f"[{timestamp}] AI Response:\n" + "─" * 30 + "\n\n"
        
        self.text_widget.insert(tk.END, header, "header")
        self.text_widget.insert(tk.END, response)
        
        # Configure text tags for styling
        self.text_widget.tag_config("header", foreground=self.accent_color, font=("Consolas", 9, "bold"))
        
        # Auto-scroll to top
        self.text_widget.see(1.0)
        
        # Update status
        self.update_status("Response Ready", self.success_color)
        
    def display_error(self, error: str):
        """Display error message in the overlay."""
        self.show_window()
        
        if self.text_widget is None:
            return
            
        # Clear previous content
        self.text_widget.delete(1.0, tk.END)
        
        # Add error header
        timestamp = time.strftime("%H:%M:%S")
        header = f"[{timestamp}] ERROR:\n" + "─" * 30 + "\n\n"
        
        self.text_widget.insert(tk.END, header, "error_header")
        self.text_widget.insert(tk.END, error)
        
        # Configure error styling
        self.text_widget.tag_config("error_header", foreground=self.warning_color, font=("Consolas", 9, "bold"))
        
        # Auto-scroll to top
        self.text_widget.see(1.0)
        
        # Update status
        self.update_status("Error", self.warning_color)
        
    def clear_text(self):
        """Clear the text display."""
        if self.text_widget is not None:
            self.text_widget.delete(1.0, tk.END)
        self.update_status("Ready")
        
    def set_processing_status(self):
        """Show processing status with animation."""
        if self.text_widget is not None:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, "🤖 Processing your request...\n\n")
            self.text_widget.insert(tk.END, "⚡ Analyzing screenshot\n")
            self.text_widget.insert(tk.END, "🎤 Transcribing voice\n") 
            self.text_widget.insert(tk.END, "🧠 Generating response\n")
        
        self.update_status("Processing...", self.accent_color)
        self.show_window()


# Global overlay instance
_overlay_instance = None


def get_overlay() -> SciFiOverlay:
    """Get or create the global overlay instance."""
    global _overlay_instance
    if _overlay_instance is None:
        _overlay_instance = SciFiOverlay()
    return _overlay_instance