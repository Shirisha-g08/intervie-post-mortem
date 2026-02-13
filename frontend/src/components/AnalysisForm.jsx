import { useState } from 'react'

function AnalysisForm({ onComplete }) {
    const [resume, setResume] = useState(null)
    const [jd, setJd] = useState('')
    const [experience, setExperience] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!resume || !jd || !experience) {
            setError('Please fill in all fields.')
            return
        }

        setLoading(true)
        setError('')

        const formData = new FormData()
        formData.append('resume', resume)
        formData.append('job_description', jd)
        formData.append('interview_experience', experience)

        try {
            const response = await fetch('http://127.0.0.1:8000/analyze', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                throw new Error('Analysis failed')
            }

            const data = await response.json()
            onComplete(data)
        } catch (err) {
            setError('An error occurred. Please try again.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-2xl mx-auto">
            <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Start Your Analysis</h2>

            <div className="card">
                <form onSubmit={handleSubmit}>

                    <div className="form-group">
                        <label className="form-label">Upload Resume (PDF)</label>
                        <input
                            type="file"
                            accept=".pdf"
                            onChange={(e) => setResume(e.target.files[0])}
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Job Description</label>
                        <textarea
                            placeholder="Paste the full job description here..."
                            value={jd}
                            onChange={(e) => setJd(e.target.value)}
                            className="form-textarea"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Interview Experience</label>
                        <textarea
                            placeholder="Describe your interview answers clearly. e.g. 'When asked about a challenge, I said I tried to fix it...'"
                            value={experience}
                            onChange={(e) => setExperience(e.target.value)}
                            className="form-textarea"
                        />
                        <small style={{ color: '#64748b' }}>Be as detailed as possible about what you said.</small>
                    </div>

                    {error && <div style={{ color: 'var(--error-color)', marginBottom: '1rem' }}>{error}</div>}

                    {loading ? (
                        <div className="loading-spinner"></div>
                    ) : (
                        <button type="submit" className="btn" style={{ width: '100%' }}>
                            Analyze
                        </button>
                    )}

                </form>
            </div>
        </div>
    )
}

export default AnalysisForm
