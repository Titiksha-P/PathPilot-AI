/**
 * Guidance Engine API Service
 * Handles communication with Python server.py backend, with fallback for offline mode.
 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Submit student profile (or preset name) for adaptive guidance analysis
 */
export async function submitProfile(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/guidance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status} error`);
    }

    return await response.json();
  } catch (err) {
    console.warn("Backend API unreachable, using client fallback demo server:", err.message);
    return getOfflineFallback(payload);
  }
}

/**
 * Fetch sample preset personas
 */
export async function fetchSamplePersonas() {
  try {
    const response = await fetch(`${API_BASE_URL}/sample-personas`);
    if (response.ok) {
      return await response.json();
    }
  } catch (err) {
    console.warn("Sample personas fallback active");
  }

  return {
    class10: { name: "Aarav Sharma", stage: "class10", marks: { mathematics: 92, science: 88, english: 78 } },
    class12: { name: "Priya Verma", stage: "class12", stream: "science pcb", marks: { overall: 86, biology: 91, chemistry: 84 } },
    aryan: { name: "Aryan Shelar", stage: "college", skills: [{ name: "Python", level: "advanced", evidence: "Built ADK orchestrator" }] }
  };
}

/**
 * Offline Fallback calculation generator if backend API is not running
 */
function getOfflineFallback(payload) {
  const profile = payload.profile || {
    name: payload.preset ? payload.preset.toUpperCase() : "Student",
    stage: payload.stage || "class10",
    marks: { mathematics: 88, science: 85 }
  };

  const isClass10 = profile.stage === 'class10';
  const isClass12 = profile.stage === 'class12';

  const matches = isClass10 ? [
    {
      pathway_id: "science_pcm",
      pathway_type: "stream",
      title: "Science (PCM)",
      rank_role: "best_fit",
      score: 92,
      reasons: ["Strong performance in Mathematics and Science", "High analytical problem-solving fit"],
      evidence: ["Mathematics: 88%", "Science: 85%"],
      matched_attributes: ["Mathematics", "Science", "Technology"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Meets Class 10 subject thresholds"],
      missing_requirements: [],
      risks_tradeoffs: ["High mathematical workload", "Competitive entrance preparation required"],
      estimated_duration: "2 years (Classes 11–12)",
      cost_category: "medium",
      next_actions: ["Review Class 11 Math prerequisites", "Try a basic coding or electronics mini-project"],
      related_outcomes: ["B.Tech / BE", "B.Sc Computer Science"]
    },
    {
      pathway_id: "commerce_math",
      pathway_type: "stream",
      title: "Commerce with Mathematics",
      rank_role: "strong_alternative",
      score: 84,
      reasons: ["Solid quantitative foundation", "Fits analytical & business interest profile"],
      evidence: ["Mathematics: 88%"],
      matched_attributes: ["Mathematics", "Analytics"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Meets commerce entry thresholds"],
      missing_requirements: [],
      risks_tradeoffs: ["CA/CS exams require dedicated multi-year prep"],
      estimated_duration: "2 years (Classes 11–12)",
      cost_category: "low-medium",
      next_actions: ["Try a budgeting or business case activity", "Explore CA & Finance options"],
      related_outcomes: ["B.Com", "BBA", "CA / Financial Analyst"]
    },
    {
      pathway_id: "polytechnic_vocational",
      pathway_type: "stream",
      title: "Polytechnic / Vocational Technology",
      rank_role: "safe_backup",
      score: 76,
      reasons: ["Hands-on technical orientation", "Affordable direct path to practical skills"],
      evidence: ["Science: 85%"],
      matched_attributes: ["Hands-on", "Technology"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Meets vocational admission rules"],
      missing_requirements: [],
      risks_tradeoffs: ["Early specialisation may require lateral entry for degree"],
      estimated_duration: "3 years diploma",
      cost_category: "low",
      next_actions: ["Visit local technical institute", "Compare diploma specialisations"],
      related_outcomes: ["Diploma Engineering", "Technical Specialist"]
    }
  ] : isClass12 ? [
    {
      pathway_id: "btech_cs",
      pathway_type: "course",
      title: "B.Tech Computer Science & Engineering",
      rank_role: "best_fit",
      score: 90,
      reasons: ["Strong PCM foundation", "High interest in technology & software"],
      evidence: ["Overall: 88%", "Mathematics: 90%"],
      matched_attributes: ["Coding", "Problem Solving"],
      eligibility_status: "conditionally_eligible",
      eligibility_reasons: ["Academic marks meet cutoffs; entrance exam score required"],
      missing_requirements: ["Prepare for entrance exam: JEE Main / MHT-CET"],
      risks_tradeoffs: ["Demanding academic curriculum", "Competitive admissions"],
      estimated_duration: "4 years",
      cost_category: "medium",
      next_actions: ["Register for entrance exams", "Start foundational programming in Python"],
      related_outcomes: ["Software Engineer", "AI/ML Engineer"]
    },
    {
      pathway_id: "bsc_data_science",
      pathway_type: "course",
      title: "B.Sc. Data Science & Analytics",
      rank_role: "strong_alternative",
      score: 83,
      reasons: ["Strong quantitative & statistical affinity"],
      evidence: ["Mathematics: 90%"],
      matched_attributes: ["Data Analysis", "Mathematics"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Meets all degree prerequisites"],
      missing_requirements: [],
      risks_tradeoffs: ["Requires continuous self-learning in tools & SQL"],
      estimated_duration: "3–4 years",
      cost_category: "medium",
      next_actions: ["Explore Python data analysis libraries"],
      related_outcomes: ["Data Analyst", "Business Intelligence Specialist"]
    },
    {
      pathway_id: "bca",
      pathway_type: "course",
      title: "BCA (Bachelor of Computer Applications)",
      rank_role: "safe_backup",
      score: 78,
      reasons: ["Direct entry software pathway", "Less entrance exam stress"],
      evidence: ["Overall marks meet criteria"],
      matched_attributes: ["Computer Applications"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Satisfies eligibility"],
      missing_requirements: [],
      risks_tradeoffs: ["May need MCA or certifications for top product roles"],
      estimated_duration: "3 years",
      cost_category: "low-medium",
      next_actions: ["Apply to top regional BCA colleges"],
      related_outcomes: ["Web Developer", "System Administrator"]
    }
  ] : [
    {
      pathway_id: "ai_agent_engineer",
      pathway_type: "career",
      title: "AI Agent & Automation Engineer",
      rank_role: "best_fit",
      score: 95,
      reasons: ["Demonstrated skills: LLM integration, Python, ADK", "Portfolio projects demonstrate practical implementation"],
      evidence: ["Project: SIH Career Advisor — Google ADK & Gemini Engine"],
      matched_attributes: ["Python", "LLM", "Google ADK", "API Integration"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Portfolio contains strong verifiable technical signals"],
      missing_requirements: [],
      risks_tradeoffs: ["Rapidly evolving technology stack requires active skill updating"],
      estimated_duration: "Immediate career trajectory",
      cost_category: "low",
      next_actions: ["Deploy live demo to GitHub", "Add API rate limit handling docs"],
      related_outcomes: ["AI Engineer", "Automation Architect"]
    },
    {
      pathway_id: "fullstack_developer",
      pathway_type: "career",
      title: "Full Stack Software Developer",
      rank_role: "strong_alternative",
      score: 87,
      reasons: ["Strong backend Python skills combined with React frontend capability"],
      evidence: ["Skills: Python, JavaScript, React"],
      matched_attributes: ["React", "Python", "REST API"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Relevant projects and tech stack match"],
      missing_requirements: [],
      risks_tradeoffs: ["Needs continuous exposure to modern devops/deployment"],
      estimated_duration: "Immediate placement",
      cost_category: "low",
      next_actions: ["Build end-to-end full stack portfolio showcase"],
      related_outcomes: ["Frontend/Backend Developer", "Full Stack Specialist"]
    },
    {
      pathway_id: "data_analyst",
      pathway_type: "career",
      title: "Data & Business Intelligence Analyst",
      rank_role: "safe_backup",
      score: 79,
      reasons: ["Solid analytical reasoning and structured data processing"],
      evidence: ["Python data handling & Pydantic validation experience"],
      matched_attributes: ["Data Analysis", "Python"],
      eligibility_status: "eligible",
      eligibility_reasons: ["Technical evidence supports entry role"],
      missing_requirements: ["Add SQL database project"],
      risks_tradeoffs: ["Domain knowledge in finance/marketing usually required"],
      estimated_duration: "1–3 months preparation",
      cost_category: "low",
      next_actions: ["Complete a SQL dashboard case study"],
      related_outcomes: ["Data Analyst", "BI Developer"]
    }
  ];

  return {
    profile,
    recommendations: { matches },
    verification: { approved: true, issues: [], final_recommendations: { matches } }
  };
}
