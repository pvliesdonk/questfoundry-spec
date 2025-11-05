# Gamebook Design Metrics

**Purpose:** Industry-standard metrics for interactive fiction / gamebook design based on published CYOA (Choose Your Own Adventure) titles.

**Source:** Analysis of published print and digital gamebooks across multiple platforms (Twine, ChoiceScript, inkle, traditional print).

**Note:** These are **informational guidelines**, not enforced constraints. Users may choose any valid values within schema limits.

---

## Length Categories by Scope

Based on analysis of published gamebooks, typical length categories are:

| Category | Section Count | Total Word Count | Typical Playtime | Branching Complexity |
|----------|--------------|------------------|------------------|---------------------|
| **Short** | 50 - 150 | 10,000 - 30,000 | ~30 minutes | **Low.** Simple paths with 2-4 distinct endings. Choices frequently merge back to central trunk. Ideal for tutorials, focused stories, or game jam entries. |
| **Medium** | 250 - 500 | 30,000 - 70,000 | ~1 hour | **Moderate.** Standard for full-length commercial title. Supports 5-10+ endings and several distinct sub-plots. Good replayability without overwhelming scope. |
| **Long** | 500 - 1,000 | 70,000 - 150,000 | ~2 hours | **High.** Complex digital titles or premium print collections. Can support 15-20+ endings. Major choices lead to significantly different mid-games. High replayability. |
| **Epic** | 1,000+ | 150,000 - 500,000+ | 3+ hours | **Very High / Sandboxy.** Dozens of endings or persistent world states. Paths deeply divergent; often impossible to see all content in few playthroughs. Rare in traditional gamebooks, more common in digital IF. |

### Notes on Length

**Section count** refers to distinct passages/nodes, not total words. A "section" is a single beat in the story with choices leading to other sections.

**Word count** is approximate total across all sections (not a single playthrough). Actual reading varies significantly based on path taken.

**Playtime** assumes average reading speed of ~250 words/minute for prose. Actual time varies based on decision-making time and replayability.

---

## Content Pacing Defaults

These defaults target **Medium scope** but are scalable to other lengths:

| Unit | Default Value | Rationale |
|------|--------------|-----------|
| **Standard Section** | ~125 words | Core "beat" of the game. Long enough to set scene and present problem, short enough to maintain momentum. (e.g., 50,000 words / 400 sections ≈ 125 words/section) |
| **Standard Paragraph** | ~50 words | Readability default. 125-word section = 2-3 visual chunks to avoid "wall of text." Improves scanability and pacing. |
| **"Fail" Section** | < 50 words | Clear "Game Over" or "Bad Ending." Purpose is finality, not exposition. Quick read signals consequence. |
| **"Hub" Section** | < 100 words | Recurring location (e.g., town square, base camp, main menu). Short and functional for re-orientation without repetition fatigue. |
| **Choices per Section** | 3 | Ergonomic standard. 2 choices feels binary/limiting; 4+ causes decision fatigue. 3 provides meaningful agency without overwhelm. |

### Variations by Genre

Different genres adjust these defaults:

- **Horror/Thriller:** Sections often < 100 words for rapid page-turning tension
- **Romance:** Sections often 150-200 words for character development and dialogue
- **Fantasy/RPG:** Variable length; hub sections are short, lore sections can be 200+ words
- **Mystery:** Investigation sections can be longer (150-200 words) for clue details

See `genre_conventions.md` for specific genre variations.

---

## Default Structural Logic: "Branch and Merge"

**Problem:** Pure exponential branching is logistically unwritable.

With 3 choices per section, a 5-level deep tree = 3^5 = 243 unique sections. Unsustainable.

**Solution:** Branch-and-merge pattern (also called "delayed branching" or "gauntlet structure"):

### How It Works

1. **Branch:** Major choice leads to divergent paths (A, B, C)
2. **Diverge:** Each path continues for 3-5 unique sections showing consequences
3. **Set Consequence:** Track choice via variable (e.g., `ally_status = "angered"`)
4. **Merge:** All paths converge at next major plot-point section
5. **Check Later:** Future sections reference variable (`IF ally_status = "angered"`) for long-term consequences

### Example Structure

