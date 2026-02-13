function LandingPage({ onStart }) {
    return (
        <div className="landing-hero fade-in">
            <h1>Didn’t get selected? <br /><span style={{ color: 'var(--primary-color)' }}>Understand why.</span></h1>
            <p>
                Get structured feedback on your interview performance based on alignment with the job description and your communication style.
            </p>
            <button className="btn" onClick={onStart} style={{ fontSize: '1.25rem', padding: '1rem 2.5rem' }}>
                Analyze My Interview
            </button>

            <div style={{ marginTop: '4rem', display: 'flex', gap: '2rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                <div className="card" style={{ maxWidth: '300px', textAlign: 'left' }}>
                    <h3>Resume Analysis</h3>
                    <p>Find out matched keywords and missing skills compared to the JD.</p>
                </div>
                <div className="card" style={{ maxWidth: '300px', textAlign: 'left' }}>
                    <h3>Communication Check</h3>
                    <p>Detect passive language and unstructured responses in your answers.</p>
                </div>
                <div className="card" style={{ maxWidth: '300px', textAlign: 'left' }}>
                    <h3>Actionable Tips</h3>
                    <p>Receive specific advice on how to improve for next time.</p>
                </div>
            </div>
        </div>
    )
}

export default LandingPage
