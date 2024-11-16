# Genshin Impact Artifact Recommendation

A comprehensive tool for analyzing and recommending artifacts in Genshin Impact. This application helps players evaluate artifact effectiveness across different characters and provides character-specific recommendations.

## Credits

- **Code Development**: This application was developed with the assistance of AI (Codeium)
- **Artifact Weights**: The character-specific weights and recommendations are based on community guides and theorycrafting resources, not AI-generated

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

### Artifact Import and Analysis
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

## Artifact Ranking System

The application uses a comprehensive ranking system to evaluate artifacts:

### SS Rank 
- Perfect combination of on-set main stat and best-in-slot substats
- Nearly all substat rolls into highly desired stats for the character
- Represents the ideal artifact piece

### S Rank 
- Correct artifact set
- Appropriate main and substats
- Significantly improves character performance
- Minor improvements possible but excellent overall

### A Rank 
- Either correct set or appropriate substats
- May need some substat improvements
- Serviceable piece for most content
- Good temporary option until SS/S rank found

### B Rank 
- Usable but suboptimal
- Either wrong set or suboptimal substats
- Should be replaced when better artifacts are obtained
- Adequate for early/mid-game content

### C Rank 
- Neither correct set nor appropriate stats
- May be useful for other characters
- Recommended to find replacement
- Consider as temporary placeholder

## Supported Features
- All artifact sets from version 4.3
- Character-specific stat weightings based on community guides
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
- Adding new character weights (with guide references)
- Updating artifact set recommendations
- Improving the scoring algorithm
- Enhancing the UI/UX

## License
Open source - feel free to use and modify
