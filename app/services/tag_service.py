"""Tag matching and routing service."""

from typing import List, Dict, Set, Optional
from sqlalchemy.orm import Session
from app.models.work_order import WorkOrderTag
from app.core.enums import TagCategory


class TagProtocolService:
    """Service for tag protocol matching and validation."""
    
    @staticmethod
    def parse_tag(tag_text: str) -> Dict[str, any]:
        """
        Parse a tag into components.
        Format: #<weight>_<semantic>[.<suffix>]
        Example: #1_analysis_required, #2_no_external_api_calls
        """
        if not tag_text.startswith("#"):
            raise ValueError(f"Invalid tag format: {tag_text}")
        
        tag_text = tag_text.lstrip("#")
        parts = tag_text.split("_", 1)
        
        if len(parts) != 2:
            raise ValueError(f"Invalid tag format: #{tag_text}")
        
        try:
            weight = int(parts[0])
            if not (1 <= weight <= 5):
                raise ValueError("Weight must be 1-5")
        except ValueError:
            raise ValueError(f"Invalid weight in tag: {parts[0]}")
        
        semantic = parts[1]
        if "." in semantic:
            semantic, suffix = semantic.split(".", 1)
        else:
            suffix = None
        
        return {
            "weight": weight,
            "semantic": semantic,
            "suffix": suffix,
            "full_text": f"#{parts[0]}_{semantic}" + (f".{suffix}" if suffix else "")
        }
    
    @staticmethod
    def detect_conflicts(tags: List[str]) -> List[Dict[str, any]]:
        """
        Detect conflicts between tags.
        Rules:
        - Lower weight takes priority
        - Prohibition tags override permission tags at same weight
        """
        parsed = []
        conflicts = []
        
        for tag in tags:
            try:
                parsed.append(TagProtocolService.parse_tag(tag))
            except ValueError:
                continue
        
        # Group by weight
        by_weight = {}
        for p in parsed:
            w = p["weight"]
            if w not in by_weight:
                by_weight[w] = []
            by_weight[w].append(p)
        
        # Check for conflicts at same weight
        for weight, tags_at_weight in by_weight.items():
            if len(tags_at_weight) > 1:
                # Check for prohibition vs permission conflicts
                semantics = [t["semantic"] for t in tags_at_weight]
                if len(semantics) != len(set(semantics)):
                    conflicts.append({
                        "weight": weight,
                        "message": f"Conflicting tags at weight {weight}: {semantics}"
                    })
        
        return conflicts
    
    @staticmethod
    def match_tags_to_capabilities(
        work_order_tags: List[str],
        agent_capabilities: List[str],
        db: Session = None
    ) -> Dict[str, any]:
        """
        Match work order tags to AI agent capabilities.
        Returns match score and matching results.
        """
        matches = []
        mismatches = []
        
        tag_mapping = {
            "analysis_required": "analysis",
            "design_needed": "design",
            "implementation_needed": "implementation",
            "testing_required": "testing",
            "review_required": "review",
            "translation_required": "translation",
            "research_needed": "research",
        }
        
        for tag in work_order_tags:
            try:
                parsed = TagProtocolService.parse_tag(tag)
                semantic = parsed["semantic"]
                
                # Check if semantic maps to capability
                required_capability = tag_mapping.get(semantic)
                if required_capability:
                    if required_capability in agent_capabilities:
                        matches.append({
                            "tag": tag,
                            "matched_capability": required_capability
                        })
                    else:
                        mismatches.append({
                            "tag": tag,
                            "required_capability": required_capability
                        })
            except ValueError:
                continue
        
        match_score = len(matches) / len(work_order_tags) if work_order_tags else 0
        
        return {
            "match_score": match_score,
            "matched_count": len(matches),
            "total_required": len(work_order_tags),
            "matches": matches,
            "mismatches": mismatches,
            "can_handle": len(mismatches) == 0
        }
    
    @staticmethod
    def get_highest_priority_tags(tags: List[str]) -> List[str]:
        """Get tags sorted by weight (lowest weight = highest priority)."""
        try:
            parsed_tags = [TagProtocolService.parse_tag(t) for t in tags]
            sorted_tags = sorted(parsed_tags, key=lambda x: x["weight"])
            return [t["full_text"] for t in sorted_tags]
        except ValueError:
            return tags
