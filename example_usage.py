"""
Example usage of Trade Opportunities API
Demonstrates how to use the API programmatically
"""

import requests
import json
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8001"
API_KEY = "trade-api-key-2024"


class TradeOpportunitiesClient:
    """Client for Trade Opportunities API"""
    
    def __init__(self, base_url: str = BASE_URL, api_key: str = API_KEY):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API
            api_key: API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key
    
    def analyze_sector(self, sector: str, client_id: Optional[str] = None) -> str:
        """
        Analyze a sector and get market opportunities.
        
        Args:
            sector: Sector name (e.g., pharmaceuticals, technology)
            client_id: Optional client identifier for session tracking
        
        Returns:
            Markdown formatted market analysis report
        
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        headers = {
            "X-API-Key": self.api_key,
            "Client-ID": client_id or "default-client"
        }
        
        url = f"{self.base_url}/analyze/{sector}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.text
    
    def health_check(self) -> dict:
        """
        Check API health status.
        
        Returns:
            Health status dictionary
        """
        url = f"{self.base_url}/health"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_session_stats(self) -> dict:
        """
        Get session statistics.
        
        Returns:
            Session statistics dictionary
        """
        headers = {"X-API-Key": self.api_key}
        url = f"{self.base_url}/session-stats"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


def example_1_basic_analysis():
    """Example 1: Basic sector analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Sector Analysis")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    
    try:
        # Analyze pharmaceuticals sector
        report = client.analyze_sector("pharmaceuticals", client_id="example-user-1")
        
        # Print first 1000 characters
        print("Report Preview:")
        print(report[:1000])
        print("\n... [Report continues] ...\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def example_2_multiple_sectors():
    """Example 2: Analyze multiple sectors"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Analyze Multiple Sectors")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    sectors = ["pharmaceuticals", "technology", "agriculture"]
    
    for sector in sectors:
        try:
            print(f"Analyzing {sector}...")
            report = client.analyze_sector(sector, client_id="example-user-2")
            
            # Extract title from report
            lines = report.split('\n')
            title = lines[0] if lines else "Unknown"
            print(f"✓ {title}\n")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error analyzing {sector}: {e}\n")


def example_3_save_report():
    """Example 3: Save report to file"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Save Report to File")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    
    try:
        # Analyze sector
        report = client.analyze_sector("technology", client_id="example-user-3")
        
        # Save to file
        filename = "technology_analysis.md"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✓ Report saved to {filename}")
        print(f"  File size: {len(report)} bytes")
        
    except Exception as e:
        print(f"Error: {e}")


def example_4_health_check():
    """Example 4: Health check"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Health Check")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    
    try:
        status = client.health_check()
        print(f"API Status: {json.dumps(status, indent=2)}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def example_5_session_stats():
    """Example 5: Get session statistics"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Session Statistics")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    
    try:
        stats = client.get_session_stats()
        print(f"Session Statistics:")
        print(json.dumps(stats, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def example_6_error_handling():
    """Example 6: Error handling"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Error Handling")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    
    # Test 1: Invalid API key
    print("Test 1: Invalid API key")
    try:
        invalid_client = TradeOpportunitiesClient(api_key="invalid-key")
        invalid_client.analyze_sector("pharmaceuticals")
    except requests.exceptions.HTTPError as e:
        print(f"✓ Caught error: {e.response.status_code} - {e.response.json()['detail']}\n")
    
    # Test 2: Invalid sector
    print("Test 2: Invalid sector (with numbers)")
    try:
        client.analyze_sector("pharma123")
    except requests.exceptions.HTTPError as e:
        print(f"✓ Caught error: {e.response.status_code} - {e.response.json()['detail']}\n")
    
    # Test 3: Rate limiting
    print("Test 3: Rate limiting (5 requests per minute)")
    try:
        for i in range(6):
            print(f"  Request {i+1}...", end=" ")
            client.analyze_sector("agriculture", client_id="rate-limit-test")
            print("✓")
    except requests.exceptions.HTTPError as e:
        print(f"✗ Rate limited: {e.response.status_code}")
        print(f"  {e.response.json()['detail']}\n")


def example_7_batch_analysis():
    """Example 7: Batch analysis with error handling"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Batch Analysis")
    print("="*60 + "\n")
    
    client = TradeOpportunitiesClient()
    sectors = [
        "pharmaceuticals",
        "technology",
        "agriculture",
        "renewable_energy",
        "finance"
    ]
    
    results = {}
    
    for sector in sectors:
        try:
            print(f"Analyzing {sector}...", end=" ")
            report = client.analyze_sector(sector, client_id="batch-analysis")
            
            # Extract key information
            lines = report.split('\n')
            title = lines[0] if lines else "Unknown"
            
            results[sector] = {
                "status": "success",
                "title": title,
                "length": len(report)
            }
            print("✓")
            
        except requests.exceptions.HTTPError as e:
            results[sector] = {
                "status": "error",
                "error": str(e)
            }
            print("✗")
    
    print("\nBatch Analysis Results:")
    print(json.dumps(results, indent=2))


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("TRADE OPPORTUNITIES API - USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        ("Basic Analysis", example_1_basic_analysis),
        ("Multiple Sectors", example_2_multiple_sectors),
        ("Save Report", example_3_save_report),
        ("Health Check", example_4_health_check),
        ("Session Stats", example_5_session_stats),
        ("Error Handling", example_6_error_handling),
        ("Batch Analysis", example_7_batch_analysis),
    ]
    
    for name, func in examples:
        try:
            func()
        except requests.exceptions.ConnectionError:
            print(f"\n✗ Cannot connect to API server")
            print("Make sure the API is running: python main.py")
            break
        except Exception as e:
            print(f"\n✗ Error in {name}: {str(e)}")
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
