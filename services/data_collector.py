"""
Data collection module for gathering market data and news
Uses DuckDuckGo search with fallback to mock data
"""

import logging
import asyncio
from typing import List, Dict

logger = logging.getLogger(__name__)


class DataCollector:
    """
    Collects market data, news, and trends for a given sector.
    Uses web search with fallback to realistic mock data.
    """
    
    def __init__(self):
        """Initialize data collector"""
        logger.info("[INIT] Initializing DataCollector...")
        try:
            self.mock_data = self._get_mock_data()
            logger.info("[INIT] ✓ DataCollector initialized successfully")
        except Exception as e:
            logger.error(f"[INIT] ✗ Failed to initialize DataCollector: {str(e)}", exc_info=True)
            raise
    
    async def collect_data(self, sector: str) -> List[Dict]:
        """
        Collect market data for a sector.
        
        Args:
            sector: The sector to collect data for
        
        Returns:
            List of data items with news, trends, and insights
        """
        try:
            logger.info(f"[COLLECT] Starting data collection for sector: {sector}")
            
            # Try to fetch real data from DuckDuckGo
            data = await self._fetch_from_search(sector)
            
            if data:
                logger.info(f"[COLLECT] ✓ Successfully collected {len(data)} items from live search")
                return data
            
        except Exception as e:
            logger.warning(f"[COLLECT] ✗ Error fetching real data: {str(e)}")
        
        # Fallback to mock data
        logger.info(f"[COLLECT] Using fallback mock data for sector: {sector}")
        mock_data = self._get_sector_mock_data(sector)
        logger.info(f"[COLLECT] ✓ Loaded {len(mock_data)} mock data items")
        return mock_data
    
    async def _fetch_from_search(self, sector: str) -> List[Dict]:
        """
        Fetch data from DuckDuckGo search (async wrapper for sync call).
        
        Args:
            sector: The sector to search for
        
        Returns:
            List of search results
        """
        try:
            from duckduckgo_search import DDGS
            
            logger.info(f"[SEARCH] Attempting to fetch live data from DuckDuckGo for: {sector}")
            
            ddgs = DDGS()
            
            # Search for recent news and market data
            search_queries = [
                f"{sector} market trends India 2024",
                f"{sector} industry news India",
                f"{sector} opportunities India"
            ]
            
            all_results = []
            
            for query in search_queries:
                try:
                    logger.debug(f"[SEARCH] Executing query: {query}")
                    
                    # Run sync DuckDuckGo call in thread pool to avoid blocking
                    loop = asyncio.get_event_loop()
                    results = await loop.run_in_executor(
                        None,
                        lambda q=query: ddgs.text(q, max_results=3)
                    )
                    
                    logger.debug(f"[SEARCH] Query returned {len(results)} results")
                    
                    for result in results:
                        all_results.append({
                            "title": result.get("title", ""),
                            "body": result.get("body", ""),
                            "href": result.get("href", ""),
                            "source": "web_search"
                        })
                except Exception as e:
                    logger.debug(f"[SEARCH] Error in query '{query}': {str(e)}")
                    continue
            
            if all_results:
                logger.info(f"[SEARCH] ✓ Successfully fetched {len(all_results)} live results from DuckDuckGo")
                return all_results[:10]
            else:
                logger.warning(f"[SEARCH] No results from DuckDuckGo, will use fallback")
                return []
            
        except ImportError:
            logger.warning(f"[SEARCH] ✗ duckduckgo_search library not available, using mock data")
            return []
        except Exception as e:
            logger.error(f"[SEARCH] ✗ Error fetching from DuckDuckGo: {str(e)}", exc_info=True)
            return []
    
    def _get_sector_mock_data(self, sector: str) -> List[Dict]:
        """
        Get mock data for a specific sector.
        
        Args:
            sector: The sector to get mock data for
        
        Returns:
            List of mock data items
        """
        sector_lower = sector.lower()
        
        if sector_lower in self.mock_data:
            return self.mock_data[sector_lower]
        
        # Return generic mock data if sector not found
        return self.mock_data["generic"]
    
    def _get_mock_data(self) -> Dict[str, List[Dict]]:
        """
        Get comprehensive mock data for various sectors.
        
        Returns:
            Dictionary of sector-specific mock data
        """
        return {
            "pharmaceuticals": [
                {
                    "title": "India Pharma Market Growth",
                    "body": "Indian pharmaceutical market expected to grow at 8-10% CAGR through 2025. Generic drugs dominate 80% of market. Biosimilars and specialty drugs showing strong growth.",
                    "source": "market_data"
                },
                {
                    "title": "API Manufacturing Opportunities",
                    "body": "Active Pharmaceutical Ingredients (APIs) production in India growing. Export opportunities to US, EU markets. Government incentives for domestic manufacturing.",
                    "source": "market_data"
                },
                {
                    "title": "Healthcare Spending Increase",
                    "body": "India's healthcare spending projected to reach $372B by 2024. Rising middle class driving demand for quality medicines and treatments.",
                    "source": "market_data"
                }
            ],
            "technology": [
                {
                    "title": "India Tech Startup Boom",
                    "body": "India has 100+ unicorns as of 2024. Tech sector contributing 12% to GDP. AI and cloud computing driving innovation.",
                    "source": "market_data"
                },
                {
                    "title": "IT Services Export Growth",
                    "body": "Indian IT services exports reached $245B in FY2024. Digital transformation driving demand for cloud, AI, and cybersecurity services.",
                    "source": "market_data"
                },
                {
                    "title": "Semiconductor Manufacturing",
                    "body": "India establishing semiconductor manufacturing hubs. Government incentives through PLI scheme. Potential to become global chip manufacturing hub.",
                    "source": "market_data"
                }
            ],
            "agriculture": [
                {
                    "title": "AgriTech Revolution",
                    "body": "AgriTech startups in India growing rapidly. Precision farming, IoT sensors, and AI-driven crop management gaining adoption.",
                    "source": "market_data"
                },
                {
                    "title": "Export Opportunities",
                    "body": "India's agricultural exports reached $50B in 2024. Organic farming and specialty crops showing strong demand in global markets.",
                    "source": "market_data"
                },
                {
                    "title": "Food Processing Growth",
                    "body": "Food processing sector growing at 12% annually. Government support through PMKSY-AF scheme. Export potential for processed foods.",
                    "source": "market_data"
                }
            ],
            "renewable_energy": [
                {
                    "title": "Solar Energy Expansion",
                    "body": "India targeting 500 GW renewable energy by 2030. Solar capacity additions leading at 15+ GW annually.",
                    "source": "market_data"
                },
                {
                    "title": "Green Hydrogen Opportunity",
                    "body": "India launching green hydrogen mission. Potential to become global green hydrogen hub. Investment opportunities in production and infrastructure.",
                    "source": "market_data"
                },
                {
                    "title": "Battery Manufacturing",
                    "body": "Battery manufacturing capacity expanding. EV adoption driving demand. Government incentives for battery production.",
                    "source": "market_data"
                }
            ],
            "generic": [
                {
                    "title": "Market Growth Trends",
                    "body": "Indian economy growing at 7%+ annually. Rising consumer spending and digital adoption creating new opportunities.",
                    "source": "market_data"
                },
                {
                    "title": "Government Initiatives",
                    "body": "Make in India, Atmanirbhar Bharat, and PLI schemes supporting sector growth. Tax incentives and infrastructure development.",
                    "source": "market_data"
                },
                {
                    "title": "Export Opportunities",
                    "body": "India's exports growing across sectors. Global demand for Indian products and services increasing.",
                    "source": "market_data"
                }
            ]
        }
