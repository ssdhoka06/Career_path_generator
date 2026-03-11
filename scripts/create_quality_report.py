"""
Create quality_report.json with comprehensive statistics
"""

import json
from collections import Counter
from datetime import datetime

def create_quality_report():
    """Generate quality report from combined knowledge base"""

    print("Loading combined knowledge base...")
    with open('data/processed/combined_knowledge_base.json', 'r', encoding='utf-8') as f:
        docs = json.load(f)

    print(f"Loaded {len(docs)} documents")

    # Calculate distributions
    doc_types = Counter([d['metadata']['doc_type'] for d in docs])
    domains = Counter([d['metadata']['domain'] for d in docs])
    exp_levels = Counter([d['metadata']['experience_level'] for d in docs if d['metadata']['experience_level']])
    regions = Counter([d['metadata']['region'] for d in docs])

    # Calculate text length statistics
    text_lengths = [len(doc['text'].split()) for doc in docs]
    avg_length = sum(text_lengths) / len(text_lengths)
    min_length = min(text_lengths)
    max_length = max(text_lengths)
    under_200 = sum(1 for l in text_lengths if l < 200)
    over_400 = sum(1 for l in text_lengths if l > 400)

    # Calculate demo scenario coverage
    edtech_docs = sum(1 for d in docs if 'EdTech' in d['metadata']['domain'])
    edtech_transition = sum(1 for d in docs if 'EdTech' in d['metadata']['domain'] and d['metadata']['doc_type'] == 'transition_path')
    edtech_salary = sum(1 for d in docs if 'EdTech' in d['metadata']['domain'] and d['metadata']['doc_type'] == 'salary_data')

    # Create quality report
    quality_report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_docs": len(docs),
        "doc_type_distribution": dict(doc_types),
        "domain_distribution": dict(domains),
        "experience_level_distribution": dict(exp_levels),
        "region_distribution": dict(regions),
        "avg_text_length_words": round(avg_length, 1),
        "min_text_length_words": min_length,
        "max_text_length_words": max_length,
        "docs_under_200_words": under_200,
        "docs_over_400_words": over_400,
        "demo_scenario_coverage": {
            "engineer_to_edtech_docs": edtech_docs,
            "edtech_transition_path_docs": edtech_transition,
            "edtech_salary_docs": edtech_salary
        },
        "chroma_db_status": "not_tested",
        "ready_for_demo": False
    }

    # Save quality report
    output_path = 'data/processed/quality_report.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(quality_report, f, indent=2, ensure_ascii=False)

    print(f"\nQuality report saved to {output_path}")

    # Print summary
    print("\n" + "="*70)
    print("QUALITY REPORT SUMMARY")
    print("="*70)
    print(f"Total documents: {quality_report['total_docs']}")
    print(f"\nDoc Type Distribution:")
    for dt, count in sorted(doc_types.items(), key=lambda x: -x[1]):
        print(f"  {dt}: {count}")
    print(f"\nTop 10 Domains:")
    for domain, count in sorted(domains.items(), key=lambda x: -x[1])[:10]:
        print(f"  {domain}: {count}")
    print(f"\nExperience Levels:")
    for level, count in sorted(exp_levels.items(), key=lambda x: -x[1]):
        print(f"  {level}: {count}")
    print(f"\nText Length Statistics:")
    print(f"  Average: {avg_length:.1f} words")
    print(f"  Min: {min_length} words")
    print(f"  Max: {max_length} words")
    print(f"  Under 200 words: {under_200}")
    print(f"  Over 400 words: {over_400}")
    print(f"\nDemo Scenario Coverage:")
    print(f"  EdTech total docs: {edtech_docs}")
    print(f"  EdTech transition paths: {edtech_transition}")
    print(f"  EdTech salary data: {edtech_salary}")
    print("="*70)

    return quality_report

if __name__ == "__main__":
    create_quality_report()
