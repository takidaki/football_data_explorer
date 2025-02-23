# Football Match Data Explorer

⚽ A Streamlit application for exploring football match data, providing insights into match statistics, league performance, and head-to-head comparisons.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Load and visualize football match data from a CSV file.
- Filter matches by league, season, home team, and away team.
- Display head-to-head statistics between selected teams.
- Show league statistics and compare them with overall data.
- Interactive user interface built with Streamlit.

## Installation

To run this application, you need to have Python installed on your machine. Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/takidaki/football-data-explorer.git
   cd football-data-explorer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the `Streamlit Full Database.csv` file in the same directory as the script.
2. Run the application:
   ```bash
   streamlit run football_data.py
   ```
3. Open your web browser and go to `http://localhost:8501` to view the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
