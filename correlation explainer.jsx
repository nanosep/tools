import React, { useState, useEffect, useCallback } from 'react';
import { ArrowRight, ArrowLeft, ArrowUpDown, Circle, Shuffle, Eye, EyeOff, ChevronDown, ChevronUp, Play, Pause, RotateCcw, HelpCircle, CheckCircle, XCircle, Lightbulb, BookOpen, FlaskConical, Target, AlertTriangle, Info } from 'lucide-react';

const correlationTypes = [
  {
    id: 'causation',
    title: 'Direct Causation',
    subtitle: 'A actually causes B',
    icon: 'arrow-right',
    color: '#22c55e',
    lightColor: '#bbf7d0',
    examples: [
      { a: 'Smoking', b: 'Lung Cancer', explanation: 'Cigarette smoke contains carcinogens that directly damage lung tissue and DNA, leading to cancer. Mechanism is well-understood at the molecular level.' },
      { a: 'Aspirin', b: 'Reduced Blood Clots', explanation: 'Aspirin inhibits cyclooxygenase enzymes, reducing thromboxane production and platelet aggregation. Clear biochemical pathway.' },
      { a: 'Seatbelt Use', b: 'Crash Survival', explanation: 'Seatbelts physically restrain occupants, distributing crash forces across stronger body parts and preventing ejection.' }
    ],
    description: 'Variable A directly causes changes in Variable B through a clear, identifiable mechanism. This is what most people assume when they see correlation, but it\'s actually the least common explanation.',
    keyQuestion: 'Is there a plausible mechanism by which A could cause B?',
    howToTest: [
      { method: 'Randomized Controlled Trial', description: 'Gold standard—randomly assign A, measure B', difficulty: 'Hard' },
      { method: 'Dose-Response Relationship', description: 'More A = proportionally more B?', difficulty: 'Medium' },
      { method: 'Temporal Sequence', description: 'Does A consistently precede B?', difficulty: 'Easy' },
      { method: 'Mechanism Identification', description: 'Can you explain HOW A causes B?', difficulty: 'Medium' }
    ],
    realWorld: 'Establishing true causation typically requires controlled experiments, which are often impossible or unethical with humans.',
    probability: 15,
    probabilityLabel: 'Uncommon',
    dangerLevel: 'low',
    commonMistakes: [
      'Assuming correlation implies causation',
      'Ignoring alternative explanations',
      'Confusing temporal sequence with causation'
    ],
    historicalExample: {
      title: 'Semmelweis & Handwashing',
      story: 'In 1847, Ignaz Semmelweis noticed doctors who performed autopsies had higher patient death rates. He hypothesized "cadaverous particles" caused infections. Handwashing reduced maternal mortality from 18% to 2%. Despite clear evidence, doctors rejected his theory for decades because the mechanism (germs) wasn\'t yet understood.'
    }
  },
  {
    id: 'reverse',
    title: 'Reverse Causation',
    subtitle: 'B actually causes A',
    icon: 'arrow-left',
    color: '#f59e0b',
    lightColor: '#fef3c7',
    examples: [
      { a: 'Hospital Visits', b: 'Death Rate', explanation: 'People don\'t die because they visit hospitals—they visit hospitals because they\'re already sick. The illness causes both.' },
      { a: 'Antidepressant Use', b: 'Suicide Risk', explanation: 'Early studies suggested antidepressants increased suicide risk. Actually, severely depressed people (higher suicide risk) are more likely to be prescribed antidepressants.' },
      { a: 'Low Cholesterol', b: 'Cancer', explanation: 'Some studies found low cholesterol correlated with cancer. But cancer itself can lower cholesterol levels, not the reverse.' }
    ],
    description: 'We naturally assume A causes B, but the causal arrow actually points backward. B causes A. This is especially common in health research where illness drives behavior.',
    keyQuestion: 'Could B be causing A instead of the other way around?',
    howToTest: [
      { method: 'Temporal Analysis', description: 'Which variable actually changes first?', difficulty: 'Medium' },
      { method: 'Prospective Studies', description: 'Measure A before B can occur', difficulty: 'Hard' },
      { method: 'Mechanism Plausibility', description: 'Is reverse causation mechanistically possible?', difficulty: 'Easy' },
      { method: 'Instrumental Variables', description: 'Find a variable that affects A but not B directly', difficulty: 'Hard' }
    ],
    realWorld: 'Extremely common in observational health studies. Always ask: "What if the arrow points the other way?"',
    probability: 20,
    probabilityLabel: 'Common',
    dangerLevel: 'high',
    commonMistakes: [
      'Assuming the "obvious" direction is correct',
      'Ignoring that sick people behave differently',
      'Not considering bidirectional relationships'
    ],
    historicalExample: {
      title: 'Hormone Replacement Therapy',
      story: 'For decades, observational studies showed HRT reduced heart disease in women. Doctors widely prescribed it. Then randomized trials (WHI, 2002) showed HRT actually INCREASED heart disease risk. The original correlation existed because healthier, wealthier women were more likely to take HRT—and more likely to have good heart health anyway.'
    }
  },
  {
    id: 'confounding',
    title: 'Confounding Variable',
    subtitle: 'C causes both A and B',
    icon: 'hidden',
    color: '#ef4444',
    lightColor: '#fecaca',
    examples: [
      { a: 'Ice Cream Sales', b: 'Drowning Deaths', explanation: 'Summer weather (confounder) causes both. Hot days → more ice cream AND more swimming → more drownings.' },
      { a: 'Shoe Size', b: 'Reading Ability', explanation: 'Age is the confounder. Older children have bigger feet AND read better. Shoes don\'t teach reading.' },
      { a: 'Yellow Fingers', b: 'Lung Cancer', explanation: 'Smoking causes both yellow fingers (tar stains) and lung cancer. Cleaning your fingers won\'t prevent cancer.' }
    ],
    description: 'A hidden third variable causes both A and B, creating a spurious correlation between them. This is the MOST common explanation for correlations that aren\'t causal.',
    keyQuestion: 'What third variable could be driving both A and B?',
    howToTest: [
      { method: 'Statistical Control', description: 'Control for suspected confounders in analysis', difficulty: 'Medium' },
      { method: 'Stratification', description: 'Analyze relationship within subgroups', difficulty: 'Medium' },
      { method: 'Randomization', description: 'Random assignment eliminates confounding', difficulty: 'Hard' },
      { method: 'DAG Analysis', description: 'Draw causal diagrams to identify confounders', difficulty: 'Medium' }
    ],
    realWorld: 'The most common cause of spurious correlations. With any correlation, your first question should be: "What else could explain this?"',
    probability: 35,
    probabilityLabel: 'Very Common',
    dangerLevel: 'high',
    commonMistakes: [
      'Failing to consider unmeasured confounders',
      'Assuming statistical control is sufficient',
      'Not drawing causal diagrams before analysis'
    ],
    historicalExample: {
      title: 'Coffee & Lung Cancer',
      story: 'Early studies found coffee drinkers had higher lung cancer rates. Panic ensued. But researchers failed to control for smoking—and coffee drinkers were much more likely to smoke. Once smoking was controlled for, the coffee-cancer link disappeared. Smoking was the confounder.'
    }
  },
  {
    id: 'mediator',
    title: 'Mediated Causation',
    subtitle: 'A → M → B (chain reaction)',
    icon: 'chain',
    color: '#8b5cf6',
    lightColor: '#ddd6fe',
    examples: [
      { a: 'Education', b: 'Income', explanation: 'Education → Better job opportunities (mediator) → Higher income. The relationship is real but indirect.' },
      { a: 'Exercise', b: 'Weight Loss', explanation: 'Exercise → Increased metabolism + Muscle mass (mediators) → Weight loss. Multiple pathways exist.' },
      { a: 'Poverty', b: 'Crime', explanation: 'Poverty → Reduced opportunities + Stress + Desperation (mediators) → Property crime. Complex causal chain.' }
    ],
    description: 'A does cause B, but through one or more intermediate variables. Understanding the mediator helps identify intervention points and explains WHY the relationship exists.',
    keyQuestion: 'What\'s the mechanism? What intermediate steps connect A to B?',
    howToTest: [
      { method: 'Mediation Analysis', description: 'Decompose direct and indirect effects', difficulty: 'Medium' },
      { method: 'Path Analysis', description: 'Model the full causal chain', difficulty: 'Hard' },
      { method: 'Intervention Studies', description: 'Block the mediator, see if effect disappears', difficulty: 'Hard' },
      { method: 'Sequential Testing', description: 'Verify A→M and M→B separately', difficulty: 'Medium' }
    ],
    realWorld: 'Understanding mediators is crucial for designing interventions. Sometimes targeting the mediator is easier than targeting the root cause.',
    probability: 25,
    probabilityLabel: 'Common',
    dangerLevel: 'low',
    commonMistakes: [
      'Treating mediators as confounders (very different!)',
      'Over-controlling for mediators, hiding true effects',
      'Assuming single mediator when multiple exist'
    ],
    historicalExample: {
      title: 'Smoking → Cancer Mechanism',
      story: 'For decades, tobacco companies argued correlation wasn\'t causation. The breakthrough came from identifying mediators: Smoking → DNA damage (via carcinogens like benzo[a]pyrene) → Mutation in tumor suppressor genes (p53, KRAS) → Uncontrolled cell growth → Cancer. Mapping the chain made causation undeniable.'
    }
  },
  {
    id: 'bidirectional',
    title: 'Bidirectional Causation',
    subtitle: 'A ⇄ B (feedback loop)',
    icon: 'bidirectional',
    color: '#06b6d4',
    lightColor: '#cffafe',
    examples: [
      { a: 'Exercise', b: 'Mental Health', explanation: 'Exercise improves mood (endorphins, routine). Better mood increases motivation to exercise. A virtuous cycle.' },
      { a: 'Poverty', b: 'Poor Health', explanation: 'Poverty causes poor health (stress, nutrition, healthcare access). Poor health causes poverty (lost wages, medical costs). Vicious cycle.' },
      { a: 'Confidence', b: 'Success', explanation: 'Confidence leads to taking risks and performing better. Success reinforces confidence. Self-fulfilling prophecy.' }
    ],
    description: 'Both directions of causation are true simultaneously. A causes B AND B causes A. This creates feedback loops—either virtuous cycles (positive outcomes) or vicious cycles (negative outcomes).',
    keyQuestion: 'Could both directions of causation be true? Is there a feedback loop?',
    howToTest: [
      { method: 'Cross-Lagged Panel', description: 'Measure both variables at multiple time points', difficulty: 'Hard' },
      { method: 'Granger Causality', description: 'Test if past A predicts future B and vice versa', difficulty: 'Hard' },
      { method: 'Intervention Both Ways', description: 'Experimentally manipulate each variable', difficulty: 'Hard' },
      { method: 'Systems Modeling', description: 'Model the feedback loop mathematically', difficulty: 'Hard' }
    ],
    realWorld: 'Common in complex adaptive systems: economics, social dynamics, biology. Breaking vicious cycles often requires intervening on both variables.',
    probability: 15,
    probabilityLabel: 'Common in complex systems',
    dangerLevel: 'medium',
    commonMistakes: [
      'Forcing a single causal direction',
      'Ignoring feedback dynamics',
      'Underestimating intervention difficulty'
    ],
    historicalExample: {
      title: 'The Poverty-Crime Cycle',
      story: 'Researchers long debated: Does poverty cause crime, or do crime-ridden areas become poor? Longitudinal studies show both are true. Poverty increases crime through limited opportunities. Crime decreases property values and business investment, deepening poverty. Breaking the cycle requires addressing both simultaneously.'
    }
  },
  {
    id: 'chance',
    title: 'Random Chance',
    subtitle: 'Statistical noise (no real relationship)',
    icon: 'shuffle',
    color: '#64748b',
    lightColor: '#e2e8f0',
    examples: [
      { a: 'Nicolas Cage Films', b: 'Pool Drownings', explanation: 'Correlated r=0.67 from 1999-2009. Pure coincidence. With enough variables, some will correlate by chance.' },
      { a: 'Cheese Consumption', b: 'Bedsheet Tangling Deaths', explanation: 'Another spurious correlation (r=0.95). Demonstrates that correlation strength doesn\'t imply causation.' },
      { a: 'Margarine Consumption', b: 'Maine Divorce Rate', explanation: 'Correlated r=0.99 over a decade. Both declined for unrelated reasons. Perfect correlation, zero causation.' }
    ],
    description: 'No real relationship exists. The correlation appeared by random chance, especially when testing many variables. This is statistically guaranteed when you look at enough data.',
    keyQuestion: 'Could this be coincidence? How many comparisons were made?',
    howToTest: [
      { method: 'Replication', description: 'Does it hold in new, independent data?', difficulty: 'Medium' },
      { method: 'Multiple Comparison Correction', description: 'Bonferroni, FDR adjustment', difficulty: 'Easy' },
      { method: 'Effect Size', description: 'Is the effect practically meaningful?', difficulty: 'Easy' },
      { method: 'Pre-Registration', description: 'Specify hypotheses before seeing data', difficulty: 'Medium' }
    ],
    realWorld: 'If you test 20 hypotheses at p<0.05, you\'ll get ~1 false positive by chance. Data mining without correction guarantees spurious findings.',
    probability: 30,
    probabilityLabel: 'Guaranteed at scale',
    dangerLevel: 'high',
    commonMistakes: [
      'Not adjusting for multiple comparisons',
      'Cherry-picking significant results',
      'Confusing statistical and practical significance'
    ],
    historicalExample: {
      title: 'The Replication Crisis',
      story: 'In 2015, scientists tried to replicate 100 psychology studies. Only 36% replicated. Many original findings were likely false positives from small samples, p-hacking, and publication bias. This sparked a revolution in scientific methodology, emphasizing pre-registration, larger samples, and replication.'
    }
  },
  {
    id: 'selection',
    title: 'Selection Bias',
    subtitle: 'Biased sample creates illusion',
    icon: 'filter',
    color: '#ec4899',
    lightColor: '#fbcfe8',
    examples: [
      { a: 'Attractiveness', b: 'Niceness (on dating apps)', explanation: 'You might think attractive people are less nice. But you only see attractive people who bothered making good profiles. Boring attractive people get no matches.' },
      { a: 'Company Age', b: 'Success', explanation: 'Survivorship bias: You only see successful old companies. Failed companies don\'t survive to be studied. Old ≠ successful; survival requires success.' },
      { a: 'Hospital Quality', b: 'Death Rate', explanation: 'Top hospitals often have higher death rates because they treat the sickest patients. Comparing raw rates is misleading.' }
    ],
    description: 'The correlation exists in your sample because of how subjects were selected, but doesn\'t exist in the general population. The selection process created the illusion.',
    keyQuestion: 'Is my sample representative? What filtering created this dataset?',
    howToTest: [
      { method: 'Population Comparison', description: 'Compare sample demographics to population', difficulty: 'Medium' },
      { method: 'Selection Model', description: 'Model the selection process explicitly', difficulty: 'Hard' },
      { method: 'Sensitivity Analysis', description: 'How much selection bias would change conclusions?', difficulty: 'Medium' },
      { method: 'Random Sampling', description: 'Use probability sampling when possible', difficulty: 'Medium' }
    ],
    realWorld: 'Survivorship bias, Berkson\'s paradox, and collider bias are all forms of selection bias. Ask: "Who\'s missing from this data?"',
    probability: 25,
    probabilityLabel: 'Very common',
    dangerLevel: 'high',
    commonMistakes: [
      'Only looking at survivors/successes',
      'Using convenience samples',
      'Ignoring who opted out or was excluded'
    ],
    historicalExample: {
      title: 'WWII Airplane Armor',
      story: 'Military analyzed bullet holes in returning planes to decide where to add armor. Statistician Abraham Wald pointed out the flaw: They were only seeing planes that SURVIVED. The holes showed where planes could be hit and survive. They needed to armor the places with NO holes—those hits were fatal, and those planes never returned.'
    }
  },
  {
    id: 'ecological',
    title: 'Ecological Fallacy',
    subtitle: 'Group patterns ≠ Individual patterns',
    icon: 'group',
    color: '#14b8a6',
    lightColor: '#ccfbf1',
    examples: [
      { a: 'Country Chocolate Consumption', b: 'Country Nobel Prizes', explanation: 'Countries eating more chocolate have more Nobels. But this doesn\'t mean chocolate makes individuals smarter. Wealthy countries have both more chocolate AND better research institutions.' },
      { a: 'State Education Spending', b: 'State Test Scores', explanation: 'States spending more may have lower scores if they\'re spending more because students are struggling. Aggregate data hides individual effects.' },
      { a: 'Neighborhood Income', b: 'Neighborhood Crime', explanation: 'Poor neighborhoods have more crime, but most poor individuals commit no crimes. Individual behavior differs from group statistics.' }
    ],
    description: 'A correlation exists at the group/aggregate level but doesn\'t apply to individuals. Making individual predictions from group data is a logical error.',
    keyQuestion: 'Am I assuming group-level patterns apply to individuals?',
    howToTest: [
      { method: 'Multi-Level Analysis', description: 'Analyze both group and individual levels', difficulty: 'Hard' },
      { method: 'Individual Data', description: 'Get individual-level data when possible', difficulty: 'Medium' },
      { method: 'Within-Group Variation', description: 'Check if pattern holds within groups', difficulty: 'Medium' },
      { method: 'Simpson\'s Paradox Check', description: 'See if relationship reverses at different levels', difficulty: 'Medium' }
    ],
    realWorld: 'Common in policy debates using country or state-level data. Individual behavior is hidden in averages.',
    probability: 20,
    probabilityLabel: 'Common with aggregate data',
    dangerLevel: 'medium',
    commonMistakes: [
      'Using country-level data for individual claims',
      'Ignoring within-group variation',
      'Treating averages as universal truths'
    ],
    historicalExample: {
      title: 'Simpson\'s Paradox in UC Berkeley Admissions',
      story: 'In 1973, Berkeley was sued for gender discrimination: 44% of male applicants were admitted vs. 35% of females. But when analyzed by department, women had equal or higher admission rates in most departments. Women applied more to competitive departments with low admission rates. The aggregate pattern reversed at the individual level.'
    }
  }
];

