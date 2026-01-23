import React, { useState } from 'react';
import { Lightbulb, Zap, Target, Shuffle, Users, Brain, ChevronRight } from 'lucide-react';

const CreativeThinkingExplorer = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedTechnique, setSelectedTechnique] = useState(null);
  const [selectedDepartment, setSelectedDepartment] = useState(null);

  const categories = [
    {
      id: 'divergent',
      name: 'Divergent Thinking',
      icon: Lightbulb,
      color: 'bg-amber-500',
      description: 'Generate multiple ideas and possibilities'
    },
    {
      id: 'convergent',
      name: 'Convergent Thinking',
      icon: Target,
      color: 'bg-blue-500',
      description: 'Focus and refine ideas to find solutions'
    },
    {
      id: 'lateral',
      name: 'Lateral Thinking',
      icon: Shuffle,
      color: 'bg-purple-500',
      description: 'Approach problems from unexpected angles'
    },
    {
      id: 'collaborative',
      name: 'Collaborative Methods',
      icon: Users,
      color: 'bg-green-500',
      description: 'Harness collective intelligence'
    },
    {
      id: 'reframing',
      name: 'Reframing Techniques',
      icon: Brain,
      color: 'bg-rose-500',
      description: 'Change perspective to unlock new insights'
    },
    {
      id: 'structured',
      name: 'Structured Ideation',
      icon: Zap,
      color: 'bg-indigo-500',
      description: 'Systematic approaches to creativity'
    }
  ];

  const techniques = {
    divergent: [
      {
        name: 'Brainstorming',
        description: 'Classic rapid idea generation without judgment',
        when: 'Need volume of ideas quickly',
        how: 'Set timer, defer judgment, build on others\' ideas, encourage wild ideas',
        tip: 'Quantity breeds quality - aim for 50+ ideas in 15 minutes',
        prompts: [
          { dept: 'Sales', prompt: 'Generate 30 unconventional lead generation tactics for {{product/service}} targeting {{industry}}. Focus on channels competitors ignore. No budget constraints. List all ideas without evaluation.' },
          { dept: 'Marketing', prompt: 'Brainstorm 40 campaign concepts for {{brand}} to increase {{metric}} by 20%. Include guerrilla tactics, digital experiments, and partnership ideas. Defer all judgment until complete list.' },
          { dept: 'Legal', prompt: 'Generate 25 creative approaches to {{compliance challenge}} that satisfy regulatory requirements while reducing operational friction. Include technology solutions, process redesigns, and partnership models.' },
          { dept: 'IT', prompt: 'Brainstorm 35 ways to improve {{system/infrastructure}} performance. Include unconventional architectures, emerging technologies, vendor alternatives, and process changes. No idea too wild.' }
        ]
      },
      {
        name: 'SCAMPER',
        description: 'Systematic prompts to modify existing concepts',
        when: 'Improving or adapting existing solutions',
        how: 'Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse',
        tip: 'Work through each prompt methodically, even if some seem irrelevant',
        prompts: [
          { dept: 'Operations', prompt: 'Apply SCAMPER to our {{process name}} workflow. For each letter: What could we Substitute (vendors, tools, steps)? Combine (with other processes)? Adapt (from other industries)? Modify (timing, sequence)? Put to other use? Eliminate? Reverse? Generate 3 ideas per letter.' },
          { dept: 'Finance', prompt: 'Use SCAMPER on our {{financial process/report}}. Substitute: alternative data sources? Combine: merge with which reports? Adapt: best practices from where? Modify: frequency or format? Put to other use: repurpose for what? Eliminate: unnecessary fields? Reverse: who receives it first?' },
          { dept: 'R&D', prompt: 'SCAMPER our {{innovation process}}. Substitute: different research methods? Combine: merge with customer feedback loops? Adapt: practices from other industries? Modify: prototype iterations? Put to other use: repurpose failed experiments? Eliminate: approval bottlenecks? Reverse: start with commercialization?' },
          { dept: 'Supply Chain', prompt: 'Apply SCAMPER to {{logistics challenge}}. Substitute: alternative suppliers/routes? Combine: consolidate shipments? Adapt: solutions from other sectors? Modify: delivery timing/batch sizes? Put to other use: reverse logistics? Eliminate: intermediaries? Reverse: pull vs push?' }
        ]
      },
      {
        name: 'Mind Mapping',
        description: 'Visual branching of connected ideas',
        when: 'Exploring relationships between concepts',
        how: 'Start with central concept, branch out with associations, use colors and images',
        tip: 'Don\'t worry about organization initially - let it grow organically',
        prompts: [
          { dept: 'Product', prompt: 'Create a mind map for {{product feature}}. Center: feature name. First branches: user needs, technical requirements, competitive advantages, risks, dependencies. Let each branch spawn 5+ sub-branches. Identify 3 unexpected connections between distant branches.' },
          { dept: 'HR', prompt: 'Mind map our employee retention strategy. Center: "Retain Top Talent". Main branches: compensation, culture, growth, work-life, recognition. Branch each into specific tactics. Find connections between branches that suggest integrated solutions.' },
          { dept: 'Business Development', prompt: 'Mind map {{partnership opportunity}}. Center: partner name. Branches: value exchange, integration points, market access, risks, resource requirements, competitive dynamics. Explore sub-branches. What non-obvious synergies emerge?' },
          { dept: 'Communications', prompt: 'Create mind map for {{crisis communication plan}}. Center: crisis scenario. Branches: stakeholders, messages, channels, timing, escalation, monitoring. Sub-branch each thoroughly. Which connections reveal communication gaps?' }
        ]
      },
      {
        name: 'Random Word Association',
        description: 'Force connections between unrelated concepts',
        when: 'Breaking mental patterns',
        how: 'Pick random word, force connections to your challenge',
        tip: 'The more absurd the connection seems, the more creative the insight',
        prompts: [
          { dept: 'Sales', prompt: 'Random word: OCEAN. Force 10 connections between "ocean" and solving {{sales challenge}}. Example: "Ocean has waves → create rhythmic follow-up cadence". Make connections even if they seem ridiculous initially.' },
          { dept: 'Customer Success', prompt: 'Random words: GARDEN, SYMPHONY, VOLCANO. For each word, force 5 metaphorical connections to improving {{customer metric}}. Extract one actionable insight from the most absurd connection.' },
          { dept: 'Data Analytics', prompt: 'Random word: ARCHAEOLOGY. Force 8 connections between archaeological methods and {{data challenge}}. Example: "Archaeologists use layers → temporal data stratification". What data practice emerges from the metaphor?' },
          { dept: 'Procurement', prompt: 'Random words: JAZZ, ECOSYSTEM, IMMUNE SYSTEM. For each, force 6 connections to {{procurement issue}}. Jazz improvisation → supplier flexibility? Extract concrete procurement tactics from each metaphor.' }
        ]
      }
    ],
    convergent: [
      {
        name: 'Six Thinking Hats',
        description: 'Evaluate ideas from six distinct perspectives',
        when: 'Need thorough evaluation of promising ideas',
        how: 'White (facts), Red (emotions), Black (risks), Yellow (benefits), Green (creative), Blue (process)',
        tip: 'Separate the hats - wear each fully before switching',
        prompts: [
          { dept: 'Strategy', prompt: 'Evaluate {{strategic initiative}} using Six Hats. White: What data exists? Red: What\'s my gut feeling? Black: What could go wrong? Yellow: What are the upsides? Green: What alternatives exist? Blue: What\'s the decision process? Spend 3 minutes per hat.' },
          { dept: 'Marketing', prompt: 'Apply Six Hats to {{campaign proposal}}. White Hat: performance data from similar campaigns. Red Hat: team emotional reactions. Black Hat: 5 failure scenarios. Yellow Hat: 5 success outcomes. Green Hat: 3 creative variations. Blue Hat: next steps.' },
          { dept: 'IT', prompt: 'Evaluate {{technology decision}} with Six Hats. White: technical specs and costs. Red: team enthusiasm vs resistance. Black: security risks, technical debt, vendor lock-in. Yellow: efficiency gains, scalability. Green: alternative architectures. Blue: implementation roadmap.' },
          { dept: 'Training', prompt: 'Apply Six Hats to {{training program}}. White: completion rates, test scores. Red: learner feedback sentiment. Black: engagement risks, knowledge retention issues. Yellow: performance improvements, career impact. Green: alternative delivery methods. Blue: rollout plan.' }
        ]
      },
      {
        name: 'Impact-Effort Matrix',
        description: 'Plot ideas by potential impact vs required effort',
        when: 'Prioritizing multiple options',
        how: 'Create 2x2 grid, plot each idea, focus on high-impact/low-effort quadrant',
        tip: 'Be honest about effort - overconfidence kills execution',
        prompts: [
          { dept: 'Product', prompt: 'Plot these {{feature ideas}} on Impact-Effort Matrix. For each: estimate effort (1-10), estimate impact on {{key metric}} (1-10). Identify top 3 high-impact/low-effort quick wins. What kills the high-effort ideas?' },
          { dept: 'Operations', prompt: 'Map {{process improvements}} to Impact-Effort grid. Impact = cost savings or time saved. Effort = implementation hours × complexity. List Quick Wins, Major Projects, Fill-Ins, and Time Wasters. What should we do this quarter?' },
          { dept: 'Quality Assurance', prompt: 'Impact-Effort matrix for {{quality improvements}}. Impact: defect reduction + customer satisfaction gain. Effort: testing time + tool costs + training. Plot 15 QA initiatives. Which quick wins should we implement immediately?' },
          { dept: 'Business Development', prompt: 'Plot {{partnership opportunities}} on matrix. Impact: revenue potential + strategic value. Effort: integration complexity + relationship building time. Identify low-hanging fruit partnerships vs long-term strategic plays.' }
        ]
      },
      {
        name: 'Pros-Cons-Fixes',
        description: 'List positives, negatives, then solutions to negatives',
        when: 'Balancing trade-offs in a specific idea',
        how: 'Column 1: pros, Column 2: cons, Column 3: ways to mitigate each con',
        tip: 'The "fixes" column often reveals the path forward',
        prompts: [
          { dept: 'Sales', prompt: 'Analyze {{pricing/commission change}}. List 5 pros, 5 cons, then propose 2 fixes for each con. Fixes must be specific and actionable. Which fixes convert the biggest cons into neutral or positive outcomes?' },
          { dept: 'Finance', prompt: 'Evaluate {{investment/software purchase}} with Pros-Cons-Fixes. Pros: quantified benefits. Cons: risks with probability estimates. Fixes: mitigation strategies with costs. Does the fixes column make this viable?' },
          { dept: 'Legal', prompt: 'Pros-Cons-Fixes for {{policy change}}. Pros: compliance improvements, risk reduction. Cons: operational friction, costs, employee resistance. Fixes: implementation approaches that preserve benefits while minimizing downsides. What makes this enforceable?' },
          { dept: 'Supply Chain', prompt: 'Analyze {{supplier change}} with Pros-Cons-Fixes. Pros: cost savings, quality, reliability. Cons: transition risks, relationship loss, quality unknowns. Fixes: pilot programs, dual sourcing, staged transitions. What de-risks the switch?' }
        ]
      },
      {
        name: 'Devil\'s Advocate',
        description: 'Systematically challenge assumptions',
        when: 'Testing idea robustness',
        how: 'Argue forcefully against the idea, then address each objection',
        tip: 'Get someone else to play devil\'s advocate - you\'ll defend more honestly',
        prompts: [
          { dept: 'Strategy', prompt: 'Play devil\'s advocate against {{strategic plan}}. Generate 10 harsh objections: why it will fail, what we\'re overlooking, flawed assumptions, market reasons it won\'t work. Then systematically dismantle each objection with evidence.' },
          { dept: 'Product', prompt: 'Attack {{product roadmap}} as devil\'s advocate. Why is this the wrong prioritization? What customer needs are we ignoring? What tech debt will this create? Why will competitors outmaneuver us? Respond to each attack with data.' },
          { dept: 'R&D', prompt: 'Challenge {{research direction}} as devil\'s advocate. Why is this scientifically questionable? What market assumptions are flawed? Why will this fail commercially? What are we missing? Counter each objection with evidence and adjusted approach.' },
          { dept: 'Communications', prompt: 'Attack {{messaging strategy}} harshly. Why will this messaging fail? What audiences are we alienating? What crisis scenarios does this create? Why will media/public reject this? Address each objection and refine the strategy.' }
        ]
      }
    ],
    lateral: [
      {
        name: 'Provocation Technique',
        description: 'Start with deliberately impossible statements',
        when: 'Stuck in conventional thinking',
        how: 'Say "What if..." then state something absurd, explore implications',
        tip: 'Example: "What if customers paid us to NOT use our product?"',
        prompts: [
          { dept: 'Sales', prompt: 'Provocation: "What if we fired our best salesperson and banned cold calling?" Explore 5 implications of each provocation. What alternative sales model emerges? Extract 2 actionable insights from the absurdity.' },
          { dept: 'Customer Success', prompt: 'Provocation: "What if customers could only contact us once per year?" and "What if we called every customer daily?" Explore extremes. What balanced approach emerges? What self-service tools become obvious?' },
          { dept: 'Procurement', prompt: 'Provocations: "What if we had only ONE supplier for everything?" and "What if we changed suppliers weekly?" Explore implications. What procurement model emerges? What relationship/flexibility balance is revealed?' },
          { dept: 'Data Analytics', prompt: 'Provocation: "What if we deleted all historical data?" and "What if we had to analyze 100x more data?" Explore both extremes. What data strategy emerges? What\'s essential vs noise?' }
        ]
      },
      {
        name: 'Reverse Thinking',
        description: 'Solve for the opposite of your goal',
        when: 'Making no progress on direct solutions',
        how: 'Ask "How would I make this problem worse?" then reverse those actions',
        tip: 'Often reveals hidden assumptions blocking your solution',
        prompts: [
          { dept: 'Marketing', prompt: 'Reverse: "How would we guarantee {{campaign}} completely fails?" List 15 ways to ensure failure. Now reverse each into a success principle. Which reversed principle is most counterintuitive?' },
          { dept: 'Operations', prompt: 'Reverse: "How could we maximize {{process}} inefficiency and cost?" Generate 12 ways to make it terrible. Reverse each. Which reversals reveal hidden optimization opportunities we\'ve been missing?' },
          { dept: 'Training', prompt: 'Reverse: "How would we ensure {{training}} teaches nothing and wastes time?" List 10 failure methods. Reverse each into teaching principles. Which reversal reveals your biggest training gap?' },
          { dept: 'Quality Assurance', prompt: 'Reverse: "How could we guarantee maximum defects in {{product}}?" Generate 15 ways to ensure quality failure. Reverse each. Which reversal suggests a QA process we\'re currently missing?' }
        ]
      },
      {
        name: 'Analogies from Other Domains',
        description: 'Apply patterns from completely different fields',
        when: 'Need fresh mental models',
        how: 'Ask "How does nature/military/theater/sports solve this?" then translate',
        tip: 'Biological systems and military strategy are goldmines for business problems',
        prompts: [
          { dept: 'Sales', prompt: 'Apply 3 domain analogies to {{sales challenge}}. Military: how would a general approach this? Nature: how do predators/ecosystems solve this? Sports: what would a championship coach do? Extract one tactic from each domain.' },
          { dept: 'HR', prompt: 'Solve {{HR challenge}} using analogies. How does: 1) An orchestra conductor handle this? 2) An immune system respond? 3) A restaurant kitchen manage this? 4) Professional sports teams address this? Translate each analogy into HR tactics.' },
          { dept: 'IT', prompt: 'Apply domain analogies to {{infrastructure challenge}}. How does: 1) A city\'s infrastructure work? 2) A biological nervous system function? 3) A power grid manage load? 4) An ant colony self-organize? Extract architectural principles.' },
          { dept: 'Supply Chain', prompt: 'Solve {{logistics problem}} with analogies. How does: 1) Blood circulation work? 2) A river delta distribute water? 3) An airport hub system operate? 4) A mycelium network share resources? What logistics model emerges?' }
        ]
      },
      {
        name: 'Constraint Removal',
        description: 'Imagine key constraints don\'t exist',
        when: 'Feeling limited by resources or rules',
        how: 'Remove budget/time/technology constraints, design ideal solution, work backward',
        tip: 'Often the "impossible" solution reveals a creative compromise',
        prompts: [
          { dept: 'Product', prompt: 'Design {{product feature}} with ZERO constraints: unlimited budget, no technical limits, perfect team, instant deployment. Describe the ideal. Now: what 20% of that vision could we achieve with current constraints? What\'s the creative compromise?' },
          { dept: 'Finance', prompt: 'Remove all constraints from {{financial process}}. Unlimited automation budget, perfect data, no compliance limits, instant reporting. Design the ideal. Work backward: what 3 changes get us 60% there within current constraints?' },
          { dept: 'Legal', prompt: 'Design ideal {{compliance solution}} with no constraints: unlimited budget, perfect technology, instant implementation, full cooperation. What does perfect look like? Work backward: what pragmatic version captures 70% of the value?' },
          { dept: 'R&D', prompt: 'Remove all constraints from {{research project}}. Unlimited funding, perfect equipment, dream team, no time pressure. Design the ideal research program. What scaled-down version delivers breakthrough results within real constraints?' }
        ]
      }
    ],
    collaborative: [
      {
        name: 'Brainwriting',
        description: 'Silent parallel idea generation',
        when: 'Avoiding groupthink or dominant voices',
        how: 'Everyone writes ideas simultaneously, rotate papers, build on others\' ideas',
        tip: 'Introverts often contribute more with this method',
        prompts: [
          { dept: 'Sales', prompt: 'Brainwriting session for {{sales initiative}}. Round 1: Each person writes 3 ideas (5 min). Round 2: Pass papers clockwise, add 2 ideas or build on existing (4 min). Round 3: Repeat. Compile all ideas. What unexpected combinations emerged?' },
          { dept: 'Marketing', prompt: 'Silent brainwriting: {{campaign challenge}}. Each team member writes 5 tactics. Pass sheets. Next person adds 3 variations to each tactic. Pass again. Third person identifies best hybrid ideas. What emerged that wouldn\'t in a meeting?' },
          { dept: 'Business Development', prompt: 'Brainwriting for {{partnership strategy}}. Round 1: Everyone writes 4 potential partner types (silent, 6 min). Round 2: Rotate, add specific company names + rationale. Round 3: Rotate, add value proposition for each. What non-obvious partnerships emerged?' },
          { dept: 'Quality Assurance', prompt: 'Silent brainwriting: {{quality issue}}. Each QA member writes 3 root causes + 2 fixes. Pass. Next person adds testing scenarios for each fix. Pass. Final person prioritizes by impact. What systematic solution emerged?' }
        ]
      },
      {
        name: 'Round Robin',
        description: 'Structured turn-taking for input',
        when: 'Ensuring equal participation',
        how: 'Each person shares one idea in turn, continue multiple rounds',
        tip: 'Don\'t allow skipping - "pass" counts as a turn',
        prompts: [
          { dept: 'Product', prompt: 'Round Robin for {{feature prioritization}}. Each person shares 1 feature with 1-sentence rationale. No discussion. Continue 5 rounds minimum. No passing. After: vote on top 5 using dot voting. What ideas emerged late that wouldn\'t have in open discussion?' },
          { dept: 'Operations', prompt: 'Structured Round Robin: {{efficiency problem}}. Person 1: shares one improvement. Person 2: adds different improvement. Continue until 20 ideas total. Track which round generates best ideas. Do later rounds show more creativity or fatigue?' },
          { dept: 'IT', prompt: 'Round Robin for {{system architecture}}. Each engineer shares one architectural decision (5 seconds, no justification). Continue 7 rounds. No skipping. After all rounds: discuss top 5 by vote. What emerged that wouldn\'t in whiteboard debates?' },
          { dept: 'Training', prompt: 'Round Robin: {{learning objectives}}. Each person names one skill employees need. One sentence only. Continue 6 rounds minimum. No discussion until complete. After: cluster similar skills. What critical gaps appeared only in late rounds?' }
        ]
      },
      {
        name: 'Nominal Group Technique',
        description: 'Combine individual and group work',
        when: 'Need both creativity and consensus',
        how: 'Individual ideation, shared listing, discussion, anonymous voting',
        tip: 'The anonymity in voting reveals true preferences',
        prompts: [
          { dept: 'Strategy', prompt: 'NGT for {{strategic decision}}. Phase 1: Silent 10-min individual brainstorm. Phase 2: Round-robin sharing (no discussion). Phase 3: Clarification only. Phase 4: Anonymous ranking (1-5). Tally votes. How does anonymous voting differ from typical meetings?' },
          { dept: 'Finance', prompt: 'Nominal Group: {{budget allocation}} across departments. Individual: list priorities with rationale (15 min). Share all. Discuss briefly. Anonymous vote: allocate $100 across options. Compare individual vs group allocation. What changed?' },
          { dept: 'Communications', prompt: 'NGT for {{messaging priorities}}. Individual: write 5 key messages (10 min). Round-robin share (no debate). Brief clarification. Anonymous ranking. What message won that wouldn\'t have in open discussion? Why does anonymity matter here?' },
          { dept: 'Procurement', prompt: 'Nominal Group: {{vendor selection criteria}}. Silent brainstorm: what matters most (12 min). Share all criteria. Clarify only. Anonymous weighting: distribute 100 points across criteria. What got high points anonymously but low voice in meetings?' }
        ]
      },
      {
        name: 'Role Storming',
        description: 'Brainstorm from another person\'s perspective',
        when: 'Breaking team mental patterns',
        how: 'Everyone adopts a different persona (customer, competitor, expert), ideates in character',
        tip: 'Choose personas who would see the problem differently than you do',
        prompts: [
          { dept: 'Sales', prompt: 'Role Storm {{sales challenge}} from 4 personas: 1) Skeptical CFO buyer, 2) Aggressive competitor, 3) Enthusiastic early adopter, 4) Burned-out procurement manager. Each persona: 5 ideas for solving challenge from their perspective. What emerges?' },
          { dept: 'Customer Success', prompt: 'Solve {{churn problem}} as: 1) Frustrated customer who just cancelled, 2) Your best customer, 3) Customer success leader at competitor, 4) Industry analyst. Each persona: what would they do? Extract best 3 ideas.' },
          { dept: 'R&D', prompt: 'Role Storm {{research direction}} as: 1) Skeptical scientist from adjacent field, 2) Venture capitalist, 3) End user with problem, 4) Competitor\'s CTO. Each persona: evaluate the research. What pivot do multiple personas suggest?' },
          { dept: 'Data Analytics', prompt: 'Approach {{analytics challenge}} as: 1) Investigative journalist, 2) Academic researcher, 3) Management consultant, 4) Data engineer. Each persona: how would they analyze this? What methodology does each persona reveal?' }
        ]
      }
    ],
    reframing: [
      {
        name: 'Five Whys',
        description: 'Dig deeper by asking "why" repeatedly',
        when: 'Surface problem masks root issue',
        how: 'State problem, ask why, use answer as next problem, repeat 5 times',
        tip: 'You know you\'re done when the answer becomes organizational or human nature',
        prompts: [
          { dept: 'Sales', prompt: 'Five Whys for {{sales problem}}. Problem: {{state problem}}. Why? {{answer}}. Why does that happen? Continue 5 levels deep. At what level does the root cause become clear? What intervention targets the actual root?' },
          { dept: 'Operations', prompt: 'Apply Five Whys to {{process failure}}. Layer 1: Why did it fail? Layer 2: Why did that cause failure? Layer 3-5: Continue deeper. Root cause is usually: inadequate process, misaligned incentives, or missing capability. Which is it?' },
          { dept: 'IT', prompt: 'Five Whys for {{system outage}}. Why did it fail? Why wasn\'t that prevented? Why wasn\'t that monitored? Why isn\'t that in the runbook? Why doesn\'t the runbook exist? What systemic fix addresses the deepest why?' },
          { dept: 'Supply Chain', prompt: 'Five Whys: {{delivery delay}}. Why was it late? Why wasn\'t that anticipated? Why isn\'t there buffer? Why can\'t we see it coming? Why don\'t we have visibility? What root cause emerges? Process, system, or relationship?' }
        ]
      },
      {
        name: 'Perspective Shifting',
        description: 'View challenge through stakeholder lenses',
        when: 'Stuck in your own viewpoint',
        how: 'Ask "How would [customer/engineer/CFO/competitor] see this?"',
        tip: 'Physically move to different locations when shifting perspectives',
        prompts: [
          { dept: 'Product', prompt: 'View {{product decision}} from 5 perspectives: Customer (what do they actually need?), Engineer (what\'s technically elegant?), Sales (what closes deals?), CFO (what\'s ROI?), Support (what creates tickets?). Which perspective reveals the biggest blind spot?' },
          { dept: 'Marketing', prompt: 'Shift perspectives on {{campaign}}. CEO view: strategic impact? CMO view: brand alignment? Sales view: lead quality? Customer view: actual value? Analyst view: market positioning? Which perspective demands a major change?' },
          { dept: 'Legal', prompt: 'View {{compliance approach}} from multiple angles: Regulator (what do they scrutinize?), Business unit (what enables revenue?), IT (what\'s implementable?), Auditor (what\'s verifiable?), Employee (what\'s practical?). What compliance model satisfies all?' },
          { dept: 'Procurement', prompt: 'Shift perspectives on {{sourcing decision}}. Finance: total cost of ownership? Operations: reliability and speed? Quality: standards and consistency? Legal: contract and risk? Supplier: their economics? What procurement strategy emerges?' }
        ]
      },
      {
        name: 'Time Travel',
        description: 'Project to past or future to gain insight',
        when: 'Present constraints feel overwhelming',
        how: 'Ask "What would we do if this was 1990? 2050?" or "What will we wish we had done?"',
        tip: 'The future perspective reveals values, the past reveals resources',
        prompts: [
          { dept: 'Strategy', prompt: 'Time travel for {{strategy}}. Past (1995): How would we solve this with only phones, fax, human networks? Future (2035): How would this be solved with perfect AI, infinite data, instant global coordination? What does each era teach us?' },
          { dept: 'HR', prompt: 'Project to 2030: You\'re reviewing today\'s {{HR decision}}. What do you wish you had done differently? What trend did you miss? Now return to present: what decision does future-you demand?' },
          { dept: 'Business Development', prompt: 'Time travel {{partnership decision}}. Past (2000): How would we build this relationship pre-internet? Future (2040): How will market consolidation/AI change this? What timeless principle vs temporary tactic emerges?' },
          { dept: 'Training', prompt: 'Project to 2032: How will employees learn {{skill}} then? AI tutors? VR? Brain-computer interface? Now: what training investment today prepares for that future? What current method will seem ancient?' }
        ]
      },
      {
        name: 'Problem Redefinition',
        description: 'Rewrite the problem statement itself',
        when: 'Making no progress on current problem',
        how: 'Write 5 different versions of the problem, pick the most interesting',
        tip: 'Change scale, scope, stakeholders, or desired outcome',
        prompts: [
          { dept: 'Sales', prompt: 'Redefine {{sales problem}} 5 ways. Version 1: Narrow the scope. Version 2: Expand the scope. Version 3: Change the stakeholder. Version 4: Flip the desired outcome. Version 5: Reframe as an opportunity. Which reframe makes the solution obvious?' },
          { dept: 'Operations', prompt: 'Current problem: {{state problem}}. Rewrite it as: 1) A people problem, 2) A technology problem, 3) A process problem, 4) A measurement problem, 5) A strategic misalignment. Which reframing reveals the real issue?' },
          { dept: 'Data Analytics', prompt: 'Redefine {{analytics challenge}} 5 ways: 1) Data quality problem, 2) Wrong question problem, 3) Tool limitation problem, 4) Organizational adoption problem, 5) Insights-to-action problem. Which reframe changes the solution completely?' },
          { dept: 'Communications', prompt: 'Reframe {{communications challenge}}: 1) As a listening problem, 2) As a timing problem, 3) As a messenger problem, 4) As a channel problem, 5) As an expectations problem. Which reframe reveals root cause?' }
        ]
      }
    ],
    structured: [
      {
        name: 'TRIZ Principles',
        description: '40 inventive principles from patent analysis',
        when: 'Engineering or technical innovation',
        how: 'Match your contradiction to TRIZ categories, apply suggested principles',
        tip: 'Segmentation, asymmetry, and "taking out" are surprisingly versatile',
        prompts: [
          { dept: 'Product', prompt: 'Apply TRIZ to {{product trade-off}}. Contradiction: {{describe opposing requirements}}. Try these principles: 1) Segmentation (divide into parts), 2) Taking out (remove problematic element), 3) Asymmetry (make it non-uniform), 4) Dynamics (make it adaptive). Which principle resolves the contradiction?' },
          { dept: 'Operations', prompt: 'TRIZ for {{process problem}}. Identify the contradiction: we need {{X}} but that requires {{Y}} which conflicts with {{Z}}. Apply: Beforehand cushioning, Intermediary, Self-service, Copying. Which principle suggests a breakthrough?' },
          { dept: 'Quality Assurance', prompt: 'TRIZ for {{quality vs speed}} contradiction. We need thorough testing but also fast releases. Apply principles: 1) Prior action (test earlier), 2) Intermediary (automated testing layer), 3) Self-service (developers self-test), 4) Partial or excessive (over-test critical paths only). What resolves it?' },
          { dept: 'IT', prompt: 'Apply TRIZ to {{security vs usability}} trade-off. Try: 1) Segmentation (different security tiers), 2) Asymmetry (adaptive authentication), 3) Another dimension (biometrics), 4) Dynamics (risk-based security). Which principle works best?' }
        ]
      },
      {
        name: 'Morphological Analysis',
        description: 'Systematically combine attributes',
        when: 'Exploring all possible combinations',
        how: 'List key attributes, list options for each, combine in new ways',
        tip: 'Creates completeness but can be overwhelming - prioritize combinations',
        prompts: [
          { dept: 'Marketing', prompt: 'Morphological box for {{campaign type}}. Attributes: Channel (email/social/events/PR), Message (fear/aspiration/logic/emotion), Timing (morning/evening/weekend), Offer (trial/demo/discount/content). Create grid. Combine 10 unusual pairings. Which combination is most novel?' },
          { dept: 'Sales', prompt: 'Build morphological matrix for {{sales approach}}. Dimensions: Outreach (cold/warm/referral), Content (case study/demo/ROI calc), Frequency (daily/weekly/monthly), Incentive (discount/free trial/consulting). Generate 15 combinations. Which are we not testing?' },
          { dept: 'Training', prompt: 'Morphological analysis for {{training program}}. Dimensions: Format (live/recorded/hybrid), Duration (1-hour/1-day/weekly), Content (lecture/hands-on/case study), Assessment (test/project/peer review). Generate 12 combinations. Which matches learning objectives best?' },
          { dept: 'Procurement', prompt: 'Build morphological matrix for {{supplier strategy}}. Dimensions: Relationship (transactional/partnership/strategic), Geography (local/regional/global), Volume (single/split/diverse), Contract (spot/annual/multi-year). Create 15 combinations. What strategy emerges?' }
        ]
      },
      {
        name: 'Attribute Listing',
        description: 'Break down and modify each component',
        when: 'Improving a specific product or process',
        how: 'List all attributes, systematically change each one',
        tip: 'Change size, material, color, shape, weight, time, location',
        prompts: [
          { dept: 'Product', prompt: 'List all attributes of {{product/feature}}: Size, Speed, Material, Cost, Complexity, Frequency, Location, User type. For each attribute, generate 3 variations (increase, decrease, eliminate). Which variation is most valuable?' },
          { dept: 'Finance', prompt: 'Attributes of {{financial process}}: Frequency (monthly→daily?), Automation level (manual→full auto?), Detail level (summary→granular?), Distribution (who gets it?), Format (spreadsheet→dashboard?). Modify each. What\'s the optimized version?' },
          { dept: 'Business Development', prompt: 'List attributes of {{partnership model}}: Duration, Revenue share, Exclusivity, Geography, Integration depth, Support level, Commitment. Modify each systematically. What partnership structure is most attractive to ideal partners?' },
          { dept: 'Data Analytics', prompt: 'Attributes of {{analytics dashboard}}: Update frequency, Granularity, Visualization type, Interactivity, Data freshness, User segments, Delivery method. Modify each. Which modifications drive the most adoption and action?' }
        ]
      },
      {
        name: 'Forced Connections',
        description: 'Combine unrelated elements systematically',
        when: 'Need breakthrough vs incremental ideas',
        how: 'List elements of problem, list random objects/concepts, force pairings',
        tip: 'The discomfort of forced connections is where creativity lives',
        prompts: [
          { dept: 'Sales', prompt: 'Force connections between {{sales challenge}} and these random concepts: LIBRARY, GARDENING, SURGERY, JAZZ BAND. For each: force 3 connections. Example: "Library→organize leads like books in Dewey Decimal". What unexpected tactic emerges?' },
          { dept: 'Customer Success', prompt: 'Connect {{CS metric}} with: BEEHIVE, MARATHON, RESTAURANT KITCHEN, CHESS TOURNAMENT. Force analogies. Beehive→what does swarm intelligence teach about CS? Marathon→what does pacing teach? Extract one novel approach from each forced connection.' },
          { dept: 'Legal', prompt: 'Force connections between {{compliance challenge}} and: IMMUNE SYSTEM, TRAFFIC FLOW, AIRPORT SECURITY, THERMOSTAT. How does each system balance protection vs flow? What compliance model emerges from biological/physical analogies?' },
          { dept: 'R&D', prompt: 'Connect {{research challenge}} with random domains: JAZZ IMPROVISATION, ECOSYSTEM SUCCESSION, SURGICAL TRIAGE, GAME THEORY. Force 4 connections per domain. What research methodology or prioritization emerges from unlikely parallels?' }
        ]
      }
    ]
  };

  // Extract all unique departments from prompts
  const allDepartments = [...new Set(
    Object.values(techniques)
      .flat()
      .flatMap(tech => tech.prompts?.map(p => p.dept) || [])
  )].sort();

  // Filter techniques based on selected department
  const getFilteredTechniques = (categoryTechniques) => {
    if (!selectedDepartment) return categoryTechniques;
    return categoryTechniques.filter(tech => 
      tech.prompts?.some(p => p.dept === selectedDepartment)
    );
  };

  // Count prompts per department
  const getDepartmentCount = (dept) => {
    return Object.values(techniques)
      .flat()
      .reduce((count, tech) => {
        return count + (tech.prompts?.filter(p => p.dept === dept).length || 0);
      }, 0);
  };

  const CategoryCard = ({ category }) => {
    const Icon = category.icon;
    return (
      <button
        onClick={() => {
          setSelectedCategory(category.id);
          setSelectedTechnique(null);
        }}
        className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-all border-2 border-transparent hover:border-gray-300 text-left w-full"
      >
        <div className="flex items-start gap-4">
          <div className={`${category.color} p-3 rounded-lg`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-lg mb-1">{category.name}</h3>
            <p className="text-gray-600 text-sm">{category.description}</p>
          </div>
          <ChevronRight className="w-5 h-5 text-gray-400 mt-1" />
        </div>
      </button>
    );
  };

  const TechniqueCard = ({ technique }) => {
    const isSelected = selectedTechnique?.name === technique.name;
    const filteredPrompts = selectedDepartment 
      ? technique.prompts?.filter(p => p.dept === selectedDepartment)
      : technique.prompts;
    
    return (
      <div className="bg-white rounded-lg shadow-md overflow-hidden border-2 border-transparent hover:border-gray-300 transition-all">
        <button
          onClick={() => setSelectedTechnique(isSelected ? null : technique)}
          className="w-full p-4 text-left flex justify-between items-center"
        >
          <div>
            <h4 className="font-bold text-base">{technique.name}</h4>
            <p className="text-sm text-gray-600 mt-1">{technique.description}</p>
          </div>
          <ChevronRight className={`w-5 h-5 text-gray-400 transition-transform ${isSelected ? 'rotate-90' : ''}`} />
        </button>
        
        {isSelected && (
          <div className="px-4 pb-4 space-y-3 border-t pt-3">
            <div>
              <span className="font-semibold text-sm text-gray-700">When to use:</span>
              <p className="text-sm text-gray-600 mt-1">{technique.when}</p>
            </div>
            <div>
              <span className="font-semibold text-sm text-gray-700">How it works:</span>
              <p className="text-sm text-gray-600 mt-1">{technique.how}</p>
            </div>
            <div className="bg-amber-50 p-3 rounded">
              <span className="font-semibold text-sm text-amber-800">💡 Pro tip:</span>
              <p className="text-sm text-amber-900 mt-1">{technique.tip}</p>
            </div>
            
            {filteredPrompts && filteredPrompts.length > 0 && (
              <div className="space-y-3 mt-4 pt-3 border-t">
                <h5 className="font-semibold text-sm text-gray-700">📋 Ready-to-Use Prompts:</h5>
                {filteredPrompts.map((prompt, idx) => (
                  <div key={idx} className="bg-blue-50 p-3 rounded border-l-2 border-blue-500">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-bold text-blue-700 bg-blue-200 px-2 py-1 rounded">{prompt.dept}</span>
                    </div>
                    <p className="text-sm text-gray-800 font-mono leading-relaxed">{prompt.prompt}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Creative Thinking Explorer</h1>
          <p className="text-gray-600">Interactive guide to proven creative problem-solving techniques</p>
        </div>

        {/* Department Filter */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-semibold text-gray-700">Filter by Department:</span>
            <button
              onClick={() => {
                setSelectedDepartment(null);
                setSelectedTechnique(null);
              }}
              className={`px-3 py-1 rounded-full text-sm transition-all ${
                !selectedDepartment 
                  ? 'bg-gray-800 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              All Departments
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {allDepartments.map(dept => (
              <button
                key={dept}
                onClick={() => {
                  setSelectedDepartment(dept === selectedDepartment ? null : dept);
                  setSelectedTechnique(null);
                }}
                className={`px-3 py-1 rounded-full text-sm transition-all ${
                  selectedDepartment === dept
                    ? 'bg-blue-600 text-white'
                    : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
                }`}
              >
                {dept} ({getDepartmentCount(dept)})
              </button>
            ))}
          </div>
        </div>

        {!selectedCategory ? (
          <div>
            {selectedDepartment && (
              <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200 flex items-center justify-between">
                <span className="text-sm text-blue-800">
                  <strong>Filtered by:</strong> {selectedDepartment} ({getDepartmentCount(selectedDepartment)} prompts)
                </span>
                <button
                  onClick={() => setSelectedDepartment(null)}
                  className="text-blue-600 hover:text-blue-800 text-sm underline"
                >
                  Clear filter
                </button>
              </div>
            )}
            <p className="text-center text-gray-600 mb-6">Choose a category to explore techniques:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {categories.map(category => (
                <CategoryCard key={category.id} category={category} />
              ))}
            </div>
          </div>
        ) : (
          <div>
            <button
              onClick={() => {
                setSelectedCategory(null);
                setSelectedTechnique(null);
              }}
              className="mb-6 text-blue-600 hover:text-blue-800 flex items-center gap-2 font-medium"
            >
              ← Back to categories
            </button>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <div className="flex items-center gap-4">
                {(() => {
                  const category = categories.find(c => c.id === selectedCategory);
                  const Icon = category.icon;
                  return (
                    <>
                      <div className={`${category.color} p-3 rounded-lg`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-800">{category.name}</h2>
                        <p className="text-gray-600">{category.description}</p>
                      </div>
                    </>
                  );
                })()}
              </div>
            </div>

            <div className="space-y-3">
              {getFilteredTechniques(techniques[selectedCategory]).map((technique, idx) => (
                <TechniqueCard key={idx} technique={technique} />
              ))}
              {getFilteredTechniques(techniques[selectedCategory]).length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <p>No techniques found for {selectedDepartment}.</p>
                  <button
                    onClick={() => setSelectedDepartment(null)}
                    className="mt-4 text-blue-600 hover:text-blue-800 underline"
                  >
                    Clear filter
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Click any technique to see when to use it, how it works, pro tips, and department-specific prompts</p>
          <p className="mt-1 text-xs">96 ready-to-use prompts across {allDepartments.length} departments including Sales, Marketing, Finance, Operations, Product, HR, Strategy, Customer Success, IT, Legal, R&D, Supply Chain, Business Development, Communications, Data Analytics, Procurement, Quality Assurance, and Training</p>
        </div>
      </div>
    </div>
  );
};

export default CreativeThinkingExplorer;