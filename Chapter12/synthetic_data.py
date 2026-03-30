"""
Synthetic data generators for Chapter 12 demonstrations.

Produces deterministic, seeded datasets for the HR (bias detection) and
Medical (explainability) case studies.

Author: Imran Ahmad
Book: 30 Agents Every AI Engineer Must Build, Chapter 12
Section Reference: Synthetic Data Spec (Strategy §4), HR p.14-23, Medical p.30-35
"""

import numpy as np
import pandas as pd
from typing import Optional

from src.utils import ColorLogger, graceful_fallback

logger = ColorLogger(name="SyntheticData")

# ---------------------------------------------------------------------------
# Skill / symptom / institution pools (chapter-derived)
# ---------------------------------------------------------------------------

_TECH_SKILLS = [
    "python", "java", "sql", "machine_learning", "deep_learning",
    "data_analysis", "cloud_computing", "devops", "nlp", "computer_vision",
    "statistics", "react", "node_js", "kubernetes", "terraform",
    "data_engineering", "spark", "tableau", "project_management", "agile",
]

_INSTITUTIONS = [
    "MIT", "Stanford University", "Carnegie Mellon", "UC Berkeley",
    "Georgia Tech", "University of Michigan", "University of Washington",
    "Harvard University", "Princeton University", "Caltech",
    "University of Illinois", "Cornell University", "Columbia University",
    "University of Texas Austin", "UCLA", "NYU", "Duke University",
    "State University A", "State University B", "State University C",
    "Regional College D", "Regional College E", "Community College F",
    "Community College G", "Technical Institute H", "Technical Institute I",
    "Online University J", "Online University K",
    "International University L", "International University M",
]

_SYMPTOMS = [
    "productive cough", "fever", "shortness of breath", "chest pain",
    "fatigue", "headache", "nausea", "chills", "night sweats",
    "wheezing", "dizziness", "dry cough", "muscle ache",
    "sore throat", "weight loss",
]

_PATIENT_HISTORY_ITEMS = ["COPD", "CHF", "diabetes", "hypertension", "asthma"]


# ---------------------------------------------------------------------------
# Section 4.1 — HR Dataset: generate_hr_dataset(n=200, seed=42)
# ---------------------------------------------------------------------------

@graceful_fallback(
    fallback_value=pd.DataFrame(),
    section_ref="Section 12 - HR Dataset Generation (p.14-23)"
)
def generate_hr_dataset(n: int = 200, seed: int = 42) -> pd.DataFrame:
    """
    Generate a synthetic HR / hiring dataset with injected gender bias.

    The raw_score formula (p.20):
        score = 0.3 + 0.1 * min(skill_matches, 5) + 0.02 * min(years_exp, 10)
    Where skill_matches = number of candidate skills matching the job's
    required skills (a subset of their total skills).

    Bias injection (p.22): gender-based penalty for female candidates,
    plus small assessment noise (simulates real interview variance).
    Calibrated to produce a four-fifths violation with disparate impact ~0.73.

    Args:
        n: Number of candidates to generate.
        seed: Random seed for reproducibility.

    Returns:
        pd.DataFrame with columns matching Strategy §4.1.
    """
    rng = np.random.RandomState(seed)
    logger.info(f"Generating HR dataset: n={n}, seed={seed}")

    # Job posting requires these 5 specific skills (used for skill_matches)
    required_skills = {"python", "machine_learning", "sql", "statistics", "cloud_computing"}

    records = []
    for i in range(n):
        # Demographics — weighted distributions per strategy spec
        gender = rng.choice(
            ["male", "female", "non_binary"],
            p=[0.55, 0.40, 0.05],
        )
        ethnicity = rng.choice(
            ["group_a", "group_b", "group_c", "group_d"],
            p=[0.50, 0.25, 0.15, 0.10],
        )
        education_level = rng.choice(
            ["bachelors", "masters", "phd"],
            p=[0.50, 0.35, 0.15],
        )
        education_institution = rng.choice(_INSTITUTIONS)

        # Skills and experience
        num_skills = rng.randint(3, 9)  # 3-8 inclusive
        skills = list(rng.choice(_TECH_SKILLS, size=num_skills, replace=False))
        years_experience = int(rng.randint(1, 21))  # Uniform(1, 20)

        # Deterministic base score (p.20-21)
        # skill_matches = overlap between candidate skills and job requirements
        skill_matches = len(set(skills) & required_skills)
        raw_score = (
            0.3
            + 0.1 * min(skill_matches, 5)
            + 0.02 * min(years_experience, 10)
        )

        # Assessment noise — simulates real interview/evaluation variance
        raw_score += rng.normal(0, 0.04)

        # Injected gender bias (p.22) — calibrated for disparate impact ~0.73
        if gender == "female":
            raw_score -= 0.03

        raw_score = round(min(max(raw_score, 0.0), 1.0), 4)

        # Ground truth qualification threshold
        qualified = raw_score >= 0.65

        records.append({
            "candidate_id": f"C-{i:04d}",
            "skills": skills,
            "years_experience": years_experience,
            "education_level": education_level,
            "education_institution": education_institution,
            "gender": gender,
            "ethnicity": ethnicity,
            "raw_score": raw_score,
            "qualified": qualified,
        })

    df = pd.DataFrame(records)
    logger.success(
        f"HR dataset generated: {len(df)} candidates, "
        f"gender distribution: {df['gender'].value_counts().to_dict()}"
    )
    return df


