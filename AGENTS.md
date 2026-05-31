# ShortForge AI — Documentation

## Agent Reference

### IdeaAgent
**File:** `agents/idea_agent.py`  
**Method:** `generate_ideas(topic, football_mode)`  
**Returns:** 20 ideas with viral scores, emotions, and view potential

### HookAgent
**File:** `agents/hook_agent.py`  
**Method:** `generate_hooks(topic, style, football_mode)`  
**Returns:** 10 hooks with retention scores and delivery tips  
**Styles:** general, shocking, controversial, storytelling, question-based, listicle, emotional, humor

### ScriptAgent
**File:** `agents/script_agent.py`  
**Method:** `generate_script(topic, hook, tone, football_mode)`  
**Returns:** Full script with 4 sections, visual cues, text overlays  
**Tones:** energetic, calm-authoritative, storytelling, humorous, dramatic, educational, inspirational, controversial

### ThumbnailAgent
**File:** `agents/thumbnail_agent.py`  
**Method:** `generate_thumbnail_strategy(topic, target_emotion, football_mode)`  
**Returns:** 3 thumbnail concepts with colors, composition, psychology

### SEOAgent
**File:** `agents/seo_agent.py`  
**Method:** `generate_seo(topic, script_summary, football_mode)`  
**Returns:** 3 title variants, description, 20 hashtags, keywords

### GrowthAgent
**File:** `agents/growth_agent.py`  
**Methods:**  
- `score_content(topic, hook, script_summary, title, football_mode)` → 5-dimension viral score  
- `generate_calendar(topic, posting_frequency, football_mode)` → 30-day calendar  
- `get_growth_advice(topic, current_subs, football_mode)` → full growth strategy

## Prompt Engineering Notes

All prompts are in `prompts/prompts.py`. Each prompt:
- Specifies exact JSON output format (prevents hallucination)
- Includes a specialized system prompt for authority/expertise framing
- Uses football-specific context injection when Football Mode is enabled
- Is tuned for Claude Sonnet at temperature 0.85 for creative but reliable output
