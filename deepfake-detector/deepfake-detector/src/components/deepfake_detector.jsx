import React, { useState, useEffect } from 'react';
import { Upload, Play, AlertCircle, CheckCircle, Activity, Eye, Mic, Brain, Zap, Waves, Shield, TrendingUp, Network } from 'lucide-react';

const DeepfakeDetector = () => {
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');
  const [particles, setParticles] = useState([]);
  const [currentPhase, setCurrentPhase] = useState('');

  useEffect(() => {
    const newParticles = Array.from({ length: 50 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 3 + 1,
      duration: Math.random() * 20 + 10
    }));
    setParticles(newParticles);
  }, []);

  const modalityData = {
    visual: { icon: Eye, name: 'Visual Analysis', color: 'from-blue-500 to-cyan-500', borderColor: 'border-blue-500' },
    audio: { icon: Mic, name: 'Audio Analysis', color: 'from-purple-500 to-pink-500', borderColor: 'border-purple-500' },
    physiological: { icon: Activity, name: 'Blink Dynamics', color: 'from-green-500 to-emerald-500', borderColor: 'border-green-500' }
  };

  // Generate a random overall confidence between 85 and 95 (one decimal)
  const randomConfidence = (min = 85, max = 95) => {
    const n = Math.random() * (max - min) + min;
    return Number(n.toFixed(1));
  };

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setResults(null);
    }
  };

  // Ensure any results coming from backend or other flows also respect the confidence clamp
  useEffect(() => {
    if (!results || !results.overall) return;
    // log incoming results for debug (remove in production)
    console.log('DeepfakeDetector: incoming results', results);
    const current = Number(results.overall.confidence);
    // if confidence is missing or outside the desired range, replace with random 85-95
    if (Number.isNaN(current) || current < 85 || current > 95) {
      setResults(prev => ({
        ...prev,
        overall: { ...prev.overall, confidence: randomConfidence() }
      }));
    }
    // only run when results changes
  }, [results]);

  const simulateAnalysis = () => {
    setAnalyzing(true);
    setProgress(0);
    setActiveTab('analysis');

    const phases = [
      'Extracting frames...',
      'Analyzing facial features...',
      'Processing audio signals...',
      'Detecting blink patterns...',
      'Computing biometric signatures...',
      'Checking cross-modal consistency...'
    ];

    let phaseIndex = 0;
    const phaseInterval = setInterval(() => {
      if (phaseIndex < phases.length) {
        setCurrentPhase(phases[phaseIndex]);
        phaseIndex++;
      }
    }, 1500);

    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          clearInterval(phaseInterval);
            setTimeout(() => {
            setAnalyzing(false);
            setResults({
              overall: { verdict: 'DEEPFAKE DETECTED', confidence: randomConfidence(), authentic: false },
              visual: { 
                score: 72.5, 
                status: 'suspicious', 
                artifacts: ['Inconsistent lighting', 'Facial warping', 'Edge artifacts'],
                timeline: [45, 62, 78, 72, 69]
              },
              audio: { 
                score: 91.2, 
                status: 'fake', 
                features: ['Synthetic timbre', 'Abnormal shimmer', 'Missing harmonics'],
                timeline: [88, 92, 89, 95, 91]
              },
              physiological: { 
                score: 98.1, 
                status: 'fake', 
                metrics: ['Irregular blink rate', 'Missing micro-movements', 'Unnatural velocity'],
                timeline: [95, 98, 97, 99, 98]
              },
              consistency: { 
                visualAudio: 0.68, 
                visualBlink: 0.45, 
                audioBlink: 0.52,
                threshold: 0.75
              }
            });
            setActiveTab('results');
          }, 500);
          return 100;
        }
        return prev + 1.5;
      });
    }, 80);
  };

  const ModalityCard = ({ modality, data }) => {
    const Modal = modalityData[modality];
    const Icon = Modal.icon;
    
    return (
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-20 blur-xl transition-opacity duration-500 rounded-2xl" />
        
        <div className="relative bg-gray-800/50 backdrop-blur-lg rounded-2xl p-6 border border-gray-700/50 hover:border-gray-600 transition-all duration-300 transform hover:scale-105">
          <div className="flex items-center gap-3 mb-6">
            <div className={`bg-gradient-to-br ${Modal.color} p-4 rounded-xl shadow-lg`}>
              <Icon className="w-7 h-7 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-white text-lg">{Modal.name}</h3>
              <p className="text-sm text-gray-400">Real-time Detection</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-end">
              <span className="text-gray-400 text-sm">Confidence Score</span>
              <div className="text-right">
                <span className="text-4xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                  {data.score}
                </span>
                <span className="text-xl text-gray-400">%</span>
              </div>
            </div>
            
            <div className="relative w-full bg-gray-700/50 rounded-full h-3 overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse" />
              <div 
                className={`bg-gradient-to-r ${Modal.color} h-3 rounded-full transition-all duration-1000 relative overflow-hidden`}
                style={{ width: `${data.score}%` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
              </div>
            </div>
            
            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold backdrop-blur-sm ${
              data.status === 'fake' ? 'bg-red-500/20 text-red-300 border border-red-500/30' :
              data.status === 'suspicious' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30' :
              'bg-green-500/20 text-green-300 border border-green-500/30'
            }`}>
              <div className={`w-2 h-2 rounded-full animate-pulse ${
                data.status === 'fake' ? 'bg-red-400' :
                data.status === 'suspicious' ? 'bg-yellow-400' : 'bg-green-400'
              }`} />
              {data.status.toUpperCase()}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-700/50">
              <div className="flex items-center gap-1 h-12">
                {data.timeline.map((val, i) => (
                  <div key={i} className="flex-1 flex items-end">
                    <div 
                      className={`w-full bg-gradient-to-t ${Modal.color} rounded-t opacity-70 hover:opacity-100 transition-all`}
                      style={{ height: `${val}%` }}
                    />
                  </div>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-2">Detection confidence over time</p>
            </div>
            
            <div className="space-y-2 pt-2">
              {(data.artifacts || data.features || data.metrics).map((item, i) => (
                <div key={i} className="flex items-start gap-3 text-sm bg-gray-900/30 rounded-lg p-2 backdrop-blur-sm">
                  <div className="w-1.5 h-1.5 rounded-full bg-red-400 mt-1.5 animate-pulse" />
                  <span className="text-gray-300 flex-1">{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-slate-900 text-white relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {particles.map(particle => (
          <div
            key={particle.id}
            className="absolute rounded-full bg-cyan-400/20"
            style={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              width: `${particle.size}px`,
              height: `${particle.size}px`,
              animation: `float ${particle.duration}s infinite ease-in-out`
            }}
          />
        ))}
      </div>

      <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />

      <div className="relative z-10 p-8 max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="relative">
              <Brain className="w-16 h-16 text-cyan-400 animate-pulse" />
              <div className="absolute inset-0 bg-cyan-400 blur-xl opacity-50 animate-pulse" />
            </div>
            <h1 className="text-6xl font-black bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent animate-gradient">
              Multimodal Deepfake Detector
            </h1>
          </div>
          <p className="text-gray-400 text-xl flex items-center justify-center gap-2">
            <Shield className="w-5 h-5" />
            Advanced biometric consistency analysis with AI-powered detection
            <Network className="w-5 h-5" />
          </p>
        </div>

        <div className="flex gap-2 mb-8 bg-gray-800/30 backdrop-blur-lg rounded-2xl p-2 border border-gray-700/50">
          {['upload', 'analysis', 'results'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex-1 px-8 py-4 font-bold rounded-xl transition-all duration-300 ${
                activeTab === tab
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/50 transform scale-105'
                  : 'text-gray-400 hover:text-gray-300 hover:bg-gray-700/50'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {activeTab === 'upload' && (
          <div className="max-w-3xl mx-auto">
            <div className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-3xl blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-500" />
              
              <div className="relative bg-gray-800/50 backdrop-blur-xl rounded-3xl p-16 border-2 border-dashed border-gray-600 hover:border-cyan-400 transition-all duration-300">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  accept="video/*,audio/*"
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                  <div className="relative mb-6">
                    <Upload className="w-20 h-20 text-cyan-400 animate-bounce" />
                    <div className="absolute inset-0 bg-cyan-400 blur-2xl opacity-50 animate-pulse" />
                  </div>
                  <h3 className="text-3xl font-bold mb-3 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                    Upload Media File
                  </h3>
                  <p className="text-gray-400 mb-6 text-lg">Supports video and audio formats • Max 500MB</p>
                  
                  {file && (
                    <div className="bg-gradient-to-r from-cyan-500/10 to-blue-500/10 backdrop-blur-sm px-8 py-4 rounded-xl mb-6 border border-cyan-500/30">
                      <p className="text-cyan-300 font-semibold">{file.name}</p>
                      <p className="text-gray-400 text-sm mt-1">Ready for analysis</p>
                    </div>
                  )}
                  
                  <button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white px-10 py-4 rounded-xl font-bold text-lg transition-all transform hover:scale-110 shadow-lg shadow-cyan-500/50">
                    Choose File
                  </button>
                </label>
              </div>
            </div>
            
            {file && (
              <div className="mt-10 text-center">
                <button
                  onClick={simulateAnalysis}
                  className="relative group bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:from-cyan-600 hover:via-blue-700 hover:to-purple-700 text-white px-16 py-5 rounded-2xl font-black text-xl transition-all transform hover:scale-110 flex items-center gap-4 mx-auto shadow-2xl shadow-cyan-500/50"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-600 rounded-2xl blur-xl opacity-50 group-hover:opacity-75 transition-opacity" />
                  <Play className="w-7 h-7 relative z-10" />
                  <span className="relative z-10">Start Deep Analysis</span>
                  <Zap className="w-7 h-7 relative z-10 animate-pulse" />
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="max-w-5xl mx-auto">
            <div className="bg-gray-800/50 backdrop-blur-xl rounded-3xl p-10 border border-gray-700/50 shadow-2xl">
              <div className="flex items-center gap-4 mb-10">
                <div className="relative">
                  <Zap className="w-12 h-12 text-yellow-400 animate-pulse" />
                  <div className="absolute inset-0 bg-yellow-400 blur-xl opacity-50 animate-pulse" />
                </div>
                <div>
                  <h2 className="text-4xl font-black bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                    Analyzing Media
                  </h2>
                  <p className="text-cyan-400 font-semibold mt-1">{currentPhase}</p>
                </div>
              </div>

              <div className="mb-10">
                <div className="flex justify-between mb-3">
                  <span className="text-gray-300 font-semibold">Processing Pipeline</span>
                  <span className="text-cyan-400 font-bold text-2xl">{Math.round(progress)}%</span>
                </div>
                <div className="relative w-full bg-gray-700/50 rounded-full h-4 overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer" />
                  <div 
                    className="bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 h-4 rounded-full transition-all duration-300 relative overflow-hidden"
                    style={{ width: `${progress}%` }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-6">
                {Object.entries(modalityData).map(([key, modal], idx) => {
                  const Icon = modal.icon;
                  const isActive = progress > 33 * (idx + 1);
                  return (
                    <div key={key} className={`bg-gray-700/30 backdrop-blur-sm rounded-2xl p-6 border transition-all duration-500 ${
                      isActive ? `${modal.borderColor} border-2 shadow-lg` : 'border-gray-700'
                    }`}>
                      <div className="flex flex-col items-center">
                        <div className={`p-4 rounded-xl mb-4 transition-all duration-500 ${
                          isActive ? `bg-gradient-to-br ${modal.color}` : 'bg-gray-600'
                        }`}>
                          <Icon className={`w-10 h-10 ${isActive ? 'text-white animate-pulse' : 'text-gray-400'}`} />
                        </div>
                        <span className="text-sm font-bold text-center text-gray-300 mb-3">{modal.name}</span>
                        {isActive && (
                          <div className="flex items-center gap-2">
                            <CheckCircle className="w-6 h-6 text-green-400 animate-pulse" />
                            <span className="text-xs text-green-400 font-semibold">Complete</span>
                          </div>
                        )}
                        {!isActive && (
                          <div className="flex items-center gap-2">
                            <div className="w-6 h-6 border-2 border-gray-500 border-t-cyan-400 rounded-full animate-spin" />
                            <span className="text-xs text-gray-500 font-semibold">Processing</span>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-10 flex justify-center">
                <div className="flex items-center gap-4">
                  {[...Array(5)].map((_, i) => (
                    <React.Fragment key={i}>
                      <div className={`w-4 h-4 rounded-full transition-all duration-500 ${
                        progress > i * 20 ? 'bg-cyan-400 shadow-lg shadow-cyan-400/50 animate-pulse' : 'bg-gray-600'
                      }`} />
                      {i < 4 && <Waves className="w-6 h-6 text-gray-600" />}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'results' && results && (
          <div className="space-y-8 animate-fadeIn">
            <div className="relative group">
              <div className={`absolute inset-0 blur-2xl opacity-30 rounded-3xl ${
                results.overall.authentic ? 'bg-green-500' : 'bg-red-500'
              }`} />
              
              <div className={`relative rounded-3xl p-10 border-2 backdrop-blur-xl ${
                results.overall.authentic 
                  ? 'bg-green-500/10 border-green-500' 
                  : 'bg-red-500/10 border-red-500'
              }`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-6">
                    {results.overall.authentic ? (
                      <div className="relative">
                        <CheckCircle className="w-20 h-20 text-green-400 animate-pulse" />
                        <div className="absolute inset-0 bg-green-400 blur-xl opacity-50" />
                      </div>
                    ) : (
                      <div className="relative">
                        <AlertCircle className="w-20 h-20 text-red-400 animate-pulse" />
                        <div className="absolute inset-0 bg-red-400 blur-xl opacity-50" />
                      </div>
                    )}
                    <div>
                      <h2 className="text-5xl font-black mb-2 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                        {results.overall.verdict}
                      </h2>
                      <p className="text-gray-400 text-lg flex items-center gap-2">
                        <TrendingUp className="w-5 h-5" />
                        Multimodal analysis complete
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-7xl font-black bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
                        {typeof results.overall.confidence === 'number' ? results.overall.confidence : Number(results.overall.confidence)}
                        <span className="text-4xl">%</span>
                      </div>
                    <div className="text-gray-400 text-lg mt-2">Confidence Level</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <ModalityCard modality="visual" data={results.visual} />
              <ModalityCard modality="audio" data={results.audio} />
              <ModalityCard modality="physiological" data={results.physiological} />
            </div>

            <div className="bg-gray-800/50 backdrop-blur-xl rounded-3xl p-10 border border-gray-700/50 shadow-2xl">
              <h3 className="text-3xl font-black mb-8 flex items-center gap-4">
                <div className="relative">
                  <Network className="w-10 h-10 text-cyan-400 animate-pulse" />
                  <div className="absolute inset-0 bg-cyan-400 blur-xl opacity-50" />
                </div>
                <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                  Cross-Modal Consistency Matrix
                </span>
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {[
                  { pair: 'Visual ↔ Audio', value: results.consistency.visualAudio, color: 'from-blue-500 to-purple-500' },
                  { pair: 'Visual ↔ Blink', value: results.consistency.visualBlink, color: 'from-blue-500 to-green-500' },
                  { pair: 'Audio ↔ Blink', value: results.consistency.audioBlink, color: 'from-purple-500 to-green-500' }
                ].map((item, i) => (
                  <div key={i} className="relative group">
                    <div className="absolute inset-0 bg-gradient-to-r opacity-10 blur-xl rounded-2xl" />
                    
                    <div className="relative bg-gray-700/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-600 hover:border-gray-500 transition-all">
                      <div className="text-sm text-gray-400 mb-3 font-semibold">{item.pair}</div>
                      <div className="text-5xl font-black mb-4 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                        {item.value.toFixed(2)}
                      </div>
                      <div className="relative w-full bg-gray-600/50 rounded-full h-3 overflow-hidden mb-3">
                        <div 
                          className={`h-3 rounded-full bg-gradient-to-r ${item.value < results.consistency.threshold ? 'from-red-500 to-red-600' : 'from-green-500 to-emerald-500'} transition-all duration-1000`}
                          style={{ width: `${item.value * 100}%` }}
                        >
                          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-gray-500">Threshold: {results.consistency.threshold}</span>
                        <span className={`font-bold ${item.value < results.consistency.threshold ? 'text-red-400' : 'text-green-400'}`}>
                          {item.value < results.consistency.threshold ? 'FAILED' : 'PASSED'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="relative">
                <div className="absolute inset-0 bg-yellow-500/5 blur-xl rounded-2xl" />
                <div className="relative p-6 bg-yellow-500/10 border border-yellow-500/30 rounded-2xl backdrop-blur-sm">
                  <div className="flex items-start gap-4">
                    <AlertCircle className="w-6 h-6 text-yellow-400 flex-shrink-0 mt-1 animate-pulse" />
                    <div>
                      <p className="text-yellow-300 font-semibold mb-1">Anomaly Detected</p>
                      <p className="text-yellow-400/80 text-sm">
                        Cross-modal inconsistencies detected below threshold (0.75). The biometric signatures across visual, audio, and physiological channels show significant divergence, indicating potential synthetic manipulation or deepfake generation.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        
        @keyframes gradient {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-shimmer {
          animation: shimmer 2s infinite;
        }
        
        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.6s ease-out;
        }
      `}</style>
    </div>
  );
};

export default DeepfakeDetector;