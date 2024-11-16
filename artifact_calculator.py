import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class ModernCombobox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            width=20,
            font=('Segoe UI', 10),
            state='readonly'
        )

class ModernEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            width=10,
            font=('Segoe UI', 10)
        )

class ArtifactScoreCalculator:
    def __init__(self):
        # Load character weights and artifact sets
        with open('character_weights.json', 'r') as f:
            self.character_weights = json.load(f)
        with open('artifact_sets.json', 'r') as f:
            self.artifact_sets = json.load(f)

        # Define stat key mappings
        self.stat_key_map = {
            "hp": "HP",
            "hp_": "HP%",
            "atk": "ATK",
            "atk_": "ATK%",
            "def": "DEF",
            "def_": "DEF%",
            "eleMas": "EM",
            "enerRech_": "ER",
            "heal_": "Healing Bonus",
            "critRate_": "CRIT Rate",
            "critDMG_": "CRIT DMG",
            "physical_dmg_": "Physical DMG Bonus",
            "anemo_dmg_": "Anemo DMG Bonus",
            "geo_dmg_": "Geo DMG Bonus",
            "electro_dmg_": "Electro DMG Bonus",
            "hydro_dmg_": "Hydro DMG Bonus",
            "pyro_dmg_": "Pyro DMG Bonus",
            "cryo_dmg_": "Cryo DMG Bonus",
            "dendro_dmg_": "Dendro DMG Bonus"
        }

        # Define set key mappings
        self.set_key_map = {
            "DeepwoodMemories": "Deepwood Memories",
            "ArchaicPetra": "Archaic Petra",
            "BlizzardStrayer": "Blizzard Strayer",
            "CrimsonWitchOfFlames": "Crimson Witch of Flames",
            "DesertPavilionChronicle": "Desert Pavilion Chronicle",
            "EchoesOfAnOffering": "Echoes of an Offering",
            "EmblemOfSeveredFate": "Emblem of Severed Fate",
            "FlowerOfParadiseLost": "Flower of Paradise Lost",
            "FragmentOfHarmonicWhimsy": "Fragment of Harmonic Whimsy",
            "GildedDreams": "Gilded Dreams",
            "GladiatorsFinale": "Gladiator's Finale",
            "GoldenTroupe": "Golden Troupe",
            "HeartOfDepth": "Heart of Depth",
            "HuskOfOpulentDreams": "Husk of Opulent Dreams",
            "MaidenBeloved": "Maiden Beloved",
            "MarechausseeHunter": "Marechaussee Hunter",
            "NighttimeWhispersInTheEchoingWoods": "Nighttime Whispers in the Echoing Woods",
            "NoblesseOblige": "Noblesse Oblige",
            "NymphsDream": "Nymph's Dream",
            "ObsidianCodex": "Obsidian Codex",
            "OceanHuedClam": "Ocean-Hued Clam",
            "PaleFlame":"Pale Flame",
            "RetracingBolide": "Retracing Bolide",
            "ScrollOfTheHeroOfCinderCity": "Scroll of the Hero of Cinder City",
            "ShimenawasReminiscence": "Shimenawa's Reminiscence",
            "SongOfDaysPast": "Song of Days Past",
            "TenacityOfTheMillelith": "Tenacity of the Millelith",
            "ThunderingFury": "Thundering Fury",
            "UnfinishedReverie": "Unfinished Reverie",
            "VermillionHereafter": "Vermillion Hereafter",
            "ViridescentVenerer": "Viridescent Venerer",
            "VourukashasGlow": "Vourukasha's Glow",
            "WanderersTroupe": "Wanderer's Troupe"
        }

        # Define slot key mappings
        self.slot_key_map = {
            "flower": "Flower",
            "plume": "Plume",
            "sands": "Sands",
            "goblet": "Goblet",
            "circlet": "Circlet"
        }

        # Store parsed artifacts
        self.artifacts = []

        # Define theoretical best values for substats
        self.max_substat_values = {
            "CRIT Rate": 23.4,  # 7.8 * 3 rolls
            "CRIT DMG": 46.8,   # 15.6 * 3 rolls
            "ATK%": 34.8,       # 11.6 * 3 rolls
            "HP%": 34.8,        # 11.6 * 3 rolls
            "DEF%": 43.8,       # 14.6 * 3 rolls
            "Flat ATK": 114,    # 38 * 3 rolls
            "Flat HP": 1794,    # 598 * 3 rolls
            "Flat DEF": 138,    # 46 * 3 rolls
            "EM": 138,          # 46 * 3 rolls
            "ER": 32.4         # 10.8 * 3 rolls
        }

        # Setup window
        self.window = tk.Tk()
        self.window.title("Genshin Impact Artifact Calculator")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')

        # Create custom styles for cards
        style = ttk.Style()
        style.configure('Card.TFrame', relief='solid', borderwidth=1)
        style.configure('CardHover.TFrame', relief='solid', borderwidth=1, background='#e0e0e0')

        # Create main frame
        main_frame = ttk.Frame(self.window, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Calculator tab
        calculator_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(calculator_frame, text="Calculator")

        # Artifacts tab
        artifacts_frame = ttk.Frame(self.notebook, padding="5")
        self.notebook.add(artifacts_frame, text="My Artifacts")

        # Left panel for inputs in calculator tab
        left_panel = ttk.Frame(calculator_frame)
        left_panel.grid(row=0, column=0, padx=(0, 5), sticky=(tk.N, tk.W))

        # Create input fields (artifact set, type, main stat, substats)
        self.create_input_fields(left_panel)

        # Right panel for results in calculator tab
        right_panel = ttk.LabelFrame(calculator_frame, text="Character Rankings", padding="5")
        right_panel.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Create scrollable results area
        results_frame = ttk.Frame(right_panel)
        results_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Add scrollbar to results
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.result_text = tk.Text(
            results_frame,
            width=40,
            height=30,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 10)
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.config(command=self.result_text.yview)

        # Create artifacts display in artifacts tab
        self.create_artifacts_display(artifacts_frame)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        calculator_frame.columnconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def create_input_fields(self, parent):
        # Artifact Set selection
        ttk.Label(parent, text="Artifact Set:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.artifact_set = ttk.Combobox(parent, values=sorted(self.artifact_sets.keys()), width=25)
        self.artifact_set.grid(row=0, column=1, columnspan=2, sticky=tk.W, pady=3)

        # Artifact Type selection
        ttk.Label(parent, text="Artifact Type:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.artifact_type = ttk.Combobox(parent, values=["Flower", "Plume", "Sands", "Goblet", "Circlet"], width=25)
        self.artifact_type.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=3)

        # Main Stat selection
        ttk.Label(parent, text="Main Stat:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.main_stat = ttk.Combobox(parent, values=self.get_main_stats(), width=25)
        self.main_stat.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=3)

        # Bind the event to update main stat options
        self.artifact_type.bind('<<ComboboxSelected>>', self.update_main_stat_options)

        # Substats frame
        substat_frame = ttk.LabelFrame(parent, text="Substats", padding="5")
        substat_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.substat_vars = []
        self.substat_value_vars = []
        for i in range(4):
            ttk.Label(substat_frame, text=f"Substat {i+1}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            stat_combo = ttk.Combobox(substat_frame, values=self.get_sub_stats(), width=15)
            stat_combo.grid(row=i, column=1, padx=3, pady=2)
            value_entry = ttk.Entry(substat_frame, width=8)
            value_entry.grid(row=i, column=2, padx=3, pady=2)
            self.substat_vars.append(stat_combo)
            self.substat_value_vars.append(value_entry)

        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_scores).grid(row=0, column=0, padx=3)
        ttk.Button(button_frame, text="Load Test Data", command=self.load_test_data).grid(row=0, column=1, padx=3)
        ttk.Button(button_frame, text="Parse Artifacts", command=self.parse_artifacts).grid(row=0, column=2, padx=3)

    def get_main_stats(self):
        if self.artifact_type.get() == "Flower":
            return ["HP"]
        elif self.artifact_type.get() == "Plume":
            return ["ATK"]
        elif self.artifact_type.get() == "Sands":
            return ["HP%", "ATK%", "DEF%", "EM", "ER"]
        elif self.artifact_type.get() == "Goblet":
            return ["HP%", "ATK%", "DEF%", "EM", 
                   "Physical DMG Bonus", "Pyro DMG Bonus", "Hydro DMG Bonus", 
                   "Cryo DMG Bonus", "Electro DMG Bonus", "Anemo DMG Bonus", 
                   "Geo DMG Bonus", "Dendro DMG Bonus"]
        else:  # Circlet
            return ["HP%", "ATK%", "DEF%", "EM", "CRIT Rate", "CRIT DMG", "Healing Bonus"]

    def get_sub_stats(self):
        return [
            "Flat HP", "Flat ATK", "Flat DEF",
            "HP%", "ATK%", "DEF%",
            "EM", "ER",
            "CRIT Rate", "CRIT DMG"
        ]

    def update_main_stat_options(self, event=None):
        self.main_stat['values'] = self.get_main_stats()
        self.main_stat.set('')

    def calculate_scores(self):
        try:
            # Get artifact details
            artifact_set = self.artifact_set.get()
            artifact_type = self.artifact_type.get()
            main_stat = self.main_stat.get()
            
            # Get substats
            substats = []
            for i in range(4):
                stat = self.substat_vars[i].get()
                if stat:
                    try:
                        value = float(self.substat_value_vars[i].get())
                        substats.append((stat, value))
                    except ValueError:
                        continue

            scores = []
            for char_data in self.character_weights:
                char_name = char_data["Character"].strip()
                
                # Calculate Main Stat Score
                # For Flower (HP) and Plume (ATK), main stat score is always 1
                if artifact_type in ["Flower", "Plume"]:
                    main_stat_score = 100  # 1 * 100
                else:
                    main_stat_key = f"Main {main_stat}"
                    main_stat_score = float(char_data.get(main_stat_key, 0)) * 100

                # Calculate Substat Score
                substat_score = 0
                for stat, value in substats:
                    stat_key = f"Sub {stat}"
                    if stat_key in char_data:
                        # Calculate relative value compared to theoretical best
                        max_value = self.max_substat_values.get(stat, 1)
                        relative_value = value / max_value
                        # Multiply by character's evaluation value for this stat
                        substat_score += relative_value * float(char_data[stat_key]) * 100

                # Calculate base score
                base_score = main_stat_score + substat_score

                # Calculate artifact set multiplier
                set_multiplier = 0.2  # Default multiplier for non-recommended sets
                if artifact_set:
                    set_data = self.artifact_sets[artifact_set]
                    if char_name in set_data["recommended_for"]:
                        # Get the priority value (1.0 for BiS, 0.8 for alternatives)
                        set_multiplier = set_data["priority"].get(char_name, 0.8)
                    else:
                        # Check if character has any recommended sets
                        has_recommended_sets = False
                        for other_set in self.artifact_sets.values():
                            if char_name in other_set["recommended_for"]:
                                has_recommended_sets = True
                                break
                        # If character has no recommended sets, use 0.8 as default
                        if not has_recommended_sets:
                            set_multiplier = 0.8

                # Apply formula: (Main + Sub) x Set Multiplier
                final_score = base_score * set_multiplier

                # Calculate rank based on score and criteria
                rank = self.calculate_rank(final_score, artifact_set, char_name, main_stat, substats)
                
                scores.append((char_name, final_score, rank))

            # Sort scores and display
            scores.sort(key=lambda x: x[1], reverse=True)
            self.display_results(scores, f"Set: {artifact_set}\nType: {artifact_type}\nMain: {main_stat}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_rank(self, score, artifact_set, char_name, main_stat, substats):
        """Calculate the rank (SS, S, A, B, or C) based on score and criteria."""
        # Get character data
        char_data = next((char for char in self.character_weights if char["Character"].strip() == char_name), None)
        if not char_data:
            return "C"

        # Check if artifact set is recommended
        is_correct_set = False
        if artifact_set in self.artifact_sets:
            set_data = self.artifact_sets[artifact_set]
            is_correct_set = char_name in set_data["recommended_for"]

        # Check if main stat is preferred
        main_stat_key = f"Main {main_stat}"
        has_correct_main = main_stat_key in char_data and float(char_data[main_stat_key]) > 0

        # Calculate substat quality
        total_substat_score = 0
        max_possible = 0
        for stat, value in substats:
            stat_key = f"Sub {stat}"
            if stat_key in char_data:
                weight = float(char_data[stat_key])
                max_value = self.max_substat_values.get(stat, 1)
                relative_value = value / max_value
                total_substat_score += relative_value * weight
                max_possible += weight

        substat_quality = total_substat_score / max_possible if max_possible > 0 else 0

        # Determine rank based on criteria
        if score >= 160 and is_correct_set and has_correct_main and substat_quality >= 0.7:
            return "SS"
        elif score >= 120 and is_correct_set and has_correct_main:
            return "S"
        elif score >= 80 and (is_correct_set or has_correct_main):
            return "A"
        elif score >= 40:
            return "B"
        else:
            return "C"

    def display_results(self, scores, artifact_info=""):
        """Display character rankings with formatting."""
        self.result_text.delete(1.0, tk.END)
        
        if artifact_info:
            self.result_text.insert(tk.END, f"Artifact Info:\n{artifact_info}\n\n", "info")
        
        self.result_text.insert(tk.END, "Character Rankings:\n\n")
        
        # Find the maximum score for percentage calculation
        max_score = scores[0][1] if scores else 0
        
        for i, (char, score, rank) in enumerate(scores, 1):
            # Calculate percentage of max score
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            # Format the display
            rank_display = f"{i:2d}."
            char_display = f"{char:15}"
            score_display = f"{score:5.1f} ({percentage:3.0f}%)"
            
            line = f"{rank_display} {char_display} [{rank}] ➤ {score_display}\n"
            
            # Apply different formatting for top 5
            if i <= 5:
                self.result_text.insert(tk.END, line, "bold")
            else:
                self.result_text.insert(tk.END, line)
            
            # Add separator after top 5
            if i == 5:
                self.result_text.insert(tk.END, "-" * 40 + "\n")
        
        # Configure tags for formatting
        self.result_text.tag_configure("bold", font=('Segoe UI', 10, 'bold'))
        self.result_text.tag_configure("info", font=('Segoe UI', 9, 'italic'))

    def load_test_data(self):
        # Set artifact set
        self.artifact_set.set("Crimson Witch of Flames")
        
        # Set type and update main stat options
        self.artifact_type.set("Plume")
        self.update_main_stat_options()
        
        # Set main stat
        self.main_stat.set("ATK")
        
        # Set substats
        test_substats = [
            ("CRIT Rate", "10.1"),
            ("CRIT DMG", "17.9"),
            ("ER", "4.5"),
            ("EM", "23")
        ]
        
        # Clear existing substat values
        for stat_combo, value_entry in zip(self.substat_vars, self.substat_value_vars):
            stat_combo.set('')
            value_entry.delete(0, tk.END)
        
        # Fill in test substats
        for i, (stat, value) in enumerate(test_substats):
            stat_combo = self.substat_vars[i]
            value_entry = self.substat_value_vars[i]
            stat_combo.set(stat)
            value_entry.insert(0, value)
        
        # Calculate scores automatically
        self.calculate_scores()

    def parse_artifacts(self):
        """Parse artifacts and display them."""
        try:
            # Open file dialog to select JSON file
            file_path = filedialog.askopenfilename(
                title="Select Artifacts JSON File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:  # User cancelled
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check if this is GOOD format
            if isinstance(data, dict) and "format" in data and data["format"] == "GOOD":
                artifacts_data = data.get("artifacts", [])
            else:
                artifacts_data = data if isinstance(data, list) else []

            # Reset artifacts list
            self.artifacts = []

            # Process each artifact
            for item in artifacts_data:
                if isinstance(item, dict) and item.get('level') == 20:
                    try:
                        # Filter out empty substats
                        valid_substats = [
                            substat for substat in item['substats']
                            if substat.get('key') and substat.get('value')
                        ]

                        parsed_artifact = {
                            'id': item.get('id', ''),
                            'set': self.set_key_map.get(item['setKey'], item['setKey']),
                            'slot': self.slot_key_map.get(item['slotKey'], item['slotKey']),
                            'main_stat': self.stat_key_map.get(item['mainStatKey'], item['mainStatKey']),
                            'substats': []
                        }

                        # Parse substats
                        for substat in valid_substats:
                            if substat['key'] and substat['value']:  # Only add non-empty substats
                                parsed_artifact['substats'].append({
                                    'stat': self.stat_key_map.get(substat['key'], substat['key']),
                                    'value': substat['value']
                                })

                        self.artifacts.append(parsed_artifact)
                    except KeyError:
                        continue

            if self.artifacts:
                self.display_artifact_cards()
                self.notebook.select(1)  # Switch to artifacts tab
                messagebox.showinfo("Success", f"Parsed {len(self.artifacts)} level 20 artifacts")
            else:
                messagebox.showwarning("Warning", "No valid level 20 artifacts found in the file")
                
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse artifacts: {str(e)}")

    def create_artifacts_display(self, parent):
        """Create the artifacts display panel."""
        # Top frame for controls
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        # Add file selection button
        ttk.Button(
            control_frame,
            text="Load Artifacts JSON",
            command=self.parse_artifacts
        ).grid(row=0, column=0, padx=5)

        # Status label
        self.status_label = ttk.Label(control_frame, text="")
        self.status_label.grid(row=0, column=1, padx=5)

        # Create canvas and scrollbar for artifact cards
        canvas_frame = ttk.Frame(parent)
        canvas_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.canvas = tk.Canvas(canvas_frame, bg='#f0f0f0', width=750)  # Set fixed width
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.artifact_frame = ttk.Frame(self.canvas)
        
        # Configure canvas scroll region when frame size changes
        def configure_scroll_region(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.artifact_frame.bind("<Configure>", configure_scroll_region)

        # Bind mouse wheel to scroll
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.artifact_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Grid layout
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

    def display_artifact_cards(self):
        """Display artifact cards in the artifacts tab."""
        # Clear existing cards
        for widget in self.artifact_frame.winfo_children():
            widget.destroy()

        # Create cards for each artifact
        for i, artifact in enumerate(self.artifacts):
            # Create a frame for the card with a border
            card_frame = ttk.Frame(self.artifact_frame, style='Card.TFrame')
            card_frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky=(tk.N, tk.W, tk.E))

            # Make the entire card clickable
            def make_callback(a):
                return lambda e: self.show_artifact_rankings(a)

            # Bind click event to the entire card
            card_frame.bind("<Button-1>", make_callback(artifact))
            
            # Add hover effect
            def on_enter(e):
                e.widget.configure(style='CardHover.TFrame')
            
            def on_leave(e):
                e.widget.configure(style='Card.TFrame')
            
            card_frame.bind("<Enter>", on_enter)
            card_frame.bind("<Leave>", on_leave)

            # Set name and slot
            ttk.Label(
                card_frame,
                text=f"{artifact['set']}",
                font=('Segoe UI', 10, 'bold'),
                wraplength=200
            ).grid(row=0, column=0, padx=5, pady=(5,0), sticky=tk.W)

            ttk.Label(
                card_frame,
                text=f"{artifact['slot']}",
                font=('Segoe UI', 9),
            ).grid(row=1, column=0, padx=5, pady=(0,5), sticky=tk.W)

            # Add substats
            for j, substat in enumerate(artifact['substats']):
                substat_text = f"{substat['stat']}: {substat['value']}"
                label = ttk.Label(
                    card_frame,
                    text=substat_text,
                    font=('Segoe UI', 9)
                )
                label.grid(row=j+2, column=0, padx=5, pady=1, sticky=tk.W)
                # Make substat labels also clickable
                label.bind("<Button-1>", make_callback(artifact))

            # Configure grid weights for card frame
            card_frame.columnconfigure(0, weight=1)

        # Update status
        self.status_label.config(text=f"{len(self.artifacts)} artifacts loaded")

    def show_artifact_rankings(self, artifact):
        """Calculate and display rankings for a specific artifact."""
        # Switch to calculator tab
        self.notebook.select(0)

        # Set the UI fields based on the artifact
        self.artifact_set.set(artifact['set'])
        self.artifact_type.set(artifact['slot'])
        self.main_stat.set(artifact['main_stat'])

        # Set substats
        for i, (combo, entry) in enumerate(zip(self.substat_vars, self.substat_value_vars)):
            if i < len(artifact['substats']):
                combo.set(artifact['substats'][i]['stat'])
                entry.delete(0, tk.END)
                entry.insert(0, str(artifact['substats'][i]['value']))
            else:
                combo.set('')
                entry.delete(0, tk.END)

        # Calculate scores
        self.calculate_scores()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = ArtifactScoreCalculator()
    calculator.run()
