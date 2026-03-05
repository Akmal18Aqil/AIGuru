import os
from typing import Optional, Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel

class LLMFactory:
    """Factory to create LLM instances based on configuration."""

    @staticmethod
    def get_llm(temperature: float = 0.5, timeout: float = 30.0) -> BaseChatModel:
        """
        Get the configured LLM instance.
        
        Args:
            temperature: The temperature for the LLM.
            timeout: Request timeout in seconds. Use higher value (e.g. 120)
                     for complex tasks like jadwal generation.

        Returns:
            An instantiated LangChain chat model.
        """
        from ai_guru.config.api_key_manager import APIKeyManager
        
        api_manager = APIKeyManager()
        provider_config = api_manager.get_llm_provider_config()
        
        provider = provider_config.get('provider', 'Google Gemini')
        api_key = provider_config.get('api_key', '')
        
        if not api_key:
            raise ValueError(f"API Key for {provider} not found.")

        # Override environment variable so langchain modules can pick it up if needed
        # Or pass it directly to the instantiation
        
        if provider == 'Google Gemini':
            from langchain_google_genai import ChatGoogleGenerativeAI
            # Ensure the environment variable is set for langchain_google_genai
            if 'GOOGLE_API_KEY' not in os.environ or os.environ['GOOGLE_API_KEY'] != api_key:
                os.environ['GOOGLE_API_KEY'] = api_key
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", # Stable production model
                temperature=temperature,
                google_api_key=api_key,
                max_retries=3,
                timeout=timeout
            )
            
        elif provider == 'OpenRouter':
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model="google/gemini-flash-1.5", 
                temperature=temperature,
                max_retries=3,
                timeout=timeout,
                default_headers={
                    "HTTP-Referer": "https://siguru.app", # Required for OpenRouter
                    "X-Title": "SiGURU AI Assistant",
                }
            )
            
        elif provider == 'Groq':
            from langchain_groq import ChatGroq
            return ChatGroq(
                api_key=api_key,
                model_name="llama-3.1-70b-versatile", # Updated model
                temperature=temperature,
                max_retries=3,
                timeout=timeout
            )
            
        elif provider == 'Anthropic':
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                api_key=api_key,
                model_name="claude-3-5-sonnet-20240620",
                temperature=temperature,
                max_retries=3,
                timeout=timeout
            )
            
        elif provider == 'Custom Provider':
            from langchain_openai import ChatOpenAI
            base_url = provider_config.get('custom_base_url', '')
            model_name = provider_config.get('custom_model_name', 'default-model')
            
            # Simple fallback if no base url
            if not base_url:
                raise ValueError("Custom Provider requires a Base URL.")
                
            return ChatOpenAI(
                base_url=base_url,
                api_key=api_key,
                model=model_name,
                temperature=temperature,
                max_retries=3,
                timeout=timeout
            )
            
        else:
            # Fallback to Google Gemini
            from langchain_google_genai import ChatGoogleGenerativeAI
            os.environ['GOOGLE_API_KEY'] = api_key
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                temperature=temperature,
                google_api_key=api_key,
                max_retries=3,
                timeout=timeout
            )
