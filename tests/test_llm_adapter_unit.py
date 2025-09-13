"""Unit tests for LLM adapter using mocked HTTP requests."""

import pytest
from unittest.mock import patch, Mock
import requests

from market_scout.adapters.llm import (
    is_llm_enabled,
    llm_health_check,
    llm_generate,
    llm_normalize_text,
    LLMDisabledError,
    LLMRequestError,
    _ollama_settings
)


class TestLLMAdapter:
    """Test LLM adapter functionality with mocked requests."""

    def test_llm_disabled_by_default(self):
        """Test that LLM is disabled by default."""
        # Reset settings to default
        _ollama_settings.enable_llm = False
        assert not is_llm_enabled()

    @patch.dict('os.environ', {'ENABLE_LLM': 'true'})
    def test_llm_can_be_enabled(self):
        """Test that LLM can be enabled via environment variable."""
        # Create new settings instance to pick up env var
        from market_scout.adapters.llm import OllamaSettings
        settings = OllamaSettings()
        assert settings.enable_llm

    def test_health_check_disabled_llm(self):
        """Test health check returns False when LLM is disabled."""
        _ollama_settings.enable_llm = False
        assert not llm_health_check()

    @patch('market_scout.adapters.llm.requests.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check."""
        _ollama_settings.enable_llm = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        assert llm_health_check()
        mock_get.assert_called_once_with(
            "http://localhost:11434/api/tags",
            timeout=30
        )

    @patch('market_scout.adapters.llm.requests.get')
    def test_health_check_failure(self, mock_get):
        """Test health check failure."""
        _ollama_settings.enable_llm = True
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        assert not llm_health_check()

    def test_generate_disabled_llm_raises_error(self):
        """Test that generate raises error when LLM is disabled."""
        _ollama_settings.enable_llm = False
        
        with pytest.raises(LLMDisabledError, match="LLM functionality is disabled"):
            llm_generate("test prompt")

    @patch('market_scout.adapters.llm.requests.post')
    def test_generate_success(self, mock_post):
        """Test successful text generation."""
        _ollama_settings.enable_llm = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Generated text"}
        mock_post.return_value = mock_response
        
        result = llm_generate("test prompt")
        
        assert result == "Generated text"
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]['json']['prompt'] == "test prompt"
        assert call_args[1]['json']['model'] == "llama3"
        assert call_args[1]['json']['stream'] is False

    @patch('market_scout.adapters.llm.requests.post')
    def test_generate_with_system_prompt(self, mock_post):
        """Test text generation with system prompt."""
        _ollama_settings.enable_llm = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "System guided response"}
        mock_post.return_value = mock_response
        
        result = llm_generate("test prompt", "system context")
        
        assert result == "System guided response"
        call_args = mock_post.call_args
        assert call_args[1]['json']['system'] == "system context"

    @patch('market_scout.adapters.llm.requests.post')
    def test_generate_request_failure(self, mock_post):
        """Test handling of request failures."""
        _ollama_settings.enable_llm = True
        mock_post.side_effect = requests.RequestException("Connection error")
        
        with pytest.raises(LLMRequestError, match="Failed to generate text"):
            llm_generate("test prompt")

    @patch('market_scout.adapters.llm.requests.post')
    def test_generate_invalid_response(self, mock_post):
        """Test handling of invalid response format."""
        _ollama_settings.enable_llm = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "Invalid format"}
        mock_post.return_value = mock_response
        
        with pytest.raises(LLMRequestError, match="Invalid response format"):
            llm_generate("test prompt")

    def test_normalize_text_disabled_llm(self):
        """Test text normalization when LLM is disabled."""
        _ollama_settings.enable_llm = False
        original_text = "Original product text"
        
        result = llm_normalize_text(original_text)
        
        assert result == original_text

    @patch('market_scout.adapters.llm.llm_generate')
    def test_normalize_text_success(self, mock_generate):
        """Test successful text normalization."""
        _ollama_settings.enable_llm = True
        mock_generate.return_value = "Normalized product: Intel Core i7"
        
        result = llm_normalize_text("אינטל קור i7 מעבד")
        
        assert result == "Normalized product: Intel Core i7"
        mock_generate.assert_called_once()

    @patch('market_scout.adapters.llm.llm_generate')
    def test_normalize_text_fallback_on_error(self, mock_generate):
        """Test fallback to original text when normalization fails."""
        _ollama_settings.enable_llm = True
        original_text = "Original product text"
        mock_generate.side_effect = LLMRequestError("Service unavailable")
        
        result = llm_normalize_text(original_text)
        
        assert result == original_text

    def teardown_method(self):
        """Reset settings after each test."""
        _ollama_settings.enable_llm = False