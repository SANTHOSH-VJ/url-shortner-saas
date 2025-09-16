import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  const [longUrl, setLongUrl] = useState('')
  const [shortUrl, setShortUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function shorten() {
    setError(null)
    setShortUrl(null)
    try {
      const res = await fetch('/api/v1/urls', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ long_url: longUrl })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed')
      setShortUrl(data.short_url)
    } catch (e: any) {
      setError(e.message)
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, Arial, sans-serif', margin: '2rem' }}>
      <h2>URL Shortener</h2>
      <div style={{ display: 'flex', gap: '.5rem' }}>
        <input value={longUrl} onChange={e => setLongUrl(e.target.value)} placeholder="https://example.com" style={{ flex: 1, padding: '.6rem .8rem' }} />
        <button onClick={shorten} style={{ padding: '.6rem 1rem' }}>Shorten</button>
      </div>
      {shortUrl && <p>Short URL: <a href={shortUrl} target="_blank" rel="noreferrer">{shortUrl}</a></p>}
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
    </div>
  )
}

createRoot(document.getElementById('root')!).render(<App />)

