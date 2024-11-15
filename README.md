# Genshin Impact Artifact Optimizer

A comprehensive tool for optimizing and evaluating artifacts in Genshin Impact. This application helps players calculate artifact effectiveness across different characters and provides character-specific recommendations.

## Features

### Artifact Calculator
- Calculate artifact scores based on character-specific stat weights
- View character rankings for any given artifact
- Support for all artifact sets and stat combinations
- Percentage-based scoring system for easy comparison

### Set Configurator
- Configure recommended characters for each artifact set
- Set priority levels for character-artifact combinations
- Dynamic character list with priorities
- Easy-to-use interface for managing artifact set recommendations

### New! Artifact Import and Analysis
- Import artifacts directly from GOOD (Genshin Open Object Description) format JSON
- Support for GO (Genshin Optimizer) exported artifacts
- Visual card display of level 20 artifacts showing:
  - Artifact set name
  - Slot type
  - All substats with values
- Click any artifact card to instantly see character recommendations

## How to Use

1. **Artifact Calculator**
   - Select artifact set, type, main stat, and substats
   - View instant character rankings
   - See percentage-based scores for each character

2. **Set Configurator**
   - Add/remove characters for each artifact set
   - Set priority levels (1-5)
   - View all characters configured for each set

3. **Artifact Import**
   - Click "Load Artifacts JSON" in the My Artifacts tab
   - Select your GOOD format JSON file
   - View all your level 20 artifacts as cards
   - Click any card to see character rankings

## Supported Features
- All artifact sets from version 4.3
- Character-specific stat weightings
- Theoretical max substat calculations
- Percentage-based scoring system
- GOOD format JSON import
- Modern, compact UI design

## Requirements
- Python 3.x
- Tkinter (included with Python)
- JSON support (included with Python)

## Future Plans
- Advanced filtering options
- Export functionality
- More detailed tooltips
- Periodic weight rebalancing
- Additional character metadata

## Contributing
Feel free to contribute by:
- Adding new character weights
- Updating artifact set recommendations
- Improving the scoring algorithm
- Enhancing the UI/UX

## License
Open source - feel free to use and modify
