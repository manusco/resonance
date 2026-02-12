import os
import json
import sys
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Missing dependencies. Run 'pip install google-api-python-client google-auth-httplib2'")
    sys.exit(1)

# Try to load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Resonance SEO GSC Engine
# Part of the Resonance Framework

class GSCEngine:
    def __init__(self, credentials_path: str = None):
        self.scopes = ["https://www.googleapis.com/auth/webmasters"]
        self.service = self._authenticate(credentials_path)

    def _authenticate(self, credentials_path):
        if not credentials_path:
            # First priority: Environment variable (e.g. from .env)
            credentials_path = os.environ.get("GSC_CREDENTIALS_PATH")
            
            # Second priority: Default filename in root
            if not credentials_path:
                credentials_path = "gsc_credentials.json"

        if not os.path.exists(credentials_path):
            return None

        try:
            creds = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=self.scopes
            )
            return build("searchconsole", "v1", credentials=creds)
        except Exception:
            return None

    def get_striking_distance(self, site_url: str, days: int = 28, min_pos: float = 8.0, max_pos: float = 20.0):
        if not self.service:
            return {
                "status": "DEEPER_INSIGHT_AVAILABLE",
                "message": "Providing GSC credentials in a .env file (GSC_CREDENTIALS_PATH) allows Resonance to analyze real-world ranking data and find 'Striking Distance' opportunities.",
                "data": []
            }

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        request = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "dimensions": ["query", "page"],
            "rowLimit": 500
        }

        try:
            response = self.service.searchanalytics().query(siteUrl=site_url, body=request).execute()
            rows = response.get("rows", [])
            
            striking_distance = []
            for row in rows:
                query = row["keys"][0]
                page = row["keys"][1]
                pos = row["position"]
                
                if min_pos <= pos <= max_pos:
                    striking_distance.append({
                        "query": query,
                        "page": page,
                        "position": round(pos, 2),
                        "clicks": row["clicks"],
                        "impressions": row["impressions"],
                        "ctr": round(row["ctr"] * 100, 2)
                    })
            
            # Sort by impressions (highest potential first)
            striking_distance.sort(key=lambda x: x["impressions"], reverse=True)
            return striking_distance
        except Exception as e:
            return {"error": str(e)}

    def inspect_url(self, site_url: str, page_url: str):
        if not self.service:
            return {
                "status": "DEEPER_INSIGHT_AVAILABLE",
                "message": "Providing GSC credentials allows Resonance to inspect indexing status and search console errors directly.",
                "result": {}
            }

        request = {
            "inspectionUrl": page_url,
            "siteUrl": site_url
        }

        try:
            response = self.service.urlInspection().index().inspect(body=request).execute()
            return response.get("inspectionResult", {})
        except Exception as e:
            return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Resonance GSC Intelligence Engine")
    parser.add_argument("--action", choices=["striking-distance", "inspect"], required=True)
    parser.add_argument("--site", required=True, help="Site URL in GSC")
    parser.add_argument("--url", help="Page URL for inspection")
    parser.add_argument("--creds", help="Path to GSC service account credentials")
    
    args = parser.parse_args()
    engine = GSCEngine(args.creds)

    if args.action == "striking-distance":
        result = engine.get_striking_distance(args.site)
        print(json.dumps(result, indent=2))
    elif args.action == "inspect":
        if not args.url:
            print("Error: --url is required for inspection")
            sys.exit(1)
        result = engine.inspect_url(args.site, args.url)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
