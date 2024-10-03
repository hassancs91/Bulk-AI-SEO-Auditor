from typing import List
from urllib.parse import urlparse
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.rapid_api import RapidAPIClient
from bs4 import BeautifulSoup
import requests
from textwrap import wrap
import json
import streamlit as st

llm_instance = LLM.create(provider=LLMProvider.ANTHROPIC,model_name="claude-3-haiku-20240307")


def display_wrapped_json(data, width=80):
    """
    Display JSON data with text wrapping for improved readability.
    """
    def wrap_str(s):
        return '\n'.join(wrap(s, width=width))
    
    def process_item(item):
        if isinstance(item, dict):
            return {k: process_item(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [process_item(i) for i in item]
        elif isinstance(item, str):
            return wrap_str(item)
        else:
            return item
    
    wrapped_data = process_item(data)
    st.code(json.dumps(wrapped_data, indent=2), language='json')

def free_seo_audit(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Basic HTTP info
        audit_result = {
            "http": {
                "status": response.status_code,
                "using_https": url.startswith("https://"),
                "response_time": f"{response.elapsed.total_seconds():.2f} seconds",
            }
        }

        # Metadata
        title_tag = soup.find("title")
        description_tag = soup.find("meta", {"name": "description"})
        audit_result["metadata"] = {
            "title": title_tag.string if title_tag else None,
            "title_length": len(title_tag.string) if title_tag else 0,
            "description": description_tag["content"] if description_tag else None,
            "description_length": len(description_tag["content"]) if description_tag else 0,
        }

        # Basic content analysis
        text_content = " ".join(soup.stripped_strings)
        headings = soup.find_all(["h1", "h2", "h3"])
        audit_result["content"] = {
            "word_count": len(text_content.split()),
            "h1_count": len([h for h in headings if h.name == "h1"]),
            "h2_count": len([h for h in headings if h.name == "h2"]),
            "h3_count": len([h for h in headings if h.name == "h3"]),
        }

        # Basic link analysis
        links = soup.find_all("a")
        internal_links = [link.get("href") for link in links if urlparse(link.get("href", "")).netloc == ""]
        external_links = [link.get("href") for link in links if urlparse(link.get("href", "")).netloc != ""]
        audit_result["links"] = {
            "total_links": len(links),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
        }

        # Basic image analysis
        images = soup.find_all("img")
        audit_result["images"] = {
            "total_images": len(images),
            "images_without_alt": sum(1 for img in images if not img.get("alt")),
        }

        return audit_result
    except Exception as ex:
        return {"error": str(ex)}

def ai_analysis(report):
    """
    Simulate AI analysis of the SEO audit report.
    In a real-world scenario, you'd integrate with an actual AI service.
    """
    seo_audit_analysis_prompt = f"""You are an expert in seo analysis.
            I will provide you with a [SEO_REPORT]
            and your task is to analyze and return a list of optimizations

            [SEO_REPORT]: {report}


            """
    
    ai_response =  llm_instance.generate_response(prompt=seo_audit_analysis_prompt,max_tokens=4096)
    return ai_response
    
def api_seo_audit(url: str):
    api_url = "https://website-seo-analyzer.p.rapidapi.com/seo/seo-audit-basic"
    api_params = {
        'url': url,
    }
    api_client = RapidAPIClient() 
    response = api_client.call_api(api_url, method='GET', params=api_params)
    return response