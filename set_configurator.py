import json
import tkinter as tk
from tkinter import ttk, messagebox

class SetConfigurator:
    def __init__(self):
        # Load data
        with open('artifact_sets.json', 'r') as f:
            self.artifact_sets = json.load(f)
        with open('character_weights.json', 'r') as f:
            self.character_weights = json.load(f)
        
        # Get character list
        self.characters = sorted([char["Character"].strip() for char in self.character_weights])
        
        # Setup window
        self.window = tk.Tk()
        self.window.title("Artifact Set Configurator")
        self.window.geometry("800x700")
        self.window.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Segoe UI', 12), background='#f0f0f0')
        style.configure('Section.TFrame', background='#f0f0f0')
        
        # Create main container
        main_container = ttk.Frame(self.window, padding="20", style='Section.TFrame')
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(
            main_container,
            text="Artifact Set Configurator",
            style='Title.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # Left panel - Set selection
        left_panel = ttk.LabelFrame(
            main_container,
            text="Artifact Sets",
            padding="10"
        )
        left_panel.grid(row=1, column=0, padx=(0, 10), sticky=(tk.N, tk.S, tk.W))
        
        # Set listbox with scrollbar
        set_frame = ttk.Frame(left_panel)
        set_frame.grid(row=0, column=0, pady=5)
        
        self.set_listbox = tk.Listbox(
            set_frame,
            width=30,
            height=20,
            font=('Segoe UI', 10),
            exportselection=0  # Prevent deselection when clicking elsewhere
        )
        self.set_listbox.grid(row=0, column=0, sticky=(tk.N, tk.S))
        
        # Add scrollbar to set listbox
        set_scrollbar = ttk.Scrollbar(set_frame, orient="vertical", command=self.set_listbox.yview)
        set_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.set_listbox.configure(yscrollcommand=set_scrollbar.set)
        
        # Populate set listbox
        for set_name in sorted(self.artifact_sets.keys()):
            self.set_listbox.insert(tk.END, set_name)
        
        # Right panel - Set details and configuration
        right_panel = ttk.LabelFrame(
            main_container,
            text="Set Configuration",
            padding="10"
        )
        right_panel.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        # Set info
        self.set_info = tk.Text(
            right_panel,
            height=5,
            width=50,
            font=('Segoe UI', 10),
            wrap=tk.WORD
        )
        self.set_info.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Character selection
        ttk.Label(
            right_panel,
            text="Add Character:",
            style='Header.TLabel'
        ).grid(row=1, column=0, pady=5, sticky=tk.W)
        
        self.char_combo = ttk.Combobox(
            right_panel,
            values=self.characters,
            width=25,
            font=('Segoe UI', 10)
        )
        self.char_combo.grid(row=1, column=1, pady=5, sticky=tk.W)
        
        # Add character filtering
        self.char_combo.bind('<KeyRelease>', self.filter_characters)
        
        # Priority selection
        ttk.Label(
            right_panel,
            text="Priority:",
            style='Header.TLabel'
        ).grid(row=2, column=0, pady=5, sticky=tk.W)
        
        self.priority_combo = ttk.Combobox(
            right_panel,
            values=["1.0 (Best in Slot)", "0.8 (Alternative)"],
            width=25,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.priority_combo.grid(row=2, column=1, pady=5, sticky=tk.W)
        
        # Add character button
        ttk.Button(
            right_panel,
            text="Add Character",
            command=self.add_character,
            padding=(20, 5)
        ).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Current characters list
        ttk.Label(
            right_panel,
            text="Current Characters:",
            style='Header.TLabel'
        ).grid(row=4, column=0, columnspan=2, pady=(10, 5), sticky=tk.W)
        
        self.char_listbox = tk.Listbox(
            right_panel,
            width=40,
            height=10,
            font=('Segoe UI', 10)
        )
        self.char_listbox.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Remove character button
        ttk.Button(
            right_panel,
            text="Remove Selected Character",
            command=self.remove_character,
            padding=(20, 5)
        ).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Save button
        ttk.Button(
            right_panel,
            text="Save Changes",
            command=self.save_changes,
            padding=(20, 5)
        ).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Select first set by default
        self.set_listbox.selection_set(0)
        self.on_set_select(None)
    
    def on_set_select(self, event):
        if not self.set_listbox.curselection():
            return
            
        set_name = self.set_listbox.get(self.set_listbox.curselection())
        set_data = self.artifact_sets[set_name]
        
        # Update set info
        self.set_info.delete(1.0, tk.END)
        self.set_info.insert(tk.END, f"Set: {set_name}\n")
        self.set_info.insert(tk.END, f"2pc: {set_data['2pc']}\n")
        self.set_info.insert(tk.END, f"4pc: {set_data['4pc']}\n")
        
        # Update character list
        self.char_listbox.delete(0, tk.END)
        for char in set_data["recommended_for"]:
            priority = set_data["priority"].get(char, "0.8")
            self.char_listbox.insert(tk.END, f"{char} (Priority: {priority})")
    
    def add_character(self):
        selected_indices = self.set_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select an artifact set first.")
            return
            
        char = self.char_combo.get()
        if not char or char not in self.characters:
            messagebox.showwarning("Warning", "Please select a valid character.")
            return
            
        priority_str = self.priority_combo.get()
        if not priority_str:
            messagebox.showwarning("Warning", "Please select a priority.")
            return
            
        priority = 1.0 if "1.0" in priority_str else 0.8
        
        set_name = self.set_listbox.get(selected_indices[0])
        set_data = self.artifact_sets[set_name]
        
        if char not in set_data["recommended_for"]:
            set_data["recommended_for"].append(char)
        set_data["priority"][char] = priority
        
        self.on_set_select(None)  # Refresh display
    
    def remove_character(self):
        if not self.set_listbox.curselection():
            messagebox.showwarning("Warning", "Please select an artifact set first.")
            return
            
        if not self.char_listbox.curselection():
            messagebox.showwarning("Warning", "Please select a character to remove.")
            return
            
        set_name = self.set_listbox.get(self.set_listbox.curselection())
        char_entry = self.char_listbox.get(self.char_listbox.curselection())
        char_name = char_entry.split(" (Priority")[0]
        
        set_data = self.artifact_sets[set_name]
        if char_name in set_data["recommended_for"]:
            set_data["recommended_for"].remove(char_name)
        if char_name in set_data["priority"]:
            del set_data["priority"][char_name]
        
        self.on_set_select(None)  # Refresh display
    
    def save_changes(self):
        try:
            with open('artifact_sets.json', 'w') as f:
                json.dump(self.artifact_sets, f, indent=4)
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
    
    def filter_characters(self, event):
        """Filter characters based on user input"""
        current_text = self.char_combo.get().lower()
        filtered_chars = [char for char in self.characters if current_text in char.lower()]
        
        if filtered_chars:
            self.char_combo['values'] = filtered_chars
            
            # Check for exact match first
            exact_matches = [char for char in filtered_chars if char.lower() == current_text]
            if exact_matches:
                self.char_combo.set(exact_matches[0])
            # Then check for single match that starts with the input
            elif len(filtered_chars) == 1:
                self.char_combo.set(filtered_chars[0])
            # Finally check for any single match that contains the input
            elif len(filtered_chars) > 1:
                starts_with = [char for char in filtered_chars if char.lower().startswith(current_text)]
                if len(starts_with) == 1:
                    self.char_combo.set(starts_with[0])
                else:
                    self.char_combo.set(current_text)
        else:
            # No matches found, keep the text but show all characters
            self.char_combo['values'] = self.characters
            self.char_combo.set(current_text)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    configurator = SetConfigurator()
    configurator.run()
