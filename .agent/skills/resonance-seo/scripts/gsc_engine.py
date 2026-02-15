import os
import json
import sys
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

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
                "message": "Providing GSC credentials allows Resonance to analyze real-world ranking data.",
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

    def inspect_url(self, site_url: str, page_url: str) -> Dict[str, Any]:
        """
        Perform a Deep Inspection of a URL to diagnose indexing and schema issues.
        """
        if not self.service:
            return {
                "status": "DEEPER_INSIGHT_AVAILABLE",
                "message": "Providing GSC credentials allows Deep Inspection (Indexing, Canonical, Rich Results).",
                "result": {}
            }

        request = {
            "inspectionUrl": page_url,
            "siteUrl": site_url
        }

        try:
            response = self.service.urlInspection().index().inspect(body=request).execute()
            inspection = response.get("inspectionResult", {})
            
            if not inspection:
                return {"error": "No inspection data found"}

            index_status = inspection.get("indexStatusResult", {})
            
            # Extract Deep Insights
            analysis = {
                "verdict": index_status.get("verdict", "UNKNOWN"),
                "coverage": index_status.get("coverageState", "Unknown"),
                "indexing_state": index_status.get("indexingState", "Unknown"),
                "last_crawl": index_status.get("lastCrawlTime", "Never"),
                "google_canonical": index_status.get("googleCanonical", "None"),
                "user_canonical": index_status.get("userCanonical", "None"),
                "referring_urls": index_status.get("referringUrls", []),
                "robots_txt": index_status.get("robotsTxtState", "Unknown"),
                "rich_results": []
            }

            # Rich Result Analysis
            if "richResultsResult" in inspection:
                rich = inspection["richResultsResult"]
                analysis["rich_results_verdict"] = rich.get("verdict", "UNKNOWN")
                
                if "detectedItems" in rich:
                    for item in rich["detectedItems"]:
                        analysis["rich_results"].append({
                            "type": item.get("richResultType", "Unknown"),
                            "items": [sub.get("name") for sub in item.get("items", []) if "name" in sub]
                        })

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def batch_inspect(self, site_url: str, urls: str):
        """
        Inspect multiple URLs (e.g. top 5 striking distance pages).
        """
        url_list = [u.strip() for u in urls.split('\n') if u.strip()]
        if len(url_list) > 10:
             return {"error": "Batch limit exceeded. Max 10 URLs."}

        results = {}
        for url in url_list:
            results[url] = self.inspect_url(site_url, url)
        
        return results

def main():
    parser = argparse.ArgumentParser(description="Resonance GSC Intelligence Engine")
    parser.add_argument("--action", choices=["striking-distance", "inspect", "batch-inspect"], required=True)
    parser.add_argument("--site", required=True, help="Site URL in GSC")
    parser.add_argument("--url", help="Page URL for inspection (single or comma-separated for batch)")
    parser.add_argument("--file", help="File containing URLs for batch inspection")
    
    args = parser.parse_args()
    engine = GSCEngine()

    if args.action == "striking-distance":
        result = engine.get_striking_distance(args.site)
        print(json.dumps(result, indent=2))
        
    elif args.action == "inspect":
        if not args.url:
            print("Error: --url is required for inspection")
            sys.exit(1)
        result = engine.inspect_url(args.site, args.url)
        print(json.dumps(result, indent=2))
        
    elif args.action == "batch-inspect":
        urls = ""
        if args.url:
            urls = args.url.replace(",", "\n")
        elif args.file and os.path.exists(args.file):
            with open(args.file, 'r') as f:
                urls = f.read()
        else:
            print("Error: --url or --file required for batch inspection")
            sys.exit(1)
            
        result = engine.batch_inspect(args.site, urls)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
