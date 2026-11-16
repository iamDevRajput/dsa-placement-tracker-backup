/**
 * JOB PREPARATION TRACKER — COMPLETE DATA REPOSITORY
 * 
 * Sourced directly from placement preparation roadmaps and slides:
 * - Eligibility Criteria & TCS 2027 Drive Details
 * - 3-Round Hiring Pipeline with ~90% OA rejection callout
 * - 35 Quantitative Aptitude topics across 6 groups
 * - 10 Verbal Ability topics (1-week roadmap)
 * - 19 Logical Reasoning topics across 7 groups (Visual Reasoning high priority)
 * - DSA 8-Week Core Roadmap (65+ curated problems + Sunday tests) + Weeks 9-11 Extension
 * - Technical Interview preparation across 6 expandable categories
 * - Daily 5-Hour Study targets (2h Aptitude, 2h DSA, 1h Core)
 */

const JOB_PREP_DATA = {
  // 1. ELIGIBILITY CRITERIA
  eligibility: {
    title: "Eligibility Criteria & Batch Verification",
    note: "Default placement criteria across tier-1 & tier-2 IT companies. Verify specific thresholds against company job descriptions.",
    criteria: [
      {
        id: "elig_cgpa",
        title: "60% or 6.0 CGPA Minimum",
        desc: "Throughout academics: 10th (SSC), 12th / Diploma (HSC), and ongoing Graduation (B.Tech / BCA / B.Sc / MCA). Some top firms require 65-70% / 7.0 CGPA.",
        fields: [
          { key: "tenth", label: "10th %", placeholder: "e.g. 85%" },
          { key: "twelfth", label: "12th %", placeholder: "e.g. 82%" },
          { key: "grad", label: "Graduation CGPA / %", placeholder: "e.g. 7.8 CGPA" }
        ],
        defaultStatus: "eligible"
      },
      {
        id: "elig_batch",
        title: "Batch Eligibility Verification",
        desc: "Slide roadmap references 2026 passout batch, but current user belongs to 2027 passout batch. Always verify drive registration year & graduation cutoff with company JD.",
        fields: [
          { key: "batchYear", label: "User Batch", placeholder: "2027" },
          { key: "driveBatch", label: "Target Drive Batch", placeholder: "2026 / 2027" }
        ],
        defaultStatus: "needs_verification" // User is 2027 passout
      },
      {
        id: "elig_backlogs",
        title: "No Active / Standing Backlogs",
        desc: "Zero active backlogs at the time of appearing for online assessment and final onboarding. History of cleared backlogs is acceptable by most MNCs (subject to company policy).",
        fields: [
          { key: "activeBacklogs", label: "Active Backlogs", placeholder: "0" },
          { key: "clearedBacklogs", label: "Cleared Backlogs", placeholder: "0" }
        ],
        defaultStatus: "eligible"
      },
      {
        id: "elig_gap",
        title: "Maximum 2 Years Education Gap",
        desc: "Maximum 24 months of total education gap allowed from 10th to graduation. Gap must not occur during the degree program without valid documented medical/academic justification.",
        fields: [
          { key: "gapMonths", label: "Total Gap (Months)", placeholder: "0" }
        ],
        defaultStatus: "eligible"
      }
    ],
    tcsReference: {
      title: "TCS Hiring Categories (Reference Comparison)",
      items: [
        {
          stream: "BCA / B.Sc (IT / CS)",
          role: "TCS Smart Hiring",
          package: "~2.5 - 3.2 LPA",
          focus: "Foundation Quants, Logical, Basic Verbal, Elementary Coding"
        },
        {
          stream: "B.Tech / BE / MCA / M.Sc",
          role: "TCS NQT — Ninja",
          package: "~3.36 - 3.6 LPA",
          focus: "Standard Foundation + Advanced Section (Quants, Reasoning, Hands-on Coding 1-2)"
        },
        {
          stream: "B.Tech / BE / MCA",
          role: "TCS NQT — Digital",
          package: "~7.0 - 7.5 LPA",
          focus: "High score in Advanced Section + Clean optimal solutions in Hands-on Coding"
        },
        {
          stream: "B.Tech / BE / MCA (Top Performers)",
          role: "TCS NQT — Prime",
          package: "~9.0 - 11.5 LPA",
          focus: "Top percentile in Advanced Coding + Strong System Architecture & CS Fundamentals"
        }
      ]
    }
  },

  // 2. HIRING PROCESS PIPELINE
  hiringPipeline: [
    {
      id: "round1_oa",
      roundNumber: 1,
      title: "Round 1 — Online Assessment (OA)",
      subtitle: "Duration: 90 - 120 Minutes | Elimination Rate: ~90%",
      dangerCallout: "⚠️ CRITICAL MILESTONE: ~90% of all applicants are eliminated in Round 1 Online Assessment. Speed, accuracy under timed pressure, zero negative marks, and passing 100% of test cases (both public and hidden edge cases) are mandatory.",
      components: [
        {
          id: "oa_quants",
          name: "Quantitative Aptitude",
          desc: "Speed arithmetic, algebra, percentages, TSD, P&L, permutations & probability under strict sectional timers."
        },
        {
          id: "oa_verbal",
          name: "Verbal Ability & Reading Comprehension",
          desc: "Reading comprehension passages, grammar error spotting, sentence improvement, vocabulary & cloze tests."
        },
        {
          id: "oa_reasoning",
          name: "Logical & Non-Verbal Reasoning",
          desc: "Series, syllogisms, seating arrangements, blood relations, and high-frequency visual reasoning figures."
        },
        {
          id: "oa_coding",
          name: "2-3 Hands-on Coding Problems (DSA)",
          desc: "Typically 1 Easy problem (Strings/Arrays/Math) + 1-2 Medium problems (Two pointers, Sliding Window, Hashing, Sorting, Binary Search)."
        }
      ],
      checklist: [
        { id: "oa_mock1", label: "Completed 1 Full-Length Timed OA Mock (90 min)", defaultDone: false },
        { id: "oa_mock2", label: "Solved at least 15 previous company OA coding questions", defaultDone: false },
        { id: "oa_camera", label: "Webcam & microphone proctoring check verified", defaultDone: false },
        { id: "oa_shortcuts", label: "Formula cheat sheet & mental math shortcuts reviewed", defaultDone: false }
      ]
    },
    {
      id: "round2_tech",
      roundNumber: 2,
      title: "Round 2 — Technical Interview",
      subtitle: "Duration: 45 - 60 Minutes | Live Problem Solving & Core CS",
      dangerCallout: "💡 TIP: Interviewers evaluate thought process, communication, and approach more than memorized code. Always verbalize your thinking, calculate brute-force before jumping to optimal, and dry-run with custom test cases.",
      components: [
        {
          id: "tech_core",
          name: "Core Computer Science Fundamentals",
          desc: "Deep questions on OOPS (4 pillars, polymorphism), OS (processes, deadlock, virtual memory), DBMS (ACID, Normalization), CN (OSI, TCP/UDP)."
        },
        {
          id: "tech_sql",
          name: "Live SQL Query Writing",
          desc: "Writing complex queries on paper/shared screen: 2nd highest salary, INNER/LEFT joins, GROUP BY with HAVING, window functions (DENSE_RANK)."
        },
        {
          id: "tech_projects",
          name: "Resume Projects & System Architecture",
          desc: "End-to-end explanation of your top 2 projects: tech stack decisions, DB schema, API design, authentication, hard bugs solved, scale tradeoffs."
        },
        {
          id: "tech_livecoding",
          name: "Live DSA Coding & Dry Running",
          desc: "Writing clean C++/Java code on Google Docs or shared whiteboard without IDE autocomplete. Clarifying constraints & edge cases."
        }
      ],
      checklist: [
        { id: "tech_mock1", label: "Conducted 1 peer technical mock interview with live coding", defaultDone: false },
        { id: "tech_resume_scrub", label: "Can explain every single word and technology on resume", defaultDone: false },
        { id: "tech_arch_diagram", label: "Can draw system architecture diagram for major project on paper", defaultDone: false }
      ]
    },
    {
      id: "round3_hr",
      roundNumber: 3,
      title: "Round 3 — HR / Behavioral Interview",
      subtitle: "Duration: 20 - 30 Minutes | Culture Fit, Mindset & Communication",
      dangerCallout: "🤝 KEY STRATEGY: Use the STAR method (Situation, Task, Action, Result) for behavioral answers. Show genuine passion, adaptability to rotational shifts/relocation, and clear career aspirations.",
      components: [
        {
          id: "hr_pitch",
          name: "'Tell Me About Yourself' (90-Sec Elevator Pitch)",
          desc: "Crisp personal intro: Education -> Technical highlights -> Key projects -> Placement goal. Natural delivery without sounding scripted."
        },
        {
          id: "hr_whyhire",
          name: "'Why Should We Hire You?'",
          desc: "Clear intersection of your technical discipline, fast learning curve, work ethic, and company business goals."
        },
        {
          id: "hr_situational",
          name: "Situational & Behavioral Questions",
          desc: "Handling team conflicts, failure in a deadline, overcoming technical hurdles, handling constructive feedback."
        },
        {
          id: "hr_company_research",
          name: "Company Knowledge & Meaningful Questions",
          desc: "Knowing company CEO, core products, recent news, and preparing 2 insightful questions to ask the interviewer at the end."
        }
      ],
      checklist: [
        { id: "hr_elevator_ready", label: "Recorded and polished 90-second intro video/audio", defaultDone: false },
        { id: "hr_star_ready", label: "Prepared 3 STAR stories (Conflict, Failure, Success)", defaultDone: false },
        { id: "hr_relocation_ready", label: "Ready to confirm relocation, shift flexibility, and service agreements", defaultDone: false }
      ]
    }
  ],

  // 3. QUANTITATIVE APTITUDE (35 Topics in 6 Groups)
  quants: {
    title: "Quantitative Aptitude Mastery (35 Topics)",
    methodology: "4-Step Mastery Method: 1) Learn Concept -> 2) Solve Same 10-15 Examples -> 3) Practice 20-30 New Problems -> 4) Sectional Timed Mock.",
    groups: [
      {
        id: "qgroup_numbers",
        name: "Group 1: Numbers & Basics",
        topics: [
          { id: "q_num_sys", name: "Number System (Classifications, Digits, Place Values)", count: 25 },
          { id: "q_lcm_hcf", name: "LCM & HCF (Properties, Fractions, Applications)", count: 20 },
          { id: "q_divisibility", name: "Divisibility Rules & Remainder Theorems", count: 20 },
          { id: "q_indices_surds", name: "Powers, Indices & Surds", count: 20 },
          { id: "q_simplification", name: "Simplification & Approximations (BODMAS)", count: 30 },
          { id: "q_percentages", name: "Percentages (Fractions Conversion & Base Shifts)", count: 30 }
        ]
      },
      {
        id: "qgroup_speed_work",
        name: "Group 2: Speed, Distance & Work",
        topics: [
          { id: "q_tsd", name: "Time, Speed & Distance (Average Speed, Late/Early)", count: 30 },
          { id: "q_trains", name: "Problems on Trains (Relative Speed, Platforms, Bridges)", count: 25 },
          { id: "q_boats", name: "Boats & Streams (Upstream, Downstream, Still Water)", count: 20 },
          { id: "q_races", name: "Races & Circular Tracks", count: 15 },
          { id: "q_time_work", name: "Time & Work (Efficiency Method & Man-Days formula)", count: 30 },
          { id: "q_pipes", name: "Pipes & Cisterns (Inlet, Outlet & Leakage)", count: 25 },
          { id: "q_work_wages", name: "Work & Wages (Distribution according to work)", count: 15 }
        ]
      },
      {
        id: "qgroup_di",
        name: "Group 3: Data Interpretation (DI)",
        topics: [
          { id: "q_di_tables_lines", name: "Tables & Line Graphs", count: 20 },
          { id: "q_di_bar_charts", name: "Bar Charts (Single, Grouped, Stacked)", count: 20 },
          { id: "q_di_pie_charts", name: "Pie Charts (Degrees to Percentages conversion)", count: 20 },
          { id: "q_di_radar_mixed", name: "Radar / Mixed Graph Sets", count: 15 },
          { id: "q_di_sufficiency", name: "Data Sufficiency in Quantitative Aptitude", count: 20 }
        ]
      },
      {
        id: "qgroup_banking_arithmetic",
        name: "Group 4: Classic Banking & Commercial Arithmetic",
        topics: [
          { id: "q_profit_loss", name: "Profit & Loss (Marked Price, Discounts, Dishonest Dealer)", count: 30 },
          { id: "q_simple_interest", name: "Simple Interest (Formulas, Rate Adjustments)", count: 25 },
          { id: "q_compound_interest", name: "Compound Interest (Compounding Half-Yearly, CI-SI Diff)", count: 25 },
          { id: "q_ratio_proportion", name: "Ratio, Proportion & Variations", count: 25 },
          { id: "q_partnership", name: "Partnership & Profit Sharing", count: 20 },
          { id: "q_alligations", name: "Mixtures & Alligations (Replacement formula)", count: 25 },
          { id: "q_averages", name: "Averages (Weighted Average, Addition/Removal of items)", count: 25 },
          { id: "q_ages", name: "Problems on Ages", count: 20 }
        ]
      },
      {
        id: "qgroup_prog_prob",
        name: "Group 5: Progression, Permutation & Probability",
        topics: [
          { id: "q_ap_gp_hp", name: "Arithmetic & Geometric Progressions (AP, GP, HP)", count: 20 },
          { id: "q_permutations", name: "Permutations & Combinations (P&C Fundamentals, Arrangements)", count: 30 },
          { id: "q_probability", name: "Probability (Dice, Coins, Cards, Conditional Probability)", count: 30 }
        ]
      },
      {
        id: "qgroup_geom_alg_sets",
        name: "Group 6: Geometry, Algebra & Sets",
        topics: [
          { id: "q_mensuration_2d", name: "Mensuration 2D (Triangles, Quadrilaterals, Circles)", count: 25 },
          { id: "q_mensuration_3d", name: "Mensuration 3D (Cylinder, Cone, Sphere, Prism, Frustum)", count: 25 },
          { id: "q_basic_algebra", name: "Basic Algebra & Linear Equations", count: 20 },
          { id: "q_quadratic", name: "Quadratic Equations (Roots, Discriminant, Sign of Roots)", count: 20 },
          { id: "q_logarithms", name: "Logarithms (Properties, Base Change, Log Tables)", count: 15 },
          { id: "q_sets_venn", name: "Set Theory & Venn Diagrams in Quants", count: 20 }
        ]
      }
    ]
  },

  // 4. VERBAL ABILITY (10 Topics, 1-Week Roadmap)
  verbal: {
    title: "Verbal Ability & English Proficiency (10 Topics)",
    roadmapNote: "1-Week Dedicated Sprint: 1-2 topics per day with grammar drills and timed passages.",
    topics: [
      { id: "v_rc", name: "Reading Comprehension (RC - Speed reading, Tone, Inference)", days: "Day 1", count: 15 },
      { id: "v_cloze", name: "Cloze Test (Passage contextual fill-ups)", days: "Day 2", count: 20 },
      { id: "v_spotting_errors", name: "Spotting Errors / Error Detection in Sentences", days: "Day 3", count: 35 },
      { id: "v_sentence_improvement", name: "Sentence Correction & Improvement", days: "Day 3", count: 30 },
      { id: "v_para_jumbles", name: "Para Jumbles / Sentence Rearrangement (Mandatory Pairs)", days: "Day 4", count: 25 },
      { id: "v_fillers", name: "Fill in the Blanks (Single & Double Fillers)", days: "Day 4", count: 25 },
      { id: "v_sva", name: "Subject-Verb Agreement (SVA Core 15 Rules)", days: "Day 5", count: 30 },
      { id: "v_tenses", name: "Tenses & Conditional Sentences (If clauses)", days: "Day 5", count: 25 },
      { id: "v_prepositions", name: "Prepositions & Conjunctions (Fixed Prepositions)", days: "Day 6", count: 35 },
      { id: "v_idioms_vocab", name: "Idioms, Phrases & High-Frequency Placement Vocabulary", days: "Day 7", count: 50 }
    ]
  },

  // 5. LOGICAL REASONING (19 Topics across 7 Groups)
  reasoning: {
    title: "Logical Reasoning & Analytical Ability (19 Topics)",
    visualNote: "⚠️ Group 7 (Visual Reasoning) is EXTREMELY COMMON in TCS, Accenture, Capgemini, and Infosys assessments. Give it highest practice priority.",
    groups: [
      {
        id: "rgroup_series",
        name: "Group 1: Series & Coding",
        topics: [
          { id: "r_num_alpha_series", name: "Number & Alphabet Series (Difference, Prime, Alternating)", priority: "standard" },
          { id: "r_coding_decoding", name: "Coding & Decoding (Letter shifting, Matrix, Number coding)", priority: "standard" }
        ]
      },
      {
        id: "rgroup_basic_logic",
        name: "Group 2: Basic Logic & Relationships",
        topics: [
          { id: "r_analogy", name: "Analogy & Classification (Odd One Out)", priority: "standard" },
          { id: "r_blood_relations", name: "Blood Relations (Coded relations, Family tree diagrams)", priority: "high" },
          { id: "r_direction_sense", name: "Direction Sense Test (Shadows, Turns, Pythagoras distances)", priority: "high" }
        ]
      },
      {
        id: "rgroup_statements",
        name: "Group 3: Statements & Deductions",
        topics: [
          { id: "r_syllogisms", name: "Syllogisms (Venn Diagrams, Some/All/No/Possibility cases)", priority: "critical" },
          { id: "r_statement_assumptions", name: "Statement & Assumptions (Implicit vs Explicit)", priority: "standard" },
          { id: "r_statement_conclusions", name: "Statement & Conclusions", priority: "standard" },
          { id: "r_cause_effect", name: "Cause & Effect Relationships", priority: "standard" }
        ]
      },
      {
        id: "rgroup_arrangements",
        name: "Group 4: Arrangements & Puzzles",
        topics: [
          { id: "r_linear_seating", name: "Linear Seating Arrangement (Single & Parallel rows, Facing North/South)", priority: "critical" },
          { id: "r_circular_seating", name: "Circular Seating Arrangement (Facing Inward, Outward & Both)", priority: "critical" },
          { id: "r_complex_puzzles", name: "Complex Floor, Day & Box Puzzles", priority: "high" }
        ]
      },
      {
        id: "rgroup_clocks_order",
        name: "Group 5: Clocks, Calendars & Order",
        topics: [
          { id: "r_clocks", name: "Clocks (Angle between hands, Faulty clocks, Coinciding hands)", priority: "standard" },
          { id: "r_calendars", name: "Calendars (Odd days method, Leap years, Same calendar year)", priority: "standard" },
          { id: "r_order_ranking", name: "Order & Ranking (Left/Right position formula, Overlapping cases)", priority: "high" }
        ]
      },
      {
        id: "rgroup_data_critical",
        name: "Group 6: Data & Critical Reasoning",
        topics: [
          { id: "r_data_sufficiency", name: "Data Sufficiency in Logical Reasoning", priority: "standard" },
          { id: "r_venn_logical", name: "Venn Diagrams (Set overlap & Logical categorization)", priority: "standard" }
        ]
      },
      {
        id: "rgroup_visual",
        name: "Group 7: Visual & Non-Verbal Reasoning (HIGH PRIORITY / VERY COMMON)",
        isHighPriority: true,
        topics: [
          { id: "r_pattern_completion", name: "Pattern Completion, Paper Folding & Cutting, Mirror / Water Images", priority: "critical" },
          { id: "r_cubes_dice", name: "Cubes & Dice (Opposite faces, Unfolded nets, Embedded Figures)", priority: "critical" }
        ]
      }
    ]
  },

  // 6. DSA 8-WEEK ROADMAP + EXTENSIONS (Weeks 9-11)
  dsaWeeks: [
    {
      weekNumber: 1,
      title: "Week 1: Fundamentals, Basic Math & Complexity Analysis",
      goal: "Master C++ Fast I/O, control flow, time/space complexity, and core mathematical reasoning.",
      problems: [
        { id: "dsa_w1_p1", title: "C++ Basics, Fast I/O & Memory Layout", difficulty: "Easy", link: "https://takeuforward.org/c/c-basics-for-dsa/" },
        { id: "dsa_w1_p2", title: "Time and Space Complexity Analysis (Big-O, Omega, Theta)", difficulty: "Easy", link: "https://takeuforward.org/data-structure/time-and-space-complexity/" },
        { id: "dsa_w1_p3", title: "Count Digits in a Number", difficulty: "Easy", link: "https://leetcode.com/problems/find-numbers-with-even-number-of-digits/" },
        { id: "dsa_w1_p4", title: "Reverse a Number (handling 32-bit overflow)", difficulty: "Easy", link: "https://leetcode.com/problems/reverse-integer/" },
        { id: "dsa_w1_p5", title: "Check if a Number is Palindrome", difficulty: "Easy", link: "https://leetcode.com/problems/palindrome-number/" },
        { id: "dsa_w1_p6", title: "GCD / HCF using Euclidean Algorithm (O(log(min(a,b))))", difficulty: "Easy", link: "https://takeuforward.org/data-structure/find-gcd-of-two-numbers/" },
        { id: "dsa_w1_p7", title: "Check Armstrong Number", difficulty: "Easy", link: "https://takeuforward.org/data-structure/check-if-a-number-is-armstrong-number-or-not/" },
        { id: "dsa_w1_p8", title: "Print all Divisors of a Given Number (O(sqrt(N)))", difficulty: "Easy", link: "https://takeuforward.org/data-structure/print-all-divisors-of-a-given-number/" },
        { id: "dsa_w1_p9", title: "Check for Prime Number (Trial Division O(sqrt(N)))", difficulty: "Easy", link: "https://takeuforward.org/data-structure/check-if-a-number-is-prime-or-not/" }
      ],
      sundayAssignment: {
        title: "Week 1 Sunday Assignment",
        desc: "Solve all 7 basic math problems purely using mathematical operations (% and /) without converting numbers to strings."
      }
    },
    {
      weekNumber: 2,
      title: "Weeks 2 & 3: Arrays Mastery (16 Core Placement Problems)",
      goal: "Master two-pointer, frequency hashing, Dutch National Flag, Moore's Voting, and Kadane's algorithm.",
      problems: [
        { id: "dsa_w2_p1", title: "Largest Element in an Array", difficulty: "Easy", link: "https://takeuforward.org/data-structure/find-the-largest-element-in-an-array/" },
        { id: "dsa_w2_p2", title: "Second Largest Element in an Array without sorting", difficulty: "Easy", link: "https://takeuforward.org/data-structure/find-second-smallest-and-second-largest-element-in-an-array/" },
        { id: "dsa_w2_p3", title: "Check if Array is Sorted and Rotated", difficulty: "Easy", link: "https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/" },
        { id: "dsa_w2_p4", title: "Remove Duplicates from Sorted Array in-place", difficulty: "Easy", link: "https://leetcode.com/problems/remove-duplicates-from-sorted-array/" },
        { id: "dsa_w2_p5", title: "Left Rotate Array by One Place", difficulty: "Easy", link: "https://takeuforward.org/data-structure/left-rotate-the-array-by-one/" },
        { id: "dsa_w2_p6", title: "Rotate Array by K Places (Reversal Algorithm)", difficulty: "Medium", link: "https://leetcode.com/problems/rotate-array/" },
        { id: "dsa_w2_p7", title: "Move Zeroes to End of Array maintaining order", difficulty: "Easy", link: "https://leetcode.com/problems/move-zeroes/" },
        { id: "dsa_w2_p8", title: "Linear Search and Sentinel Search", difficulty: "Easy", link: "https://takeuforward.org/data-structure/linear-search-in-c/" },
        { id: "dsa_w2_p9", title: "Union of Two Sorted Arrays", difficulty: "Easy", link: "https://takeuforward.org/data-structure/union-of-two-sorted-arrays/" },
        { id: "dsa_w2_p10", title: "Find Missing Number in Array (XOR & Sum formulas)", difficulty: "Easy", link: "https://leetcode.com/problems/missing-number/" },
        { id: "dsa_w2_p11", title: "Max Consecutive Ones", difficulty: "Easy", link: "https://leetcode.com/problems/max-consecutive-ones/" },
        { id: "dsa_w2_p12", title: "Single Number (Find number appearing once, others twice)", difficulty: "Easy", link: "https://leetcode.com/problems/single-number/" },
        { id: "dsa_w2_p13", title: "Two Sum (Check if pair with given sum exists)", difficulty: "Easy", link: "https://leetcode.com/problems/two-sum/" },
        { id: "dsa_w2_p14", title: "Sort Colors (0s, 1s and 2s - Dutch National Flag)", difficulty: "Medium", link: "https://leetcode.com/problems/sort-colors/" },
        { id: "dsa_w2_p15", title: "Majority Element (> n/2 times - Moore's Voting Algorithm)", difficulty: "Easy", link: "https://leetcode.com/problems/majority-element/" },
        { id: "dsa_w2_p16", title: "Maximum Subarray Sum (Kadane's Algorithm & print subarray)", difficulty: "Medium", link: "https://leetcode.com/problems/maximum-subarray/" }
      ],
      sundayAssignment: {
        title: "Weeks 2 & 3 Sunday Test",
        desc: "Solve 3 mixed array problems (Easy + Medium + Kadane variant) in a single continuous 60-minute session without looking at hints."
      }
    },
    {
      weekNumber: 4,
      title: "Week 4: Strings Mastery (12 Core Problems)",
      goal: "Character manipulation, palindrome checks, frequency maps, Roman numerals, and substring problems.",
      problems: [
        { id: "dsa_w4_p1", title: "Reverse a String in-place", difficulty: "Easy", link: "https://leetcode.com/problems/reverse-string/" },
        { id: "dsa_w4_p2", title: "Check if String is Valid Palindrome (alphanumeric only)", difficulty: "Easy", link: "https://leetcode.com/problems/valid-palindrome/" },
        { id: "dsa_w4_p3", title: "Valid Anagram (Frequency count approach)", difficulty: "Easy", link: "https://leetcode.com/problems/valid-anagram/" },
        { id: "dsa_w4_p4", title: "Longest Common Prefix", difficulty: "Easy", link: "https://leetcode.com/problems/longest-common-prefix/" },
        { id: "dsa_w4_p5", title: "Isomorphic Strings", difficulty: "Easy", link: "https://leetcode.com/problems/isomorphic-strings/" },
        { id: "dsa_w4_p6", title: "Rotate String (Check if A is rotation of B)", difficulty: "Easy", link: "https://leetcode.com/problems/rotate-string/" },
        { id: "dsa_w4_p7", title: "Maximum Nesting Depth of the Parentheses", difficulty: "Easy", link: "https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/" },
        { id: "dsa_w4_p8", title: "Roman to Integer and Integer to Roman", difficulty: "Easy", link: "https://leetcode.com/problems/roman-to-integer/" },
        { id: "dsa_w4_p9", title: "String to Integer (atoi implementation with edge cases)", difficulty: "Medium", link: "https://leetcode.com/problems/string-to-integer-atoi/" },
        { id: "dsa_w4_p10", title: "Reverse Words in a String", difficulty: "Medium", link: "https://leetcode.com/problems/reverse-words-in-a-string/" },
        { id: "dsa_w4_p11", title: "Longest Palindromic Substring (Expand around center)", difficulty: "Medium", link: "https://leetcode.com/problems/longest-palindromic-substring/" },
        { id: "dsa_w4_p12", title: "Count and Say", difficulty: "Medium", link: "https://leetcode.com/problems/count-and-say/" }
      ],
      sundayAssignment: {
        title: "Week 4 Sunday Test",
        desc: "Timed String Challenge: Solve 2 Medium string problems (Reverse Words + Longest Palindrome Substring) under 45 minutes."
      }
    },
    {
      weekNumber: 5,
      title: "Week 5: Sorting Techniques (9 Items)",
      goal: "Understand sorting mechanics, stability, recursive implementations, Quickselect, and inversion counting.",
      problems: [
        { id: "dsa_w5_p1", title: "Selection Sort (Find minimum and swap)", difficulty: "Easy", link: "https://takeuforward.org/sorting/selection-sort-algorithm/" },
        { id: "dsa_w5_p2", title: "Bubble Sort (Repeated adjacent swaps)", difficulty: "Easy", link: "https://takeuforward.org/data-structure/bubble-sort-algorithm/" },
        { id: "dsa_w5_p3", title: "Insertion Sort (Place key in sorted prefix)", difficulty: "Easy", link: "https://takeuforward.org/data-structure/insertion-sort-algorithm/" },
        { id: "dsa_w5_p4", title: "Merge Sort (Divide & Conquer, O(N log N) time, O(N) space)", difficulty: "Medium", link: "https://takeuforward.org/data-structure/merge-sort-algorithm/" },
        { id: "dsa_w5_p5", title: "Recursive Bubble Sort and Recursive Insertion Sort", difficulty: "Easy", link: "https://takeuforward.org/data-structure/recursive-bubble-sort-algorithm/" },
        { id: "dsa_w5_p6", title: "Quick Sort (Partitioning, average O(N log N))", difficulty: "Medium", link: "https://takeuforward.org/data-structure/quick-sort-algorithm/" },
        { id: "dsa_w5_p7", title: "Count Inversions in an Array (Modified Merge Sort)", difficulty: "Medium", link: "https://takeuforward.org/data-structure/count-inversions-in-an-array/" },
        { id: "dsa_w5_p8", title: "Kth Largest / Smallest Element (Quickselect algorithm)", difficulty: "Medium", link: "https://leetcode.com/problems/kth-largest-element-in-an-array/" },
        { id: "dsa_w5_p9", title: "Find Peak Element in Array", difficulty: "Medium", link: "https://leetcode.com/problems/find-peak-element/" }
      ],
      sundayAssignment: {
        title: "Week 5 Sunday Test",
        desc: "Implement Merge Sort and Quick Sort from scratch without looking at any notes or IDE autocomplete in under 30 minutes."
      }
    },
    {
      weekNumber: 6,
      title: "Week 6: Searching & Binary Search (8 Items)",
      goal: "Master iterative and recursive binary search, lower/upper bounds, and searching on rotated/answer spaces.",
      problems: [
        { id: "dsa_w6_p1", title: "Binary Search (Iterative and Recursive implementation)", difficulty: "Easy", link: "https://leetcode.com/problems/binary-search/" },
        { id: "dsa_w6_p2", title: "Implement Lower Bound and Upper Bound", difficulty: "Easy", link: "https://takeuforward.org/arrays/implement-lower-bound-bs-2/" },
        { id: "dsa_w6_p3", title: "Search Insert Position", difficulty: "Easy", link: "https://leetcode.com/problems/search-insert-position/" },
        { id: "dsa_w6_p4", title: "Floor and Ceil in Sorted Array", difficulty: "Easy", link: "https://takeuforward.org/arrays/floor-and-ceil-in-sorted-array/" },
        { id: "dsa_w6_p5", title: "First and Last Occurrence of Element in Sorted Array", difficulty: "Medium", link: "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/" },
        { id: "dsa_w6_p6", title: "Count Occurrences of a Number in Sorted Array with Duplicates", difficulty: "Easy", link: "https://takeuforward.org/data-structure/count-occurrences-in-sorted-array/" },
        { id: "dsa_w6_p7", title: "Search in Rotated Sorted Array (Unique & Duplicate elements)", difficulty: "Medium", link: "https://leetcode.com/problems/search-in-rotated-sorted-array/" },
        { id: "dsa_w6_p8", title: "Find Minimum in Rotated Sorted Array", difficulty: "Medium", link: "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/" }
      ],
      sundayAssignment: {
        title: "Week 6 Sunday Test",
        desc: "Binary Search on Answers: Solve 2 problems (Koko Eating Bananas & Split Array Largest Sum) using BS monotonic search space."
      }
    },
    {
      weekNumber: 7,
      title: "Week 7: Recursion & Backtracking (6 Items)",
      goal: "Build mental model for recursive call stacks, base cases, head/tail recursion, and recurrence trees.",
      problems: [
        { id: "dsa_w7_p1", title: "Understand Recursion: Base Cases & Call Stack visual trace", difficulty: "Easy", link: "https://takeuforward.org/recursion/introduction-to-recursion-understand-recursion-by-printing-something-n-times/" },
        { id: "dsa_w7_p2", title: "Print 1 to N and N to 1 using Recursion and Backtracking", difficulty: "Easy", link: "https://takeuforward.org/recursion/print-1-to-n-using-recursion/" },
        { id: "dsa_w7_p3", title: "Sum of First N Numbers and Factorial (Parameterized & Functional)", difficulty: "Easy", link: "https://takeuforward.org/data-structure/sum-of-first-n-natural-numbers/" },
        { id: "dsa_w7_p4", title: "Reverse an Array using Recursion (Single & Two pointers)", difficulty: "Easy", link: "https://takeuforward.org/data-structure/reverse-a-given-array/" },
        { id: "dsa_w7_p5", title: "Check if a String is Palindrome using Recursion", difficulty: "Easy", link: "https://takeuforward.org/data-structure/check-if-the-given-string-is-palindrome-or-not/" },
        { id: "dsa_w7_p6", title: "Fibonacci Number (Multiple Recursive Calls & Tree Analysis)", difficulty: "Easy", link: "https://leetcode.com/problems/fibonacci-number/" }
      ],
      sundayAssignment: {
        title: "Week 7 Sunday Test",
        desc: "Pen & Paper Tracing: Draw the complete recursion tree and activation stack frames for Fibonacci(5) and Array Reverse on paper."
      }
    },
    {
      weekNumber: 8,
      title: "Week 8: Linked List Fundamentals (6 Items)",
      goal: "Master pointer manipulation, singly & doubly linked lists, Tortoise & Hare algorithm, and loop detection.",
      problems: [
        { id: "dsa_w8_p1", title: "Singly Linked List: Insertion and Deletion at Head, Tail, and Kth Position", difficulty: "Easy", link: "https://takeuforward.org/data-structure/insertion-in-a-singly-linked-list/" },
        { id: "dsa_w8_p2", title: "Doubly Linked List: Insertion, Deletion and Reversal", difficulty: "Easy", link: "https://takeuforward.org/data-structure/introduction-to-doubly-linked-list/" },
        { id: "dsa_w8_p3", title: "Reverse a Singly Linked List (Iterative & Recursive)", difficulty: "Easy", link: "https://leetcode.com/problems/reverse-linked-list/" },
        { id: "dsa_w8_p4", title: "Middle of the Linked List (Tortoise and Hare Slow/Fast Pointers)", difficulty: "Easy", link: "https://leetcode.com/problems/middle-of-the-linked-list/" },
        { id: "dsa_w8_p5", title: "Detect a Loop in Linked List & Find Starting Node of Loop", difficulty: "Medium", link: "https://leetcode.com/problems/linked-list-cycle-ii/" },
        { id: "dsa_w8_p6", title: "Delete Node in a Linked List without Head pointer", difficulty: "Easy", link: "https://leetcode.com/problems/delete-node-in-a-linked-list/" }
      ],
      sundayAssignment: {
        title: "Week 8 Sunday Test",
        desc: "Solve 'Reverse Nodes in k-Group' or 'Merge Two Sorted Lists' under 45 minutes without dangling pointer memory leaks."
      }
    },
    {
      weekNumber: 9,
      isExtension: true,
      title: "Week 9 (Extension): Stacks & Queues",
      goal: "Monotonic stacks, parenthesis matching, stack using array/queue, and Min Stack.",
      problems: [
        { id: "dsa_w9_p1", title: "Implement Stack using Array and Linked List", difficulty: "Easy", link: "https://takeuforward.org/data-structure/implement-stack-using-array/" },
        { id: "dsa_w9_p2", title: "Implement Queue using Array and Linked List", difficulty: "Easy", link: "https://takeuforward.org/data-structure/implement-queue-using-array/" },
        { id: "dsa_w9_p3", title: "Valid Parentheses", difficulty: "Easy", link: "https://leetcode.com/problems/valid-parentheses/" },
        { id: "dsa_w9_p4", title: "Next Greater Element I", difficulty: "Medium", link: "https://leetcode.com/problems/next-greater-element-i/" },
        { id: "dsa_w9_p5", title: "Min Stack (O(1) time and space retrieval)", difficulty: "Medium", link: "https://leetcode.com/problems/min-stack/" }
      ],
      sundayAssignment: {
        title: "Week 9 Sunday Test",
        desc: "Solve Next Greater Element II (circular array) and Asteroid Collision under 45 mins."
      }
    },
    {
      weekNumber: 10,
      isExtension: true,
      title: "Week 10 (Extension): Binary Trees & BST",
      goal: "Tree traversals (BFS & DFS), height, diameter, and Binary Search Tree properties.",
      problems: [
        { id: "dsa_w10_p1", title: "Binary Tree Traversals: Inorder, Preorder, Postorder (Recursive & Iterative)", difficulty: "Easy", link: "https://takeuforward.org/binary-tree/binary-tree-traversal-inorder-preorder-postorder/" },
        { id: "dsa_w10_p2", title: "Level Order Traversal / BFS of Binary Tree", difficulty: "Medium", link: "https://leetcode.com/problems/binary-tree-level-order-traversal/" },
        { id: "dsa_w10_p3", title: "Maximum Depth / Height of Binary Tree", difficulty: "Easy", link: "https://leetcode.com/problems/maximum-depth-of-binary-tree/" },
        { id: "dsa_w10_p4", title: "Check if Binary Tree is Balanced", difficulty: "Easy", link: "https://leetcode.com/problems/balanced-binary-tree/" },
        { id: "dsa_w10_p5", title: "Search and Insert in a Binary Search Tree (BST)", difficulty: "Easy", link: "https://leetcode.com/problems/search-in-a-binary-search-tree/" }
      ],
      sundayAssignment: {
        title: "Week 10 Sunday Test",
        desc: "Implement Lowest Common Ancestor (LCA) in Binary Tree and Lowest Common Ancestor in BST."
      }
    },
    {
      weekNumber: 11,
      isExtension: true,
      title: "Week 11 (Extension): Hashing & HashMaps",
      goal: "Frequency counting, collision resolution, sliding window with hash map, and subarray sums.",
      problems: [
        { id: "dsa_w11_p1", title: "Hashing Basics & Collision Resolution (Chaining vs Open Addressing)", difficulty: "Easy", link: "https://takeuforward.org/hashing/hashing-basics-theory/" },
        { id: "dsa_w11_p2", title: "Count Frequency of Elements in Array", difficulty: "Easy", link: "https://takeuforward.org/data-structure/count-frequency-of-each-element-in-the-array/" },
        { id: "dsa_w11_p3", title: "Longest Consecutive Sequence in Unsorted Array", difficulty: "Medium", link: "https://leetcode.com/problems/longest-consecutive-sequence/" },
        { id: "dsa_w11_p4", title: "Subarray Sum Equals K (Prefix sum + Hash map)", difficulty: "Medium", link: "https://leetcode.com/problems/subarray-sum-equals-k/" }
      ],
      sundayAssignment: {
        title: "Week 11 Sunday Test",
        desc: "Implement custom Hash Map with put(), get(), and remove() handling collisions."
      }
    }
  ],

  // 7. TECHNICAL INTERVIEW SUBJECTS (6 Categories)
  technicalSubjects: [
    {
      id: "tech_oops",
      title: "Object-Oriented Programming (OOPS)",
      subtitle: "Classes, 4 Pillars, Virtual Functions, Polymorphism & Diamond Problem",
      icon: "⚡",
      defaultSubtopics: [
        "Classes, Objects, and Memory Allocation",
        "4 Pillars: Encapsulation, Abstraction, Inheritance, Polymorphism",
        "Compile-time (Overloading) vs Run-time (Overriding) Polymorphism",
        "Virtual Functions, Pure Virtual Functions, and VTABLE / VPTR mechanism",
        "Diamond Problem, Multiple Inheritance & Virtual Base Classes in C++",
        "Interface vs Abstract Class differences & practical use-cases",
        "Constructors, Destructors & Constructor Calling Order in Inheritance",
        "Deep Copy vs Shallow Copy & Copy Constructor mechanics",
        "Access Specifiers: Public, Protected, and Private access boundaries",
        "Friend Functions, Friend Classes, and Static Member variables"
      ]
    },
    {
      id: "tech_dbms",
      title: "DBMS & SQL Query Mastery",
      subtitle: "ACID, Normalization, Indexing, Transactions & Window Functions",
      icon: "🗄️",
      defaultSubtopics: [
        "DBMS vs RDBMS vs NoSQL databases & when to use what",
        "ACID Properties with real-world banking transaction examples",
        "Database Normalization: 1NF, 2NF, 3NF, BCNF & Redundancy Anomalies",
        "Primary Key vs Unique Key vs Foreign Key constraints",
        "Clustered Indexing vs Non-Clustered Indexing (B-Tree internal structure)",
        "SQL Joins: INNER, LEFT, RIGHT, FULL OUTER, and CROSS JOIN with diagrams",
        "GROUP BY vs HAVING clause differences and filtering order",
        "Subqueries vs Correlated Subqueries and performance impact",
        "Window Functions: ROW_NUMBER(), RANK(), and DENSE_RANK()",
        "Find N-th Highest Salary in SQL (OFFSET/LIMIT & DENSE_RANK methods)",
        "Database Transactions, Locks, and Concurrency Isolation Levels"
      ]
    },
    {
      id: "tech_os",
      title: "Operating Systems (OS)",
      subtitle: "Processes, Threads, Scheduling, Deadlocks, Paging & Virtual Memory",
      icon: "💻",
      defaultSubtopics: [
        "Process vs Thread & Multithreading vs Multiprocessing",
        "Process State Transition Diagram & Process Control Block (PCB)",
        "CPU Scheduling Algorithms: FCFS, SJF, Priority, and Round Robin",
        "Process Synchronization, Critical Section Problem & Race Conditions",
        "Mutex vs Counting Semaphore vs Binary Semaphore",
        "Deadlock: 4 Necessary Conditions (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait)",
        "Deadlock Handling: Prevention, Avoidance (Banker's Algorithm), and Detection",
        "Paging vs Segmentation & Translation Lookaside Buffer (TLB)",
        "Virtual Memory, Page Faults, Thrashing, and Page Replacement Algorithms (FIFO, LRU, Optimal)",
        "Inter-Process Communication (IPC): Pipes, Shared Memory, and Sockets"
      ]
    },
    {
      id: "tech_cn",
      title: "Computer Networks (CN)",
      subtitle: "OSI & TCP/IP, TCP vs UDP, DNS, HTTP/HTTPS, IP Subnetting & Web Security",
      icon: "🌐",
      defaultSubtopics: [
        "OSI 7-Layer Model vs TCP/IP 4-Layer Architecture and Layer Responsibilities",
        "What happens behind the scenes when you type a URL in the browser address bar?",
        "TCP vs UDP: Reliability, Header size, Handshake vs Connectionless transfer",
        "TCP 3-Way Handshake (SYN, SYN-ACK, ACK) and 4-Way Connection Teardown",
        "Flow Control (Sliding Window) vs Congestion Control (Slow Start, Congestion Avoidance)",
        "DNS Resolution Process from Local Cache to Root, TLD, and Authoritative Nameservers",
        "HTTP vs HTTPS: SSL/TLS Handshake, Symmetric vs Asymmetric Encryption, Certificates",
        "IPv4 vs IPv6 Addressing, Subnet Masks, and CIDR Notation",
        "Cookies vs Session Storage vs LocalStorage & Token-based Authentication (JWT)",
        "Common Network Attacks: Man-In-The-Middle (MITM), DDoS, and Cross-Site Scripting (XSS)"
      ]
    },
    {
      id: "tech_project",
      title: "Final Year / Major Placement Projects",
      subtitle: "System Architecture, Tech Stack Decisions, Database Schemas & Hardest Bugs",
      icon: "🚀",
      defaultSubtopics: [
        "60-Second Crisp Project Pitch (Problem statement, Solution, Tech stack)",
        "High-Level Architecture (Client-Server, Microservices vs Monolith, API Gateway)",
        "Tech Stack Justification: Why chosen over other popular frameworks/libraries",
        "Database Schema Design, Key Entity Relationships & Normalization choices",
        "Authentication & Authorization flow (JWT, OAuth, Session cookies, Refresh tokens)",
        "Deep-dive: The hardest technical bug/blocker encountered and how you debugged it",
        "Performance optimization, Caching (Redis), and Database Query Indexing",
        "Scalability Trade-offs: How would the project scale from 100 to 100,000 active users?",
        "Security measures implemented (Input sanitization, CORS, Rate limiting, ENV secrets)"
      ]
    },
    {
      id: "tech_resume",
      title: "Resume Technical Deep-Dive & Code Defense",
      subtitle: "Explanation of every word on resume, Primary Language internals & Git workflows",
      icon: "📄",
      defaultSubtopics: [
        "Ability to explain every single technology, framework, and tool listed on resume",
        "Primary Language Deep-Dive (C++ STL containers & iterators / Java JVM memory & GC / Python GIL)",
        "Git & Version Control: Rebase vs Merge, Branching strategy, Resolving merge conflicts",
        "Live Coding Defense: Explaining Big-O complexity of any code written within 30 seconds",
        "Clean Code Principles: DRY, KISS, Modular Architecture, and SOLID principles",
        "Past Internship / Freelance / Open-Source contributions explanation",
        "Soft Skills & Communication: Explaining complex technical logic in plain English"
      ]
    }
  ],

  // 8. DAILY STUDY TARGET TEMPLATE (Daily 5 Hours)
  dailyTemplate: {
    targetHours: 5,
    pillars: [
      { id: "aptitude", name: "Aptitude & Reasoning", targetHours: 2, icon: "🧠", color: "#f59e0b" },
      { id: "dsa", name: "DSA Coding & Practice", targetHours: 2, icon: "⚡", color: "#3b82f6" },
      { id: "core", name: "Core CS & Tech Interview", targetHours: 1, icon: "📚", color: "#10b981" }
    ]
  }
};

// Make accessible to browser window or modules
if (typeof window !== 'undefined') {
  window.JOB_PREP_DATA = JOB_PREP_DATA;
}

