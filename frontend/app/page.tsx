"use client";

import { useEffect, useState, useRef } from "react";
import { fetchEvents, processEvent, fetchEventDetails, Event } from "@/lib/api";
import { 
  LayoutDashboard, Users, FileText, Settings, Plus, MapPin, Calendar, 
  Image as ImageIcon, X, Loader2, ArrowLeft, CheckCircle2, AlertCircle, 
  BarChart3, MessageSquare, Mic, FileEdit, Upload, FolderOpen, ChevronRight
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Dashboard() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [inputMode, setInputMode] = useState<"local" | "cloud">("local");
  const [inputPath, setInputPath] = useState("input/");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<number | null>(null);
  const [eventDetails, setEventDetails] = useState<any>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadEvents = () => {
    setLoading(true);
    fetchEvents()
      .then(setEvents)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadEvents();
    // Poll for status updates every 5 seconds if there are processing events
    const interval = setInterval(() => {
        if (events.some(e => e.status === 'processing')) {
            fetchEvents().then(setEvents).catch(console.error);
        }
    }, 5000);
    return () => clearInterval(interval);
  }, [events]);

  const loadEventDetails = async (id: number) => {
    try {
      const details = await fetchEventDetails(id);
      setEventDetails(details);
      setSelectedEventId(id);
    } catch (error) {
      console.error(error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const handleProcess = async (e: React.FormEvent) => {
    e.preventDefault();
    setProcessing(true);
    try {
      // In cloud mode, we'd upload files first. 
      // For this demo, we'll trigger the local path if in local mode.
      await processEvent(inputPath);
      setShowModal(false);
      loadEvents();
    } catch (error) {
      alert(error instanceof Error ? error.message : "Processing failed");
    } finally {
      setProcessing(false);
    }
  };

  if (selectedEventId && eventDetails) {
    return (
      <div className="flex h-screen bg-[#F8FAFC] font-sans">
        {/* Sidebar (same as dashboard for consistency) */}
        <aside className="w-64 bg-white border-r border-slate-200 shadow-sm">
          <div className="p-6">
            <div className="flex items-center space-x-2" onClick={() => setSelectedEventId(null)}>
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center cursor-pointer shadow-lg shadow-indigo-100">
                <ImageIcon className="text-white w-4 h-4" />
              </div>
              <h1 className="text-lg font-bold text-slate-900 tracking-tight cursor-pointer">Sovereign Engine</h1>
            </div>
          </div>
          <nav className="mt-6 space-y-1">
            <button onClick={() => setSelectedEventId(null)} className="w-full flex items-center px-6 py-3 text-slate-500 hover:bg-slate-50 hover:text-indigo-600 transition-all font-semibold text-sm">
              <ArrowLeft className="w-4 h-4 mr-3" />
              Back to Events
            </button>
          </nav>
        </aside>

        <main className="flex-1 overflow-y-auto">
          <motion.header 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="px-10 py-10 bg-white border-b border-slate-200"
          >
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center space-x-3">
                    <h2 className="text-3xl font-black text-slate-900">{eventDetails.name}</h2>
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${
                        eventDetails.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700 animate-pulse'
                    }`}>
                        {eventDetails.status}
                    </span>
                </div>
                <div className="mt-3 flex items-center space-x-5 text-sm text-slate-400 font-bold uppercase tracking-wider">
                  <span className="flex items-center"><MapPin className="w-4 h-4 mr-1.5 text-indigo-500" /> {eventDetails.location}</span>
                  <span className="flex items-center"><Calendar className="w-4 h-4 mr-1.5 text-indigo-500" /> {new Date(eventDetails.date).toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' })}</span>
                </div>
              </div>
              <div className="flex space-x-3">
                <button className="px-5 py-2.5 bg-white border-2 border-slate-200 rounded-xl text-slate-700 font-bold text-sm hover:bg-slate-50 transition-all active:scale-95">Download PDF</button>
                <button className="px-5 py-2.5 bg-indigo-600 text-white rounded-xl font-bold text-sm hover:bg-indigo-700 shadow-xl shadow-indigo-100 transition-all active:scale-95">Publish to Social</button>
              </div>
            </div>
          </motion.header>

          <div className="p-10 space-y-16 max-w-7xl mx-auto">
            {/* Media Gallery */}
            <section>
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-black text-slate-900 flex items-center tracking-tight">
                  <div className="w-2 h-8 bg-indigo-600 rounded-full mr-4" />
                  Media Scorecard
                </h3>
                <p className="text-sm text-slate-400 font-bold">{eventDetails.assets.length} Assets Analyzed</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {eventDetails.assets.map((asset: any, index: number) => (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.05 }}
                    key={asset.id} 
                    className={`bg-white rounded-3xl border-2 p-6 transition-all hover:-translate-y-1 hover:shadow-2xl ${asset.is_selected ? 'border-indigo-100 bg-indigo-50/10' : 'border-slate-100 opacity-50'}`}
                  >
                    <div className="flex justify-between items-start mb-6">
                      <div className="flex flex-col">
                        <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest mb-1">{asset.file_type}</span>
                        <h4 className="text-sm font-bold text-slate-800 truncate max-w-[150px]">{asset.file_path.split('/').pop()}</h4>
                      </div>
                      {asset.is_selected ? (
                        <div className="bg-emerald-500 rounded-full p-1.5 shadow-lg shadow-emerald-200">
                            <CheckCircle2 className="w-4 h-4 text-white" />
                        </div>
                      ) : (
                        <div className="bg-slate-100 rounded-full p-1.5">
                            <AlertCircle className="w-4 h-4 text-slate-300" />
                        </div>
                      )}
                    </div>
                    <div className="aspect-video bg-slate-100 rounded-2xl mb-6 flex items-center justify-center group overflow-hidden">
                       <ImageIcon className="w-8 h-8 text-slate-200 group-hover:scale-110 transition-transform" />
                    </div>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div className="bg-white rounded-2xl p-3 border border-slate-50 text-center">
                        <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest mb-1">Technical</p>
                        <p className={`text-xl font-black ${asset.technical_score >= 7 ? 'text-emerald-600' : 'text-amber-500'}`}>{asset.technical_score}</p>
                      </div>
                      <div className="bg-white rounded-2xl p-3 border border-slate-50 text-center">
                        <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest mb-1">Marketing</p>
                        <p className={`text-xl font-black ${asset.marketing_score >= 7 ? 'text-indigo-600' : 'text-amber-500'}`}>{asset.marketing_score}</p>
                      </div>
                    </div>
                    <div className="bg-slate-50 rounded-2xl p-4">
                        <p className="text-xs text-slate-500 font-medium leading-relaxed italic line-clamp-3">"{asset.justification}"</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </section>

            {/* Generated Content */}
            <section>
              <h3 className="text-xl font-black text-slate-900 mb-8 flex items-center tracking-tight">
                <div className="w-2 h-8 bg-indigo-600 rounded-full mr-4" />
                Draft Output
              </h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                {eventDetails.generations.map((gen: any) => (
                  <motion.div 
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={gen.id} 
                    className="bg-white rounded-3xl shadow-xl shadow-slate-100 border border-slate-100 overflow-hidden flex flex-col"
                  >
                    <div className="p-6 border-b border-slate-50 flex justify-between items-center bg-slate-50/40">
                      <div className="flex items-center">
                        <div className="w-10 h-10 rounded-2xl bg-white border border-slate-100 flex items-center justify-center mr-4 shadow-sm">
                            {gen.platform === 'linkedin' && <MessageSquare className="w-5 h-5 text-indigo-700" />}
                            {gen.platform === 'instagram' && <ImageIcon className="w-5 h-5 text-rose-500" />}
                            {gen.platform === 'instagram_voice' && <Mic className="w-5 h-5 text-violet-500" />}
                            {gen.platform === 'case_study' && <FileText className="w-5 h-5 text-emerald-600" />}
                        </div>
                        <h4 className="font-black text-slate-800 capitalize tracking-tight">{gen.platform.replace('_', ' ')}</h4>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest flex items-center">
                            <CheckCircle2 className="w-3 h-3 mr-1" />
                            AI Grounded
                        </span>
                      </div>
                    </div>
                    <div className="p-8 flex-1">
                      <div className="text-[13px] text-slate-600 leading-relaxed font-medium whitespace-pre-wrap max-h-80 overflow-y-auto bg-slate-50/50 p-6 rounded-3xl border border-slate-100/50 scrollbar-hide">
                        {gen.content}
                      </div>
                      <div className="mt-8 flex justify-between items-center">
                        <div className="flex space-x-3">
                            <button className="flex items-center px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-bold hover:bg-slate-800 transition-all active:scale-95 shadow-lg shadow-slate-200">
                                <FileEdit className="w-3 h-3 mr-2" />
                                Edit Draft
                            </button>
                            {gen.platform === 'instagram_voice' && (
                                <button className="flex items-center px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50 transition-all active:scale-95">
                                    <Mic className="w-3 h-3 mr-2" />
                                    Play Audio
                                </button>
                            )}
                        </div>
                        <div className="flex space-x-2">
                          <button className="p-2.5 text-slate-300 hover:text-rose-500 hover:bg-rose-50 rounded-xl transition-all"><X className="w-5 h-5" /></button>
                          <button className="p-2.5 text-slate-300 hover:text-emerald-500 hover:bg-emerald-50 rounded-xl transition-all"><CheckCircle2 className="w-5 h-5" /></button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </section>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-[#F8FAFC] font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 shadow-sm">
        <div className="p-6">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-100">
              <ImageIcon className="text-white w-4 h-4" />
            </div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">Sovereign Engine</h1>
          </div>
        </div>
        <nav className="mt-8 space-y-1">
          <a href="#" className="flex items-center px-6 py-3 text-indigo-600 bg-indigo-50/50 border-r-4 border-indigo-600 font-bold text-sm">
            <LayoutDashboard className="w-4 h-4 mr-3" />
            Dashboard
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-slate-400 hover:bg-slate-50 hover:text-indigo-600 transition-all font-bold text-sm group">
            <Users className="w-4 h-4 mr-3 text-slate-300 group-hover:text-indigo-400" />
            Brand Profiles
          </a>
          <a href="#" className="flex items-center px-6 py-3 text-slate-400 hover:bg-slate-50 hover:text-indigo-600 transition-all font-bold text-sm group">
            <FileText className="w-4 h-4 mr-3 text-slate-300 group-hover:text-indigo-400" />
            Reports
          </a>
          <div className="pt-10 px-6">
            <div className="bg-indigo-600 rounded-2xl p-5 text-white shadow-xl shadow-indigo-100">
                <p className="text-[10px] font-black uppercase tracking-widest opacity-80 mb-2">Usage</p>
                <p className="text-lg font-black mb-4">42/50 Events</p>
                <div className="w-full bg-indigo-400/30 rounded-full h-1.5">
                    <div className="bg-white w-[84%] h-full rounded-full" />
                </div>
                <button className="mt-4 w-full py-2 bg-white/10 hover:bg-white/20 rounded-xl text-[10px] font-black uppercase tracking-wider transition-all">Upgrade Pro</button>
            </div>
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="flex items-center justify-between px-10 py-10 bg-white border-b border-slate-200">
          <div>
            <h2 className="text-3xl font-black text-slate-900 tracking-tight">Media Operations</h2>
            <p className="text-sm text-slate-400 font-bold mt-1 uppercase tracking-wider">Monitor and process your live event archives.</p>
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="flex items-center px-6 py-3 text-white bg-indigo-600 rounded-2xl hover:bg-indigo-700 active:scale-95 transition-all shadow-2xl shadow-indigo-200 font-black text-sm uppercase tracking-widest"
          >
            <Plus className="w-5 h-5 mr-3" />
            Launch Process
          </button>
        </header>

        <div className="p-10 max-w-7xl mx-auto">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-[50vh] space-y-6">
              <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
              <p className="text-slate-400 font-black text-xs uppercase tracking-widest">Synchronizing Infrastructure...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
              <AnimatePresence>
                {events.length === 0 ? (
                    <motion.div 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="col-span-full p-24 text-center bg-white rounded-[40px] border-4 border-dashed border-slate-100"
                    >
                    <div className="w-20 h-20 bg-slate-50 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                        <ImageIcon className="text-slate-200 w-10 h-10" />
                    </div>
                    <h3 className="text-2xl font-black text-slate-900 tracking-tight">Infrastructure Empty</h3>
                    <p className="text-slate-400 max-w-xs mx-auto mt-3 font-medium text-sm leading-relaxed">Your sovereign content archive is currently empty. Connect a data source to begin.</p>
                    <button 
                        onClick={() => setShowModal(true)}
                        className="mt-10 px-8 py-4 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-slate-800 transition-all shadow-xl shadow-slate-200 active:scale-95"
                    >
                        Process First Event →
                    </button>
                    </motion.div>
                ) : (
                    events.map((event, idx) => (
                    <motion.div 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.05 }}
                        key={event.id} 
                        onClick={() => loadEventDetails(event.id)}
                        className="bg-white rounded-[40px] shadow-2xl shadow-slate-200/50 border border-slate-100 overflow-hidden hover:shadow-indigo-100/50 hover:border-indigo-100 transition-all group cursor-pointer"
                    >
                        <div className="p-8">
                        <div className="flex justify-between items-start mb-10">
                            <div className="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center group-hover:bg-indigo-600 group-hover:rotate-6 transition-all duration-500">
                                <ImageIcon className="text-slate-200 w-6 h-6 group-hover:text-white transition-colors" />
                            </div>
                            <span className={`text-[10px] px-3 py-1.5 rounded-full font-black uppercase tracking-widest ${
                            event.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 
                            event.status === 'processing' ? 'bg-indigo-100 text-indigo-700 animate-pulse' : 
                            'bg-rose-100 text-rose-700'
                            }`}>
                            {event.status}
                            </span>
                        </div>
                        <h3 className="text-xl font-black text-slate-900 group-hover:text-indigo-600 transition-colors mb-3 leading-tight">{event.name}</h3>
                        <div className="space-y-2">
                            <div className="flex items-center text-xs text-slate-400 font-bold uppercase tracking-wider">
                            <MapPin className="w-3.5 h-3.5 mr-2 text-indigo-400" />
                            {event.location}
                            </div>
                            <div className="flex items-center text-xs text-slate-400 font-bold uppercase tracking-wider">
                            <Calendar className="w-3.5 h-3.5 mr-2 text-indigo-400" />
                            {new Date(event.date).toLocaleDateString()}
                            </div>
                        </div>
                        <div className="mt-10 grid grid-cols-2 gap-6 pt-8 border-t border-slate-50">
                            <div>
                            <p className="text-[10px] text-slate-300 font-black uppercase tracking-widest mb-1">Visuals</p>
                            <p className="text-2xl font-black text-indigo-600">{event.asset_count}</p>
                            </div>
                            <div>
                            <p className="text-[10px] text-slate-300 font-black uppercase tracking-widest mb-1">Impact</p>
                            <div className="flex items-center">
                                <p className="text-2xl font-black text-slate-900">{event.generation_count}</p>
                                <ChevronRight className="w-4 h-4 ml-2 text-slate-200 group-hover:translate-x-1 transition-transform" />
                            </div>
                            </div>
                        </div>
                        </div>
                    </motion.div>
                    ))
                )}
              </AnimatePresence>
            </div>
          )}
        </div>
      </main>

      {/* Modal */}
      <AnimatePresence>
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-md">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="bg-white w-full max-w-2xl rounded-[40px] shadow-3xl overflow-hidden border border-white/20"
          >
            <div className="p-8 border-b border-slate-50 flex justify-between items-center bg-slate-50/30">
              <div>
                <h3 className="text-2xl font-black text-slate-900 tracking-tight">Intelligence Bootloader</h3>
                <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest mt-1">Configure your ingestion vector</p>
              </div>
              <button 
                onClick={() => !processing && setShowModal(false)}
                className="bg-white p-2 rounded-2xl border border-slate-100 hover:bg-slate-50 text-slate-400 transition-all shadow-sm"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-10">
                {/* Input Mode Toggle */}
                <div className="flex bg-slate-100 p-1.5 rounded-3xl mb-10">
                    <button 
                        onClick={() => setInputMode("local")}
                        className={`flex-1 flex items-center justify-center py-4 rounded-[22px] text-xs font-black uppercase tracking-widest transition-all ${inputMode === 'local' ? 'bg-white text-indigo-600 shadow-xl shadow-slate-200' : 'text-slate-400'}`}
                    >
                        <FolderOpen className="w-4 h-4 mr-2" />
                        Local Source
                    </button>
                    <button 
                        onClick={() => setInputMode("cloud")}
                        className={`flex-1 flex items-center justify-center py-4 rounded-[22px] text-xs font-black uppercase tracking-widest transition-all ${inputMode === 'cloud' ? 'bg-white text-indigo-600 shadow-xl shadow-slate-200' : 'text-slate-400'}`}
                    >
                        <Upload className="w-4 h-4 mr-2" />
                        Cloud Stream
                    </button>
                </div>

                <form onSubmit={handleProcess} className="space-y-10">
                    <AnimatePresence mode="wait">
                        {inputMode === 'local' ? (
                            <motion.div 
                                key="local"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                            >
                                <label className="block text-[10px] font-black text-slate-400 mb-4 uppercase tracking-[0.2em]">Source Directory Path</label>
                                <div className="relative group">
                                    <div className="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                                        <FolderOpen className="h-5 w-5 text-indigo-500 group-focus-within:scale-110 transition-transform" />
                                    </div>
                                    <input 
                                        type="text" 
                                        value={inputPath}
                                        onChange={(e) => setInputPath(e.target.value)}
                                        className="w-full pl-14 pr-5 py-5 bg-slate-50 rounded-[28px] border-2 border-transparent focus:border-indigo-100 focus:bg-white outline-none transition-all font-bold text-slate-700 shadow-inner"
                                        placeholder="e.g., assets/may-event/"
                                        required
                                    />
                                </div>
                                <p className="text-[10px] text-slate-400 mt-4 font-bold flex items-center">
                                    <AlertCircle className="w-3 h-3 mr-1.5" />
                                    The engine will automatically infer event details from your visual content.
                                </p>
                            </motion.div>
                        ) : (
                            <motion.div 
                                key="cloud"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                            >
                                <label className="block text-[10px] font-black text-slate-400 mb-4 uppercase tracking-[0.2em]">Drop Zone</label>
                                <div 
                                    onClick={() => fileInputRef.current?.click()}
                                    className="w-full py-16 bg-indigo-50/30 rounded-[40px] border-4 border-dashed border-indigo-100 flex flex-col items-center justify-center group cursor-pointer hover:bg-indigo-50/50 transition-all"
                                >
                                    <div className="w-16 h-16 bg-white rounded-3xl shadow-xl shadow-indigo-100 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
                                        <Upload className="w-8 h-8 text-indigo-600" />
                                    </div>
                                    <p className="text-sm font-black text-slate-900 tracking-tight">Select Media Stream</p>
                                    <p className="text-[10px] text-indigo-400 font-bold uppercase tracking-widest mt-2">JPG, MP4 supported (Max 1GB)</p>
                                    {selectedFiles.length > 0 && (
                                        <div className="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-full text-[10px] font-black uppercase tracking-widest">
                                            {selectedFiles.length} items ready
                                        </div>
                                    )}
                                </div>
                                <input 
                                    type="file" 
                                    multiple 
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                    className="hidden" 
                                    accept="image/*,video/*"
                                />
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <button 
                        type="submit" 
                        disabled={processing || (inputMode === 'cloud' && selectedFiles.length === 0)}
                        className="w-full group relative overflow-hidden flex items-center justify-center px-10 py-6 text-white bg-indigo-600 rounded-[32px] font-black text-sm uppercase tracking-[0.3em] hover:bg-indigo-700 disabled:opacity-30 disabled:cursor-not-allowed transition-all shadow-3xl shadow-indigo-200 active:scale-95"
                    >
                        {processing ? (
                            <>
                                <Loader2 className="w-6 h-6 mr-4 animate-spin" />
                                Deploying Intelligence...
                            </>
                        ) : (
                            <>
                                Launch sovereign Engine
                                <ChevronRight className="w-5 h-5 ml-4 group-hover:translate-x-2 transition-transform" />
                            </>
                        )}
                    </button>
                </form>
            </div>
          </motion.div>
        </div>
      )}
      </AnimatePresence>
    </div>
  );
}
