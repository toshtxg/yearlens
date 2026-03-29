# **📄 Build-Ready PRD Addendum**

## **Product: YearLens**

## **Goal: Give a coding model enough precision to implement the app correctly**

---

## **1\. Product Goal**

Build a personal yearly fortune app that:

* takes user birth data and target year  
* computes astrology-based yearly periods  
* explains each period in plain English  
* covers all major life areas  
* supports **toggleable output depth**  
* is cheap to run  
* is easy to build using familiar tools

The product should be designed so that:

* the **core logic works without any LLM**  
* the **LLM is optional and inserted through placeholders**  
* infrastructure can start simple and evolve later

---

## **2\. Final User Inputs**

These should be the primary required fields in the app UI:

{  
 "birth\_date": "YYYY-MM-DD",  
 "birth\_time": "HH:MM",  
 "birth\_location": "City, Country",  
 "target\_year": 2026  
}

Optional fields:

{  
 "name": "Optional display name",  
 "year\_anchor": "birthday",  
 "preferences": {  
   "zodiac": "sidereal",  
   "ayanamsa": "lahiri",  
   "house\_system": "whole\_sign",  
   "node\_type": "true"  
 }  
}

### **Input requirements**

#### **Required**

* birth date  
* birth time  
* birth location  
* target year

#### **Optional**

* name  
* configuration preferences

### **Why birth time and location are required**

Because the app must explain:

* which house a planet is in  
* where Rahu/Ketu is  
* what that house means

Without time and place, house-based logic becomes weak or wrong.

---

## **3\. Final Output Requirements**

The app must return:

* a **year overview**  
* a list of **periods**  
* a **toggle** between concise and detailed modes

### **Concise mode**

Used for fast scanning.

Example:

* Mar 16 – Apr 22  
* Tone: Stressful  
* Key risks: networking, politics, emotional conflict  
* Advice: keep low profile, avoid joint ventures

### **Detailed mode**

Used for explanation and learning.

Example:

* Mars is activating your 5th house  
* Mars represents drive, aggression, urgency  
* The 5th house relates to emotions, self-expression, creativity, risk-taking  
* This can create emotional friction, impatience, and poor judgment in social situations

### **Output schema**

{  
 "year\_overview": {  
   "summary": "A slow but constructive year with stronger momentum after birthday.",  
   "top\_themes": \[  
     "Career pressure but growth through discipline",  
     "Networking periods require caution",  
     "Money decisions should be deliberate"  
   \],  
   "confidence": 0.84  
 },  
 "periods": \[  
   {  
     "id": "p1",  
     "start\_date": "2026-03-16",  
     "end\_date": "2026-04-22",  
     "tone": "stressful",  
     "domains": {  
       "career\_work": 6,  
       "money\_finance": 4,  
       "relationships": 3,  
       "health\_emotional": 4,  
       "travel\_overseas": 5,  
       "study\_growth": 5  
     },  
     "advice": \[  
       "Keep a low profile",  
       "Avoid unnecessary conflict",  
       "Be careful in networking"  
     \],  
     "drivers": \[  
       {  
         "planet": "Mars",  
         "house": 5,  
         "planet\_meaning": "aggression, urgency, conflict",  
         "house\_meaning": "expression, emotions, creativity, risk",  
         "combined\_effect": "impulsive reactions and emotional friction"  
       }  
     \],  
     "concise\_text": "A tense social and emotional period. Avoid conflict and manage impulse.",  
     "detailed\_text": "Mars in the 5th house can heighten emotional reactivity and impulsive expression. This may create misunderstandings in social or networking situations.",  
     "confidence": 0.81  
   }  
 \]  
}  
---

## **4\. Core Product Behavior**

The system must perform these steps:

### **Step 1: Collect user data**

* birth date  
* birth time  
* birth location  
* target year

### **Step 2: Compute natal chart**

* sidereal zodiac  
* whole sign houses  
* planets  
* Rahu/Ketu  
* ascendant

### **Step 3: Compute yearly transit events**

* planet sign changes  
* house changes relative to natal chart  
* retrogrades  
* eclipses  
* major nodal effects  
* optionally dasha periods later

