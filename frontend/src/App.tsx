import { Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from './components/layout/AppShell'
import { CountrySearchPage } from './pages/CountrySearchPage'
import { CountryDashboardPage } from './pages/CountryDashboardPage'
import { AboutDataPage } from './pages/AboutDataPage'

export function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Navigate to="/countries" replace />} />
        <Route path="/countries" element={<CountrySearchPage />} />
        <Route path="/countries/:iso3" element={<CountryDashboardPage />} />
        <Route path="/about-data" element={<AboutDataPage />} />
      </Routes>
    </AppShell>
  )
}
