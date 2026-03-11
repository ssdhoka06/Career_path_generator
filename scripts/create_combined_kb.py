"""
Create combined_knowledge_base.json from all career doc sources
"""

import json
from collections import Counter

def load_json_file(filepath):
    """Load JSON file, return empty list if file doesn't exist or is empty"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {filepath}: {e}")
        return []

def create_combined_knowledge_base():
    """Merge all career doc JSON files"""

    print("Loading career doc files...")

    # Load all sources
    sources = [
        ("outputs/career_docs_starter.json", "Starter docs"),
        ("outputs/career_docs_expanded.json", "Expanded docs"),
        ("data/processed/additional_career_docs.json", "Additional docs")
    ]

    all_docs = []
    for filepath, name in sources:
        docs = load_json_file(filepath)
        print(f"  {name}: {len(docs)} docs")
        all_docs.extend(docs)

    print(f"\nTotal docs loaded: {len(all_docs)}")

    # Deduplicate by doc_id and fix text field if it's a list
    seen_ids = set()
    unique_docs = []
    duplicates = 0
    fixed_text = 0

    for doc in all_docs:
        doc_id = doc.get('doc_id')

        # Fix text field if it's a list (join into string)
        if isinstance(doc.get('text'), list):
            doc['text'] = ' '.join(doc['text'])
            fixed_text += 1

        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            unique_docs.append(doc)
        else:
            duplicates += 1
            print(f"Warning: Duplicate doc_id found: {doc_id}")

    if duplicates > 0:
        print(f"Removed {duplicates} duplicate docs")

    if fixed_text > 0:
        print(f"Fixed {fixed_text} docs with text as list")

    # Sort by doc_id
    unique_docs.sort(key=lambda x: x.get('doc_id', ''))

    print(f"\nFinal unique docs: {len(unique_docs)}")

    # Print distribution statistics
    doc_types = Counter([d['metadata']['doc_type'] for d in unique_docs])
    domains = Counter([d['metadata']['domain'] for d in unique_docs])
    exp_levels = Counter([d['metadata']['experience_level'] for d in unique_docs])
    regions = Counter([d['metadata']['region'] for d in unique_docs])

    print(f"\n=== DISTRIBUTION STATISTICS ===")
    print(f"\nDoc Type Distribution:")
    for dt, count in sorted(doc_types.items(), key=lambda x: -x[1]):
        print(f"  {dt}: {count}")

    print(f"\nDomain Distribution:")
    for domain, count in sorted(domains.items(), key=lambda x: -x[1]):
        print(f"  {domain}: {count}")

    print(f"\nExperience Level Distribution:")
    for level, count in sorted(exp_levels.items(), key=lambda x: -x[1]):
        if level:  # Skip None values
            print(f"  {level}: {count}")

    print(f"\nRegion Distribution:")
    for region, count in sorted(regions.items(), key=lambda x: -x[1])[:10]:
        print(f"  {region}: {count}")

    # Check text lengths
    text_lengths = [len(doc['text'].split()) for doc in unique_docs]
    avg_length = sum(text_lengths) / len(text_lengths)
    min_length = min(text_lengths)
    max_length = max(text_lengths)
    under_200 = sum(1 for l in text_lengths if l < 200)
    over_400 = sum(1 for l in text_lengths if l > 400)

    print(f"\n=== TEXT LENGTH STATISTICS ===")
    print(f"Average words per doc: {avg_length:.1f}")
    print(f"Min words: {min_length}")
    print(f"Max words: {max_length}")
    print(f"Docs under 200 words: {under_200}")
    print(f"Docs over 400 words: {over_400}")

    # Save combined knowledge base
    output_path = "data/processed/combined_knowledge_base.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique_docs, f, indent=2, ensure_ascii=False)

    print(f"\nSaved combined knowledge base to {output_path}")
    print(f"Total documents in knowledge base: {len(unique_docs)}")

    return unique_docs, {
        'total_docs': len(unique_docs),
        'doc_types': dict(doc_types),
        'domains': dict(domains),
        'exp_levels': dict(exp_levels),
        'regions': dict(regions),
        'avg_length': avg_length,
        'min_length': min_length,
        'max_length': max_length,
        'under_200': under_200,
        'over_400': over_400
    }

if __name__ == "__main__":
    docs, stats = create_combined_knowledge_base()
    print("\nCombined knowledge base created successfully!")
