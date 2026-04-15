import React, { useState, useEffect, useCallback } from 'react';
import {
  Upload, Play, AlertTriangle, CheckCircle2, Activity, Eye, Mic,
  Brain, Shield, TrendingUp, BarChart3, FileVideo, FileImage,
  Loader2, ShieldCheck, ShieldAlert, X, ChevronRight, Info,
  Cpu, Lock, FlaskConical
} from 'lucide-react';

/* ================================================================
   CONSTANTS
   ================================================================ */
const API_BASE = 'http://localhost:5000';

/* ================================================================
   APP
   ================================================================ */
export default function App() {
  const [file, setFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [fileType, setFileType] = useState(null);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [phase, setPhase] = useState('upload'); // upload | analyzing | results
  const [currentStep, setCurrentStep] = useState('');
  const [backendOk, setBackendOk] = useState(null); // null=checking, true/false
  const [error, setError] = useState(null);

  /* ---------- backend health ---------- */
  const checkHealth = useCallback(async () => {
    try {
      const r = await fetch(`${API_BASE}/api/health`);
      setBackendOk(r.ok);
    } catch {
      setBackendOk(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const id = setInterval(checkHealth, 15000);
    return () => clearInterval(id);
  }, [checkHealth]);


  const clearFile = () => {
    setFile(null);
    setFilePreview(null);
    setFileType(null);
    setResults(null);
    setError(null);
    setPhase('upload');
  };

  /* ---------- drag & drop---------- */
  const onDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const onDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const f = e.dataTransfer?.files?.[0];
    if (f) {
      handleFileDrop(f);
    }
  };

  const handleFileDrop = (f) => {
    setError(null);
    setResults(null);
    setProgress(0);
    setPhase('upload');

    const isVid = f.type?.startsWith('video/');
    const isImg = f.type?.startsWith('image/');
    setFileType(isVid ? 'video' : isImg ? 'image' : null);
    setFile(f);

    if (isImg) {
      const reader = new FileReader();
      reader.onload = (ev) => setFilePreview(ev.target.result);
      reader.readAsDataURL(f);
    } else if (isVid) {
      setFilePreview(URL.createObjectURL(f));
    } else {
      setFilePreview(null);
    }
  };

  const onFilePick = (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    handleFileDrop(f);
  };

  /* ---------- analysis ---------- */
  const startAnalysis = async () => {
    if (!file) return;
    setError(null);
    setPhase('analyzing');
    setProgress(0);

    const steps = [
      'Uploading media…',
      'Extracting visual features…',
      'Running face detection (MTCNN)…',
      'Analyzing with EfficientNet model…',
      'Extracting audio spectrum…',
      'Analyzing blink dynamics…',
      'Computing cross-modal consistency…',
      'Finalizing verdict…'
    ];

    let stepIdx = 0;
    const stepTimer = setInterval(() => {
      if (stepIdx < steps.length) {
        setCurrentStep(steps[stepIdx]);
        stepIdx++;
      }
    }, 1800);

    const progTimer = setInterval(() => {
      setProgress((p) => (p >= 88 ? p : p + 1.5));
    }, 200);

    try {
      const fd = new FormData();
      fd.append('file', file);

      const resp = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        body: fd,
      });

      clearInterval(stepTimer);
      clearInterval(progTimer);
      setProgress(100);
      setCurrentStep('Analysis complete');

      if (!resp.ok) {
        let msg = 'Analysis failed';
        try { msg = (await resp.json()).error || msg; } catch {}
        throw new Error(msg);
      }

      const data = await resp.json();
      console.log('Backend result:', data);

      setTimeout(() => {
        setResults(data);
        setPhase('results');
      }, 600);
    } catch (err) {
      clearInterval(stepTimer);
      clearInterval(progTimer);
      setError(err.message);
      setPhase('upload');
    }
  };

  /* ================================================================
     RENDER
     ================================================================ */
  return (
    <div className="min-h-screen relative" style={{ background: 'var(--bg-primary)' }}>
      {/* Ambient orbs */}
      <div className="ambient-orb animate-float" style={{ width: 500, height: 500, top: -100, right: -100, background: 'radial-gradient(circle, rgba(34,211,238,0.08), transparent 70%)' }} />
      <div className="ambient-orb" style={{ width: 400, height: 400, bottom: -50, left: -80, background: 'radial-gradient(circle, rgba(139,92,246,0.07), transparent 70%)', animationDelay: '3s', animation: 'float 8s ease-in-out infinite' }} />
      <div className="ambient-orb" style={{ width: 300, height: 300, top: '50%', left: '50%', background: 'radial-gradient(circle, rgba(59,130,246,0.05), transparent 70%)', animation: 'float 10s ease-in-out infinite' }} />

      {/* Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 py-8">
        {/* Header */}
        <Header backendOk={backendOk} />

        {/* Main area */}
        {phase === 'upload' && (
          <UploadSection
            file={file}
            fileType={fileType}
            filePreview={filePreview}
            onFilePick={onFilePick}
            onDragOver={onDragOver}
            onDrop={onDrop}
            clearFile={clearFile}
            startAnalysis={startAnalysis}
            backendOk={backendOk}
            error={error}
          />
        )}

        {phase === 'analyzing' && (
          <AnalyzingSection progress={progress} currentStep={currentStep} />
        )}

        {phase === 'results' && results && (
          <ResultsSection results={results} fileType={fileType} onReset={clearFile} />
        )}

        {/* About section — always visible */}
        <AboutSection />
      </div>
    </div>
  );
}

