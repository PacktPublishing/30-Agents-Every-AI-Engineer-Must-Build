# src/synthetic_data.py
# Author: Imran Ahmad
# Book: 30 Agents Every AI Engineer Must Build, Chapter 12
# Ref: Strategy §4.1 (HR Dataset), §4.2 (Medical Dataset)
# Description: Deterministic synthetic dataset generators for the HR fairness
#              case study and the medical diagnosis explainability case study.

import random
from typing import Any

from chapter12.utils import ColorLogger

logger = ColorLogger("SyntheticData")


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

SKILL_POOL = [
    "python", "java", "sql", "machine_learning", "deep_learning",
    "data_analysis", "cloud_computing", "aws", "docker", "kubernetes",
    "react", "node_js", "tensorflow", "pytorch", "nlp",
    "computer_vision", "statistics", "project_management", "agile", "communication",
]

INSTITUTION_POOL = [
    # Tier 1 (high prestige)
    "MIT", "Stanford University", "Carnegie Mellon", "UC Berkeley",
    "Harvard University", "Caltech", "Oxford University", "ETH Zurich",
    "University of Cambridge", "Princeton University",
    # Tier 2 (mid prestige)
    "University of Michigan", "Georgia Tech", "University of Toronto",
    "University of Washington", "UT Austin", "NYU", "UCLA",
    "University of Illinois", "Penn State", "University of Maryland",
    # Tier 3 (regional / community)
    "State College of Technology", "Metro Community College",
    "Regional Technical University", "City University",
    "Community College of Arts", "Westfield State University",
    "Northern State College", "Lakeside Community College",
    "Prairie View University", "Valley Technical Institute",
]

SYMPTOM_POOL = [
    "productive cough", "dry cough", "fever", "chills",
    "shortness of breath", "chest pain", "fatigue", "headache",
    "muscle aches", "sore throat", "runny nose", "nausea",
    "wheezing", "rapid breathing", "night sweats",
]

HISTORY_POOL = ["COPD", "CHF", "diabetes", "hypertension", "asthma"]


# ---------------------------------------------------------------------------
# §4.1  HR Dataset Generator
# Ref: Bias detection and mitigation (p.14–19),
#      FairHiringAgent case study (p.20–23)
# ---------------------------------------------------------------------------

def generate_hr_dataset(n: int = 200, seed: int = 42) -> list[dict[str, Any]]:
    """
    Generate a synthetic HR dataset with injected gender bias.

    The dataset models the scenario from the FairHiringAgent case study
    (p.20–23), inspired by the Amazon AI recruiting failure (p.15, p.20).

    Bias injection (Strategy §4.1):
        score -= 0.05 for gender == 'female'
    This produces a disparate impact ratio of approximately 0.73,
    below the four-fifths rule threshold (0.80) from p.16/p.22.

    Parameters
    ----------
    n : int
        Number of candidate records to generate (default: 200).
    seed : int
        Random seed for reproducibility (default: 42).

    Returns
    -------
    list[dict]
        List of candidate records with fields per Strategy §4.1.
    """
    rng = random.Random(seed)
    dataset = []

    for i in range(n):
        candidate_id = f"C-{i:04d}"

        # Demographics — imbalanced to mirror Amazon scenario (p.15, p.20)
        gender = rng.choices(
            ["male", "female", "non_binary"],
            weights=[0.55, 0.40, 0.05],
            k=1,
        )[0]
        ethnicity = rng.choices(
            ["group_A", "group_B", "group_C", "group_D"],
            weights=[0.50, 0.25, 0.15, 0.10],
            k=1,
        )[0]

        # Qualifications
        num_skills = rng.randint(3, 8)
        skills = rng.sample(SKILL_POOL, num_skills)
        years_experience = rng.randint(1, 20)
        education_level = rng.choices(
            ["bachelors", "masters", "phd"],
            weights=[0.50, 0.35, 0.15],
            k=1,
        )[0]
        education_institution = rng.choice(INSTITUTION_POOL)

        # --- Deterministic scoring ---
        # The MockLLM._mock_resume_scoring formula (p.20–21) uses matched
        # skills against job requirements:
        #     score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(exp, 10)
        # For batch generation, we simulate partial matches (typically 1–3
        # of a candidate's skills match a 5-skill job posting) so that the
        # score distribution centers near the 0.65 qualification threshold.
        # This ensures the bias injection creates a visible DI gap.
        simulated_matches = rng.randint(1, min(num_skills, 4))
        skill_contribution = 0.1 * min(simulated_matches, 5)
        exp_contribution = 0.02 * min(years_experience, 10)
        raw_score = 0.3 + skill_contribution + exp_contribution

        # Add noise to spread the distribution around the threshold
        raw_score += rng.gauss(0, 0.06)

        # --- Bias injection (Strategy §4.1) ---
        # Penalize female candidates to produce DI ≈ 0.73 (p.22)
        if gender == "female":
            raw_score -= 0.055

        raw_score = round(max(0.0, min(1.0, raw_score)), 4)

        # Qualification threshold (p.22)
        qualified = raw_score >= 0.65

        dataset.append({
            "candidate_id": candidate_id,
            "skills": skills,
            "years_experience": years_experience,
            "education_level": education_level,
            "education_institution": education_institution,
            "gender": gender,
            "ethnicity": ethnicity,
            "raw_score": raw_score,
            "qualified": qualified,
        })

    logger.info(
        f"Generated HR dataset: {n} candidates (seed={seed}). "
        f"Bias injected for fairness demonstration."
    )
    return dataset


