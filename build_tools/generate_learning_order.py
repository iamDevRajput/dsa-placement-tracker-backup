import json, re, os
from collections import defaultdict

CATALOG_PATH = "data/mik_catalog.json"
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Group catalog problems by (topic, subtopic)
cat_grouped = defaultdict(lambda: defaultdict(list))
for p in catalog:
    t = p["topic"]
    st = p.get("subtopic", "General")
    cat_grouped[t][st].append(p)

stages = [
    {
        "id": "stage_1",
        "title": "Stage 1: Foundations & Logic Building",
        "description": "Essential mathematical intuition, bitwise operations, and recursive problem decomposition.",
        "topics": ["Mathematical", "Bit_Magic", "Recursion"]
    },
    {
        "id": "stage_2",
        "title": "Stage 2: Linear Data Structures & Pointers",
        "description": "Mastery of arrays, matrix manipulation, prefix sums, sliding window, linked lists, stacks, and queues.",
        "topics": ["Arrays", "Sliding Window", "Linked List", "Stack", "Queue"]
    },
    {
        "id": "stage_3",
        "title": "Stage 3: Hashing, Searching & Greedy",
        "description": "Fast lookups, binary search space pruning, priority queues, heaps, and greedy choice properties.",
        "topics": ["HashMap", "HashSet", "Heap", "Greedy"]
    },
    {
        "id": "stage_4",
        "title": "Stage 4: Hierarchical Structures & Strings",
        "description": "Binary trees, BSTs, prefix trees (Trie), graph traversals, shortest paths, DSU, and string algorithms.",
        "topics": ["Tree", "Trie", "Graph", "strings"]
    },
    {
        "id": "stage_5",
        "title": "Stage 5: Advanced Paradigms & System Design",
        "description": "Combinatorial backtracking, dynamic programming families, segment trees, line sweep, and data structure design.",
        "topics": ["Backtracking", "DP", "Segment Tree", "Line Sweep Technique", "Binary Lifting", "CSES", "Design"]
    }
]

# Build stages manifest
learning_roadmap = []
total_ordered_problems = 0
seen_ids = set()

for stage_cfg in stages:
    stage_topics = []
    stage_total = 0
    for topic_name in stage_cfg["topics"]:
        if topic_name not in cat_grouped:
            continue
        subtopic_dict = cat_grouped[topic_name]
        subtopics_list = []
        topic_prob_count = 0
        
        # Order subtopics logically (e.g. foundational first, General/Advanced later)
        sorted_subtopic_names = sorted(subtopic_dict.keys(), key=lambda s: (0 if s == "General" else 1, s))
        
        for st_name in sorted_subtopic_names:
            probs = subtopic_dict[st_name]
            # Order problems inside subtopic: if there's difficulty or ID sequence, order stably
            ordered_ids = [p["id"] for p in probs]
            for pid in ordered_ids:
                seen_ids.add(pid)
            topic_prob_count += len(ordered_ids)
            subtopics_list.append({
                "subtopic": st_name,
                "problem_count": len(ordered_ids),
                "problem_ids": ordered_ids
            })
            
        stage_total += topic_prob_count
        stage_topics.append({
            "topic": topic_name,
            "problem_count": topic_prob_count,
            "subtopics": subtopics_list
        })
        
    total_ordered_problems += stage_total
    learning_roadmap.append({
        "stage_id": stage_cfg["id"],
        "stage_title": stage_cfg["title"],
        "stage_description": stage_cfg["description"],
        "total_problems": stage_total,
        "topics": stage_topics
    })

print(f"Total problems in learning roadmap: {total_ordered_problems} (Unique: {len(seen_ids)})")
assert len(seen_ids) == len(catalog), f"Mismatch in problem count: {len(seen_ids)} != {len(catalog)}"

with open("data/mik_learning_order.json", "w", encoding="utf-8") as f:
    json.dump(learning_roadmap, f, indent=2)

with open("data/mik_learning_order.js", "w", encoding="utf-8") as f:
    f.write("window.MIK_LEARNING_ORDER = " + json.dumps(learning_roadmap) + ";\n")

print("Saved data/mik_learning_order.json and data/mik_learning_order.js successfully!")