```
[Section 10: Major Choice]
    ├─ A: Help the stranger → [11A] → [12A] → [13A] ─┐
    ├─ B: Ignore and leave → [11B] → [12B] → [13B] ─┼─→ [Section 14: Merge Point]
    └─ C: Report to guards → [11C] → [12C] → [13C] ─┘

[Section 14] checks variable set in A/B/C path:
- If helped: "The stranger remembers your kindness..."
- If ignored: "You recognize the stranger but they don't acknowledge you..."
- If reported: "The stranger glares at you with hostility..."
```

### Benefits

- **Manageable scope:** Writers can create *feeling* of fully branched story with reasonable section count
- **Meaningful choices:** Divergent sections show immediate consequence, variables provide long-term impact
- **Replayability:** Multiple paths create different experiences, but content is reused intelligently
- **Narratively sound:** Major plot points remain coherent while player agency is preserved

### When to Use Other Patterns

**Linear with flavor choices:** Simple stories where choices affect tone/style but not plot.
- Example: Romance where relationship develops regardless, but dialogue options change flavor

**Hub-and-spoke:** Investigation/exploration stories with central location.
- Example: Mystery where player chooses which lead to investigate next, but all leads are available

**Parallel paths:** Stories with genuinely divergent middle acts that don't merge until ending.
- Example: Fantasy where choosing faction A vs B leads to completely different questlines

**State-based:** RPG-style stories tracking many variables for complex conditional content.
- Example: Stat-tracking survival games where inventory/health determine accessible sections

See `genre_conventions.md` for which patterns work best for each genre.

---

## Genre-Based Metric Variations

Genre expectations directly influence all metrics:

| Genre | Impact on Length & Branching | Primary Focus |
|-------|----------------------------|---------------|
| **Fantasy / RPG** | Long to Epic. High section count (exploration) and high word count (lore). "Wide" branching (hub-and-spoke) with many optional side paths. | **World-building & Systems.** Supports stat-tracking, combat resolution, inventory management, explorable world. Section count often exceeds word-per-section average due to many short hub sections. |
| **Romance** | Long to Epic (by word count). "Deep" branching (many relationship variables) but not structurally divergent. Same core plot, choices modify relationship states and dialogue. | **Character & State-Tracking.** High word count for nuanced dialogue and emotional beats. A 300k-word romance may have fewer sections than a 70k-word fantasy because sections are longer and more focused on conversation. |
| **Horror / Thriller** | Short to Medium. "Lethal" branching—few golden paths to survival, many short fail-state branches. Sections often < 125 words. | **Pacing & Tension.** Short sections = rapid page-turning. Game is often puzzle: find survival path among many dead ends. Frequent bad endings increase tension. |
| **Mystery** | Medium. "Hub-and-spoke" branching. Gather clues (detailed investigation sections), return to central decision point to choose next lead. | **Information Gathering.** Structure is "web" not "tree." Replayability comes from exploring different investigation orders. Hub sections are short; clue sections are detailed (150-200 words). |
| **Sci-Fi / Cyberpunk** | Medium to Long. Moderate branching with emphasis on moral dilemmas. Technology as theme introduces conditional content based on choices. | **Ethical Choices & World-building.** Balance between lore exposition and player agency. Often includes stat-tracking (reputation, augmentations) that gates certain paths. |
| **Historical Fiction** | Medium. Moderate branching with emphasis on period accuracy. Educational potential balanced with narrative engagement. | **Authenticity & Immersion.** Research-grounded content. Choices reflect historical constraints. Often includes "what-if" alternate history branches. |

---

## Children's Gamebooks (Age-Specific Metrics)

**Note:** The metrics for children's gamebooks are dictated primarily by **reading level, attention span, and cognitive development**. Section length and sentence complexity are more critical than total word count.

The "Short/Medium/Long" scopes below are **relative to the age bracket**, not the adult scale.

### Structural Metrics by Age