# ---------------------------------------------------------------------------
# §4.2  Medical Dataset Generator
# Ref: DiagnosticAssistant case study (p.30–35),
#      Edge computing for privacy (p.31–32)
# ---------------------------------------------------------------------------

def generate_medical_dataset(n: int = 50, seed: int = 42) -> list[dict[str, Any]]:
    """
    Generate a synthetic medical dataset for the DiagnosticAssistant.

    All patient IDs are de-identified tokens (p.31–32). Vitals represent
    aggregated features from the edge processing layer, not raw sensor data.

    Parameters
    ----------
    n : int
        Number of patient records to generate (default: 50).
    seed : int
        Random seed for reproducibility (default: 42).

    Returns
    -------
    list[dict]
        List of patient records with fields per Strategy §4.2.
    """
    rng = random.Random(seed)
    dataset = []

    for i in range(n):
        patient_id = f"P-{i:04d}"

        # Vitals — aggregated features (p.32)
        heart_rate_avg = round(rng.gauss(75, 12), 1)
        spo2_min = round(max(85.0, min(100.0, rng.gauss(96, 3))), 1)
        wbc_count = round(max(2.0, min(25.0, rng.gauss(7.5, 2.5))), 1)
        temperature = round(rng.gauss(37.0, 0.8), 1)

        # Symptoms — 2 to 4 from pool (p.33)
        num_symptoms = rng.randint(2, 4)
        reported_symptoms = rng.sample(SYMPTOM_POOL, num_symptoms)

        # Chest imaging (p.34)
        chest_imaging = rng.choices(
            ["clear", "right_lower_consolidation", "bilateral_infiltrates", "normal"],
            weights=[0.25, 0.35, 0.25, 0.15],
            k=1,
        )[0]

        # True diagnosis (p.34)
        true_diagnosis = rng.choices(
            ["pneumonia", "bronchitis", "atelectasis", "pulmonary_embolism"],
            weights=[0.50, 0.25, 0.15, 0.10],
            k=1,
        )[0]

        # Patient history — 0 to 3 conditions (p.31)
        num_history = rng.randint(0, 3)
        patient_history = rng.sample(HISTORY_POOL, min(num_history, len(HISTORY_POOL)))

        dataset.append({
            "patient_id": patient_id,
            "heart_rate_avg": heart_rate_avg,
            "spo2_min": spo2_min,
            "wbc_count": wbc_count,
            "temperature": temperature,
            "reported_symptoms": reported_symptoms,
            "chest_imaging": chest_imaging,
            "true_diagnosis": true_diagnosis,
            "patient_history": patient_history,
        })

    logger.info(
        f"Generated medical dataset: {n} patients (seed={seed}). "
        f"All IDs de-identified per HIPAA/GDPR requirements."
    )
    return dataset


# ---------------------------------------------------------------------------
# Dataset summary utilities
# ---------------------------------------------------------------------------

def summarize_hr_dataset(dataset: list[dict]) -> dict:
    """Compute summary statistics for the HR dataset."""
    total = len(dataset)
    gender_counts = {}
    gender_qualified = {}
    for rec in dataset:
        g = rec["gender"]
        gender_counts[g] = gender_counts.get(g, 0) + 1
        if rec["qualified"]:
            gender_qualified[g] = gender_qualified.get(g, 0) + 1

    qualification_rates = {
        g: round(gender_qualified.get(g, 0) / gender_counts[g], 4)
        for g in gender_counts
    }

    # Disparate impact ratio (p.16, p.22): female rate / male rate
    # This mirrors the chapter's Amazon HR scenario where gender is the
    # protected attribute and the four-fifths rule applies.
    female_rate = qualification_rates.get("female", 0.0)
    male_rate = qualification_rates.get("male", 1.0)
    di_ratio = round(female_rate / male_rate, 4) if male_rate > 0 else 0.0

    return {
        "total_candidates": total,
        "gender_distribution": gender_counts,
        "qualification_rates_by_gender": qualification_rates,
        "disparate_impact_ratio": di_ratio,
        "four_fifths_compliant": di_ratio >= 0.80,
    }


def summarize_medical_dataset(dataset: list[dict]) -> dict:
    """Compute summary statistics for the medical dataset."""
    total = len(dataset)
    diagnosis_counts = {}
    for rec in dataset:
        d = rec["true_diagnosis"]
        diagnosis_counts[d] = diagnosis_counts.get(d, 0) + 1

    return {
        "total_patients": total,
        "diagnosis_distribution": diagnosis_counts,
        "avg_heart_rate": round(sum(r["heart_rate_avg"] for r in dataset) / total, 1),
        "avg_spo2": round(sum(r["spo2_min"] for r in dataset) / total, 1),
        "avg_wbc": round(sum(r["wbc_count"] for r in dataset) / total, 1),
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    hr = generate_hr_dataset()
    hr_summary = summarize_hr_dataset(hr)
    print("HR Summary:", hr_summary)
    print(f"  DI Ratio: {hr_summary['disparate_impact_ratio']} "
          f"({'PASS' if hr_summary['four_fifths_compliant'] else 'FAIL — bias detected'})")

    med = generate_medical_dataset()
    med_summary = summarize_medical_dataset(med)
    print("\nMedical Summary:", med_summary)

    logger.success("Synthetic data self-test complete.")