// Interactive Scatterplot Simulation Component
const ScatterSimulation = ({ type, isPlaying, onTogglePlay }) => {
  const [points, setPoints] = useState([]);
  const [frame, setFrame] = useState(0);
  
  const generatePoints = useCallback(() => {
    const newPoints = [];
    const n = 50;
    
    switch(type) {
      case 'causation':
        // Clear linear relationship A → B
        for (let i = 0; i < n; i++) {
          const a = Math.random() * 100;
          const b = a * 0.8 + (Math.random() - 0.5) * 20 + 10;
          newPoints.push({ x: a, y: Math.max(0, Math.min(100, b)), type: 'normal' });
        }
        break;
      case 'reverse':
        // Same pattern but labeled differently
        for (let i = 0; i < n; i++) {
          const b = Math.random() * 100;
          const a = b * 0.8 + (Math.random() - 0.5) * 20 + 10;
          newPoints.push({ x: Math.max(0, Math.min(100, a)), y: b, type: 'normal' });
        }
        break;
      case 'confounding':
        // Two clusters based on confounder
        for (let i = 0; i < n; i++) {
          const c = Math.random() > 0.5; // confounder (e.g., summer)
          const a = c ? 60 + Math.random() * 30 : 10 + Math.random() * 30;
          const b = c ? 60 + Math.random() * 30 : 10 + Math.random() * 30;
          newPoints.push({ x: a + (Math.random() - 0.5) * 15, y: b + (Math.random() - 0.5) * 15, type: c ? 'confounder-high' : 'confounder-low' });
        }
        break;
      case 'chance':
        // Random scatter, no relationship
        for (let i = 0; i < n; i++) {
          newPoints.push({ x: Math.random() * 100, y: Math.random() * 100, type: 'normal' });
        }
        break;
      case 'selection':
        // Only show points that pass a selection filter
        for (let i = 0; i < n * 2; i++) {
          const x = Math.random() * 100;
          const y = Math.random() * 100;
          // Selection: only see points where x + y > 80 (e.g., survivorship)
          if (x + y > 80) {
            newPoints.push({ x, y, type: 'selected' });
          } else if (newPoints.length < n * 0.3) {
            newPoints.push({ x, y, type: 'hidden' });
          }
        }
        break;
      case 'bidirectional':
        // Spiral/cycle pattern suggesting feedback
        for (let i = 0; i < n; i++) {
          const t = (i / n) * Math.PI * 2;
          const r = 30 + i * 0.5;
          const x = 50 + r * Math.cos(t) * 0.5 + (Math.random() - 0.5) * 10;
          const y = 50 + r * Math.sin(t) * 0.5 + (Math.random() - 0.5) * 10;
          newPoints.push({ x: Math.max(5, Math.min(95, x)), y: Math.max(5, Math.min(95, y)), type: 'normal', order: i });
        }
        break;
      case 'mediator':
        // Chain: A correlates with M, M correlates with B
        for (let i = 0; i < n; i++) {
          const a = Math.random() * 100;
          const m = a * 0.7 + (Math.random() - 0.5) * 20 + 15;
          const b = m * 0.7 + (Math.random() - 0.5) * 20 + 15;
          newPoints.push({ x: a, y: Math.max(0, Math.min(100, b)), m: Math.max(0, Math.min(100, m)), type: 'normal' });
        }
        break;
      case 'ecological':
        // Groups with different internal patterns
        const groups = ['A', 'B', 'C', 'D'];
        groups.forEach((g, gi) => {
          const baseX = 20 + gi * 20;
          const baseY = 80 - gi * 15;
          for (let i = 0; i < 12; i++) {
            // Negative relationship within groups, positive between group means
            const x = baseX + (Math.random() - 0.5) * 15;
            const y = baseY - (x - baseX) * 0.3 + (Math.random() - 0.5) * 10;
            newPoints.push({ x, y: Math.max(5, Math.min(95, y)), group: g, type: 'grouped' });
          }
        });
        break;
      default:
        for (let i = 0; i < n; i++) {
          newPoints.push({ x: Math.random() * 100, y: Math.random() * 100, type: 'normal' });
        }
    }
    return newPoints;
  }, [type]);

  useEffect(() => {
    setPoints(generatePoints());
    setFrame(0);
  }, [type, generatePoints]);

  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setFrame(f => f + 1);
      if (frame % 60 === 0) {
        setPoints(generatePoints());
      }
    }, 50);
    return () => clearInterval(interval);
  }, [isPlaying, frame, generatePoints]);

  const getPointColor = (point) => {
    if (point.type === 'hidden') return 'rgba(100,100,100,0.2)';
    if (point.type === 'confounder-high') return '#f59e0b';
    if (point.type === 'confounder-low') return '#3b82f6';
    if (point.type === 'selected') return '#22c55e';
    if (point.group) {
      const colors = { A: '#ef4444', B: '#f59e0b', C: '#22c55e', D: '#3b82f6' };
      return colors[point.group];
    }
    return '#8b5cf6';
  };

  const typeInfo = correlationTypes.find(t => t.id === type);

  return (
    <div style={{ backgroundColor: '#0f172a', borderRadius: '12px', padding: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <span style={{ fontSize: '13px', color: '#94a3b8', fontWeight: '500' }}>Interactive Simulation</span>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={onTogglePlay}
            style={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '6px',
              padding: '6px 12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              color: '#e2e8f0',
              fontSize: '12px'
            }}
          >
            {isPlaying ? <Pause size={14} /> : <Play size={14} />}
            {isPlaying ? 'Pause' : 'Animate'}
          </button>
          <button
            onClick={() => setPoints(generatePoints())}
            style={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '6px',
              padding: '6px 12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              color: '#e2e8f0',
              fontSize: '12px'
            }}
          >
            <RotateCcw size={14} />
            Regenerate
          </button>
        </div>
      </div>
      
      <svg viewBox="0 0 120 120" style={{ width: '100%', height: '200px' }}>
        {/* Grid */}
        <defs>
          <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
            <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#1e293b" strokeWidth="0.5"/>
          </pattern>
        </defs>
        <rect x="10" y="10" width="100" height="100" fill="url(#grid)" />
        
        {/* Axes */}
        <line x1="10" y1="110" x2="110" y2="110" stroke="#475569" strokeWidth="1" />
        <line x1="10" y1="10" x2="10" y2="110" stroke="#475569" strokeWidth="1" />
        <text x="60" y="119" fill="#64748b" fontSize="6" textAnchor="middle">Variable A</text>
        <text x="4" y="60" fill="#64748b" fontSize="6" textAnchor="middle" transform="rotate(-90, 4, 60)">Variable B</text>
        
        {/* Trend line for some types */}
        {(type === 'causation' || type === 'reverse') && (
          <line x1="15" y1="95" x2="105" y2="20" stroke={typeInfo.color} strokeWidth="1.5" strokeDasharray="4,4" opacity="0.6" />
        )}
        
        {/* Selection boundary for selection bias */}
        {type === 'selection' && (
          <line x1="10" y1="30" x2="90" y2="110" stroke="#ec4899" strokeWidth="1.5" strokeDasharray="4,4" opacity="0.5" />
        )}
        
        {/* Points */}
        {points.map((point, i) => (
          <circle
            key={i}
            cx={10 + point.x}
            cy={110 - point.y}
            r={point.type === 'hidden' ? 2 : 3}
            fill={getPointColor(point)}
            opacity={point.type === 'hidden' ? 0.3 : 0.8}
            style={{
              transition: 'all 0.3s ease',
              transform: isPlaying ? `scale(${1 + Math.sin((frame + i * 10) * 0.1) * 0.1})` : 'scale(1)',
              transformOrigin: `${10 + point.x}px ${110 - point.y}px`
            }}
          />
        ))}
        
        {/* Group means for ecological */}
        {type === 'ecological' && (
          <>
            <circle cx="30" cy="35" r="6" fill="none" stroke="#94a3b8" strokeWidth="1" strokeDasharray="2,2" />
            <circle cx="50" cy="45" r="6" fill="none" stroke="#94a3b8" strokeWidth="1" strokeDasharray="2,2" />
            <circle cx="70" cy="55" r="6" fill="none" stroke="#94a3b8" strokeWidth="1" strokeDasharray="2,2" />
            <circle cx="90" cy="65" r="6" fill="none" stroke="#94a3b8" strokeWidth="1" strokeDasharray="2,2" />
            <line x1="30" y1="35" x2="90" y2="65" stroke="#94a3b8" strokeWidth="1" strokeDasharray="3,3" />
            <text x="95" y="75" fill="#94a3b8" fontSize="5">Group trend ↗</text>
            <text x="95" y="82" fill="#64748b" fontSize="4">Individual trend ↘</text>
          </>
        )}
      </svg>
      
      {/* Legend */}
      <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '12px', justifyContent: 'center' }}>
        {type === 'confounding' && (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#94a3b8' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#f59e0b' }} />
              Confounder = High
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#94a3b8' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#3b82f6' }} />
              Confounder = Low
            </div>
          </>
        )}
        {type === 'selection' && (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#94a3b8' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#22c55e' }} />
              Observed (survivors)
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#94a3b8' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'rgba(100,100,100,0.4)' }} />
              Unobserved (filtered out)
            </div>
          </>
        )}
        {type === 'ecological' && (
          <div style={{ fontSize: '11px', color: '#94a3b8', textAlign: 'center' }}>
            Each color = different group. Positive trend between groups, negative within.
          </div>
        )}
      </div>
    </div>
  );
};