| Age Bracket | 3-5 (Pre-reader) | 6-8 (Early Reader) | 9-12 (Middle Grade) |
|-------------|------------------|-------------------|---------------------|
| **Primary Goal** | Shared "read-aloud" activity. Simple cause-and-effect. | Build reading confidence. Fun, simple exploration. | Empowering story. A puzzle to be "solved." |
| **Scope** | Very Short | Short | Short-to-Medium (Adult Scale) |
| **Section Count** | 10 - 20 | 30 - 60 | 80 - 130 |
| **Total Word Count** | 200 - 500 | 2,000 - 5,000 | 15,000 - 30,000 |
| **Choices per Section** | 2 (Binary) | 2-3 | 2-3 |
| **Branching Model** | **Simple Divergence.** (e.g., "Park" or "Store"). One choice leads to 1-2 unique sections, then a common end. 2-3 total endings. | **Branch-and-Loop.** "Fail" states are not endings, but loops (e.g., "That didn't work! Turn back to 10 to try again."). 3-5 positive endings. | **Lethal Branching.** (Classic CYOA model). High number of abrupt "fail" endings (e.g., "You fall in a pit. The End."). One or two "golden paths" to a true victory. |
| **Avg. Section Length** | 10 - 25 words | 30 - 60 words | 100 - 150 words |
| **Paragraphing** | N/A (Single short sentence per page/section). | 1-2 paragraphs, 1-2 simple sentences each. | 2-4 paragraphs. Sentences are clear and direct. |

### Reading Difficulty by Age

| Age Bracket | Flesch-Kincaid Grade Level | Flesch Reading Ease (Target) | Dale-Chall Score (Target) |
|-------------|---------------------------|------------------------------|---------------------------|
| **Pre-reader (3-5)** | N/A (Pre-literacy) | N/A | N/A |
| **Early Reader (6-8)** | 1.0 - 3.0 | 90 - 100 | 4.9 or lower |
| **Middle Grade (9-12)** | 4.0 - 8.0 | 70 - 90 | 5.0 - 6.9 |
| **Young Adult (13-17)** | 8.0 - 10.0 | 60 - 70 | 7.0 - 8.9 |

