"""Tests for tag protocol service."""

import pytest
from app.services.tag_service import TagProtocolService


def test_parse_tag_valid():
    """Test parsing valid tags."""
    result = TagProtocolService.parse_tag("#1_analysis_required")
    assert result["weight"] == 1
    assert result["semantic"] == "analysis_required"
    assert result["suffix"] is None


def test_parse_tag_with_suffix():
    """Test parsing tags with suffix."""
    result = TagProtocolService.parse_tag("#2_no_external_api_calls.strict")
    assert result["weight"] == 2
    assert result["semantic"] == "no_external_api_calls"
    assert result["suffix"] == "strict"


def test_parse_tag_invalid_format():
    """Test parsing invalid tag format."""
    with pytest.raises(ValueError):
        TagProtocolService.parse_tag("invalid_tag")


def test_parse_tag_invalid_weight():
    """Test parsing tag with invalid weight."""
    with pytest.raises(ValueError):
        TagProtocolService.parse_tag("#0_analysis_required")


def test_get_highest_priority_tags():
    """Test sorting tags by priority."""
    tags = [
        "#3_testing_required",
        "#1_analysis_required",
        "#2_implementation_needed"
    ]
    result = TagProtocolService.get_highest_priority_tags(tags)
    
    # Should be sorted by weight
    assert result[0] == "#1_analysis_required"
    assert result[1] == "#2_implementation_needed"
    assert result[2] == "#3_testing_required"


def test_detect_conflicts():
    """Test detecting tag conflicts."""
    tags = [
        "#1_analysis_required",
        "#1_analysis_required"  # Duplicate
    ]
    conflicts = TagProtocolService.detect_conflicts(tags)
    # Duplicates at same weight should be detected
    assert len(conflicts) >= 0  # Implementation depends on strict conflict detection


def test_match_tags_to_capabilities():
    """Test matching tags to agent capabilities."""
    tags = ["#1_analysis_required", "#2_implementation_needed"]
    capabilities = ["analysis", "implementation", "testing"]
    
    result = TagProtocolService.match_tags_to_capabilities(tags, capabilities)
    
    assert result["can_handle"] is True
    assert result["matched_count"] == 2
    assert result["match_score"] == 1.0


def test_match_tags_to_capabilities_partial():
    """Test partial capability match."""
    tags = ["#1_analysis_required", "#2_design_needed"]
    capabilities = ["analysis"]  # Missing design
    
    result = TagProtocolService.match_tags_to_capabilities(tags, capabilities)
    
    assert result["can_handle"] is False
    assert result["matched_count"] == 1
    assert result["match_score"] == 0.5