### **Step 4: Generate time periods**

* combine event boundaries into meaningful periods  
* target approximately 8 to 18 periods for the year

### **Step 5: Score all life domains**

Each period must score:

* career/work  
* money/finance  
* relationships  
* health/emotional  
* travel/overseas  
* study/growth

### **Step 6: Explain why**

Each period must include:

* active planets  
* houses involved  
* meanings of planets  
* meanings of houses  
* combined interpretation

### **Step 7: Render output in two modes**

* concise  
* detailed

---

## **5\. Infrastructure Recommendation**

You asked what is best given your familiarity with:

* GitHub  
* Supabase  
* Streamlit

That is actually enough for a very solid MVP.

## **Best MVP architecture**

### **Recommended stack**

* **Frontend:** Streamlit  
* **Backend logic:** Python inside the same Streamlit app at first  
* **Database:** Supabase Postgres  
* **Auth:** Supabase Auth, optional for V1  
* **Source control:** GitHub  
* **Deployment:** Streamlit Community Cloud for prototype, or Render/Railway later  
* **Astrology engine:** Python library wrapping Swiss Ephemeris  
* **LLM:** optional, behind a feature flag

This is the cheapest and easiest path.

---

## **6\. Architecture Options**

## **Option A — Simplest MVP**

### **Streamlit monolith**

Everything runs in one Python app:

* form input  
* astrology calculation  
* interpretation engine  
* period generation  
* display

### **Pros**

* fastest to build  
* cheapest  
* easiest for your coding model  
* fewer moving parts

### **Cons**

* less scalable  
* backend and UI tightly coupled

### **Use this if**

You want the quickest working prototype.

---

## **Option B — Better long-term setup**

### **Streamlit frontend \+ Python API \+ Supabase**

Components:

* Streamlit for UI  
* FastAPI backend for computation  
* Supabase for storage  
* optional background jobs later

### **Pros**

* cleaner separation  
* easier to scale  
* easier to swap UI later

### **Cons**

* more setup  
* slightly more complexity

### **Use this if**

You want an MVP that can grow into a real product.

---

## **My recommendation**

Start with:

### **Phase 1**

**Streamlit \+ Python services \+ optional Supabase**

* Streamlit for UI  
* internal Python modules for business logic  
* local JSON or SQLite initially if needed  
* add Supabase once you want persistence

### **Phase 2**

Split out a FastAPI backend only when needed.

That keeps the initial build simple for a coding model.

---

## **7\. Proposed System Modules**

Your coding model should build these as separate modules even if they live in one repo.

## **Module 1: `input_schema`**

Validates user input.

Responsibilities:

* validate date format  
* validate time format  
* validate target year  
* normalize place name

Example output:

class UserInput(BaseModel):  
   birth\_date: str  
   birth\_time: str  
   birth\_location: str  
   target\_year: int  
   name: str | None \= None  
   year\_anchor: str \= "birthday"  
---

## **Module 2: `astro_engine`**

Handles astrology computation.

Responsibilities:

* natal chart generation  
* house calculation  
* transit calculation  
* Rahu/Ketu positions  
* yearly event extraction

Output:

* structured astronomy/astrology facts only  
* no prose

---

## **Module 3: `period_engine`**

Turns event boundaries into periods.

Responsibilities:

* merge nearby events  
* enforce minimum and maximum period lengths  
* create final timeline periods

Config:

* min 10 days  
* max 60 days  
* target 8–18 periods

---

## **Module 4: `meaning_engine`**

Maps facts to meaning.

Responsibilities:

* interpret planet in house  
* interpret transit impacts  
* score life domains  
* attach advice tags  
* generate structured explanation objects

This should be rule-based.

---

## **Module 5: `narrative_engine`**

Responsible for output text.

Responsibilities:

* generate concise mode text  
* generate detailed mode text  
* optionally call LLM

This is where your **LLM placeholders** live.

---

## **Module 6: `storage`**

Handles saving and loading reports.

Responsibilities:

* save user input  
* save generated reports  
* save config versions  
* save cached outputs

Supabase is a good fit here.

---

## **8\. LLM Placeholder Design**

This is important. Your system should be designed so that LLM is optional and replaceable.

