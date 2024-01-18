import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import { SettingsPage } from './pages/SettingsPage'
import { SettingsHistoryPage } from './pages/SettingsHistoryPage'
import { Navigation } from './components/Navigation'

function App(){
  return(
    <div className='container mx-auto'>
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Navigate to="/create" />}/>
        <Route path="/create" element={<SettingsPage />}/>
        <Route path="/history" element={<SettingsHistoryPage />}/>
      </Routes>
    </BrowserRouter>
    </div>

  )
}

export default App