**Readability Tools:** [Hemingway Editor](https://hemingwayapp.com/), [Readable.com](https://readable.com/), [WebFX Readability Test](https://www.webfx.com/tools/read-able/)

**Important:** These formulas are **English-specific** (based on syllable counting and English word familiarity lists). For other languages, consult language-specific readability measures (e.g., LIX for Nordic languages, Gulpease for Italian).

### Key Implementation Notes by Age

**Pre-reader (3-5):**
- The "gamebook" is a light activity. Word count is minimal and secondary to illustrations.
- Choices are simple, concrete, and have immediate, visible outcomes.
- No variable-tracking or complex state.
- **Illustration-dominant:** Text is secondary to visual storytelling.

**Early Reader (6-8):**
- Design priority is **reducing friction** and building confidence.
- **Vocabulary:** Uses high-frequency, phonetically simple words.
- **Section Length:** Kept very short to provide quick "reward" for reading a block of text.
- **Branching:** Fail states must be **forgiving**. A "Game Over" is discouraging. Structure redirects gently, doesn't punish.
- **Example:** "That didn't work! Turn back to section 10 to try something else."

**Middle Grade (9-12):**
- This is the demographic that defined the print gamebook boom (*Choose Your Own Adventure*, *Fighting Fantasy*).
- **Section Length:** The ~125-word default is surprisingly robust here. Key difference is not length but **complexity**—vocabulary is simpler, sentences have fewer clauses.
- **Branching:** The "Lethal Branching" model is a **key feature**. Fun derives from exploring, failing, and re-reading to "beat" the book.
- **Replayability:** High number of fail endings makes total section count (100+) misleading—a single playthrough is short, encouraging multiple attempts.
- **Consequences:** Choices are **immediate and final**, unlike adult "branch-and-merge" which relies on tracking variables for delayed consequences.

**Young Adult (13-17):**
- Bridge category between middle grade and adult.
- Uses **adult structural metrics** (250-500 sections for medium scope, branch-and-merge patterns).
- **Reading difficulty:** Targets 8.0-10.0 F-K Grade (Plain English baseline).
- **Themes:** Age-appropriate (coming-of-age, identity, social issues) but structurally equivalent to adult gamebooks.
- **Genre:** Often distinct YA genres (dystopian, paranormal romance, contemporary realistic).

### Children's Genre Examples

While children's gamebooks are primarily defined by age bracket, some common genre patterns:

**Pre-reader (3-5):**
- **Animal Friends:** Simple stories with anthropomorphic animals making choices (e.g., "Does Bunny go to the meadow or the pond?")
- **Everyday Adventures:** Familiar settings (park, store, playground) with cause-and-effect choices

**Early Reader (6-8):**
- **Educational Adventure:** Stories that teach concepts (counting, colors, problem-solving) through interactive choices
- **Beginner Mystery:** Very simple "whodunit" with 3-4 suspects and obvious clues

**Middle Grade (9-12):**
- **Fantasy Quest:** Classic hero's journey with stats, inventory, and monster encounters (*Fighting Fantasy* style)
- **Survival Adventure:** Outdoor or wilderness survival with resource management and environmental challenges
- **School Stories:** Contemporary settings with social choices and relationship navigation

---

## Section Count vs. Playthrough Length

**Important distinction:**

- **Total sections:** All possible passages in the entire game tree
- **Playthrough sections:** Number of sections encountered in a single read

### Typical Ratios

| Branching Complexity | Total Sections | Sections per Playthrough | Ratio |
|---------------------|----------------|-------------------------|-------|
| Low (linear) | 50 | 45-50 | ~1.0x - 1.1x |
| Moderate (branch-and-merge) | 300 | 80-120 | ~2.5x - 3.75x |
| High (parallel paths) | 800 | 150-250 | ~3.2x - 5.3x |
| Very High (exponential) | 1500+ | 200-400 | ~3.75x - 7.5x |

**Insight:** A medium-scope game (300 total sections, moderate branching) provides ~90 sections per playthrough, or ~11,250 words read (at 125 words/section). At 250 words/minute, that's ~45 minutes reading + decision time ≈ **~1 hour playtime**.

This ratio helps calculate **replayability factor** = Total sections / Sections per playthrough.

---

## Word Count Guidelines by Section Type

Different section types have different length expectations:

| Section Type | Word Count | Purpose | Example |
|--------------|-----------|---------|---------|
| **Opening Hook** | 150-250 | Establish tone, setting, protagonist. Draw reader in. | "You wake in a rain-soaked alley, the neon signs overhead buzzing like angry wasps. Your head throbs. The last thing you remember is..." |
| **Standard Narrative** | 100-150 | Advance plot, present situation, offer meaningful choice. | "The bartender eyes you suspiciously. You could press him for information, but he looks like the type who values loyalty over truth. Or you could slip him a twenty and see if that loosens his tongue." |
| **Descriptive / Lore** | 150-250 | World-building, atmosphere, character development. | "The Archives stretch before you, shelf after dusty shelf of forgotten histories. The air smells of old paper and broken promises. Somewhere in here is the answer to who really killed Mayor Grimwald..." |
| **Action Sequence** | 75-125 | Fast pacing, tension, immediate consequence. | "You run. Behind you, footsteps echo—fast, closing. Left or right? The alley splits. No time to think." |
| **Fail State** | 25-75 | Quick resolution, clear consequence, invitation to retry. | "The blade finds its mark. As darkness closes in, you realize you should have trusted the stranger. THE END. [Restart from checkpoint?]" |
| **Success / Reward** | 100-150 | Acknowledge player's smart choice, advance plot. | "Your hunch paid off. The bartender's eyes widen as you mention the name 'Vallejo.' He nods slowly, slides a folded note across the bar. 'Be careful,' he whispers. 'They're watching.'" |
| **Hub / Menu** | 50-100 | Functional re-orientation, present options without repetition. | "You're back at the precinct. Where do you want to focus your investigation next? [Review evidence] [Interview witnesses] [Follow the money trail]" |

---

## Pacing Best Practices

### Rhythm and Flow

**Vary section length** to create rhythm:
- Long → Short → Medium → Short → Long creates dynamic pacing
- All sections at 125 words feels monotonous
- Mix lore/description (longer) with action/decision (shorter)

**Front-load engagement:**
- First 3-5 sections should be engaging and fast-paced
- Hook reader before settling into world-building
- Early meaningful choice (section 3-5) increases investment

**Checkpoint pacing:**
- Major decision points every 8-12 sections
- Gives natural "save point" feeling
- Prevents decision fatigue from too-frequent branching

### Choice Meaningfulness

**Immediate vs. delayed consequences:**
- **Immediate:** Next section shows direct result (satisfying agency)
- **Delayed:** Variable set now, consequence appears 20+ sections later (depth)
- Best practice: Mix both. Some choices have instant gratification, others build toward major reveals.

**Telegraph consequences:**
- Foreshadow risk: "This seems dangerous..." prepares player for fail state
- Reward observation: Clues earlier should pay off in later choices
- Avoid "gotcha" deaths where player had no way to know

**False choices vs. real branches:**
- **False choice:** Both options lead to same next section (flavor only)
- **Real branch:** Options lead to different content (structural)
- Best practice: Most choices should be real branches. Use false choices sparingly for dialogue flavor.

---

## Target Audience Considerations

Different audiences have different expectations:

| Audience | Typical Length Preference | Pacing Preference | Notes |
|----------|-------------------------|------------------|-------|
| **Casual / Mobile** | Short to Medium (50-300 sections) | Fast, frequent choices | Short sections (75-100 words), mobile-friendly, can be completed in one session |
| **CYOA Enthusiasts** | Medium to Long (250-800 sections) | Moderate, strategic choices | Expect replayability, hidden paths, achievement hunting |
| **Literary IF Fans** | Medium to Long (200-1000+ sections) | Slower, prose-focused | Appreciate longer sections (150-250 words), literary style, fewer choices |
| **RPG Gamers** | Long to Epic (500-1500+ sections) | Varied, system-driven | Expect stat tracking, combat, inventory, character customization |
| **Horror Fans** | Short to Medium (50-400 sections) | Fast, tense | Short sections, frequent bad endings, atmospheric description |

---

## Common Pitfalls to Avoid

### Exponential Branching

**Problem:** "I want every choice to matter, so each choice splits into 3 new paths..."

**Result:** 3^10 = 59,049 sections. Impossible to write.

**Solution:** Use branch-and-merge. Diverge for 3-5 sections, then merge at plot points.

### Choice Overload

**Problem:** Presenting 6-8 choices per section for "maximum agency"

**Result:** Decision fatigue, analysis paralysis, unclear priorities

**Solution:** Stick to 3 choices. If you need more options, use hub-and-spoke pattern (return to hub after each investigation).

### "Fake" Choices

**Problem:** All choices lead to same outcome, player agency is illusion

**Result:** Player feels cheated, replayability is nil

**Solution:** At minimum, vary flavor text. Ideally, choices should branch for 2-3 sections before merging.

### Death Spirals

**Problem:** Early bad choice leads to inevitable failure 30 sections later with no warning

**Result:** Player forced to replay large portion, frustration

**Solution:** Telegraph consequences, provide checkpoints, allow recovery paths.

### Unbalanced Paths

**Problem:** Path A has 50 sections of content, Path B has 8 sections and dead ends

**Result:** One path feels "canon," others feel like afterthoughts

**Solution:** Balance content across major branches. If one path must be shorter, make it clearly a "fail fast" path (quick bad ending).

---

## Calculating Your Project Scope

Use this worksheet to estimate scope:

1. **Choose target playtime:** 30min / 1hr / 2hr / 3hr+
2. **Estimate reading speed:** 250 words/minute
3. **Calculate playthrough words:** playtime × reading speed × 0.75 (to account for decision time)
   - Example: 1hr × 250 × 0.75 = ~11,250 words per playthrough
4. **Choose section length:** 125 words average
5. **Calculate playthrough sections:** playthrough words / section length
   - Example: 11,250 / 125 = 90 sections per playthrough
6. **Choose branching complexity:** Low (1.1x) / Moderate (3x) / High (5x)
7. **Calculate total sections:** playthrough sections × complexity ratio
   - Example: 90 × 3 = 270 total sections
8. **Add ~20% buffer** for hub sections, fail states, optional content
   - Example: 270 × 1.2 = 324 total sections

**Result:** For a 1-hour, medium-complexity gamebook, target ~300-350 sections at ~125 words each = **~40,000 total words** across all paths.

---

## References & Further Reading

**Classic Gamebook Analysis:**
- *Ultimate Ending* (2011) by various - Analysis of CYOA series structure
- Demian Katz's "Zarfian Theory" essays on IF structure patterns
- Emily Short's blog posts on choice architecture

**Modern Digital IF:**
- *80 Days* (inkle, 2014) - 750,000 words, exemplar of branch-and-merge at scale
- *Choice of Games* catalog - Consistent ~200k-400k word counts, stat-based branching
- *Twine* community best practices documentation

**Structural Patterns:**
- Sam Kabo Ashwell's "Standard Patterns in Choice-Based Games" (2015)
- Failbetter Games' blog on StoryNexus structure (salience, hub-and-spoke)

---

**Last Updated:** 2025-11-05

**Note:** These metrics are based on analysis of published works and should be treated as guidelines, not rules. Innovation often comes from breaking conventions thoughtfully.
