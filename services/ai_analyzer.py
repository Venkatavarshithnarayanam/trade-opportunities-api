"""
AI analysis module for generating insights using Google Gemini API
Includes fallback to rule-based analysis
"""

import os
import logging
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

logger = logging.getLogger(__name__)

# Thread pool for running sync Gemini API calls without blocking event loop
executor = ThreadPoolExecutor(max_workers=5)


class AIAnalyzer:
    """
    Analyzes market data using Google Gemini API with fallback to rule-based analysis.
    Generates structured insights including overview, trends, opportunities, risks, and outlook.
    """
    
    def __init__(self):
        """Initialize AI analyzer"""
        logger.info("[INIT] Initializing AIAnalyzer...")
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                logger.info("[INIT] GEMINI_API_KEY found, attempting to import google.generativeai...")
                import google.generativeai as genai
                logger.info("[INIT] google.generativeai imported successfully")
                
                logger.info("[INIT] Configuring Gemini API...")
                genai.configure(api_key=self.api_key)
                
                logger.info("[INIT] Creating GenerativeModel instance...")
                self.client = genai.GenerativeModel("gemini-pro")
                logger.info("[INIT] ✓ Gemini API initialized successfully")
            except ImportError as e:
                logger.warning(f"[INIT] ✗ google.generativeai not installed: {str(e)}")
                logger.warning("[INIT] Will use fallback rule-based analysis")
                self.client = None
            except Exception as e:
                logger.warning(f"[INIT] ✗ Failed to initialize Gemini API: {str(e)}")
                logger.warning("[INIT] Will use fallback rule-based analysis")
                self.client = None
        else:
            logger.info("[INIT] GEMINI_API_KEY not set, will use fallback rule-based analysis")
    
    async def analyze(self, sector: str, market_data: List[Dict]) -> Dict:
        """
        Analyze market data and generate insights.
        
        Args:
            sector: The sector being analyzed
            market_data: List of market data items
        
        Returns:
            Dictionary with analysis results
        """
        try:
            if self.client:
                logger.info(f"[ANALYZE] Using Gemini API for analysis of {sector}")
                return await self._analyze_with_gemini(sector, market_data)
        except Exception as e:
            logger.warning(f"[ANALYZE] ✗ Gemini API analysis failed: {str(e)}")
            logger.warning(f"[ANALYZE] Falling back to rule-based analysis")
        
        # Fallback to rule-based analysis
        logger.info(f"[ANALYZE] Using fallback rule-based analysis for {sector}")
        return self._analyze_with_rules(sector, market_data)
    
    async def _analyze_with_gemini(self, sector: str, market_data: List[Dict]) -> Dict:
        """
        Analyze using Google Gemini API (async wrapper for sync call).
        
        Args:
            sector: The sector being analyzed
            market_data: List of market data items
        
        Returns:
            Analysis results
        """
        try:
            # Prepare context from market data
            context = "\n".join([
                f"- {item.get('title', '')}: {item.get('body', '')}"
                for item in market_data[:5]
            ])
            
            prompt = f"""Analyze the following market data for the {sector} sector in India and provide a structured analysis.

Market Data:
{context}

Please provide analysis in the following JSON format:
{{
    "overview": "2-3 sentence overview of the sector",
    "key_trends": ["trend 1", "trend 2", "trend 3"],
    "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
    "risks": ["risk 1", "risk 2", "risk 3"],
    "future_outlook": "2-3 sentence outlook for next 2-3 years"
}}

Respond with only valid JSON."""
            
            logger.info(f"[GEMINI] Sending request to Gemini API for sector: {sector}")
            logger.debug(f"[GEMINI] Prompt length: {len(prompt)} characters")
            
            # Run sync Gemini call in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                executor,
                self.client.generate_content,
                prompt
            )
            
            logger.info(f"[GEMINI] Received response from Gemini API")
            
            # Parse response
            response_text = response.text.strip()
            logger.debug(f"[GEMINI] Response length: {len(response_text)} characters")
            
            # Try to extract JSON from response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text
            
            analysis = json.loads(json_str)
            logger.info(f"[GEMINI] ✓ Successfully analyzed {sector} with Gemini API")
            logger.debug(f"[GEMINI] Analysis keys: {list(analysis.keys())}")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"[GEMINI] ✗ Failed to parse Gemini response as JSON: {str(e)}")
            logger.error(f"[GEMINI] Response was: {response_text[:200]}...")
            raise
        except Exception as e:
            logger.error(f"[GEMINI] ✗ Gemini API error: {str(e)}", exc_info=True)
            raise
    
    def _analyze_with_rules(self, sector: str, market_data: List[Dict]) -> Dict:
        """
        Fallback rule-based analysis.
        
        Args:
            sector: The sector being analyzed
            market_data: List of market data items
        
        Returns:
            Analysis results
        """
        sector_lower = sector.lower()
        
        # Rule-based analysis templates
        analysis_templates = {
            "pharmaceuticals": {
                "overview": "The Indian pharmaceutical sector is a global leader in generic drug manufacturing and API production. With strong government support and growing healthcare spending, the sector presents significant opportunities for expansion and innovation.",
                "key_trends": [
                    "Shift towards specialty drugs and biosimilars",
                    "Increasing focus on API manufacturing and exports",
                    "Digital health and telemedicine integration",
                    "Rising healthcare spending in India"
                ],
                "opportunities": [
                    "Export of generic drugs to regulated markets (US, EU)",
                    "Biosimilar development and manufacturing",
                    "Contract manufacturing for global pharma companies",
                    "Healthcare infrastructure development"
                ],
                "risks": [
                    "Regulatory compliance and pricing pressures",
                    "Competition from other generic manufacturers",
                    "Supply chain disruptions",
                    "Patent litigation risks"
                ],
                "future_outlook": "The Indian pharmaceutical sector is expected to grow at 8-10% CAGR through 2025. Opportunities in specialty drugs, biosimilars, and contract manufacturing will drive growth. Government initiatives and rising healthcare spending will support expansion."
            },
            "technology": {
                "overview": "India's technology sector is booming with 100+ unicorns and a thriving startup ecosystem. The sector is driving digital transformation across industries and contributing significantly to GDP growth.",
                "key_trends": [
                    "AI and machine learning adoption across sectors",
                    "Cloud computing and SaaS growth",
                    "Cybersecurity and data protection focus",
                    "Semiconductor manufacturing initiatives"
                ],
                "opportunities": [
                    "AI-powered solutions for various industries",
                    "Cloud infrastructure and services",
                    "Cybersecurity and compliance services",
                    "Semiconductor design and manufacturing"
                ],
                "risks": [
                    "Intense competition from global tech companies",
                    "Talent retention and brain drain",
                    "Regulatory changes and data localization",
                    "Geopolitical tensions affecting tech trade"
                ],
                "future_outlook": "India's tech sector will continue to grow as a global innovation hub. AI, cloud computing, and semiconductor manufacturing will be key growth drivers. The sector is expected to contribute 20% to GDP by 2030."
            },
            "agriculture": {
                "overview": "India's agriculture sector is undergoing digital transformation with AgriTech innovations. The sector offers significant opportunities in precision farming, food processing, and agricultural exports.",
                "key_trends": [
                    "AgriTech adoption and precision farming",
                    "Organic farming and sustainable practices",
                    "Food processing and value addition",
                    "Agricultural exports growth"
                ],
                "opportunities": [
                    "AgriTech startups and solutions",
                    "Organic and specialty crop production",
                    "Food processing and export",
                    "Agricultural supply chain optimization"
                ],
                "risks": [
                    "Weather and climate variability",
                    "Market price volatility",
                    "Limited access to credit and technology",
                    "Export market competition"
                ],
                "future_outlook": "India's agriculture sector will benefit from AgriTech adoption and government support. Organic farming and food processing will drive growth. Agricultural exports are expected to reach $100B by 2030."
            },
            "renewable_energy": {
                "overview": "India is a global leader in renewable energy with ambitious targets for solar and wind power. The sector offers significant investment opportunities in clean energy infrastructure.",
                "key_trends": [
                    "Solar energy capacity expansion",
                    "Green hydrogen development",
                    "Battery manufacturing growth",
                    "Energy storage solutions"
                ],
                "opportunities": [
                    "Solar and wind power projects",
                    "Green hydrogen production",
                    "Battery manufacturing and recycling",
                    "Energy storage infrastructure"
                ],
                "risks": [
                    "Intermittency and grid integration challenges",
                    "High capital requirements",
                    "Technology obsolescence",
                    "Policy and regulatory changes"
                ],
                "future_outlook": "India's renewable energy sector will grow rapidly to meet 500 GW target by 2030. Green hydrogen and battery manufacturing will create new opportunities. The sector will attract significant domestic and foreign investment."
            }
        }
        
        # Return sector-specific or generic analysis
        if sector_lower in analysis_templates:
            return analysis_templates[sector_lower]
        
        # Generic analysis for unknown sectors
        return {
            "overview": f"The {sector} sector in India presents emerging opportunities with growing market demand and government support. The sector is positioned for significant growth in the coming years.",
            "key_trends": [
                "Market expansion and growth",
                "Digital transformation and innovation",
                "Government policy support",
                "Rising consumer demand"
            ],
            "opportunities": [
                "Market expansion opportunities",
                "Innovation and technology adoption",
                "Export potential",
                "Infrastructure development"
            ],
            "risks": [
                "Market competition",
                "Regulatory changes",
                "Economic volatility",
                "Supply chain disruptions"
            ],
            "future_outlook": f"The {sector} sector is expected to grow significantly in the next 2-3 years. Government initiatives and rising demand will drive expansion. The sector presents attractive opportunities for investors and entrepreneurs."
        }
