# Reverse Geocoding App

A Python application that converts geographic coordinates (latitude and longitude) into postal codes using the **Geoapify API**.

## 📋 Overview

This tool processes Excel files containing latitude and longitude coordinates and retrieves the corresponding postal codes (pincodes) for each location. It's particularly useful for batch geocoding operations across multiple locations.

**Key Features:**
- Batch processing of Excel files
- Automatic pincode lookup using Geoapify Reverse Geocoding API
- Rate limiting to avoid API throttling
- Error handling for network issues and invalid coordinates
- Progress tracking with detailed summaries
- Skips existing pincodes to avoid redundant API calls

## 📊 Input & Output

### Input Format
An Excel file (`database.xlsx`) with the following structure:

| LAT | LONG |
|-----|------|
| 28.6448 | 77.216721 |
| 12.972442 | 77.580643 |
| 19.07609 | 72.877426 |

### Output Format
The processed Excel file (`database_with_pincodes.xlsx`) includes a new `Pincode` column:

| LAT | LONG | Pincode |
|-----|------|---------|
| 28.6448 | 77.216721 | 110006 |
| 12.972442 | 77.580643 | 560009 |
| 19.07609 | 72.877426 | 400070 |

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArhamShah01/geocoder-pincode-finder.git
   cd geocoder-pincode-finder
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root directory:
   ```
   GEOAPIFY_API_KEY=your_geoapify_api_key_here
   ```

   To get your API key:
   - Visit [Geoapify](https://www.geoapify.com/)
   - Sign up for a free account
   - Navigate to your API Keys section
   - Copy your API key and add it to the `.env` file

## 💻 Usage

### Basic Usage

1. **Prepare your input file** (`database.xlsx`) with `LAT` and `LONG` columns

2. **Run the application:**
   ```bash
   python reverse_geocoding.py
   ```

3. **Check the output** (`database_with_pincodes.xlsx`) for results

### Output Example
```
============================================================
REVERSE GEOCODING APP - Geoapify
============================================================
Input file: database.xlsx
Output file: database_with_pincodes.xlsx

Reading file: database.xlsx
Total rows: 50
Starting reverse geocoding...

This may take a while, please wait...

Processed: 50/50 rows

Saving results to: database_with_pincodes.xlsx
✓ File saved successfully!

Summary:
 Total rows: 50
 Pincodes filled: 48
 Empty pincodes: 2

============================================================
Process completed!
============================================================
```

## 🔧 Configuration

You can customize the behavior by modifying the `main()` function:

```python
# File paths
INPUT_FILE = "database.xlsx"           # Change input file name
OUTPUT_FILE = "database_with_pincodes.xlsx"  # Change output file name

# Or use the process_file method with custom column names:
app.process_file(
    input_file="custom_input.xlsx",
    output_file="custom_output.xlsx",
    lat_col="LAT",                     # Latitude column name
    lon_col="LONG",                    # Longitude column name
    pincode_col="Pincode"              # Pincode column name
)
```

## ⚠️ Error Handling

The application handles various error scenarios:

| Error | Handling |
|-------|----------|
| Invalid coordinates (non-numeric) | Skips and returns None |
| Network timeout | Prints timeout message and continues |
| API errors (4xx/5xx) | Logs status code and continues |
| Missing columns | Raises ValueError with helpful message |
| File not found | Prints error and stops execution |
| Request exceptions | Logs error details and continues |


## 🔒 Security

Create a  `.env` file which should contain:
```
GEOAPIFY_API_KEY=your_api_key_here
```

## 📦 Dependencies

- `pandas` - Data manipulation and Excel file handling
- `requests` - HTTP requests to Geoapify API
- `python-dotenv` - Environment variable management

See `requirements.txt` for specific versions.

## Errors

### "Columns not found"
- Verify your Excel file has `LAT` and `LONG` columns

### Low success rate
- Check if coordinates are valid (moreover, Indian)
- The coordinates should not have any spaces or other characters

## Upcoming feature I want to add to this project
- Tehsil name from lat, long data
