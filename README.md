# Water Supply Projects Map

An interactive map application for visualizing water supply projects in Greece, built with Streamlit and Folium.

## Features

- Interactive map visualization of water supply projects
- Filter projects by region and status
- Detailed project information and statistics
- Data can be loaded from a file or use sample data

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/water-supply-maps.git
   cd water-supply-maps
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run map_projects.py
```

Then open your web browser to `http://localhost:8501`

## Data Format

The application can load Excel files with the following structure:
- Project Name
- Region
- Status
- Latitude
- Longitude
- Other project details

## License

This project is licensed under the MIT License.