## **Rule**

The LLM must never be the source of truth for:

* chart math  
* houses  
* transit dates  
* period boundaries  
* raw scoring

The LLM may be used for:

* polishing English  
* expanding explanations  
* personalizing tone  
* converting structured data into more human-readable narrative

## **Placeholder interface**

Your coding model should implement something like:

class NarrativeProvider(Protocol):  
   def generate\_concise(self, period\_data: dict) \-\> str: ...  
   def generate\_detailed(self, period\_data: dict) \-\> str: ...

Then provide two implementations:

### **1\. `TemplateNarrativeProvider`**

* no API cost  
* fully deterministic

### **2\. `LLMNarrativeProvider`**

* calls OpenAI / Anthropic / other model  
* optional  
* behind environment variable or feature flag

This is the cleanest way to future-proof the app.

---

## **9\. Cheapest Deployment Plan**

## **Prototype**

* GitHub repo  
* Streamlit app  
* local Python modules  
* no database required initially  
* deploy on Streamlit Community Cloud

This can be nearly free.

## **MVP with saved reports**

* add Supabase  
* store users and generated reports  
* deploy Streamlit frontend  
* keep compute in app process

Still cheap.

## **Later**

* move heavy compute into FastAPI on Render/Railway/Fly.io  
* Streamlit becomes client UI only

---

## **10\. Recommended Free / Low-Cost Tools**

Given your familiarity, here is the best shortlist.

### **Best immediate choices**

* **GitHub** for repo and versioning  
* **Streamlit** for app UI  
* **Supabase** for storage and auth  
* **Python** for all core logic

### **Other useful free-ish options**

* **Render** for hosting Python APIs  
* **Railway** for quick deployments  
* **SQLite** for early local prototyping  
* **Pydantic** for schema validation  
* **FastAPI** if you split backend later

### **Not necessary yet**

* Kubernetes  
* message queues  
* microservices  
* vector DB  
* OCR pipelines  
* complex agents

You do not need any of that for V1.

---

## **11\. Suggested Repo Structure**

This is the kind of structure your coding model should generate:

yearlens/  
├── app/  
│   ├── main.py  
│   ├── ui/  
│   │   ├── form.py  
│   │   ├── timeline.py  
│   │   └── report.py  
│   ├── core/  
│   │   ├── input\_schema.py  
│   │   ├── astro\_engine.py  
│   │   ├── period\_engine.py  
│   │   ├── meaning\_engine.py  
│   │   ├── narrative\_engine.py  
│   │   └── config.py  
│   ├── providers/  
│   │   ├── template\_narrative.py  
│   │   └── llm\_narrative.py  
│   ├── storage/  
│   │   ├── supabase\_client.py  
│   │   └── report\_repository.py  
│   └── tests/  
│       ├── test\_input\_schema.py  
│       ├── test\_period\_engine.py  
│       └── test\_meaning\_engine.py  
├── requirements.txt  
├── .env.example  
└── README.md

This structure is very coding-model-friendly.

---

## **12\. Suggested Database Tables**

If you use Supabase, keep it simple.

## **`profiles`**

id uuid primary key  
created\_at timestamp  
display\_name text

## **`birth_profiles`**

id uuid primary key  
profile\_id uuid references profiles(id)  
birth\_date date  
birth\_time text  
birth\_location text  
year\_anchor text default 'birthday'  
preferences jsonb  
created\_at timestamp

## **`reports`**

id uuid primary key  
profile\_id uuid references profiles(id)  
target\_year int  
input\_snapshot jsonb  
report\_json jsonb  
created\_at timestamp

## **`llm_generations` optional**

id uuid primary key  
report\_id uuid references reports(id)  
provider text  
mode text  
prompt\_version text  
output\_text text  
created\_at timestamp

This lets you cache and audit generated outputs.

---

## **13\. UI Requirements**

The UI should be simple and centered on clarity.

## **Screen 1: Input form**

Fields:

* birth date  
* birth time  
* birth location  
* target year  
* toggle advanced settings

Button:

* Generate Reading

## **Screen 2: Year overview**

Shows:

* overall year summary  
* main themes  
* top caution periods  
* top opportunity periods

