import json, re

CATALOG_PATH = "data/mik_catalog.json"
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Define pattern categories with matching rules
patterns = [
    # --- SLIDING WINDOW ---
    {
        "id": "pat_sw_fixed",
        "category": "Sliding Window",
        "name": "Fixed-Size Window",
        "description": "Maintain a window of constant width k while updating running statistics (sum, counts, frequency).",
        "keywords": ["size k", "length k", "anagram", "permutation in string", "distinct", "substrings of length"],
        "topics": ["Sliding Window", "Arrays"]
    },
    {
        "id": "pat_sw_variable",
        "category": "Sliding Window",
        "name": "Variable-Size Window (Longest/Shortest)",
        "description": "Expand right pointer to satisfy conditions, contract left pointer when condition is violated or to minimize window.",
        "keywords": ["longest substring", "minimum size", "without repeating", "at most k", "at least k", "fruit into baskets"],
        "topics": ["Sliding Window", "Arrays"]
    },
    {
        "id": "pat_sw_freq",
        "category": "Sliding Window",
        "name": "Frequency Map & Substring Matching",
        "description": "Use hash map or count array within sliding window to match character counts or target patterns.",
        "keywords": ["minimum window", "all anagrams", "frequency", "character replacement"],
        "topics": ["Sliding Window", "strings"]
    },
    
    # --- BINARY SEARCH ---
    {
        "id": "pat_bs_sorted",
        "category": "Binary Search",
        "name": "Standard Sorted Array Search",
        "description": "Halve the search space by comparing target with mid element.",
        "keywords": ["binary search", "search insert", "kth missing"],
        "topics": ["Arrays"]
    },
    {
        "id": "pat_bs_rotated",
        "category": "Binary Search",
        "name": "Rotated Sorted Array",
        "description": "Identify which half of the rotated array is sorted and adjust low/high accordingly.",
        "keywords": ["rotated", "rotation count", "minimum in rotated"],
        "topics": ["Arrays"]
    },
    {
        "id": "pat_bs_boundary",
        "category": "Binary Search",
        "name": "Boundary & Position Search",
        "description": "Locate lower bound, upper bound, first occurrence, or last occurrence of elements.",
        "keywords": ["first and last", "peak index", "find in mountain", "single element"],
        "topics": ["Arrays"]
    },
    {
        "id": "pat_bs_answer",
        "category": "Binary Search",
        "name": "Search Space on Answer (Predicate/Feasibility)",
        "description": "Binary search on monotonic answer range [low, high] with a check(mid) feasibility function.",
        "keywords": ["koko", "bouquets", "capacity", "minimize maximum", "maximize minimum", "smallest divisor", "speed to arrive", "days to make", "magnetic force", "split array largest sum"],
        "topics": ["Arrays"]
    },
    {
        "id": "pat_bs_matrix",
        "category": "Binary Search",
        "name": "2D Matrix Binary Search",
        "description": "Binary search on row-wise or column-wise sorted matrices.",
        "keywords": ["search a 2d matrix", "matrix", "count negative"],
        "topics": ["Arrays"]
    },

    # --- TWO POINTERS ---
    {
        "id": "pat_tp_opposite",
        "category": "Two Pointers",
        "name": "Opposite-Direction Pointers",
        "description": "Two pointers moving toward each other from opposite ends of a sorted array or sequence.",
        "keywords": ["two sum", "palindrome", "container with most water", "trapping rain water", "squares of a sorted"],
        "topics": ["Arrays", "strings"]
    },
    {
        "id": "pat_tp_fast_slow",
        "category": "Two Pointers",
        "name": "Fast & Slow Pointers",
        "description": "Two pointers moving at different speeds to detect cycles or find middle elements.",
        "keywords": ["cycle", "middle of", "remove duplicates", "happy number"],
        "topics": ["Linked List", "Arrays"]
    },

    # --- BACKTRACKING ---
    {
        "id": "pat_bt_subsets",
        "category": "Backtracking",
        "name": "Subsets & Subsequences (Include/Exclude)",
        "description": "Explore 2^N state space by making include or exclude decisions at each level.",
        "keywords": ["subsets", "subsequence", "power set"],
        "topics": ["Backtracking", "Recursion"]
    },
    {
        "id": "pat_bt_permutations",
        "category": "Backtracking",
        "name": "Permutations & Orderings",
        "description": "Explore N! permutations using visited flags or swapping in place.",
        "keywords": ["permutations", "next permutation", "letter tile"],
        "topics": ["Backtracking"]
    },
    {
        "id": "pat_bt_combinations",
        "category": "Backtracking",
        "name": "Combinations & Target Sums",
        "description": "Choose k elements or sum to target with or without replacement.",
        "keywords": ["combination sum", "combinations", "target sum"],
        "topics": ["Backtracking"]
    },
    {
        "id": "pat_bt_grid",
        "category": "Backtracking",
        "name": "Grid, Board & Constraint Search",
        "description": "Exhaustive search on 2D grids (N-Queens, Sudoku, Word Search, Maze).",
        "keywords": ["n-queens", "sudoku", "word search", "rat in a maze", "unique paths iii"],
        "topics": ["Backtracking"]
    },

    # --- DYNAMIC PROGRAMMING ---
    {
        "id": "pat_dp_1d",
        "category": "Dynamic Programming",
        "name": "1-D Linear DP (Fibonacci & Stepping)",
        "description": "Transition depends on previous 1 or 2 states: dp[i] = f(dp[i-1], dp[i-2]).",
        "keywords": ["climbing stairs", "house robber", "fibonacci", "tribonacci", "decode ways", "min cost climbing"],
        "topics": ["DP"]
    },
    {
        "id": "pat_dp_knapsack",
        "category": "Dynamic Programming",
        "name": "Knapsack & Subset Sums",
        "description": "Select subset of items subject to weight/capacity constraints (0/1 or Unbounded).",
        "keywords": ["knapsack", "subset sum", "partition equal", "coin change", "target sum"],
        "topics": ["DP"]
    },
    {
        "id": "pat_dp_lis",
        "category": "Dynamic Programming",
        "name": "Longest Increasing Subsequence (LIS)",
        "description": "Find maximum length subsequence with ordered property, solved via O(N^2) DP or O(N log N) patience sorting.",
        "keywords": ["increasing subsequence", "russian doll", "largest divisible", "number of lis"],
        "topics": ["DP"]
    },
    {
        "id": "pat_dp_strings",
        "category": "Dynamic Programming",
        "name": "DP on Strings (LCS & Edit Distance)",
        "description": "2D state dp[i][j] representing prefix matching between two strings.",
        "keywords": ["longest common subsequence", "edit distance", "distinct subsequences", "interleaving", "palindromic substring", "wildcard"],
        "topics": ["DP"]
    },
    {
        "id": "pat_dp_grids",
        "category": "Dynamic Programming",
        "name": "DP on Grids & Matrices",
        "description": "Finding paths, costs, or counts on 2D boards (down/right transitions).",
        "keywords": ["unique paths", "minimum path sum", "dungeon game", "cherry pickup", "maximal square"],
        "topics": ["DP"]
    },
    {
        "id": "pat_dp_games",
        "category": "Dynamic Programming",
        "name": "Game Strategy & Minimax",
        "description": "Two-player turn-based optimal play via minimax DP.",
        "keywords": ["stone game", "predict the winner", "can i win", "nim game"],
        "topics": ["DP"]
    },

    # --- TREES & GRAPHS ---
    {
        "id": "pat_tree_traversal",
        "category": "Trees",
        "name": "Tree Traversals & Views",
        "description": "Preorder, Inorder, Postorder, and Level Order (BFS) traversals and vertical/side views.",
        "keywords": ["traversal", "level order", "zigzag", "vertical order", "right side view", "bottom view"],
        "topics": ["Tree"]
    },
    {
        "id": "pat_tree_paths",
        "category": "Trees",
        "name": "Tree Paths, Diameter & LCA",
        "description": "Path sums, max path sum, tree diameter, and lowest common ancestor.",
        "keywords": ["lowest common ancestor", "diameter", "path sum", "maximum path sum", "distance k"],
        "topics": ["Tree"]
    },
    {
        "id": "pat_graph_bfs_dfs",
        "category": "Graphs",
        "name": "Graph BFS/DFS & Component Traversal",
        "description": "Traversing connected components, counting islands, and flood fill.",
        "keywords": ["number of islands", "clone graph", "flood fill", "bipartite", "connected components"],
        "topics": ["Graph"]
    },
    {
        "id": "pat_graph_multisource",
        "category": "Graphs",
        "name": "Multi-Source BFS",
        "description": "Push all initial source nodes into queue simultaneously for radial expansion.",
        "keywords": ["01 matrix", "rotting oranges", "as far from land", "multi-source", "shortest bridge", "walls and gates"],
        "topics": ["Graph", "Arrays"]
    },
    {
        "id": "pat_graph_topo",
        "category": "Graphs",
        "name": "Topological Sorting (Kahn's / DFS)",
        "description": "Order nodes in Directed Acyclic Graph based on dependencies/in-degrees.",
        "keywords": ["course schedule", "alien dictionary", "topological", "find eventual safe"],
        "topics": ["Graph"]
    },
    {
        "id": "pat_graph_shortest",
        "category": "Graphs",
        "name": "Shortest Paths (Dijkstra / Bellman-Ford)",
        "description": "Single-source shortest paths in weighted graphs using priority queue relaxation.",
        "keywords": ["network delay", "cheapest flights", "dijkstra", "shortest path in a grid"],
        "topics": ["Graph"]
    },
    {
        "id": "pat_graph_dsu",
        "category": "Graphs",
        "name": "Disjoint Set Union (DSU / Kruskal)",
        "description": "Union-Find with path compression and rank/size for dynamic connectivity and MST.",
        "keywords": ["redundant connection", "accounts merge", "min cost to connect", "provinces", "disjoint set"],
        "topics": ["Graph"]
    },

    # --- MONOTONIC STRUCTURES & INTERVALS ---
    {
        "id": "pat_mono_stack",
        "category": "Monotonic Structures",
        "name": "Monotonic Stack (Next Greater/Smaller)",
        "description": "Maintain increasing or decreasing stack to find next greater or smaller elements in O(N).",
        "keywords": ["next greater", "daily temperatures", "largest rectangle in histogram", "maximal rectangle", "online stock span"],
        "topics": ["Stack"]
    },
    {
        "id": "pat_intervals",
        "category": "Intervals",
        "name": "Interval Merging & Sweeping",
        "description": "Sort intervals by start/end time and merge overlapping segments.",
        "keywords": ["merge intervals", "insert interval", "meeting rooms", "non-overlapping"],
        "topics": ["Arrays"]
    },
    {
        "id": "pat_diff_array",
        "category": "Range Updates",
        "name": "Difference Array Technique",
        "description": "Perform range updates [L, R] in O(1) time and reconstruct array via prefix sum.",
        "keywords": ["difference array", "corporate flight", "car pooling", "range addition"],
        "topics": ["Arrays"]
    }
]

