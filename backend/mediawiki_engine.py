import os
import json
import httpx
import re
from typing import Dict, Any, Optional
from salience_distiller import SalienceDistiller

class DynamicMediaWikiEngine:
    """
    100% Real-time Knowledge Harvester via official MediaWiki API.
    Zero pre-canned templates.
    Workflow:
      1. Action=query&list=search -> Finds best matching article title
      2. Action=query&prop=extracts&explaintext=1 -> Pulls real un-hallucinated article text
      3. Distills into coherent 3-4 sentence response via SalienceDistiller
    """
    def __init__(self):
        self.endpoint = "https://en.wikipedia.org/w/api.php"
        self.headers = {"User-Agent": "AthenaAlexaPlus/2.0 (AmazonDeveloperHackathon2026; contact@athena.dev)"}

    async def search_and_extract(self, user_query: str) -> Dict[str, Any]:
        # 1. Clean query of conversational filler ("who is the", "tell me about", "what is")
        cleaned_search = re.sub(r"^(who is (the|a)?|who was (the|a)?|what is (the|a)?|what are|tell me about|explain|describe)\s+", "", user_query, flags=re.I).strip(" ?.!\"'")
        if not cleaned_search:
            cleaned_search = user_query.strip(" ?.!\"'")

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                # Step 1: Search Wikipedia for the best matching page
                search_params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": cleaned_search,
                    "srlimit": 3,
                    "format": "json"
                }
                resp1 = await client.get(self.endpoint, params=search_params, headers=self.headers)
                if resp1.status_code != 200:
                    return {"found": False}

                data1 = resp1.json()
                results = data1.get("query", {}).get("search", [])
                if not results:
                    return {"found": False}

                # Resolve most relevant title
                resolved_title = results[0]["title"]

                # Step 2: Fetch the plain text extract for that resolved title
                extract_params = {
                    "action": "query",
                    "prop": "extracts",
                    "exintro": 1,
                    "explaintext": 1,
                    "titles": resolved_title,
                    "format": "json"
                }
                resp2 = await client.get(self.endpoint, params=extract_params, headers=self.headers)
                if resp2.status_code != 200:
                    return {"found": False}

                data2 = resp2.json()
                pages = data2.get("query", {}).get("pages", {})
                for pid, pdata in pages.items():
                    if pid != "-1":
                        raw_extract = pdata.get("extract", "")
                        if raw_extract:
                            # Step 3: Run Salience Distillation for 3-4 information-dense lines
                            synthesis = SalienceDistiller.condense_to_detailed_paragraph(
                                raw_extract, 
                                entity_name=resolved_title, 
                                min_sentences=3, 
                                max_sentences=4
                            )
                            return {
                                "found": True,
                                "resolved_title": resolved_title,
                                "synthesis": synthesis,
                                "source": f"Live MediaWiki Knowledge Core: {resolved_title}"
                            }

        except Exception as e:
            print(f"[MediaWikiEngine] Error querying: {e}")

        return {"found": False}
