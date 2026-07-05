import { Link, NavLink } from 'react-router-dom'
import { Globe } from 'lucide-react'

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  isActive
    ? 'text-blue-600 font-medium'
    : 'text-slate-600 hover:text-slate-900'

export function Header() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link to="/countries" className="flex items-center gap-2">
          <Globe className="h-6 w-6 text-blue-600" />
          <span className="text-lg font-semibold">TradeLens</span>
        </Link>
        <nav className="flex items-center gap-6 text-sm">
          <NavLink to="/countries" className={navLinkClass}>
            Countries
          </NavLink>
          <NavLink to="/about-data" className={navLinkClass}>
            About Data
          </NavLink>
        </nav>
      </div>
    </header>
  )
}