/* ================================================================
   ABOUT SECTION
   ================================================================ */
function AboutSection() {
  const features = [
    {
      icon: Eye,
      color: 'var(--accent-cyan)',
      gradient: 'rgba(34,211,238,0.12)',
      title: 'Visual Analysis',
      desc: 'EfficientNet-B4 deep learning model analyzes facial regions frame-by-frame to detect pixel-level manipulation artifacts invisible to the naked eye.',
    },
    {
      icon: Mic,
      color: 'var(--accent-violet)',
      gradient: 'rgba(139,92,246,0.12)',
      title: 'Audio Analysis',
      desc: 'Spectral decomposition and MFCC feature extraction identify synthetic voice patterns, unnatural pitch shifts, and audio-visual desynchronization.',
    },
    {
      icon: Activity,
      color: 'var(--accent-emerald)',
      gradient: 'rgba(16,185,129,0.12)',
      title: 'Blink Dynamics',
      desc: 'MediaPipe facial landmark tracking measures eye blink rate and patterns. Deepfakes often exhibit abnormal or absent blink behaviour.',
    },
  ];

  const stack = [
    { label: 'EfficientNet-B4', tag: 'Visual Model' },
    { label: 'MTCNN', tag: 'Face Detection' },
    { label: 'MediaPipe', tag: 'Landmark Tracking' },
    { label: 'Librosa', tag: 'Audio DSP' },
    { label: 'Flask + Python', tag: 'Backend API' },
    { label: 'React + Vite', tag: 'Frontend' },
  ];

  return (
    <section className="mt-20 animate-fade-in-up" style={{ animationDelay: '400ms' }}>
      {/* Divider */}
      <div className="flex items-center gap-4 mb-14">
        <div className="flex-1 h-px" style={{ background: 'linear-gradient(90deg, transparent, var(--border-accent))' }} />
        <div className="flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-bold tracking-widest uppercase"
          style={{ background: 'rgba(34,211,238,0.06)', border: '1px solid rgba(34,211,238,0.15)', color: 'var(--accent-cyan)' }}>
          <Info className="w-3.5 h-3.5" /> About DeepGuard
        </div>
        <div className="flex-1 h-px" style={{ background: 'linear-gradient(90deg, var(--border-accent), transparent)' }} />
      </div>

      {/* Hero blurb */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <h2 className="text-3xl sm:text-4xl font-black mb-4 gradient-text">Multimodal Deepfake Detection</h2>
        <p className="text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
          DeepGuard is an AI-powered media authenticity platform that fuses <strong style={{ color: 'var(--text-primary)' }}>visual</strong>,{' '}
          <strong style={{ color: 'var(--text-primary)' }}>audio</strong>, and{' '}
          <strong style={{ color: 'var(--text-primary)' }}>physiological</strong> signals to deliver high-confidence verdicts on whether
          an image or video has been synthetically generated or manipulated.
        </p>
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-14 stagger-children max-w-5xl mx-auto">
        {features.map(({ icon: Icon, color, gradient, title, desc }) => (
          <div key={title} className="glass-card p-6 animate-fade-in-up">
            <div className="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
              style={{ background: gradient }}>
              <Icon className="w-6 h-6" style={{ color }} />
            </div>
            <h3 className="text-sm font-bold mb-2" style={{ color: 'var(--text-primary)' }}>{title}</h3>
            <p className="text-xs leading-relaxed" style={{ color: 'var(--text-muted)' }}>{desc}</p>
          </div>
        ))}
      </div>

      {/* How it works */}
      <div className="glass-card p-8 mb-14">
        <div className="flex items-center gap-3 mb-8">
          <Brain className="w-6 h-6" style={{ color: 'var(--accent-cyan)' }} />
          <h3 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>How It Works</h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {[
            { step: '01', icon: Upload, color: 'var(--accent-cyan)', title: 'Upload Media', desc: 'Drop an image or video file. Supported formats: JPG, PNG, MP4, AVI, MOV.' },
            { step: '02', icon: Cpu, color: 'var(--accent-violet)', title: 'Pipeline Runs', desc: 'Three parallel analysis modules — visual, audio, and blink — process the media simultaneously.' },
            { step: '03', icon: ShieldCheck, color: 'var(--accent-emerald)', title: 'Verdict Delivered', desc: 'A fusion layer weighs all signals and delivers a final Authentic or Deepfake verdict with a confidence score.' },
          ].map(({ step, icon: Icon, color, title, desc }) => (
            <div key={step} className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center font-black text-sm"
                  style={{ background: `${color}18`, color, border: `1px solid ${color}33` }}>
                  {step}
                </div>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Icon className="w-4 h-4" style={{ color }} />
                  <h4 className="text-sm font-bold" style={{ color: 'var(--text-primary)' }}>{title}</h4>
                </div>
                <p className="text-xs leading-relaxed" style={{ color: 'var(--text-muted)' }}>{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tech stack */}
      <div className="glass-card p-8 mb-14">
        <div className="flex items-center gap-3 mb-6">
          <FlaskConical className="w-6 h-6" style={{ color: 'var(--accent-violet)' }} />
          <h3 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>Technology Stack</h3>
        </div>
        <div className="flex flex-wrap gap-3">
          {stack.map(({ label, tag }) => (
            <div key={label} className="flex items-center gap-2 px-4 py-2.5 rounded-xl"
              style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-subtle)' }}>
              <span className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{label}</span>
              <span className="text-xs px-2 py-0.5 rounded-full font-medium"
                style={{ background: 'rgba(34,211,238,0.1)', color: 'var(--accent-cyan)', border: '1px solid rgba(34,211,238,0.2)' }}>
                {tag}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center py-10 mt-4" style={{ borderTop: '1px solid var(--border-subtle)' }}>
        <div className="flex items-center justify-center gap-2 mb-3">
          <Shield className="w-5 h-5" style={{ color: 'var(--accent-cyan)' }} />
          <span className="font-black text-lg gradient-text">DeepGuard AI</span>
        </div>
        <p className="text-xs mb-4" style={{ color: 'var(--text-muted)' }}>
          Multimodal deepfake detection · Visual · Audio · Physiological signals
        </p>
        <div className="flex items-center justify-center gap-1 text-xs" style={{ color: 'var(--text-muted)' }}>
          <Lock className="w-3 h-3" />
          <span>Media is processed locally and never stored.</span>
          <span className="mx-2">·</span>
          <span>Built for academic research &amp; media authenticity.</span>
        </div>
        <p className="mt-6 text-xs" style={{ color: 'var(--text-muted)', opacity: 0.5 }}>
          &copy; {new Date().getFullYear()} DeepGuard — AI Research Project
        </p>
      </footer>
    </section>
  );
}

/* ================================================================
   HEADER
   ================================================================ */
function Header({ backendOk }) {
  return (
    <header className="text-center mb-12 animate-fade-in-up">
      <div className="flex items-center justify-center gap-3 mb-4">
        <div className="relative">
          <Shield className="w-10 h-10" style={{ color: 'var(--accent-cyan)' }} />
          <div className="absolute inset-0 rounded-full animate-pulse-ring" style={{ border: '2px solid var(--accent-cyan)', opacity: 0.3 }} />
        </div>
        <h1 className="text-4xl sm:text-5xl font-black tracking-tight gradient-text">
          DeepGuard
        </h1>
      </div>
      <p className="text-lg font-medium" style={{ color: 'var(--text-secondary)' }}>
        AI-Based Deepfake Detection System
      </p>
      <p className="mt-1 text-sm" style={{ color: 'var(--text-muted)' }}>
        Multimodal analysis · Visual · Audio · Physiological · Cross-Modal Consistency
      </p>

      {/* Backend status pill */}
      <div className="mt-4 inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold"
        style={{
          background: backendOk === true ? 'rgba(16,185,129,0.1)' : backendOk === false ? 'rgba(244,63,94,0.1)' : 'rgba(255,255,255,0.05)',
          border: `1px solid ${backendOk === true ? 'rgba(16,185,129,0.3)' : backendOk === false ? 'rgba(244,63,94,0.3)' : 'rgba(255,255,255,0.1)'}`,
          color: backendOk === true ? '#34d399' : backendOk === false ? '#fb7185' : 'var(--text-muted)'
        }}>
        <div className="w-2 h-2 rounded-full" style={{
          background: backendOk === true ? '#34d399' : backendOk === false ? '#f43f5e' : '#64748b',
          boxShadow: backendOk === true ? '0 0 8px rgba(52,211,153,0.5)' : 'none',
        }} />
        {backendOk === true ? 'Backend Connected' : backendOk === false ? 'Backend Offline' : 'Checking…'}
      </div>
    </header>
  );
}

/* ================================================================
   UPLOAD SECTION
   ================================================================ */
function UploadSection({ file, fileType, filePreview, onFilePick, onDragOver, onDrop, clearFile, startAnalysis, backendOk, error }) {
  const openImagePicker = () => { const el = document.getElementById('image-input'); if (el) { el.value = ''; el.click(); } };
  const openVideoPicker = () => { const el = document.getElementById('video-input'); if (el) { el.value = ''; el.click(); } };

  return (
    <div className="max-w-2xl mx-auto animate-fade-in-up delay-200">
      {/* Hidden inputs – outside the drop zone to avoid event conflicts */}
      <input id="image-input" type="file" accept="image/*" className="hidden" onChange={onFilePick} />
      <input id="video-input" type="file" accept="video/*" className="hidden" onChange={onFilePick} />

      <div className="glass-card p-8">
        {/* Upload zone */}
        <div className={`upload-zone ${file ? 'has-file' : ''}`}
          onClick={() => !file && openImagePicker()}
          onDragOver={onDragOver}
          onDrop={onDrop}
          >
          {!file ? (
            <>
              <div className="relative inline-block mb-4">
                <Upload className="w-14 h-14 mx-auto" style={{ color: 'var(--accent-cyan)', opacity: 0.7 }} />
              </div>
              <h3 className="text-xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>
                Upload Media for Analysis
              </h3>
              <p className="text-sm mb-6" style={{ color: 'var(--text-muted)' }}>
                Drag & drop or click to select · Images (JPG, PNG) or Videos (MP4, AVI, MOV)
              </p>
              <div className="flex items-center justify-center gap-3">
                <button className="btn-secondary" onClick={(e) => { e.stopPropagation(); openImagePicker(); }}>
                  <FileImage className="w-4 h-4" /> Image
                </button>
                <button className="btn-secondary" onClick={(e) => { e.stopPropagation(); openVideoPicker(); }}>
                  <FileVideo className="w-4 h-4" /> Video
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-4">
              {/* Preview thumbnail */}
              <div className="w-20 h-20 rounded-xl overflow-hidden flex-shrink-0 bg-black/30 flex items-center justify-center">
                {fileType === 'image' && filePreview ? (
                  <img src={filePreview} alt="preview" className="w-full h-full object-cover" />
                ) : fileType === 'video' ? (
                  <FileVideo className="w-8 h-8" style={{ color: 'var(--accent-violet)' }} />
                ) : (
                  <FileImage className="w-8 h-8" style={{ color: 'var(--accent-cyan)' }} />
                )}
              </div>
              <div className="flex-1 text-left min-w-0">
                <p className="font-semibold truncate" style={{ color: 'var(--text-primary)' }}>{file.name}</p>
                <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>
                  {fileType === 'video' ? 'Video' : 'Image'} · {(file.size / (1024 * 1024)).toFixed(1)} MB
                </p>
              </div>
              <button onClick={(e) => { e.stopPropagation(); clearFile(); }} className="p-2 rounded-lg hover:bg-white/5 transition">
                <X className="w-5 h-5" style={{ color: 'var(--text-muted)' }} />
              </button>
            </div>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="mt-4 p-3 rounded-xl flex items-start gap-3" style={{ background: 'rgba(244,63,94,0.08)', border: '1px solid rgba(244,63,94,0.2)' }}>
            <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: '#f43f5e' }} />
            <p className="text-sm" style={{ color: '#fb7185' }}>{error}</p>
          </div>
        )}

        {/* Backend warning */}
        {file && backendOk === false && (
          <div className="mt-4 p-3 rounded-xl flex items-start gap-3" style={{ background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.2)' }}>
            <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: '#f59e0b' }} />
            <div>
              <p className="text-sm font-semibold" style={{ color: '#fbbf24' }}>Backend Not Connected</p>
              <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>Start the backend: <code className="px-1.5 py-0.5 rounded text-xs" style={{ background: 'rgba(255,255,255,0.06)' }}>python run.py</code></p>
            </div>
          </div>
        )}

        {/* Analyze button */}
        {file && (
          <div className="mt-6 text-center">
            <button
              className="btn-primary text-lg px-10 py-4"
              onClick={startAnalysis}
              disabled={!backendOk}
            >
              <Play className="w-5 h-5" />
              Start Deep Analysis
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-3 gap-3 mt-6 stagger-children">
        {[
          { icon: Eye, label: 'Visual Analysis', desc: 'EfficientNet + face detection', color: 'var(--accent-cyan)' },
          { icon: Mic, label: 'Audio Analysis', desc: 'Spectral & MFCC features', color: 'var(--accent-violet)' },
          { icon: Activity, label: 'Blink Dynamics', desc: 'MediaPipe eye tracking', color: 'var(--accent-emerald)' },
        ].map(({ icon: Icon, label, desc, color }) => (
          <div key={label} className="glass-card p-4 text-center animate-fade-in-up">
            <Icon className="w-6 h-6 mx-auto mb-2" style={{ color }} />
            <p className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{label}</p>
            <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ================================================================
   ANALYZING SECTION
   ================================================================ */
function AnalyzingSection({ progress, currentStep }) {
  const pipelineSteps = [
    { label: 'Visual', icon: Eye, threshold: 15 },
    { label: 'Audio', icon: Mic, threshold: 40 },
    { label: 'Blink', icon: Activity, threshold: 60 },
    { label: 'Consistency', icon: BarChart3, threshold: 80 },
  ];

  return (
    <div className="max-w-3xl mx-auto animate-fade-in-up">
      <div className="glass-card p-10">
        {/* Title */}
        <div className="flex items-center gap-4 mb-8">
          <div className="relative">
            <Brain className="w-10 h-10 animate-spin-slow" style={{ color: 'var(--accent-cyan)' }} />
          </div>
          <div>
            <h2 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>
              Analyzing Media
            </h2>
            <p className="text-sm font-medium mt-1" style={{ color: 'var(--accent-cyan)' }}>
              {currentStep}
            </p>
          </div>
        </div>

        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>Processing Pipeline</span>
            <span className="text-lg font-bold" style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)' }}>
              {Math.round(progress)}%
            </span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>

        {/* Pipeline steps */}
        <div className="grid grid-cols-4 gap-4">
          {pipelineSteps.map(({ label, icon: Icon, threshold }) => {
            const active = progress >= threshold;
            const done = progress >= threshold + 20;
            return (
              <div key={label} className="text-center p-4 rounded-xl transition-all duration-500" style={{
                background: active ? 'rgba(34,211,238,0.06)' : 'rgba(255,255,255,0.02)',
                border: `1px solid ${active ? 'rgba(34,211,238,0.2)' : 'var(--border-subtle)'}`,
              }}>
                <div className="w-12 h-12 mx-auto rounded-xl flex items-center justify-center mb-3" style={{
                  background: active ? 'linear-gradient(135deg, rgba(34,211,238,0.15), rgba(59,130,246,0.15))' : 'rgba(255,255,255,0.04)',
                }}>
                  {done ? (
                    <CheckCircle2 className="w-6 h-6" style={{ color: '#34d399' }} />
                  ) : active ? (
                    <Loader2 className="w-6 h-6 animate-spin" style={{ color: 'var(--accent-cyan)' }} />
                  ) : (
                    <Icon className="w-6 h-6" style={{ color: 'var(--text-muted)' }} />
                  )}
                </div>
                <p className="text-xs font-semibold" style={{ color: active ? 'var(--text-primary)' : 'var(--text-muted)' }}>{label}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ================================================================
   RESULTS SECTION
   ================================================================ */
function ResultsSection({ results, fileType, onReset }) {
  const overall = results?.overall || {};
  const isAuthentic = overall.authentic;
  const confidence = overall.confidence || 0;
  const isImage = fileType === 'image';

  return (
    <div className="max-w-5xl mx-auto space-y-6 stagger-children">
      {/* Verdict banner */}
      <VerdictBanner isAuthentic={isAuthentic} confidence={confidence} verdict={overall.verdict} />

      {/* Modality cards */}
      <div className={`grid grid-cols-1 ${isImage ? 'max-w-md mx-auto' : 'md:grid-cols-3'} gap-4`}>
        <ModalityCard
          title="Visual Analysis"
          icon={Eye}
          color="var(--accent-cyan)"
          gradientFrom="rgba(34,211,238,0.12)"
          data={results.visual}
        />
        {!isImage && (
          <>
            <ModalityCard
              title="Audio Analysis"
              icon={Mic}
              color="var(--accent-violet)"
              gradientFrom="rgba(139,92,246,0.12)"
              data={results.audio}
            />
            <ModalityCard
              title="Blink Dynamics"
              icon={Activity}
              color="var(--accent-emerald)"
              gradientFrom="rgba(16,185,129,0.12)"
              data={results.physiological}
            />
          </>
        )}
      </div>



      {/* Reset button */}
      <div className="text-center pt-4 animate-fade-in-up">
        <button className="btn-secondary text-base px-8 py-3" onClick={onReset}>
          <Upload className="w-4 h-4" /> Analyze Another File
        </button>
      </div>
    </div>
  );
}

/* ================================================================
   VERDICT BANNER
   ================================================================ */
function VerdictBanner({ isAuthentic, confidence, verdict }) {
  const accentColor = isAuthentic ? 'var(--accent-emerald)' : 'var(--accent-rose)';
  const bgGlow = isAuthentic ? 'rgba(16,185,129,0.06)' : 'rgba(244,63,94,0.06)';
  const borderColor = isAuthentic ? 'rgba(16,185,129,0.3)' : 'rgba(244,63,94,0.3)';

  return (
    <div className="animate-fade-in-up glass-card p-8" style={{
      background: `linear-gradient(135deg, ${bgGlow}, transparent)`,
      borderColor,
      boxShadow: isAuthentic ? 'var(--shadow-glow-cyan)' : 'var(--shadow-glow-rose)',
    }}>
      <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <div className="relative">
            {isAuthentic ? (
              <ShieldCheck className="w-16 h-16" style={{ color: accentColor }} />
            ) : (
              <ShieldAlert className="w-16 h-16" style={{ color: accentColor }} />
            )}
            <div className="absolute inset-0 rounded-full" style={{
              background: accentColor,
              filter: 'blur(20px)',
              opacity: 0.2,
            }} />
          </div>
          <div>
            <h2 className={`text-3xl sm:text-4xl font-black tracking-tight ${isAuthentic ? 'gradient-text-emerald' : 'gradient-text-rose'}`}>
              {verdict || (isAuthentic ? 'AUTHENTIC' : 'DEEPFAKE DETECTED')}
            </h2>
            <p className="mt-1 text-sm flex items-center gap-2" style={{ color: 'var(--text-secondary)' }}>
              <TrendingUp className="w-4 h-4" />
              Multimodal analysis complete
            </p>
          </div>
        </div>

        {/* Confidence ring */}
        <div className="text-center flex-shrink-0">
          <div className="relative w-28 h-28">
            <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
              <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="6" />
              <circle cx="50" cy="50" r="42" fill="none" stroke={accentColor} strokeWidth="6"
                strokeDasharray={`${confidence * 2.64} 264`}
                strokeLinecap="round"
                style={{ transition: 'stroke-dasharray 1.2s cubic-bezier(0.4,0,0.2,1)' }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-2xl font-black" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>
                {confidence}
              </span>
              <span className="text-xs font-semibold" style={{ color: 'var(--text-muted)' }}>%</span>
            </div>
          </div>
          <p className="text-xs mt-1 font-medium" style={{ color: 'var(--text-muted)' }}>Confidence</p>
        </div>
      </div>
    </div>
  );
}

/* ================================================================
   MODALITY CARD
   ================================================================ */
function ModalityCard({ title, icon: Icon, color, gradientFrom, data }) {
  const score = data?.score ?? 0;
  const status = data?.status || 'unknown';
  const timeline = data?.timeline || [0,0,0,0,0];
  const details = data?.features || data?.metrics || data?.artifacts || [];

  const statusClass = status === 'authentic' ? 'status-authentic'
    : status === 'suspicious' ? 'status-suspicious'
    : status === 'fake' ? 'status-fake'
    : 'status-suspicious';

  const statusLabel = status === 'authentic' ? 'Authentic'
    : status === 'suspicious' ? 'Suspicious'
    : status === 'fake' ? 'Fake Detected'
    : 'N/A';

  const maxTimeline = Math.max(...timeline, 1);

  return (
    <div className="glass-card p-6 animate-fade-in-up">
      {/* Header */}
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: gradientFrom }}>
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
        <div>
          <h3 className="text-sm font-bold" style={{ color: 'var(--text-primary)' }}>{title}</h3>
          <span className={`status-badge mt-1 ${statusClass}`}>
            <span className="w-1.5 h-1.5 rounded-full" style={{ background: 'currentColor' }} />
            {statusLabel}
          </span>
        </div>
      </div>

      {/* Score */}
      <div className="flex items-end justify-between mb-3">
        <span className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>Score</span>
        <span className="text-3xl font-black" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>
          {score}<span className="text-base font-semibold" style={{ color: 'var(--text-muted)' }}>%</span>
        </span>
      </div>

      {/* Progress bar */}
      <div className="progress-track mb-5">
        <div className="progress-fill" style={{ width: `${Math.min(score, 100)}%`, background: `linear-gradient(90deg, ${color}, ${color}88)` }} />
      </div>

      {/* Mini timeline */}
      <div className="flex items-end gap-1 h-10 mb-4">
        {timeline.map((v, i) => (
          <div key={i} className="flex-1 flex items-end">
            <div className="w-full rounded-t transition-all duration-700"
              style={{
                height: `${Math.max((v / maxTimeline) * 100, 4)}%`,
                background: `linear-gradient(to top, ${color}88, ${color}33)`,
                minHeight: 2,
              }}
            />
          </div>
        ))}
      </div>

      {/* Details */}
      {details.length > 0 && (
        <div className="space-y-1.5">
          {details.slice(0, 3).map((d, i) => (
            <div key={i} className="flex items-start gap-2 text-xs" style={{ color: 'var(--text-muted)' }}>
              <Info className="w-3 h-3 mt-0.5 flex-shrink-0" style={{ color }} />
              <span>{d}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

