function ResultsDashboard({ data, onReset }) {
    if (!data) return null;

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2>Analysis Results</h2>
                <button onClick={onReset} className="btn" style={{ backgroundColor: 'white', color: 'var(--text-color)', border: '1px solid #e2e8f0' }}>
                    Analyze Another
                </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                {/* Match Score */}
                <div className="card score-card">
                    <div className="score-value">{data.match_score}%</div>
                    <div className="score-label">Resume Match</div>
                    <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#64748b' }}>{data.skill_gap_explanation}</p>
                </div>

                {/* Clarity Score */}
                <div className="card score-card">
                    <div className="score-value text-blue-500">{data.clarity_score}</div>
                    <div className="score-label">Clarity Score</div>
                    <div className="badge" style={{ marginTop: '1rem', background: '#e0f2fe', color: '#0369a1' }}>
                        Confidence: {data.confidence_rating}
                    </div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>

                {/* Likely Rejection Reasons */}
                <div>
                    <h3 style={{ marginBottom: '1rem' }}>Likely Rejection Reasons</h3>
                    {data.rejection_reasons.map((reason, idx) => (
                        <div key={idx} className={`card reason-card ${reason.severity}`}>
                            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                <h4 style={{ margin: '0 0 0.5rem 0' }}>{reason.reason}</h4>
                                <span className={`badge ${reason.severity}`}>{reason.severity} Severity</span>
                            </div>
                            <p style={{ margin: 0, color: '#475569' }}>{reason.explanation}</p>
                            <div style={{ marginTop: '1rem', fontSize: '0.9rem', fontWeight: 600, color: 'var(--primary-color)' }}>
                                💡 Fix: {reason.fix}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Action Plan */}
                <div>
                    <h3 style={{ marginBottom: '1rem' }}>Action Plan</h3>

                    <div className="card">
                        <h4 style={{ marginTop: 0 }}>Resume Improvements</h4>
                        {data.match_score === 100 ? (
                            <p>Your resume is perfectly aligned!</p>
                        ) : (
                            <ul style={{ paddingLeft: '1.25rem' }}>
                                {data.action_plan.resume_improvements.length > 0 ? (
                                    data.action_plan.resume_improvements.map((item, i) => (
                                        <li key={i} style={{ marginBottom: '0.5rem' }}>{item}</li>
                                    ))
                                ) : (
                                    <li>Review missing skills.</li>
                                )}
                            </ul>
                        )}

                        <h4 style={{ marginTop: '1.5rem' }}>Interview Prep</h4>
                        <ul style={{ paddingLeft: '1.25rem' }}>
                            {data.action_plan.interview_prep.map((item, i) => (
                                <li key={i} style={{ marginBottom: '0.5rem' }}>{item}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="card">
                        <h4 style={{ marginTop: 0 }}>Missing Skills</h4>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                            {data.missing_skills.map((skill, i) => (
                                <span key={i} style={{ background: '#f1f5f9', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.85rem' }}>
                                    {skill}
                                </span>
                            ))}
                            {data.missing_skills.length === 0 && <span style={{ color: '#64748b' }}>None detected.</span>}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}

export default ResultsDashboard
