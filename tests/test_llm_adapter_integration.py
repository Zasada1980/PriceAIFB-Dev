"""Integration tests for LLM adapter requiring actual Ollama service."""

import pytest
import requests

from market_scout.adapters.llm import (
    LLMDisabledError,
    LLMRequestError,
    _ollama_settings,
    is_llm_enabled,
    llm_generate,
    llm_health_check,
    llm_normalize_text,
)


def is_ollama_available():
    """Check if Ollama service is available for integration testing."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


@pytest.mark.ollama
class TestLLMIntegration:
    """Integration tests requiring actual Ollama service."""

    def setup_method(self):
        """Setup for integration tests."""
        if not is_ollama_available():
            pytest.skip("Ollama service not available")

        # Enable LLM for integration tests
        _ollama_settings.enable_llm = True
        _ollama_settings.ollama_host = "http://localhost:11434"
        _ollama_settings.ollama_model = "llama3"
        _ollama_settings.ollama_timeout_seconds = 60  # Longer timeout for real requests

    def test_health_check_real_service(self):
        """Test health check against real Ollama service."""
        assert llm_health_check()

    def test_generate_real_request(self):
        """Test text generation with real Ollama service."""
        prompt = "What is 2+2? Answer with just the number."

        try:
            result = llm_generate(prompt)

            # Basic validation - should get some response
            assert isinstance(result, str)
            assert len(result.strip()) > 0

        except LLMRequestError as e:
            if "model" in str(e).lower() and "not found" in str(e).lower():
                pytest.skip(f"Required model not available: {e}")
            raise

    def test_generate_with_system_prompt_real(self):
        """Test generation with system prompt on real service."""
        system_prompt = "You are a helpful calculator. Respond only with numbers."
        prompt = "What is 5+5?"

        try:
            result = llm_generate(prompt, system_prompt)

            # Should get a response
            assert isinstance(result, str)
            assert len(result.strip()) > 0

        except LLMRequestError as e:
            if "model" in str(e).lower() and "not found" in str(e).lower():
                pytest.skip(f"Required model not available: {e}")
            raise

    def test_normalize_text_real(self):
        """Test text normalization with real service."""
        test_text = "Intel Core i7-12700K CPU processor"

        try:
            result = llm_normalize_text(test_text)

            # Should get some normalized result
            assert isinstance(result, str)
            assert len(result.strip()) > 0

        except LLMRequestError as e:
            if "model" in str(e).lower() and "not found" in str(e).lower():
                pytest.skip(f"Required model not available: {e}")
            raise

    def test_timeout_handling(self):
        """Test timeout handling with very short timeout."""
        # Temporarily set very short timeout
        original_timeout = _ollama_settings.ollama_timeout_seconds
        _ollama_settings.ollama_timeout_seconds = 1  # Very short timeout

        try:
            # This might succeed or timeout depending on service speed
            result = llm_generate("Simple test")
            # If it succeeds, just verify we got a string
            assert isinstance(result, str)

        except LLMRequestError:
            # Timeout is expected with very short timeout
            pass
        finally:
            _ollama_settings.ollama_timeout_seconds = original_timeout

    def teardown_method(self):
        """Reset settings after each test."""
        _ollama_settings.enable_llm = False


@pytest.mark.ollama
def test_integration_environment_disabled():
    """Test that integration tests are skipped when LLM is explicitly disabled."""
    # Force disable even if service is available
    _ollama_settings.enable_llm = False

    assert not is_llm_enabled()
    assert not llm_health_check()

    with pytest.raises(LLMDisabledError):
        llm_generate("test")


@pytest.mark.ollama
def test_service_unavailable_handling():
    """Test handling when service is configured but unavailable."""
    # Point to non-existent service
    _ollama_settings.enable_llm = True
    _ollama_settings.ollama_host = "http://localhost:99999"

    # Health check should fail gracefully
    assert not llm_health_check()

    # Generate should raise appropriate error
    with pytest.raises(LLMRequestError):
        llm_generate("test prompt")