# ---------------------------------------------------------------------------
# Section 4.2 — Medical Dataset: generate_medical_dataset(n=50, seed=42)
# ---------------------------------------------------------------------------

@graceful_fallback(
    fallback_value=pd.DataFrame(),
    section_ref="Section 12 - Medical Dataset Generation (p.30-35)"
)
def generate_medical_dataset(n: int = 50, seed: int = 42) -> pd.DataFrame:
    """
    Generate a synthetic medical / diagnostic dataset.

    All distributions match the Strategy §4.2 specification. Vital signs
    are clipped to physiologically plausible ranges.

    Args:
        n: Number of patient records.
        seed: Random seed for reproducibility.

    Returns:
        pd.DataFrame with columns matching Strategy §4.2.
    """
    rng = np.random.RandomState(seed)
    logger.info(f"Generating Medical dataset: n={n}, seed={seed}")

    records = []
    for i in range(n):
        # Vital signs — Normal distributions with physiological clipping
        heart_rate_avg = round(float(rng.normal(75, 12)), 1)
        spo2_min = round(float(np.clip(rng.normal(96, 3), 85, 100)), 1)
        wbc_count = round(float(np.clip(rng.normal(7.5, 2.5), 2, 25)), 1)
        temperature = round(float(rng.normal(37.0, 0.8)), 1)

        # Symptoms — 2-4 sampled from pool
        num_symptoms = rng.randint(2, 5)  # 2-4 inclusive
        reported_symptoms = list(
            rng.choice(_SYMPTOMS, size=num_symptoms, replace=False)
        )

        # Chest imaging — weighted categories
        chest_imaging = rng.choice(
            ["clear", "right_lower_consolidation",
             "bilateral_infiltrates", "normal"],
            p=[0.25, 0.35, 0.25, 0.15],
        )

        # True diagnosis — weighted categories
        true_diagnosis = rng.choice(
            ["pneumonia", "bronchitis", "atelectasis", "pulmonary_embolism"],
            p=[0.50, 0.25, 0.15, 0.10],
        )

        # Patient history — 0-3 conditions
        num_history = rng.randint(0, 4)  # 0-3 inclusive
        patient_history = list(
            rng.choice(_PATIENT_HISTORY_ITEMS, size=num_history, replace=False)
        ) if num_history > 0 else []

        records.append({
            "patient_id": f"P-{i:04d}",
            "heart_rate_avg": heart_rate_avg,
            "spo2_min": spo2_min,
            "wbc_count": wbc_count,
            "temperature": temperature,
            "reported_symptoms": ", ".join(reported_symptoms),
            "chest_imaging": chest_imaging,
            "true_diagnosis": true_diagnosis,
            "patient_history": patient_history,
        })

    df = pd.DataFrame(records)
    logger.success(
        f"Medical dataset generated: {len(df)} patients, "
        f"diagnosis distribution: {df['true_diagnosis'].value_counts().to_dict()}"
    )
    return df


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # HR dataset
    hr_df = generate_hr_dataset(n=200, seed=42)
    logger.info(f"HR shape: {hr_df.shape}")
    logger.info(f"HR columns: {list(hr_df.columns)}")
    logger.info(f"HR score stats:\n{hr_df['raw_score'].describe()}")

    # Verify bias injection: female selection rate / male selection rate
    male_rate = hr_df[hr_df["gender"] == "male"]["qualified"].mean()
    female_rate = hr_df[hr_df["gender"] == "female"]["qualified"].mean()
    disparate_impact = round(female_rate / male_rate, 2) if male_rate > 0 else 0
    logger.info(
        f"Disparate impact ratio: {disparate_impact} "
        f"(expected ~0.73, four-fifths threshold is 0.80)"
    )

    # Medical dataset
    med_df = generate_medical_dataset(n=50, seed=42)
    logger.info(f"Medical shape: {med_df.shape}")
    logger.info(f"Medical columns: {list(med_df.columns)}")

    logger.success("All synthetic data self-tests passed.")