# Match catalog problems to patterns
pattern_manifest = []
total_matched = 0

for p_def in patterns:
    prob_ids = []
    for p in catalog:
        # Check topic match
        if p["topic"] not in p_def["topics"] and p_def["category"] not in p["topic"]:
            # Also allow subtopic check
            if p.get("subtopic") not in p_def["topics"]:
                continue
        
        # Check text match in title, subtopic, approaches
        text = (p["title"] + " " + p.get("subtopic", "") + " " + " ".join(p.get("approaches", []))).lower()
        matched = False
        for kw in p_def["keywords"]:
            if kw in text:
                matched = True
                break
        
        # Topic-level fallbacks for specialized topics
        if not matched:
            if p_def["id"] == "pat_diff_array" and p.get("subtopic") == "Difference Array Technique":
                matched = True
            elif p_def["id"] == "pat_bs_answer" and p.get("subtopic") == "Binary Search" and any(k in text for k in ["min", "max"]):
                matched = True
            elif p_def["id"] == "pat_dp_knapsack" and p.get("subtopic") == "Knapsack Series":
                matched = True
            elif p_def["id"] == "pat_dp_lis" and p.get("subtopic") == "LIS & Variants":
                matched = True
            elif p_def["id"] == "pat_dp_strings" and p.get("subtopic") == "DP on Strings":
                matched = True
            elif p_def["id"] == "pat_dp_grids" and p.get("subtopic") == "DP on Grids":
                matched = True
            elif p_def["id"] == "pat_dp_games" and p.get("subtopic") == "Game Strategy":
                matched = True
            elif p_def["id"] == "pat_graph_topo" and p.get("subtopic") == "Topological Sorting":
                matched = True
            elif p_def["id"] == "pat_graph_dsu" and p.get("subtopic") == "Disjoint Set":
                matched = True
            elif p_def["id"] == "pat_graph_shortest" and "dijkstra" in p.get("subtopic", "").lower():
                matched = True
            elif p_def["id"] == "pat_graph_multisource" and p.get("subtopic") == "Multi-Source BFS":
                matched = True
            elif p_def["id"] == "pat_mono_stack" and p.get("subtopic") == "Monotonic Stack":
                matched = True

        if matched and p["id"] not in prob_ids:
            prob_ids.append(p["id"])

    pattern_manifest.append({
        "id": p_def["id"],
        "category": p_def["category"],
        "name": p_def["name"],
        "description": p_def["description"],
        "problem_count": len(prob_ids),
        "problem_ids": prob_ids
    })
    total_matched += len(prob_ids)
    print(f"[{p_def['category']}] {p_def['name']}: {len(prob_ids)} problems")

print(f"\nGenerated {len(pattern_manifest)} patterns with {total_matched} problem references.")

with open("data/mik_patterns.json", "w", encoding="utf-8") as f:
    json.dump(pattern_manifest, f, indent=2)

with open("data/mik_patterns.js", "w", encoding="utf-8") as f:
    f.write("window.MIK_PATTERNS = " + json.dumps(pattern_manifest) + ";\n")

print("Saved data/mik_patterns.json and data/mik_patterns.js")
