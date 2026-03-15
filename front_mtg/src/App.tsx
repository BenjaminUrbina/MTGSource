import './App.css'
import { API_BASE_URL } from './lib/api'

const nextSteps = [
  'Create an auth module for register, login and token refresh.',
  'Add an inventory screen that consumes /api/mis-inventarios/.',
  'Add shared API helpers and typed DTOs before feature work grows.',
]

function App() {
  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">MTGSource frontend</p>
        <h1>React + TypeScript + Vite base</h1>
        <p className="lead">
          This is a clean starting point for the frontend. No UI system, no
          routing, and no feature code yet.
        </p>
      </section>

      <section className="card">
        <h2>API</h2>
        <p>
          Default base URL: <code>{API_BASE_URL}</code>
        </p>
        <p>
          In local development, Vite proxies <code>/api</code> to the Django
          server on <code>http://127.0.0.1:8000</code>.
        </p>
      </section>

      <section className="card">
        <h2>Suggested next steps</h2>
        <ul>
          {nextSteps.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default App
