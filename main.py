import os
import pandas as pd
import requests
import time
from typing import Optional

class ReverseGeocodingApp:
    
    def __init__(self, api_key: str):

        self.api_key = api_key
        self.base_url = "https://api.geoapify.com/v1/geocode/reverse"
        self.session = requests.Session()
        self.rate_limit_delay = 0.1  # 100ms delay between requests to avoid rate limiting
        
    def get_pincode(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Get pincode for given latitude and longitude
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            Optional[str]: Pincode if found, None otherwise
        """
        try:
            # Skip invalid coordinates
            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                return None
            
            params = {
                'lat': latitude,
                'lon': longitude,
                'apiKey': self.api_key
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract pincode from features
                if 'features' in data and len(data['features']) > 0:
                    properties = data['features'][0].get('properties', {})
                    pincode = properties.get('postcode')
                    
                    if pincode:
                        return str(pincode)
                    
                return None
            else:
                print(f"API Error for ({latitude}, {longitude}): Status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"Timeout for coordinates ({latitude}, {longitude})")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error for ({latitude}, {longitude}): {str(e)}")
            return None
        except Exception as e:
            print(f"Error processing ({latitude}, {longitude}): {str(e)}")
            return None
    
    def process_file(self, input_file: str, output_file: str, lat_col: str = 'LAT', 
                     lon_col: str = 'LONG', pincode_col: str = 'Pincode') -> None:
        """
        Process entire Excel file and fill pincode column
        
        Args:
            input_file (str): Path to input Excel file
            output_file (str): Path to output Excel file
            lat_col (str): Column name for latitude (default: 'LAT')
            lon_col (str): Column name for longitude (default: 'LONG')
            pincode_col (str): Column name for pincode (default: 'Pincode')
        """
        try:
            # Read Excel file
            print(f"Reading file: {input_file}")
            df = pd.read_excel(input_file)
            
            # Validate columns exist
            if lat_col not in df.columns or lon_col not in df.columns:
                raise ValueError(f"Columns '{lat_col}' or '{lon_col}' not found in file")
            
            # Initialize pincode column as string dtype if not exists
            if pincode_col not in df.columns:
                df[pincode_col] = pd.Series(dtype='object')
            else:
                # Convert to object dtype to avoid dtype conflicts
                df[pincode_col] = df[pincode_col].astype('object')
            
            total_rows = len(df)
            print(f"Total rows: {total_rows}")
            print(f"Starting reverse geocoding...\n")
            print("This may take a while, please wait...\n")
            
            # Collect results to avoid dtype issues
            pincodes = []
            
            # Process each row
            for idx, row in df.iterrows():
                lat = row[lat_col]
                lon = row[lon_col]
                
                # Check if already has valid pincode
                current_pincode = df.loc[idx, pincode_col]
                if pd.notna(current_pincode) and str(current_pincode).strip() != '':
                    pincodes.append(current_pincode)
                    continue
                
                # Skip rural/invalid entries
                if isinstance(lat, str) or isinstance(lon, str):
                    pincodes.append(None)
                    continue
                
                # Get pincode
                pincode = self.get_pincode(lat, lon)
                pincodes.append(pincode)
                
                # Progress update every 50 rows
                if (idx + 1) % 50 == 0:
                    print(f"Processed: {idx + 1}/{total_rows} rows")
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
            
            # Assign all pincodes at once to avoid dtype issues
            df[pincode_col] = pincodes
            
            # Save to output file
            print(f"\nSaving results to: {output_file}")
            df.to_excel(output_file, index=False)
            print("✓ File saved successfully!")
            
            # Print summary
            filled_count = sum(1 for p in pincodes if p is not None and str(p).strip() != '')
            empty_count = total_rows - filled_count
            print(f"\nSummary:")
            print(f"  Total rows: {total_rows}")
            print(f"  Pincodes filled: {filled_count}")
            print(f"  Empty pincodes: {empty_count}")
            
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found")
        except Exception as e:
            print(f"Error processing file: {str(e)}")

def main():
    """Main function to run the reverse geocoding app"""
    
    # API Key
    API_KEY = os.getenv("GEOAPIFY_API_KEY")
    
    # File paths
    INPUT_FILE = "database.xlsx"
    OUTPUT_FILE = "database_with_pincodes.xlsx"
    
    # Initialize app
    print("=" * 60)
    print("REVERSE GEOCODING APP - Geoapify")
    print("=" * 60)
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {OUTPUT_FILE}\n")
    
    app = ReverseGeocodingApp(API_KEY)
    
    # Process file
    app.process_file(INPUT_FILE, OUTPUT_FILE)
    
    print("\n" + "=" * 60)
    print("Process completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
