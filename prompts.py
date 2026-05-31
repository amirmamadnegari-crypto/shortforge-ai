"""
ShortForge AI - Prompt Templates
All LLM prompts for every agent, engineered for maximum viral output.
"""

from config import config

# ─── SYSTEM PROMPTS ────────────────────────────────────────────────────────────

SYSTEM_BASE = """You are ShortForge AI, an elite YouTube Shorts growth strategist with 10+ years 
of experience creating viral content. You have deep expertise in:
- YouTube algorithm optimization
- Human psychology and attention patterns
- Viral content formulas that drive shares, comments, and watch time
- Trend analysis and cultural relevance

You ALWAYS respond in valid JSON format as specified. Be specific, creative, and data-driven.
Your goal: help creators go viral with every single Short they post."""

SYSTEM_FOOTBALL = """You are ShortForge AI Football Edition — the world's #1 football content strategist.
You have encyclopedic knowledge of football history, statistics, iconic moments, player stories,
and what makes football fans stop scrolling and watch.

You understand:
- What football fans obsess over (rivalries, records, GOAT debates)
- Emotional triggers in football (comebacks, heartbreak, glory)
- Platform-specific viral patterns for football content
- How to frame facts and stories for maximum shock and shareability

Respond ONLY in valid JSON as specified."""


# ─── IDEA GENERATOR PROMPTS ───────────────────────────────────────────────────

def idea_generator_prompt(topic: str, football_mode: bool = False, football_config=None) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    football_extra = ""
    if football_mode and football_config:
        football_extra = f"""
Football-specific angles to explore:
- Pillars: {', '.join(football_config.content_pillars)}
- Viral angles: {', '.join(football_config.viral_angles)}
- League focus: {football_config.league_focus}
- Era: {football_config.player_era}
"""

    prompt = f"""Generate exactly {config.content.ideas_count} viral YouTube Shorts ideas for the topic: "{topic}"
{football_extra}
For each idea, provide:
1. A compelling title (max 70 characters)
2. Viral score (1-100)
3. Why it will go viral (specific psychological/algorithmic reason)
4. Target emotion (curiosity / shock / inspiration / nostalgia / humor / controversy)
5. Estimated view potential (Low / Medium / High / Mega-viral)
6. Best posting time (morning / afternoon / evening / night)

Rank ideas by viral score (highest first).

Respond ONLY with this exact JSON structure:
{{
  "topic": "{topic}",
  "ideas": [
    {{
      "rank": 1,
      "title": "...",
      "viral_score": 95,
      "viral_reason": "...",
      "target_emotion": "...",
      "view_potential": "Mega-viral",
      "best_posting_time": "evening",
      "niche_fit": "..."
    }}
  ],
  "top_insight": "..."
}}"""
    return system, prompt


# ─── HOOK GENERATOR PROMPTS ───────────────────────────────────────────────────

