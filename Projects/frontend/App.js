const { useState, useEffect, useRef } = React;

const App = () => {
    const [events, setEvents] = useState([]);
    const [threats, setThreats] = useState([]);
    const [stats, setStats] = useState({ riskScore: 28, activeThreats: 2, logsSpeed: "1.2k/s", systemHealth: "HEALTHY" });
    const [isAutonomous, setIsAutonomous] = useState("ADVISORY");
    const [activeTab, setActiveTab] = useState("DASHBOARD");
    const [promptLabInput, setPromptLabInput] = useState("");
    const [promptLabResult, setPromptLabResult] = useState(null);
    const graphRef = useRef(null);

    // Sidebar Icons (SVG)
    const Icons = {
        Dashboard: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>,
        Prompt: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 1 1-7.6-11.7 1 1 0 0 1 .4 1.9 6.5 6.5 0 1 0 5.2 6z"></path><polyline points="16 12 12 8 8 12"></polyline><line x1="12" y1="16" x2="12" y2="8"></line></svg>,
        Graph: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>,
        Policy: () => <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
    };

    useEffect(() => {
        const interval = setInterval(() => {
            const types = ["IAM_LOGIN", "API_REQUEST", "WAF_BLOCK", "DNS_QUERY", "LLM_SCAN"];
            const status = Math.random() > 0.1 ? "ALLOW" : "ALERT";
            const newEvent = {
                id: Math.random().toString(36).substr(2, 9),
                timestamp: new Date().toLocaleTimeString(),
                type: types[Math.floor(Math.random() * types.length)],
                actor: "worker_" + Math.floor(Math.random() * 50),
                status: status,
                risk: Math.floor(Math.random() * 20)
            };
            setEvents(prev => [newEvent, ...prev.slice(0, 25)]);
        }, 1500);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (!graphRef.current) return;
        const width = graphRef.current.clientWidth;
        const height = graphRef.current.clientHeight;
        const svg = d3.select(graphRef.current).html("").append("svg")
            .attr("width", "100%").attr("height", "100%")
            .style("background", "radial-gradient(circle at center, #1e293b 0%, #0f172a 100%)");

        const nodes = Array.from({ length: activeTab === "GRAPH" ? 40 : 22 }, (_, i) => ({
            id: i,
            label: i < 5 ? "User" : i < 15 ? "Service" : "Honeypot",
            glow: i % 7 === 0 ? "rgba(59, 130, 246, 0.5)" : "none"
        }));

        const links = Array.from({ length: activeTab === "GRAPH" ? 60 : 30 }, () => ({
            source: Math.floor(Math.random() * (activeTab === "GRAPH" ? 40 : 22)),
            target: Math.floor(Math.random() * (activeTab === "GRAPH" ? 40 : 22))
        }));

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(activeTab === "GRAPH" ? 120 : 80))
            .force("charge", d3.forceManyBody().strength(activeTab === "GRAPH" ? -250 : -150))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g").selectAll("line").data(links).enter().append("line")
            .attr("stroke", "#334155").attr("stroke-width", 1).attr("stroke-dasharray", "4 2");

        const node = svg.append("g").selectAll("g").data(nodes).enter().append("g");

        node.append("circle")
            .attr("r", d => d.label === "User" ? 10 : 7)
            .attr("fill", d => d.label === "User" ? "#3b82f6" : d.label === "Honeypot" ? "#f43f5e" : "#10b981")
            .attr("filter", d => d.glow !== "none" ? "drop-shadow(0 0 8px #3b82f6)" : "none");

        simulation.on("tick", () => {
            link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });
    }, [activeTab]);

    const handlePromptLab = async () => {
        setPromptLabResult("Scanning prompt for injection vectors...");
        setTimeout(() => {
            const malicious = ["ignore", "system", "delete", "admin"].some(w => promptLabInput.toLowerCase().includes(w));
            setPromptLabResult(malicious ? "🚨 ALERT: Injection Attempt Blocked. Confidence: 99.8%" : "✅ PROMPT SAFE: Verified by Mistral Defensive Layer.");
        }, 1200);
    };

    return (
        <div className="flex h-screen w-full bg-[#020617] text-slate-200 overflow-hidden font-['Inter']">
            {/* Ultra-Modern Vertical Nav */}
            <div className="w-20 border-r border-slate-800 flex flex-col items-center py-8 gap-10 bg-black/40 backdrop-blur-3xl">
                <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-900/40 cursor-pointer">
                    <span className="text-2xl font-black">B</span>
                </div>
                <nav className="flex flex-col gap-8">
                    {[
                        { id: "DASHBOARD", icon: Icons.Dashboard },
                        { id: "PROMPT_LAB", icon: Icons.Prompt },
                        { id: "GRAPH", icon: Icons.Graph },
                        { id: "POLICIES", icon: Icons.Policy }
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            title={tab.id}
                            className={`p-3 rounded-xl transition-all ${activeTab === tab.id ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20' : 'text-slate-500 hover:text-slate-300 hover:bg-white/5'}`}
                        >
                            <tab.icon />
                        </button>
                    ))}
                </nav>
                <div className="mt-auto flex flex-col gap-4">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse mx-auto shadow-[0_0_8px_rgba(34,197,94,0.6)]" />
                    <span className="text-[10px] font-bold text-slate-600 -rotate-90 tracking-tighter">PRD-CORE-01</span>
                </div>
            </div>

            {/* Main Workspace */}
            <div className="flex-1 flex flex-col p-8 overflow-hidden gap-8 relative">
                <header className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                            {activeTab.replace("_", " ")}
                        </h1>
                        <p className="text-slate-500 text-sm font-medium mt-1 uppercase tracking-widest">BOTCOP DEFENSE PLATFORM v2.4</p>
                    </div>

                    <div className="flex bg-slate-900/80 p-1.5 rounded-full border border-slate-800">
                        {["OFF", "ADVISORY", "FULL"].map(mode => (
                            <button
                                key={mode}
                                onClick={() => setIsAutonomous(mode)}
                                className={`px-4 py-1.5 rounded-full text-[10px] font-black transition-all ${isAutonomous === mode ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
                            >
                                {mode}
                            </button>
                        ))}
                    </div>
                </header>

                <div className="flex-1 min-h-0 flex flex-col">
                    {activeTab === "DASHBOARD" && (
                        <div className="flex-1 grid grid-cols-12 gap-8 min-h-0">
                            <div className="col-span-8 flex flex-col gap-8">
                                <div className="grid grid-cols-4 gap-6">
                                    {[
                                        { title: "Threat Risk", value: stats.riskScore, color: "text-orange-500", trend: "+4%" },
                                        { title: "Active Logs", value: stats.logsSpeed, color: "text-blue-500", trend: "Stable" },
                                        { title: "System Health", value: stats.systemHealth, color: "text-green-500", trend: "99.9%" },
                                        { title: "AI Precision", value: "98.4%", color: "text-purple-500", trend: "High" }
                                    ].map(s => (
                                        <div key={s.title} className="bg-slate-900/40 p-5 rounded-3xl border border-white/5 group hover:border-white/10 transition-all">
                                            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{s.title}</p>
                                            <div className="flex items-baseline gap-2 mt-2">
                                                <h3 className={`text-3xl font-black ${s.color}`}>{s.value}</h3>
                                                <span className="text-[10px] font-bold text-slate-600">{s.trend}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <div className="flex-1 bg-slate-900/20 rounded-[40px] border border-white/5 relative overflow-hidden">
                                    <div ref={graphRef} className="w-full h-full" />
                                </div>
                            </div>

                            <div className="col-span-4 flex flex-col gap-8 overflow-hidden bg-slate-900/40 rounded-[40px] border border-white/5 p-6 backdrop-blur-xl">
                                <h2 className="text-sm font-bold uppercase tracking-widest text-slate-500">Live Ingestion Feed</h2>
                                <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar">
                                    {events.map(e => (
                                        <div key={e.id} className={`p-4 rounded-2xl border border-white/5 ${e.status === 'ALERT' ? 'bg-red-900/10 border-red-500/20' : 'bg-black/20'}`}>
                                            <div className="flex justify-between items-center mb-1">
                                                <span className="text-[9px] font-black text-slate-500 uppercase">{e.type}</span>
                                                <span className={e.status === 'ALERT' ? 'text-red-500' : 'text-green-500'}>{e.status}</span>
                                            </div>
                                            <p className="text-sm font-bold text-white/80">{e.actor}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === "PROMPT_LAB" && (
                        <div className="flex-1 flex flex-col items-center justify-center max-w-4xl mx-auto w-full gap-8">
                            <div className="text-center">
                                <h2 className="text-4xl font-black mb-2 tracking-tighter">PHANTOM SANITIZER</h2>
                                <p className="text-slate-500">Neural Gateway for Prompt Injection Defense</p>
                            </div>
                            <div className="w-full bg-slate-900/40 p-10 rounded-[40px] border border-white/5 shadow-2xl">
                                <textarea
                                    value={promptLabInput}
                                    onChange={(e) => setPromptLabInput(e.target.value)}
                                    className="w-full h-40 bg-black/40 rounded-3xl p-6 text-slate-200 border border-white/10 focus:border-blue-500 focus:outline-none placeholder:text-slate-700 font-mono text-sm mb-6"
                                    placeholder="Test injection attempt here..."
                                />
                                <button onClick={handlePromptLab} className="w-full py-5 bg-blue-600 hover:bg-blue-700 rounded-3xl text-sm font-black shadow-xl">ANALYZE PAYLOAD</button>
                                {promptLabResult && (
                                    <div className={`mt-8 p-6 rounded-3xl border ${promptLabResult.includes('🚨') ? 'bg-red-500/10 border-red-500/30 text-red-200' : 'bg-green-500/10 border-green-500/30 text-green-200'}`}>
                                        {promptLabResult}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {activeTab === "GRAPH" && (
                        <div className="flex-1 bg-slate-900/40 rounded-[40px] border border-white/5 relative overflow-hidden">
                            <div className="absolute top-10 left-10 z-10 flex flex-col gap-2">
                                <h2 className="text-2xl font-black">Entity Relationship Engine</h2>
                                <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">N-Order Graph Deep Scan</p>
                            </div>
                            <div className="absolute bottom-10 left-10 z-10 flex gap-4">
                                <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2 rounded-2xl border border-white/5">
                                    <div className="w-2 h-2 rounded-full bg-blue-500" />
                                    <span className="text-[10px] font-bold text-slate-300 uppercase">Users</span>
                                </div>
                                <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2 rounded-2xl border border-white/5">
                                    <div className="w-2 h-2 rounded-full bg-green-500" />
                                    <span className="text-[10px] font-bold text-slate-300 uppercase">Cloud Assets</span>
                                </div>
                                <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2 rounded-2xl border border-white/5">
                                    <div className="w-2 h-2 rounded-full bg-red-500" />
                                    <span className="text-[10px] font-bold text-slate-300 uppercase">Honeypots</span>
                                </div>
                            </div>
                            <div ref={graphRef} className="w-full h-full" />
                        </div>
                    )}

                    {activeTab === "POLICIES" && (
                        <div className="flex-1 grid grid-cols-2 gap-8 items-start">
                            <div className="bg-slate-900/40 rounded-[40px] border border-white/5 p-10 flex flex-col gap-6">
                                <h2 className="text-2xl font-black mb-2">Autonomous Lockdown</h2>
                                {[
                                    { name: "Critical Log Spike", action: "ISOLATE_CONTAINER", threshold: 90 },
                                    { name: "Suspicious API Depth", action: "REVOKE_TOKEN_DECOY", threshold: 85 },
                                    { name: "Prompt Injection Detected", action: "BLOCK_IP_WAF", threshold: 95 },
                                    { name: "Biometric Typing Anomaly", action: "ENFORCE_MFA", threshold: 75 }
                                ].map((p, idx) => (
                                    <div key={idx} className="bg-black/40 p-6 rounded-3xl border border-white/5 flex justify-between items-center group hover:bg-white/[0.02] transition-all">
                                        <div>
                                            <p className="text-[10px] font-bold text-blue-500 uppercase tracking-widest leading-none mb-1">Policy {idx + 1}</p>
                                            <h3 className="font-bold text-lg">{p.name}</h3>
                                            <p className="text-xs text-slate-500 uppercase mt-1 font-bold">Mitigation: {p.action}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm font-black text-slate-200">{p.threshold}% Confidence</p>
                                            <div className="w-12 h-6 bg-blue-600 rounded-full flex items-center px-1 mt-2">
                                                <div className="w-4 h-4 bg-white rounded-full ml-auto shadow-sm" />
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="bg-gradient-to-br from-blue-900/20 to-slate-900/40 rounded-[40px] border border-white/5 p-10">
                                <h2 className="text-2xl font-black mb-4">Neural Learning Policy</h2>
                                <p className="text-slate-400 text-sm leading-relaxed mb-8">
                                    These policies are updated dynamically by the Mistral 7B reasoning engine.
                                    When a new attack vector is identified in the wild, the reasoning server generates
                                    a temporary enforcement rule that stays active until the threat is mitigated.
                                </p>
                                <div className="space-y-4">
                                    <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                                        <span>Active Rule Propagation</span>
                                        <span>Fast Mode</span>
                                    </div>
                                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                        <div className="w-2/3 bg-blue-500 h-full rounded-full" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <style>{`
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
                .custom-scrollbar::-webkit-scrollbar { width: 4px; }
                .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
                .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.05); border-radius: 10px; }
            `}</style>
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