// Decision Flowchart Component
const DecisionFlowchart = ({ onSelectType }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  
  const steps = [
    {
      id: 'start',
      question: 'You found a correlation between A and B. Let\'s figure out what\'s really going on.',
      options: [
        { text: 'Start Analysis →', next: 'temporal' }
      ]
    },
    {
      id: 'temporal',
      question: 'Does A consistently occur BEFORE B in time?',
      options: [
        { text: 'Yes, A precedes B', next: 'mechanism', answer: 'a_first' },
        { text: 'No, B precedes A', next: 'reverse_confirm', answer: 'b_first' },
        { text: 'They change together / unclear', next: 'bidirectional_check', answer: 'together' }
      ]
    },
    {
      id: 'reverse_confirm',
      question: 'Could B be causing A? Is there a plausible mechanism for B → A?',
      options: [
        { text: 'Yes, B → A makes sense', next: 'result_reverse', answer: 'reverse_yes' },
        { text: 'No, it must be something else', next: 'confounder_check', answer: 'reverse_no' }
      ]
    },
    {
      id: 'bidirectional_check',
      question: 'Could A cause B AND B cause A (feedback loop)?',
      options: [
        { text: 'Yes, both directions seem plausible', next: 'result_bidirectional', answer: 'bidirectional_yes' },
        { text: 'No, only one direction makes sense', next: 'mechanism', answer: 'bidirectional_no' }
      ]
    },
    {
      id: 'mechanism',
      question: 'Is there a clear, identifiable mechanism by which A could cause B?',
      options: [
        { text: 'Yes, I can explain HOW A causes B', next: 'experiment', answer: 'mechanism_yes' },
        { text: 'No, I can\'t explain the mechanism', next: 'confounder_check', answer: 'mechanism_no' }
      ]
    },
    {
      id: 'experiment',
      question: 'Has this been tested with a controlled experiment (RCT)?',
      options: [
        { text: 'Yes, experiments confirm A → B', next: 'result_causation', answer: 'experiment_yes' },
        { text: 'No, only observational data', next: 'confounder_check', answer: 'experiment_no' }
      ]
    },
    {
      id: 'confounder_check',
      question: 'Could a third variable (C) be causing BOTH A and B?',
      options: [
        { text: 'Yes, I can think of confounders', next: 'result_confounding', answer: 'confounder_yes' },
        { text: 'No obvious confounders', next: 'sample_check', answer: 'confounder_no' }
      ]
    },
    {
      id: 'sample_check',
      question: 'Is your sample representative? Could selection bias be at play?',
      options: [
        { text: 'Sample might be biased', next: 'result_selection', answer: 'selection_yes' },
        { text: 'Sample is representative', next: 'multiple_check', answer: 'selection_no' }
      ]
    },
    {
      id: 'multiple_check',
      question: 'Were many variables tested? Could this be a multiple comparison issue?',
      options: [
        { text: 'Yes, tested many variables', next: 'result_chance', answer: 'multiple_yes' },
        { text: 'No, hypothesis was pre-specified', next: 'aggregate_check', answer: 'multiple_no' }
      ]
    },
    {
      id: 'aggregate_check',
      question: 'Is your data at the group/aggregate level rather than individual?',
      options: [
        { text: 'Yes, aggregate data', next: 'result_ecological', answer: 'aggregate_yes' },
        { text: 'No, individual-level data', next: 'mediator_check', answer: 'aggregate_no' }
      ]
    },
    {
      id: 'mediator_check',
      question: 'Does A cause B through an intermediate variable (A → M → B)?',
      options: [
        { text: 'Yes, there\'s a mediator', next: 'result_mediator', answer: 'mediator_yes' },
        { text: 'No, direct effect', next: 'result_causation', answer: 'mediator_no' }
      ]
    },
    // Results
    { id: 'result_causation', result: 'causation', question: 'This looks like DIRECT CAUSATION. A likely causes B.' },
    { id: 'result_reverse', result: 'reverse', question: 'This is likely REVERSE CAUSATION. B causes A, not the other way around.' },
    { id: 'result_confounding', result: 'confounding', question: 'This is likely a CONFOUNDING VARIABLE. A third variable causes both A and B.' },
    { id: 'result_bidirectional', result: 'bidirectional', question: 'This is likely BIDIRECTIONAL CAUSATION. A and B influence each other in a feedback loop.' },
    { id: 'result_chance', result: 'chance', question: 'This is likely RANDOM CHANCE. The correlation may be a statistical artifact.' },
    { id: 'result_selection', result: 'selection', question: 'This is likely SELECTION BIAS. The correlation only exists in your biased sample.' },
    { id: 'result_ecological', result: 'ecological', question: 'Watch out for the ECOLOGICAL FALLACY. Group patterns may not apply to individuals.' },
    { id: 'result_mediator', result: 'mediator', question: 'This is MEDIATED CAUSATION. A causes B through an intermediate variable.' }
  ];

  const currentStepData = steps.find(s => s.id === (currentStep === 0 ? 'start' : steps[currentStep]?.id)) || steps[0];
  
  const handleOption = (option) => {
    if (option.answer) {
      setAnswers({ ...answers, [currentStepData.id]: option.answer });
    }
    const nextStep = steps.findIndex(s => s.id === option.next);
    setCurrentStep(nextStep);
  };

  const reset = () => {
    setCurrentStep(0);
    setAnswers({});
  };

  const isResult = currentStepData.result;
  const resultType = isResult ? correlationTypes.find(t => t.id === currentStepData.result) : null;

  return (
    <div style={{
      backgroundColor: '#0f172a',
      borderRadius: '12px',
      padding: '24px',
      border: '1px solid #334155'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h3 style={{ margin: 0, fontSize: '16px', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Target size={18} style={{ color: '#f59e0b' }} />
          Diagnostic Flowchart
        </h3>
        <button
          onClick={reset}
          style={{
            backgroundColor: '#1e293b',
            border: '1px solid #334155',
            borderRadius: '6px',
            padding: '6px 12px',
            cursor: 'pointer',
            color: '#94a3b8',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <RotateCcw size={14} />
          Start Over
        </button>
      </div>

      <div style={{
        backgroundColor: isResult ? `${resultType?.color}15` : '#1e293b',
        borderRadius: '8px',
        padding: '20px',
        border: isResult ? `2px solid ${resultType?.color}50` : '1px solid #334155'
      }}>
        <p style={{
          fontSize: '15px',
          color: isResult ? resultType?.color : '#e2e8f0',
          margin: '0 0 16px 0',
          fontWeight: isResult ? '600' : '400',
          lineHeight: '1.5'
        }}>
          {currentStepData.question}
        </p>

        {!isResult && currentStepData.options && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {currentStepData.options.map((option, i) => (
              <button
                key={i}
                onClick={() => handleOption(option)}
                style={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #475569',
                  borderRadius: '8px',
                  padding: '12px 16px',
                  cursor: 'pointer',
                  color: '#e2e8f0',
                  fontSize: '14px',
                  textAlign: 'left',
                  transition: 'all 0.2s'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = '#60a5fa';
                  e.currentTarget.style.backgroundColor = '#1e293b';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = '#475569';
                  e.currentTarget.style.backgroundColor = '#0f172a';
                }}
              >
                {option.text}
              </button>
            ))}
          </div>
        )}

        {isResult && (
          <button
            onClick={() => onSelectType(resultType)}
            style={{
              backgroundColor: resultType?.color,
              border: 'none',
              borderRadius: '8px',
              padding: '12px 20px',
              cursor: 'pointer',
              color: '#fff',
              fontSize: '14px',
              fontWeight: '600',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            Learn more about {resultType?.title} →
          </button>
        )}
      </div>

      {/* Progress */}
      <div style={{ marginTop: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ fontSize: '12px', color: '#64748b' }}>Progress:</span>
        <div style={{ flex: 1, height: '4px', backgroundColor: '#1e293b', borderRadius: '2px' }}>
          <div style={{
            height: '100%',
            width: `${Math.min(100, (Object.keys(answers).length / 6) * 100)}%`,
            backgroundColor: isResult ? resultType?.color : '#60a5fa',
            borderRadius: '2px',
            transition: 'all 0.3s'
          }} />
        </div>
      </div>
    </div>
  );
};

// Quick Reference Card
const QuickReference = () => (
  <div style={{
    backgroundColor: '#1e293b',
    borderRadius: '12px',
    padding: '20px',
    border: '1px solid #334155'
  }}>
    <h3 style={{ margin: '0 0 16px 0', fontSize: '16px', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px' }}>
      <Lightbulb size={18} style={{ color: '#f59e0b' }} />
      Quick Reference: Questions to Always Ask
    </h3>
    <div style={{ display: 'grid', gap: '12px' }}>
      {[
        { q: 'Which came first?', hint: 'Reverse causation', color: '#f59e0b' },
        { q: 'What else could explain both?', hint: 'Confounding', color: '#ef4444' },
        { q: 'Is my sample representative?', hint: 'Selection bias', color: '#ec4899' },
        { q: 'How many things did I test?', hint: 'Random chance', color: '#64748b' },
        { q: 'Could both directions be true?', hint: 'Bidirectional', color: '#06b6d4' },
        { q: 'What\'s the mechanism?', hint: 'Mediated vs direct', color: '#8b5cf6' },
        { q: 'Is this group or individual data?', hint: 'Ecological fallacy', color: '#14b8a6' }
      ].map((item, i) => (
        <div key={i} style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          backgroundColor: '#0f172a',
          padding: '10px 14px',
          borderRadius: '8px',
          borderLeft: `3px solid ${item.color}`
        }}>
          <HelpCircle size={16} style={{ color: item.color, flexShrink: 0 }} />
          <span style={{ color: '#e2e8f0', fontSize: '14px', flex: 1 }}>{item.q}</span>
          <span style={{ color: '#64748b', fontSize: '12px', whiteSpace: 'nowrap' }}>→ {item.hint}</span>
        </div>
      ))}
    </div>
  </div>
);

// Danger Rating Component  
const DangerRating = ({ level, color }) => {
  const levels = { low: 1, medium: 2, high: 3 };
  const count = levels[level] || 0;
  
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <span style={{ fontSize: '12px', color: '#64748b', marginRight: '4px' }}>Misleading potential:</span>
      {[1, 2, 3].map(i => (
        <AlertTriangle
          key={i}
          size={14}
          style={{
            color: i <= count ? (count === 3 ? '#ef4444' : count === 2 ? '#f59e0b' : '#22c55e') : '#334155'
          }}
        />
      ))}
    </div>
  );
};

// Main Component
export default function CorrelationExplainer() {
  const [selectedType, setSelectedType] = useState(correlationTypes[0]);
  const [activeTab, setActiveTab] = useState('explore');
  const [expandedSections, setExpandedSections] = useState(['example']);
  const [isSimPlaying, setIsSimPlaying] = useState(false);
  const [currentExampleIndex, setCurrentExampleIndex] = useState(0);

  const toggleSection = (section) => {
    setExpandedSections(prev =>
      prev.includes(section) ? prev.filter(s => s !== section) : [...prev, section]
    );
  };

  const handleTypeSelect = (type) => {
    setSelectedType(type);
    setCurrentExampleIndex(0);
    setActiveTab('explore');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0f172a',
      color: '#e2e8f0',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
        borderBottom: '1px solid #334155',
        padding: '24px 24px 0'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <h1 style={{
              fontSize: '32px',
              fontWeight: '700',
              marginBottom: '8px',
              background: 'linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              Correlation ≠ Causation
            </h1>
            <p style={{ color: '#94a3b8', fontSize: '16px', maxWidth: '600px', margin: '0 auto' }}>
              The complete guide to understanding what correlations actually mean—and the 8 ways they can mislead you
            </p>
          </div>

          {/* Tab Navigation */}
          <div style={{ display: 'flex', gap: '4px', justifyContent: 'center' }}>
            {[
              { id: 'explore', label: 'Explore Types', icon: BookOpen },
              { id: 'diagnose', label: 'Diagnose Your Data', icon: FlaskConical },
              { id: 'reference', label: 'Quick Reference', icon: Lightbulb }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  backgroundColor: activeTab === tab.id ? '#1e293b' : 'transparent',
                  border: 'none',
                  borderBottom: activeTab === tab.id ? '2px solid #60a5fa' : '2px solid transparent',
                  padding: '12px 20px',
                  cursor: 'pointer',
                  color: activeTab === tab.id ? '#e2e8f0' : '#64748b',
                  fontSize: '14px',
                  fontWeight: '500',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  borderRadius: '8px 8px 0 0'
                }}
              >
                <tab.icon size={16} />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
        {activeTab === 'diagnose' && (
          <DecisionFlowchart onSelectType={handleTypeSelect} />
        )}

        {activeTab === 'reference' && (
          <QuickReference />
        )}

        {activeTab === 'explore' && (
          <>
            {/* Type Selector Grid */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
              gap: '10px',
              marginBottom: '24px'
            }}>
              {correlationTypes.map((type) => (
                <button
                  key={type.id}
                  onClick={() => handleTypeSelect(type)}
                  style={{
                    padding: '14px 10px',
                    borderRadius: '10px',
                    border: selectedType.id === type.id ? `2px solid ${type.color}` : '2px solid #334155',
                    backgroundColor: selectedType.id === type.id ? `${type.color}15` : '#1e293b',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  <div style={{
                    fontSize: '11px',
                    fontWeight: '600',
                    color: selectedType.id === type.id ? type.color : '#94a3b8',
                    textAlign: 'center',
                    lineHeight: '1.3'
                  }}>
                    {type.title}
                  </div>
                  <div style={{
                    fontSize: '10px',
                    color: '#64748b',
                    textAlign: 'center'
                  }}>
                    {type.probabilityLabel}
                  </div>
                  <div style={{
                    width: '100%',
                    height: '4px',
                    backgroundColor: '#0f172a',
                    borderRadius: '2px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${type.probability}%`,
                      height: '100%',
                      backgroundColor: selectedType.id === type.id ? type.color : '#475569',
                      transition: 'all 0.3s'
                    }} />
                  </div>
                </button>
              ))}
            </div>

            {/* Main Content */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: '24px' }}>
              {/* Left Column - Main Content */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {/* Header Card */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '16px',
                  border: `2px solid ${selectedType.color}40`,
                  overflow: 'hidden'
                }}>
                  <div style={{
                    padding: '24px',
                    background: `linear-gradient(135deg, ${selectedType.color}15, transparent)`
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                      <div>
                        <h2 style={{ fontSize: '26px', fontWeight: '700', color: selectedType.color, margin: '0 0 4px 0' }}>
                          {selectedType.title}
                        </h2>
                        <p style={{ color: '#94a3b8', margin: 0, fontSize: '16px' }}>{selectedType.subtitle}</p>
                      </div>
                      <DangerRating level={selectedType.dangerLevel} />
                    </div>
                    <p style={{ fontSize: '15px', color: '#cbd5e1', lineHeight: '1.6', margin: 0 }}>
                      {selectedType.description}
                    </p>
                  </div>

                  {/* Key Question */}
                  <div style={{
                    padding: '16px 24px',
                    backgroundColor: `${selectedType.color}10`,
                    borderTop: `1px solid ${selectedType.color}30`
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <HelpCircle size={20} style={{ color: selectedType.color, flexShrink: 0 }} />
                      <p style={{
                        fontSize: '15px',
                        fontWeight: '600',
                        color: selectedType.color,
                        margin: 0,
                        fontStyle: 'italic'
                      }}>
                        "{selectedType.keyQuestion}"
                      </p>
                    </div>
                  </div>
                </div>

                {/* Examples Section */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '12px',
                  border: '1px solid #334155',
                  overflow: 'hidden'
                }}>
                  <button
                    onClick={() => toggleSection('example')}
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      backgroundColor: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#e2e8f0'
                    }}
                  >
                    <span style={{ fontWeight: '600', fontSize: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      📊 Real-World Examples
                      <span style={{
                        backgroundColor: selectedType.color + '30',
                        color: selectedType.color,
                        padding: '2px 8px',
                        borderRadius: '12px',
                        fontSize: '12px'
                      }}>
                        {selectedType.examples.length}
                      </span>
                    </span>
                    {expandedSections.includes('example') ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                  {expandedSections.includes('example') && (
                    <div style={{ padding: '0 20px 20px' }}>
                      {/* Example Tabs */}
                      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
                        {selectedType.examples.map((_, i) => (
                          <button
                            key={i}
                            onClick={() => setCurrentExampleIndex(i)}
                            style={{
                              padding: '6px 14px',
                              borderRadius: '6px',
                              border: 'none',
                              backgroundColor: currentExampleIndex === i ? selectedType.color : '#0f172a',
                              color: currentExampleIndex === i ? '#fff' : '#94a3b8',
                              cursor: 'pointer',
                              fontSize: '13px',
                              fontWeight: '500'
                            }}
                          >
                            Example {i + 1}
                          </button>
                        ))}
                      </div>

                      {/* Current Example */}
                      <div style={{
                        display: 'grid',
                        gridTemplateColumns: '1fr auto 1fr',
                        gap: '16px',
                        alignItems: 'center',
                        marginBottom: '16px'
                      }}>
                        <div style={{
                          backgroundColor: '#1e3a5f',
                          padding: '16px',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontSize: '11px', color: '#60a5fa', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Variable A</div>
                          <div style={{ fontWeight: '600', fontSize: '15px' }}>{selectedType.examples[currentExampleIndex].a}</div>
                        </div>
                        <div style={{ color: '#64748b', fontSize: '24px' }}>↔</div>
                        <div style={{
                          backgroundColor: '#4a1d4a',
                          padding: '16px',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontSize: '11px', color: '#f472b6', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Variable B</div>
                          <div style={{ fontWeight: '600', fontSize: '15px' }}>{selectedType.examples[currentExampleIndex].b}</div>
                        </div>
                      </div>
                      <div style={{
                        backgroundColor: '#0f172a',
                        padding: '16px',
                        borderRadius: '8px',
                        borderLeft: `3px solid ${selectedType.color}`
                      }}>
                        <p style={{ margin: 0, lineHeight: '1.6', color: '#cbd5e1', fontSize: '14px' }}>
                          {selectedType.examples[currentExampleIndex].explanation}
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Historical Example */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '12px',
                  border: '1px solid #334155',
                  overflow: 'hidden'
                }}>
                  <button
                    onClick={() => toggleSection('history')}
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      backgroundColor: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#e2e8f0'
                    }}
                  >
                    <span style={{ fontWeight: '600', fontSize: '15px' }}>📜 Historical Case Study</span>
                    {expandedSections.includes('history') ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                  {expandedSections.includes('history') && (
                    <div style={{ padding: '0 20px 20px' }}>
                      <div style={{
                        backgroundColor: '#0f172a',
                        padding: '20px',
                        borderRadius: '10px',
                        border: `1px solid ${selectedType.color}30`
                      }}>
                        <h4 style={{ margin: '0 0 12px 0', color: selectedType.color, fontSize: '16px' }}>
                          {selectedType.historicalExample.title}
                        </h4>
                        <p style={{ margin: 0, lineHeight: '1.7', color: '#cbd5e1', fontSize: '14px' }}>
                          {selectedType.historicalExample.story}
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {/* How to Test */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '12px',
                  border: '1px solid #334155',
                  overflow: 'hidden'
                }}>
                  <button
                    onClick={() => toggleSection('test')}
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      backgroundColor: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#e2e8f0'
                    }}
                  >
                    <span style={{ fontWeight: '600', fontSize: '15px' }}>🔬 How to Test For This</span>
                    {expandedSections.includes('test') ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                  {expandedSections.includes('test') && (
                    <div style={{ padding: '0 20px 20px' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {selectedType.howToTest.map((test, i) => (
                          <div key={i} style={{
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '14px',
                            backgroundColor: '#0f172a',
                            padding: '14px 16px',
                            borderRadius: '8px'
                          }}>
                            <div style={{
                              width: '28px',
                              height: '28px',
                              borderRadius: '50%',
                              backgroundColor: selectedType.color + '30',
                              color: selectedType.color,
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              fontSize: '13px',
                              fontWeight: '600',
                              flexShrink: 0
                            }}>
                              {i + 1}
                            </div>
                            <div style={{ flex: 1 }}>
                              <div style={{ fontWeight: '600', color: '#e2e8f0', fontSize: '14px', marginBottom: '2px' }}>
                                {test.method}
                              </div>
                              <div style={{ color: '#94a3b8', fontSize: '13px' }}>{test.description}</div>
                            </div>
                            <span style={{
                              backgroundColor: test.difficulty === 'Hard' ? '#7f1d1d' : test.difficulty === 'Medium' ? '#78350f' : '#14532d',
                              color: test.difficulty === 'Hard' ? '#fca5a5' : test.difficulty === 'Medium' ? '#fcd34d' : '#86efac',
                              padding: '3px 10px',
                              borderRadius: '12px',
                              fontSize: '11px',
                              fontWeight: '500'
                            }}>
                              {test.difficulty}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Common Mistakes */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '12px',
                  border: '1px solid #334155',
                  overflow: 'hidden'
                }}>
                  <button
                    onClick={() => toggleSection('mistakes')}
                    style={{
                      width: '100%',
                      padding: '16px 20px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      backgroundColor: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#e2e8f0'
                    }}
                  >
                    <span style={{ fontWeight: '600', fontSize: '15px' }}>⚠️ Common Mistakes</span>
                    {expandedSections.includes('mistakes') ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                  {expandedSections.includes('mistakes') && (
                    <div style={{ padding: '0 20px 20px' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {selectedType.commonMistakes.map((mistake, i) => (
                          <div key={i} style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            backgroundColor: '#0f172a',
                            padding: '12px 14px',
                            borderRadius: '8px',
                            borderLeft: '3px solid #ef4444'
                          }}>
                            <XCircle size={16} style={{ color: '#ef4444', flexShrink: 0 }} />
                            <span style={{ color: '#e2e8f0', fontSize: '14px' }}>{mistake}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Right Column - Simulation & Stats */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {/* Simulation */}
                <ScatterSimulation
                  type={selectedType.id}
                  isPlaying={isSimPlaying}
                  onTogglePlay={() => setIsSimPlaying(!isSimPlaying)}
                />

                {/* Probability Card */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '12px',
                  padding: '20px',
                  border: '1px solid #334155'
                }}>
                  <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', color: '#94a3b8' }}>
                    How Often This Explains Correlations
                  </h4>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                    <div style={{
                      fontSize: '36px',
                      fontWeight: '700',
                      color: selectedType.color
                    }}>
                      ~{selectedType.probability}%
                    </div>
                    <div style={{
                      backgroundColor: selectedType.color + '20',
                      color: selectedType.color,
                      padding: '4px 12px',
                      borderRadius: '16px',
                      fontSize: '12px',
                      fontWeight: '600'
                    }}>
                      {selectedType.probabilityLabel}
                    </div>
                  </div>
                  <div style={{
                    width: '100%',
                    height: '8px',
                    backgroundColor: '#0f172a',
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${selectedType.probability}%`,
                      height: '100%',
                      backgroundColor: selectedType.color,
                      borderRadius: '4px',
                      transition: 'all 0.5s'
                    }} />
                  </div>
                  <p style={{ margin: '12px 0 0', fontSize: '13px', color: '#94a3b8', lineHeight: '1.5' }}>
                    {selectedType.realWorld}
                  </p>
                </div>

                {/* Info Card */}
                <div style={{
                  backgroundColor: '#172554',
                  borderRadius: '12px',
                  padding: '16px',
                  border: '1px solid #1e3a8a'
                }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                    <Info size={18} style={{ color: '#60a5fa', flexShrink: 0, marginTop: '2px' }} />
                    <div>
                      <div style={{ fontWeight: '600', color: '#93c5fd', fontSize: '13px', marginBottom: '4px' }}>
                        Pro Tip
                      </div>
                      <p style={{ margin: 0, fontSize: '13px', color: '#bfdbfe', lineHeight: '1.5' }}>
                        Before concluding causation, systematically work through each of these 8 alternatives. Most correlations in media and research are NOT direct causation.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Distribution Overview */}
                <div style={{
                  backgroundColor: '#1e293b',
                  borderRadius: '12px',
                  padding: '20px',
                  border: '1px solid #334155'
                }}>
                  <h4 style={{ margin: '0 0 16px 0', fontSize: '14px', color: '#94a3b8' }}>
                    All Types at a Glance
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {correlationTypes.sort((a, b) => b.probability - a.probability).map(type => (
                      <div
                        key={type.id}
                        onClick={() => handleTypeSelect(type)}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '10px',
                          cursor: 'pointer',
                          padding: '6px 8px',
                          borderRadius: '6px',
                          backgroundColor: selectedType.id === type.id ? `${type.color}15` : 'transparent',
                          border: selectedType.id === type.id ? `1px solid ${type.color}40` : '1px solid transparent'
                        }}
                      >
                        <div style={{
                          width: '10px',
                          height: '10px',
                          borderRadius: '50%',
                          backgroundColor: type.color
                        }} />
                        <span style={{
                          fontSize: '12px',
                          color: selectedType.id === type.id ? type.color : '#94a3b8',
                          flex: 1
                        }}>
                          {type.title}
                        </span>
                        <div style={{
                          width: '60px',
                          height: '4px',
                          backgroundColor: '#0f172a',
                          borderRadius: '2px'
                        }}>
                          <div style={{
                            width: `${type.probability}%`,
                            height: '100%',
                            backgroundColor: type.color,
                            borderRadius: '2px'
                          }} />
                        </div>
                        <span style={{ fontSize: '11px', color: '#64748b', width: '30px', textAlign: 'right' }}>
                          {type.probability}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Footer */}
        <div style={{
          marginTop: '32px',
          padding: '20px',
          backgroundColor: '#1e293b',
          borderRadius: '12px',
          border: '1px solid #334155',
          textAlign: 'center'
        }}>
          <p style={{ margin: 0, color: '#64748b', fontSize: '13px' }}>
            Remember: Finding a correlation is the beginning of the investigation, not the end. 
            <span style={{ color: '#f59e0b' }}> True causation is rare and precious—don't claim it lightly.</span>
          </p>
        </div>
      </div>
    </div>
  );
}