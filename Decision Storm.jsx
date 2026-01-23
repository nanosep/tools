import React, { useState } from 'react';
import { Shuffle, Zap, TrendingUp, AlertTriangle, Users, DollarSign, Clock, Target } from 'lucide-react';

export default function DecisionStormGenerator() {
  const [scenario, setScenario] = useState('');
  const [stormCount, setStormCount] = useState(3);
  const [storms, setStorms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState({ current: 0, total: 0 });

  const lensTypes = [
    { name: 'Risk-First', icon: AlertTriangle, color: 'bg-red-50 border-red-200', prompt: 'Analyze this scenario focusing primarily on risks, threats, and what could go wrong. What are the failure modes?' },
    { name: 'Opportunity-First', icon: TrendingUp, color: 'bg-green-50 border-green-200', prompt: 'Analyze this scenario focusing primarily on opportunities, upside potential, and what could go right. What are the breakthrough possibilities?' },
    { name: 'Resource-First', icon: DollarSign, color: 'bg-blue-50 border-blue-200', prompt: 'Analyze this scenario focusing primarily on resource allocation, costs, and ROI. What does this require and what does it return?' },
    { name: 'Timeline-First', icon: Clock, color: 'bg-purple-50 border-purple-200', prompt: 'Analyze this scenario focusing primarily on timing, sequencing, and velocity. What should happen when, and how fast can we move?' },
    { name: 'Stakeholder-First', icon: Users, color: 'bg-orange-50 border-orange-200', prompt: 'Analyze this scenario focusing primarily on people, stakeholders, and organizational dynamics. Who cares about this and how will they react?' },
    { name: 'Strategic-First', icon: Target, color: 'bg-indigo-50 border-indigo-200', prompt: 'Analyze this scenario focusing primarily on strategic positioning, competitive advantage, and long-term implications. How does this change the game?' },
  ];

  const generateStorms = async () => {
    if (!scenario.trim()) {
      setError('Please enter a scenario first');
      return;
    }
    
    setLoading(true);
    setStorms([]);
    setError(null);
    
    // Select random lenses for the storm count
    const shuffled = [...lensTypes].sort(() => Math.random() - 0.5);
    const selectedLenses = shuffled.slice(0, stormCount);
    setProgress({ current: 0, total: selectedLenses.length });
    
    const results = [];
    
    try {
      // Make requests sequentially to avoid rate limiting
      for (let i = 0; i < selectedLenses.length; i++) {
        const lens = selectedLenses[i];
        setProgress({ current: i + 1, total: selectedLenses.length });
        
        console.log(`Generating storm ${i + 1}/${selectedLenses.length}:`, lens.name);
        
        const response = await fetch("https://api.anthropic.com/v1/messages", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "claude-sonnet-4-20250514",
            max_tokens: 1000,
            messages: [
              {
                role: "user",
                content: `${lens.prompt}

SCENARIO:
${scenario}

Provide a focused analysis from this perspective. Be specific and actionable. Structure your response as:
1. Key Insight (one sentence)
2. Critical Factors (3-4 bullet points)
3. Recommended Action (one clear next step)

Keep it concise and decision-oriented.`
              }
            ]
          })
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API request failed: ${response.status} - ${errorText}`);
        }
        
        const data = await response.json();
        
        const stormResult = {
          lens: lens.name,
          icon: lens.icon,
          color: lens.color,
          analysis: data.content[0].text
        };
        
        results.push(stormResult);
        // Update storms incrementally so user sees them appear one by one
        setStorms([...results]);
        
        console.log(`Storm ${i + 1} completed:`, lens.name);
        
        // Add a small delay between requests to avoid rate limiting
        if (i < selectedLenses.length - 1) {
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }
      
      console.log('All storms generated successfully');
    } catch (err) {
      console.error('Error generating storms:', err);
      setError(`Failed to generate storms: ${err.message}`);
    } finally {
      setLoading(false);
      setProgress({ current: 0, total: 0 });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Shuffle className="w-10 h-10 text-slate-700" />
            <h1 className="text-4xl font-bold text-slate-800">Decision Storm Generator</h1>
          </div>
          <p className="text-slate-600 text-lg">
            Transform one scenario into multiple strategic perspectives
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            Enter Your Scenario or Decision
          </label>
          <textarea
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            placeholder="Example: We're considering launching a new B2B SaaS product targeting mid-market companies. Initial development would take 6 months and $500K. Early customer interviews show strong interest but we'd be entering a crowded market..."
            className="w-full h-32 p-4 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none resize-none"
          />
          
          <div className="flex items-center gap-6 mt-4">
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-slate-700">
                Number of Perspectives:
              </label>
              <select
                value={stormCount}
                onChange={(e) => setStormCount(Number(e.target.value))}
                className="px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-blue-500 focus:outline-none"
              >
                <option value={2}>2</option>
                <option value={3}>3</option>
                <option value={4}>4</option>
                <option value={5}>5</option>
                <option value={6}>6</option>
              </select>
            </div>
            
            <button
              onClick={generateStorms}
              disabled={loading || !scenario.trim()}
              className="flex items-center gap-2 px-6 py-3 bg-slate-800 text-white rounded-lg hover:bg-slate-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors font-medium"
            >
              <Zap className="w-5 h-5" />
              {loading ? 'Generating Storms...' : 'Generate Decision Storms'}
            </button>
          </div>
          
          <p className="text-xs text-slate-500 mt-3">
            💡 Perspectives are generated one at a time to avoid rate limits. Each takes ~10 seconds.
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 mb-8">
            <div className="flex items-center gap-2 text-red-800">
              <AlertTriangle className="w-5 h-5" />
              <p className="font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-8 mb-8 text-center">
            <div className="flex items-center justify-center gap-3 mb-3">
              <Zap className="w-6 h-6 text-blue-600 animate-pulse" />
              <p className="text-lg font-semibold text-blue-800">
                Generating perspective {progress.current} of {progress.total}...
              </p>
            </div>
            <p className="text-sm text-blue-600">
              Processing sequentially to avoid rate limits (~10 seconds per perspective)
            </p>
          </div>
        )}

        {/* Results Grid */}
        {storms.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {storms.map((storm, index) => {
              const IconComponent = storm.icon;
              return (
                <div
                  key={index}
                  className={`${storm.color} border-2 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow`}
                >
                  <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-current opacity-40">
                    <IconComponent className="w-6 h-6" />
                    <h3 className="text-xl font-bold">{storm.lens} Lens</h3>
                  </div>
                  <div className="prose prose-sm max-w-none">
                    <div className="whitespace-pre-line text-slate-700 leading-relaxed">
                      {storm.analysis}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Empty State */}
        {storms.length === 0 && !loading && (
          <div className="bg-white rounded-lg shadow-lg p-12 text-center">
            <Shuffle className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-700 mb-2">
              Ready to Create Decision Storms
            </h3>
            <p className="text-slate-500">
              Enter a scenario above and click generate to see multiple strategic perspectives
            </p>
          </div>
        )}

        {/* Available Lenses Info */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-slate-800 mb-4">Available Analytical Lenses</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {lensTypes.map((lens) => {
              const IconComponent = lens.icon;
              return (
                <div key={lens.name} className="flex items-center gap-2">
                  <IconComponent className="w-5 h-5 text-slate-500" />
                  <span className="text-sm text-slate-600">{lens.name}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}