## **Screen 3: Period timeline**

Each period card shows:

* date range  
* tone  
* major domain impacts  
* concise or detailed view toggle

## **Screen 4: Expanded period detail**

Shows:

* planet-by-planet explanation  
* house meanings  
* advice  
* confidence

---

## **14\. Toggle Requirements**

The app must support a visible toggle:

### **Toggle values**

* concise  
* detailed

### **Concise mode rules**

* 1 short summary paragraph  
* 3 max advice bullets  
* compact domain summary

### **Detailed mode rules**

* full explanation  
* planet meaning  
* house meaning  
* combined effect  
* deeper reasoning

### **Engineering rule**

Both modes should come from the same structured period object.  
Do not compute two separate forecasts.

---

## **15\. Core Rule System Requirements**

The coding model must build a rules dictionary or rules config that maps:

* planet → meaning  
* house → meaning  
* planet in house → combined meaning  
* transit type → intensity modifier  
* Rahu/Ketu → special effects  
* domain mapping → which life areas get impacted

Example:

PLANET\_MEANINGS \= {  
   "Mars": \["drive", "conflict", "urgency"\],  
   "Jupiter": \["growth", "wisdom", "expansion"\],  
   "Saturn": \["restriction", "delay", "discipline"\],  
   "Rahu": \["instability", "ambition", "obsession", "confusion"\]  
}  
HOUSE\_MEANINGS \= {  
   2: \["money", "speech", "family resources"\],  
   5: \["creativity", "expression", "romance", "risk"\],  
   6: \["work", "obstacles", "stress", "discipline"\],  
   11: \["networks", "gains", "social circles"\]  
}

The LLM should never replace this layer.

---

## **16\. Recommended Implementation Order**

This is the order your coding model should build in.

### **Milestone 1**

* input form  
* schema validation  
* hardcoded mock report rendering

### **Milestone 2**

* astrology computation module  
* natal chart \+ basic transits  
* raw JSON output

### **Milestone 3**

* period engine  
* build yearly periods

### **Milestone 4**

* rule-based meaning engine  
* domain scoring  
* advice generation

### **Milestone 5**

* concise/detailed toggle  
* template narrative generator

### **Milestone 6**

* Supabase persistence

### **Milestone 7**

* optional LLM narrative provider

That order minimizes risk.

---

## **17\. Best Practical Recommendation**

Given what you know already, I would tell your coding model to build:

### **V1 stack**

* Python  
* Streamlit  
* Swiss Ephemeris-compatible Python library  
* Pydantic  
* template-based narratives  
* optional Supabase persistence

### **V1.5**

* FastAPI extraction if code gets messy  
* LLM narrative placeholder activated  
* saved reports

This is much easier than starting with a fancy multi-service architecture.

---

## **18\. Exact Product Philosophy for the Build**

The code model should follow these rules:

1. All astrological calculations must be deterministic.  
2. All interpretations must be based on explicit rule mappings.  
3. Every period must include an explanation layer.  
4. All life domains must be scored every period.  
5. Output must support concise and detailed toggles.  
6. LLM usage must be optional, pluggable, and non-essential.  
7. Infrastructure must be simple enough for a solo builder.

---

## **19\. What to tell your coding model**

You can give it instructions like this:

Build a Python Streamlit app called YearLens.  
The app collects birth date, birth time, birth location, and target year.  
It computes a sidereal natal chart with whole sign houses, computes yearly transit change points, converts them into 8–18 periods, scores all major life domains, and renders a period-by-period report.  
Each period must include concise and detailed text modes driven from the same structured explanation object.  
The architecture must include a pluggable narrative provider interface with a template implementation and an LLM placeholder implementation.  
Use modular Python files for input schema, astrology engine, period engine, meaning engine, narrative engine, and storage.  
Keep the core app functional without any LLM dependency.

That is the kind of implementation prompt that usually works well.

---

## **20\. Final recommendation**

For your case, the best path is:

**GitHub \+ Streamlit \+ Python modular app \+ optional Supabase \+ LLM placeholders**

That gives you:

* low cost  
* low complexity  
* fast prototype speed  
* enough structure for a coding model to execute well

