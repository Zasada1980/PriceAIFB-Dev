"""LLM (Ollama) adapter for text generation and normalization."""

import logging
import os
from typing import Optional

import requests
from pydantic import Field
from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


class LLMDisabledError(Exception):
    """Raised when LLM functionality is disabled."""
    pass


class LLMRequestError(Exception):
    """Raised when LLM request fails."""
    pass


class OllamaSettings(BaseSettings):
    """Ollama-specific configuration settings."""
    
    enable_llm: bool = Field(default=False, env="ENABLE_LLM")
    ollama_host: str = Field(default="http://localhost:11434", env="OLLAMA_HOST")
    ollama_model: str = Field(default="llama3", env="OLLAMA_MODEL")
    ollama_timeout_seconds: int = Field(default=30, env="OLLAMA_TIMEOUT_SECONDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
_ollama_settings = OllamaSettings()


def is_llm_enabled() -> bool:
    """Check if LLM functionality is enabled."""
    return _ollama_settings.enable_llm


def llm_health_check() -> bool:
    """Check if Ollama service is available and healthy.
    
    Returns:
        bool: True if service is healthy, False otherwise.
    """
    if not is_llm_enabled():
        return False
        
    try:
        response = requests.get(
            f"{_ollama_settings.ollama_host}/api/tags",
            timeout=_ollama_settings.ollama_timeout_seconds
        )
        return response.status_code == 200
    except requests.RequestException as e:
        logger.warning(f"Ollama health check failed: {e}")
        return False


def llm_generate(prompt: str, system_prompt: Optional[str] = None) -> str:
    """Generate text using Ollama LLM.
    
    Args:
        prompt: The main prompt text
        system_prompt: Optional system prompt for context
        
    Returns:
        str: Generated text response
        
    Raises:
        LLMDisabledError: If LLM functionality is disabled
        LLMRequestError: If the request fails
    """
    if not is_llm_enabled():
        raise LLMDisabledError("LLM functionality is disabled. Set ENABLE_LLM=true to enable.")
    
    try:
        payload = {
            "model": _ollama_settings.ollama_model,
            "prompt": prompt,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        response = requests.post(
            f"{_ollama_settings.ollama_host}/api/generate",
            json=payload,
            timeout=_ollama_settings.ollama_timeout_seconds
        )
        
        response.raise_for_status()
        result = response.json()
        
        if "response" not in result:
            raise LLMRequestError("Invalid response format from Ollama")
            
        return result["response"].strip()
        
    except requests.RequestException as e:
        logger.error(f"Ollama request failed: {e}")
        raise LLMRequestError(f"Failed to generate text: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in LLM generation: {e}")
        raise LLMRequestError(f"Unexpected error: {e}")


def llm_normalize_text(text: str) -> str:
    """Normalize product listing text using LLM.
    
    Args:
        text: Raw listing text to normalize
        
    Returns:
        str: Normalized text or original text if LLM is disabled
    """
    if not is_llm_enabled():
        logger.debug("LLM disabled, returning original text")
        return text
    
    try:
        system_prompt = (
            "You are a product listing normalizer for computer components. "
            "Extract and standardize product information from Hebrew/English text. "
            "Return only the normalized product name and key specifications."
        )
        
        prompt = f"Normalize this product listing: {text}"
        
        return llm_generate(prompt, system_prompt)
        
    except (LLMDisabledError, LLMRequestError) as e:
        logger.warning(f"LLM normalization failed, returning original text: {e}")
        return text