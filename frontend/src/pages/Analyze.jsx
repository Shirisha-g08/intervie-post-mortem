
import { useState } from 'react'
import AnalysisForm from '../components/AnalysisForm'
import ResultsDashboard from '../components/ResultsDashboard'

function Analyze() {
    const [results, setResults] = useState(null)

    const handleAnalysisComplete = (data) => {
        setResults(data)
    }

    // When "Analyze Another" is clicked, clear results to show form again.
    // Alternatively, could navigate('/') if desired, but clearing state keeps user in flow.
    const handleReset = () => {
        setResults(null)
    }

    return (
        <div>
            {results ? (
                <ResultsDashboard data={results} onReset={handleReset} />
            ) : (
                <AnalysisForm onComplete={handleAnalysisComplete} />
            )}
        </div>
    )
}

export default Analyze