def hook_generator_prompt(topic: str, style: str = "general", football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    prompt = f"""Generate exactly {config.content.hooks_count} ultra-powerful YouTube Shorts hooks for: "{topic}"

Style preference: {style}

Rules for elite hooks:
- Must grab attention in under 3 seconds
- Create immediate FOMO or curiosity
- Never start with "In this video..." 
- Use pattern interrupts, bold claims, or shocking facts
- Each hook should use a different psychological trigger

Hook types to include:
1. Shocking statistic hook
2. Controversial statement hook  
3. "Most people don't know..." hook
4. Story hook (in medias res)
5. Question hook
6. Countdown hook ("3 reasons why...")
7. Comparison hook
8. Fear/FOMO hook
9. Achievement/record hook
10. Mystery/cliffhanger hook

Respond ONLY with this exact JSON:
{{
  "topic": "{topic}",
  "hooks": [
    {{
      "rank": 1,
      "hook_text": "...",
      "hook_type": "Shocking statistic",
      "psychological_trigger": "...",
      "retention_score": 95,
      "word_count": 12,
      "delivery_tip": "..."
    }}
  ],
  "best_hook": 1,
  "strategy_note": "..."
}}"""
    return system, prompt


# ─── SCRIPT GENERATOR PROMPTS ─────────────────────────────────────────────────

def script_generator_prompt(topic: str, hook: str, tone: str = "energetic", football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    prompt = f"""Write a complete, ready-to-record YouTube Shorts script for: "{topic}"

Opening hook: "{hook}"
Tone: {tone}
Target length: {config.content.script_min_seconds}-{config.content.script_max_seconds} seconds

The script MUST include these 4 sections:
1. HOOK (0-3 seconds): The attention grabber
2. MAIN STORY (3-45 seconds): Core content with storytelling
3. CURIOSITY LOOP (45-55 seconds): Re-engage, add twist or surprising fact
4. CALL TO ACTION (55-60 seconds): Drive follows, comments, or shares

Script requirements:
- Every sentence must earn its place
- Use short punchy sentences
- Include [PAUSE] markers for dramatic effect
- Include [VISUAL CUE] suggestions
- Include [TEXT OVERLAY] suggestions
- Natural speaking pace: ~150 words/minute

Respond ONLY with this exact JSON:
{{
  "topic": "{topic}",
  "tone": "{tone}",
  "estimated_duration_seconds": 55,
  "word_count": 140,
  "script": {{
    "hook": {{
      "text": "...",
      "duration_seconds": 3,
      "visual_cue": "...",
      "text_overlay": "..."
    }},
    "main_story": {{
      "text": "...",
      "duration_seconds": 42,
      "visual_cues": ["...", "..."],
      "text_overlays": ["...", "..."],
      "key_beats": ["beat1", "beat2", "beat3"]
    }},
    "curiosity_loop": {{
      "text": "...",
      "duration_seconds": 10,
      "twist": "...",
      "visual_cue": "..."
    }},
    "call_to_action": {{
      "text": "...",
      "duration_seconds": 5,
      "cta_type": "follow/comment/share",
      "urgency_trigger": "..."
    }}
  }},
  "full_script_readable": "...",
  "pro_tips": ["...", "...", "..."],
  "viral_elements": ["...", "...", "..."]
}}"""
    return system, prompt


# ─── THUMBNAIL INTELLIGENCE PROMPTS ──────────────────────────────────────────

def thumbnail_prompt(topic: str, target_emotion: str = "curiosity", football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    football_note = "Focus on football players, stadiums, match moments, trophies, and iconic celebrations." if football_mode else ""

    prompt = f"""Design a complete thumbnail intelligence report for a YouTube Short about: "{topic}"
Target emotion: {target_emotion}
{football_note}

Provide a comprehensive thumbnail strategy that maximizes CTR (Click-Through Rate).

Respond ONLY with this exact JSON:
{{
  "topic": "{topic}",
  "thumbnail_concepts": [
    {{
      "concept_name": "...",
      "emotion_target": "...",
      "color_palette": {{
        "primary": "#FF0000",
        "secondary": "#000000",
        "accent": "#FFFFFF",
        "background": "#1A1A1A",
        "rationale": "..."
      }},
      "thumbnail_text": {{
        "main_text": "...",
        "sub_text": "...",
        "font_style": "...",
        "text_placement": "..."
      }},
      "composition": {{
        "layout": "...",
        "focal_point": "...",
        "rule_of_thirds": "...",
        "visual_elements": ["...", "..."],
        "background_style": "..."
      }},
      "psychology": {{
        "why_it_works": "...",
        "curiosity_gap": "...",
        "emotional_hook": "...",
        "pattern_interrupt": "..."
      }},
      "ctr_score": 88,
      "a_b_test_variant": "..."
    }}
  ],
  "recommended_concept": 1,
  "thumbnail_dont": ["...", "...", "..."],
  "mobile_optimization_tip": "..."
}}"""
    return system, prompt


# ─── SEO GENERATOR PROMPTS ────────────────────────────────────────────────────

def seo_generator_prompt(topic: str, script_summary: str = "", football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    prompt = f"""Generate a complete YouTube SEO package for a Short about: "{topic}"
Script context: {script_summary if script_summary else "Not provided"}

Create SEO that maximizes discoverability on YouTube Search, Shorts feed, and Google.

Respond ONLY with this exact JSON:
{{
  "topic": "{topic}",
  "titles": [
    {{"title": "...", "character_count": 65, "seo_score": 92, "click_bait_level": "High"}},
    {{"title": "...", "character_count": 58, "seo_score": 88, "click_bait_level": "Medium"}},
    {{"title": "...", "character_count": 71, "seo_score": 85, "click_bait_level": "Curiosity"}}
  ],
  "description": {{
    "full_description": "...",
    "character_count": 400,
    "keyword_density": "optimal",
    "timestamps": false
  }},
  "hashtags": {{
    "primary": ["#Shorts", "#YouTube", "..."],
    "niche": ["...", "...", "...", "...", "..."],
    "trending": ["...", "...", "..."],
    "total_count": {config.content.hashtags_count}
  }},
  "keywords": {{
    "primary_keywords": ["...", "...", "..."],
    "long_tail": ["...", "...", "..."],
    "lsi_keywords": ["...", "...", "..."],
    "competition_level": "Medium"
  }},
  "tags": ["...", "...", "...", "...", "..."],
  "best_title": 1,
  "seo_strategy": "..."
}}"""
    return system, prompt


# ─── VIRAL SCORE PROMPTS ──────────────────────────────────────────────────────

def viral_score_prompt(content_package: dict, football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    prompt = f"""Analyze this YouTube Shorts content package and provide a comprehensive viral score analysis:

Content package:
{content_package}

Score each dimension from 0-100 and provide specific improvement recommendations.

Respond ONLY with this exact JSON:
{{
  "overall_viral_score": 87,
  "grade": "A",
  "dimensions": {{
    "curiosity": {{
      "score": 90,
      "reason": "...",
      "improvement": "..."
    }},
    "emotion": {{
      "score": 85,
      "reason": "...",
      "improvement": "..."
    }},
    "shareability": {{
      "score": 88,
      "reason": "...",
      "improvement": "..."
    }},
    "retention_potential": {{
      "score": 82,
      "reason": "...",
      "improvement": "..."
    }},
    "trend_alignment": {{
      "score": 91,
      "reason": "...",
      "improvement": "..."
    }}
  }},
  "strengths": ["...", "...", "..."],
  "weaknesses": ["...", "..."],
  "quick_wins": ["...", "...", "..."],
  "predicted_performance": {{
    "views_range": "50K - 500K",
    "engagement_rate": "8-12%",
    "virality_probability": "High"
  }},
  "competitor_edge": "..."
}}"""
    return system, prompt


# ─── CONTENT CALENDAR PROMPTS ─────────────────────────────────────────────────

def content_calendar_prompt(topic: str, posting_frequency: str = "daily", football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    prompt = f"""Create a strategic {config.content.calendar_days}-day YouTube Shorts content calendar for the niche: "{topic}"
Posting frequency: {posting_frequency}

Build a calendar that:
- Builds momentum week by week
- Mixes content types strategically
- Leverages trending patterns
- Includes seasonal/event hooks
- Optimizes for algorithm growth

Respond ONLY with this exact JSON:
{{
  "niche": "{topic}",
  "strategy_overview": "...",
  "weeks": [
    {{
      "week": 1,
      "theme": "...",
      "goal": "...",
      "days": [
        {{
          "day": 1,
          "date_offset": "Day 1",
          "content_type": "...",
          "title_idea": "...",
          "hook_style": "...",
          "posting_time": "18:00",
          "expected_performance": "...",
          "notes": "..."
        }}
      ]
    }}
  ],
  "monthly_strategy": {{
    "week1_focus": "Foundation & Discovery",
    "week2_focus": "...",
    "week3_focus": "...",
    "week4_focus": "..."
  }},
  "content_mix": {{
    "educational": "30%",
    "entertainment": "40%",
    "inspirational": "20%",
    "controversial": "10%"
  }},
  "milestone_targets": {{
    "day_7": "...",
    "day_14": "...",
    "day_30": "..."
  }}
}}"""
    return system, prompt


# ─── GROWTH ADVISOR PROMPTS ───────────────────────────────────────────────────

def growth_advisor_prompt(topic: str, current_subs: int = 0, football_mode: bool = False) -> str:
    system = SYSTEM_FOOTBALL if football_mode else SYSTEM_BASE

    prompt = f"""Create a comprehensive YouTube channel growth strategy for a {topic} channel.
Current subscribers: {current_subs}

Provide a detailed, actionable growth roadmap tailored to this niche.

Respond ONLY with this exact JSON:
{{
  "channel_analysis": {{
    "niche": "{topic}",
    "current_stage": "...",
    "growth_potential": "...",
    "competition_level": "..."
  }},
  "posting_strategy": {{
    "recommended_frequency": "...",
    "best_posting_times": ["...", "..."],
    "consistency_score": "...",
    "rationale": "..."
  }},
  "content_pillars": [
    {{
      "pillar_name": "...",
      "description": "...",
      "posting_ratio": "30%",
      "example_ideas": ["...", "...", "..."]
    }}
  ],
  "audience_targeting": {{
    "primary_audience": "...",
    "secondary_audience": "...",
    "demographics": {{
      "age_range": "18-34",
      "interests": ["...", "...", "..."],
      "platform_behavior": "..."
    }},
    "pain_points": ["...", "..."],
    "desires": ["...", "..."]
  }},
  "growth_phases": [
    {{
      "phase": 1,
      "name": "Launch Phase",
      "duration": "Days 1-30",
      "goal": "...",
      "tactics": ["...", "...", "..."],
      "success_metrics": "..."
    }},
    {{
      "phase": 2,
      "name": "Growth Phase",
      "duration": "Days 31-90",
      "goal": "...",
      "tactics": ["...", "...", "..."],
      "success_metrics": "..."
    }},
    {{
      "phase": 3,
      "name": "Scale Phase",
      "duration": "Days 91-180",
      "goal": "...",
      "tactics": ["...", "...", "..."],
      "success_metrics": "..."
    }}
  ],
  "monetization_path": {{
    "milestone_1k_subs": "...",
    "milestone_10k_subs": "...",
    "revenue_streams": ["...", "...", "..."]
  }},
  "quick_wins": ["...", "...", "...", "...", "..."],
  "avoid_mistakes": ["...", "...", "..."]
}}"""
    return system, prompt
