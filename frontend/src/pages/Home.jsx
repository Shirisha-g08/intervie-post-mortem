
import { useNavigate } from 'react-router-dom'
import LandingPage from '../components/LandingPage'

function Home() {
    const navigate = useNavigate()

    const handleStart = () => {
        navigate('/analyze')
    }

    return <LandingPage onStart={handleStart} />
}

export default Home
