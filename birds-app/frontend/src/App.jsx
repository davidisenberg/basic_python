import { useState, useCallback, useRef, useMemo, useEffect } from 'react'
import './App.css'

const COLUMNS = [
  { key: 'locName',            line1: 'Hotspot',      line2: '',           numeric: false },
  { key: 'score',              line1: 'Score',        line2: '',           numeric: true  },
  { key: 'numSpeciesTwoWeeks', line1: 'Species',      line2: '2 wks',      numeric: true  },
  { key: 'numBirdsTwoWeeks',   line1: 'Birds',        line2: '2 wks',      numeric: true  },
  { key: 'numHighValue',       line1: 'Migrants',     line2: '',           numeric: true  },
  { key: 'numRaptors',         line1: 'Raptors',      line2: '',           numeric: true  },
  { key: 'numWarblers',        line1: 'Warblers',     line2: '',           numeric: true  },
  { key: 'numShorebirds',      line1: 'Shore',        line2: 'birds',      numeric: true  },
  { key: 'numWaterfowl',       line1: 'Water',        line2: 'fowl',       numeric: true  },
  { key: 'numChecklists',      line1: 'Check',        line2: 'lists',      numeric: true  },
  { key: 'numContributors',    line1: 'Contrib',      line2: 'utors',      numeric: true  },
  { key: 'numSpeciesAllTime',  line1: 'Species',      line2: 'all time',   numeric: true  },
  { key: 'distance_miles',     line1: 'Dist',         line2: 'mi',         numeric: true  },
  { key: 'duration2',          line1: 'Drive',        line2: 'hrs',        numeric: true  },
]

const DEFAULT_WEIGHTS = {
  migrants:     3.0,
  raptors:      2.0,
  warblers:     3.0,
  shorebirds:   1.5,
  waterfowl:    0.7,
  other:        1.0,
  drivePenalty: 0.75,
}

function computeRank(row, w) {
  const other = Math.max(0,
    (row.numSpeciesTwoWeeks ?? 0)
    - (row.numHighValue ?? 0) - (row.numRaptors ?? 0) - (row.numWarblers ?? 0)
    - (row.numShorebirds ?? 0) - (row.numWaterfowl ?? 0)
  )
  const weighted =
    (row.numHighValue  ?? 0) * w.migrants +
    (row.numRaptors    ?? 0) * w.raptors +
    (row.numWarblers   ?? 0) * w.warblers +
    (row.numShorebirds ?? 0) * w.shorebirds +
    (row.numWaterfowl  ?? 0) * w.waterfowl +
    other * w.other
  const checklistFactor = Math.max(1, row.numChecklists ?? 1) ** 0.3
  const durationMins = Math.max(1, (row.duration2 ?? 0) * 60)
  return (row.numSpeciesTwoWeeks ?? 0) ** 2 * weighted * checklistFactor / durationMins ** w.drivePenalty
}

function applyScores(results, weights) {
  const ranked = results.map(row => ({ ...row, _rank: computeRank(row, weights) }))
  const ranks = ranked.map(r => r._rank)
  const lo = Math.min(...ranks)
  const hi = Math.max(...ranks)
  return ranked.map(row => ({
    ...row,
    score: hi > lo ? Math.round(1 + 99 * (row._rank - lo) / (hi - lo)) : 50,
    golden_rank: row._rank,
  }))
}

function TooltipCell({ value, names, content }) {
  const [pos, setPos] = useState(null)
  const ref = useRef(null)

  const text = content ?? (names ? names.split(', ').filter(Boolean).join('\n') : null)
  if (!text) return <td className="numeric">{value}</td>

  const show = () => {
    const r = ref.current.getBoundingClientRect()
    const above = window.innerHeight - r.bottom < 160
    setPos({ right: window.innerWidth - r.right, above, y: above ? window.innerHeight - r.top : r.bottom })
  }

  return (
    <td className="numeric has-tooltip" ref={ref} onMouseEnter={show} onMouseLeave={() => setPos(null)}>
      {value}
      {pos && (
        <div className="tooltip" style={{
          position: 'fixed',
          right: pos.right,
          ...(pos.above ? { bottom: pos.y } : { top: pos.y }),
        }}>
          {text}
        </div>
      )}
    </td>
  )
}

function scoreBreakdown(row, w) {
  const other = Math.max(0,
    (row.numSpeciesTwoWeeks ?? 0)
    - (row.numHighValue ?? 0) - (row.numRaptors ?? 0) - (row.numWarblers ?? 0)
    - (row.numShorebirds ?? 0) - (row.numWaterfowl ?? 0)
  )
  const pad = (s) => s.padEnd(12)
  return [
    `${pad('Migrants:')}  ${row.numHighValue} × ${w.migrants.toFixed(1)} = ${(row.numHighValue * w.migrants).toFixed(1)}`,
    `${pad('Raptors:')}   ${row.numRaptors} × ${w.raptors.toFixed(1)} = ${(row.numRaptors * w.raptors).toFixed(1)}`,
    `${pad('Warblers:')}  ${row.numWarblers} × ${w.warblers.toFixed(1)} = ${(row.numWarblers * w.warblers).toFixed(1)}`,
    `${pad('Shorebirds:')}${row.numShorebirds} × ${w.shorebirds.toFixed(1)} = ${(row.numShorebirds * w.shorebirds).toFixed(1)}`,
    `${pad('Waterfowl:')} ${row.numWaterfowl} × ${w.waterfowl.toFixed(1)} = ${(row.numWaterfowl * w.waterfowl).toFixed(1)}`,
    `${pad('Other:')}     ${other} × ${w.other.toFixed(1)} = ${(other * w.other).toFixed(1)}`,
    `──────────────────────`,
    `${pad('Species²:')}  ${row.numSpeciesTwoWeeks}² = ${(row.numSpeciesTwoWeeks ?? 0) ** 2}`,
    `${pad('Checklists:')}${row.numChecklists} × ^0.3 = ${(Math.max(row.numChecklists ?? 1, 1) ** 0.3).toFixed(2)}`,
    `${pad('Drive:')}     ${Math.round((row.duration2 ?? 0) * 60)} min ^${w.drivePenalty.toFixed(1)} = ${(Math.max(1, (row.duration2 ?? 0) * 60) ** w.drivePenalty).toFixed(2)}`,
    `──────────────────────`,
    `${pad('Raw rank:')}  ${row.golden_rank?.toExponential(3)}`,
  ].join('\n')
}

function SortIcon({ dir }) {
  if (!dir) return <span className="sort-icon">⇅</span>
  return <span className="sort-icon">{dir === 'asc' ? '↑' : '↓'}</span>
}

function WeightsPanel({ weights, onChange }) {
  const [open, setOpen] = useState(false)

  const fields = [
    { key: 'migrants',     label: 'Migrants',      min: 0, max: 5,   step: 0.1 },
    { key: 'raptors',      label: 'Raptors',        min: 0, max: 5,   step: 0.1 },
    { key: 'warblers',     label: 'Warblers',       min: 0, max: 5,   step: 0.1 },
    { key: 'shorebirds',   label: 'Shorebirds',     min: 0, max: 5,   step: 0.1 },
    { key: 'waterfowl',    label: 'Waterfowl',      min: 0, max: 5,   step: 0.1 },
    { key: 'other',        label: 'Other',          min: 0, max: 5,   step: 0.1 },
    { key: 'drivePenalty', label: 'Drive penalty',  min: 0, max: 1,   step: 0.05 },
  ]

  const handleSlider = (key, val) => onChange({ ...weights, [key]: parseFloat(val) })
  const reset = () => onChange(DEFAULT_WEIGHTS)
  const isDefault = fields.every(f => weights[f.key] === DEFAULT_WEIGHTS[f.key])

  return (
    <div className="panel-control">
      <button className="panel-toggle" onClick={() => setOpen(o => !o)}>
        ⚖️ Weights {open ? '▲' : '▼'}
      </button>
      {open && (
        <div className="panel-dropdown">
          {fields.map(({ key, label, min, max, step }) => (
            <div key={key} className="weight-row">
              <label>{label}</label>
              <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={weights[key]}
                onChange={e => handleSlider(key, e.target.value)}
              />
              <span className="weight-val">{weights[key].toFixed(1)}</span>
            </div>
          ))}
          <button className="weights-reset" onClick={reset} disabled={isDefault}>
            Reset to defaults
          </button>
        </div>
      )}
    </div>
  )
}

function useIsMobile(breakpoint = 768) {
  const [isMobile, setIsMobile] = useState(() => window.matchMedia(`(max-width: ${breakpoint}px)`).matches)
  useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${breakpoint}px)`)
    const handler = e => setIsMobile(e.matches)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [breakpoint])
  return isMobile
}

const NAME_FIELDS = [
  { field: 'highValueNames', label: 'Migrants'   },
  { field: 'raptorNames',    label: 'Raptors'    },
  { field: 'warblerNames',   label: 'Warblers'   },
  { field: 'shorebirdNames', label: 'Shorebirds' },
  { field: 'waterfowlNames', label: 'Waterfowl'  },
]

function BirdFilter({ results, selectedBird, onChange }) {
  const [open, setOpen]     = useState(false)
  const [query, setQuery]   = useState('')
  const inputRef            = useRef(null)

  const allBirds = useMemo(() => {
    const seen = new Map()
    NAME_FIELDS.forEach(({ field, label }) => {
      results.forEach(row => {
        row[field]?.split(', ').filter(Boolean).forEach(name => {
          if (!seen.has(name)) seen.set(name, label)
        })
      })
    })
    return [...seen.entries()].map(([name, cat]) => ({ name, cat })).sort((a, b) => a.name.localeCompare(b.name))
  }, [results])

  const filtered = query.trim()
    ? allBirds.filter(b => b.name.toLowerCase().includes(query.toLowerCase()))
    : allBirds

  const select = (name) => { onChange(name); setOpen(false); setQuery('') }
  const clear  = ()     => { onChange(null); setOpen(false); setQuery('') }

  const toggle = () => {
    setOpen(o => {
      if (!o) setTimeout(() => inputRef.current?.focus(), 0)
      return !o
    })
  }

  const buttonLabel = selectedBird ? `🐦 ${selectedBird}` : '🐦 Filter'

  return (
    <div className="panel-control">
      <button className="panel-toggle" onClick={toggle}>
        {buttonLabel} {open ? '▲' : '▼'}
      </button>
      {open && (
        <div className="panel-dropdown bird-filter-dropdown">
          <input
            ref={inputRef}
            className="bird-search"
            type="text"
            placeholder="Search species…"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
          <div className="bird-list">
            {filtered.length === 0 && <div className="bird-list-empty">No matches</div>}
            {filtered.map(({ name, cat }) => (
              <div
                key={name}
                className={`bird-list-item${name === selectedBird ? ' selected' : ''}`}
                onClick={() => select(name)}
              >
                <span className="bird-list-name">{name}</span>
                <span className="bird-list-cat">{cat}</span>
              </div>
            ))}
          </div>
          {selectedBird && (
            <button type="button" className="link-btn bird-clear" onClick={clear}>
              Clear filter
            </button>
          )}
        </div>
      )}
    </div>
  )
}

const CARD_SORT_OPTIONS = [
  { key: 'score',              label: 'Score'          },
  { key: 'numSpeciesTwoWeeks', label: 'Species (2 wk)' },
  { key: 'numHighValue',       label: 'Migrants'       },
  { key: 'numWarblers',        label: 'Warblers'       },
  { key: 'numRaptors',         label: 'Raptors'        },
  { key: 'numShorebirds',      label: 'Shorebirds'     },
  { key: 'numWaterfowl',       label: 'Waterfowl'      },
  { key: 'distance_miles',     label: 'Distance'       },
  { key: 'duration2',          label: 'Drive time'     },
]

function CardTip({ label, count, names }) {
  const [pos, setPos] = useState(null)
  const ref = useRef(null)
  const text = names?.split(', ').filter(Boolean).join('\n')

  const show = () => {
    if (!text) return
    const r = ref.current.getBoundingClientRect()
    const above = window.innerHeight - r.bottom < 160
    setPos({ right: window.innerWidth - r.right, above, y: above ? window.innerHeight - r.top : r.bottom })
  }

  return (
    <div className={`card-col${text ? ' has-tooltip' : ''}`} ref={ref} onMouseEnter={show} onMouseLeave={() => setPos(null)}>
      <span className="col-label">{label}</span>
      <span className="col-value">{count ?? 0}</span>
      {pos && text && (
        <div className="tooltip" style={{ position: 'fixed', right: pos.right, ...(pos.above ? { bottom: pos.y } : { top: pos.y }) }}>
          {text}
        </div>
      )}
    </div>
  )
}

function HotspotCard({ row }) {
  return (
    <div className="hotspot-card">
      <div className="card-header">
        <a
          className="card-name"
          href={`https://www.google.com/maps?q=${row.lat},${row.lng}`}
          target="_blank" rel="noreferrer"
        >
          {row.locName}
        </a>
        <span className="card-score">{row.score}</span>
      </div>

      <div className="card-meta">
        {row.distance_miles    != null && <span>{row.distance_miles.toFixed(1)} mi</span>}
        {row.duration2         != null && <span>{row.duration2.toFixed(1)} hrs drive</span>}
        {row.numSpeciesAllTime != null && <span>{row.numSpeciesAllTime} species all time</span>}
      </div>

      <div className="card-data">
        <div className="card-col">
          <span className="col-label">Species<br/>(2 wk)</span>
          <span className="col-value">{row.numSpeciesTwoWeeks}</span>
        </div>
        <div className="card-col">
          <span className="col-label">Birds</span>
          <span className="col-value">{row.numBirdsTwoWeeks?.toLocaleString()}</span>
        </div>
        <CardTip label="Migrants"   count={row.numHighValue}  names={row.highValueNames}  />
        <CardTip label="Raptors"    count={row.numRaptors}    names={row.raptorNames}     />
        <CardTip label="Warblers"   count={row.numWarblers}   names={row.warblerNames}    />
        <CardTip label="Shorebirds" count={row.numShorebirds} names={row.shorebirdNames}  />
        <CardTip label="Waterfowl"  count={row.numWaterfowl}  names={row.waterfowlNames}  />
        <div className="card-col">
          <span className="col-label">Checklists</span>
          <span className="col-value">{row.numChecklists}</span>
        </div>
        <div className="card-col">
          <span className="col-label">Contributors</span>
          <span className="col-value">{row.numContributors}</span>
        </div>
      </div>
    </div>
  )
}

function HotspotCards({ results, weights, onWeightsChange, selectedBird, onBirdChange }) {
  const [sortKey, setSortKey] = useState('score')

  const scored = useMemo(() => applyScores(results, weights), [results, weights])

  const filtered = useMemo(() => (
    selectedBird
      ? scored.filter(row => NAME_FIELDS.some(({ field }) =>
          row[field]?.split(', ').includes(selectedBird)
        ))
      : scored
  ), [scored, selectedBird])

  const sorted = useMemo(() => (
    [...filtered].sort((a, b) => {
      const av = a[sortKey] ?? -Infinity
      const bv = b[sortKey] ?? -Infinity
      return bv - av
    })
  ), [filtered, sortKey])

  return (
    <div className="cards-container">
      <div className="cards-sort">
        <label>Sort by</label>
        <select value={sortKey} onChange={e => setSortKey(e.target.value)}>
          {CARD_SORT_OPTIONS.map(o => <option key={o.key} value={o.key}>{o.label}</option>)}
        </select>
        <BirdFilter results={results} selectedBird={selectedBird} onChange={onBirdChange} />
        <WeightsPanel weights={weights} onChange={onWeightsChange} />
      </div>
      <div className="cards-grid">
        {sorted.map((row, i) => <HotspotCard key={i} row={row} />)}
      </div>
    </div>
  )
}

function HotspotGrid({ results, weights, selectedBird }) {
  const [sort, setSort] = useState({ key: 'score', dir: 'desc' })

  const scored = useMemo(() => applyScores(results, weights), [results, weights])

  const toggleSort = (key) => {
    setSort(prev =>
      prev.key === key
        ? { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' }
        : { key, dir: 'desc' }
    )
  }

  const filtered = useMemo(() => (
    selectedBird
      ? scored.filter(row => NAME_FIELDS.some(({ field }) =>
          row[field]?.split(', ').includes(selectedBird)
        ))
      : scored
  ), [scored, selectedBird])

  const sorted = [...filtered].sort((a, b) => {
    const av = a[sort.key]
    const bv = b[sort.key]
    if (av == null) return 1
    if (bv == null) return -1
    const cmp = typeof av === 'string' ? av.localeCompare(bv) : av - bv
    return sort.dir === 'asc' ? cmp : -cmp
  })

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            {COLUMNS.map(col => (
              <th
                key={col.key}
                className={col.numeric ? 'numeric' : ''}
                onClick={() => toggleSort(col.key)}
              >
                <span className="col-line1">
                  {col.line1}
                  {!col.line2 && <SortIcon dir={sort.key === col.key ? sort.dir : null} />}
                </span>
                {col.line2 && (
                  <span className="col-line2">
                    {col.line2}
                    <SortIcon dir={sort.key === col.key ? sort.dir : null} />
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, i) => (
            <tr key={i}>
              <td><a href={`https://www.google.com/maps?q=${row.lat},${row.lng}`} target="_blank" rel="noreferrer">{row.locName}</a></td>
              <TooltipCell value={row.score} content={scoreBreakdown(row, weights)} />
              <td className="numeric">{row.numSpeciesTwoWeeks}</td>
              <td className="numeric">{row.numBirdsTwoWeeks?.toLocaleString()}</td>
              <TooltipCell value={row.numHighValue}   names={row.highValueNames} />
              <TooltipCell value={row.numRaptors}    names={row.raptorNames} />
              <TooltipCell value={row.numWarblers}   names={row.warblerNames} />
              <TooltipCell value={row.numShorebirds} names={row.shorebirdNames} />
              <TooltipCell value={row.numWaterfowl}  names={row.waterfowlNames} />
              <td className="numeric">{row.numChecklists}</td>
              <td className="numeric">{row.numContributors}</td>
              <td className="numeric">{row.numSpeciesAllTime}</td>
              <td className="numeric">{row.distance_miles?.toFixed(1)}</td>
              <td className="numeric">{row.duration2?.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function ProgressBar({ progress, onStop }) {
  const isIndeterminate = !progress || progress.total === 0
  const pct = isIndeterminate ? 0 : Math.round((progress.current / progress.total) * 100)

  return (
    <div className="progress-container">
      <div className="progress-row">
        <div className="progress-track">
          <div
            className={`progress-fill${isIndeterminate ? ' indeterminate' : ''}`}
            style={isIndeterminate ? {} : { width: `${pct}%` }}
          />
        </div>
        <button className="stop-btn" onClick={onStop} title="Stop">&#9632;</button>
      </div>
      <p className="progress-label">
        {isIndeterminate ? 'Fetching eBird data…' : `${progress.message} (${pct}%)`}
      </p>
    </div>
  )
}

const SIMPLE_RE = /^\d{5}$|^[A-Za-z]{3}$/

export default function App() {
  const [input, setInput]       = useState('')
  const [maxNum, setMaxNum]     = useState(20)
  const [loading, setLoading]   = useState(false)
  const [progress, setProgress] = useState(null)
  const [error, setError]       = useState(null)
  const [data, setData]         = useState(null)
  const [weights, setWeights]       = useState(DEFAULT_WEIGHTS)
  const [advanced, setAdvanced]     = useState(false)
  const [formatError, setFormatError] = useState(null)
  const [selectedBird, setSelectedBird] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const esRef = useRef(null)
  const suggestTimer = useRef(null)

  const fetchSuggestions = useCallback((val) => {
    clearTimeout(suggestTimer.current)
    const trimmed = val.trim()
    if (trimmed.length < 2 || /^\d+$/.test(trimmed)) { setSuggestions([]); return }
    suggestTimer.current = setTimeout(async () => {
      try {
        const res = await fetch(`/api/airports?q=${encodeURIComponent(trimmed)}`)
        if (res.ok) setSuggestions(await res.json())
      } catch { /* network offline */ }
    }, 280)
  }, [])

  const pickSuggestion = useCallback((code) => {
    setInput(code)
    setSuggestions([])
    setFormatError(null)
  }, [])

  const toggleAdvanced = useCallback(() => {
    setAdvanced(a => !a)
    setFormatError(null)
    setInput('')
    setSuggestions([])
  }, [])

  const search = useCallback((e) => {
    e.preventDefault()
    if (!input.trim()) return

    if (!advanced && !SIMPLE_RE.test(input.trim())) {
      setFormatError('Enter a 5-digit ZIP code or 3-letter airport code (e.g. 07030 or EWR)')
      return
    }
    setFormatError(null)

    if (maxNum > 50) {
      const ok = window.confirm(`Are you sure you want to search for ${maxNum} hotspots? This will take some time to fetch.`)
      if (!ok) return
    }

    if (esRef.current) esRef.current.close()
    setSuggestions([])

    setLoading(true)
    setProgress(null)
    setError(null)
    setData(null)
    setSelectedBird(null)

    const url = `/api/goldens/stream?location=${encodeURIComponent(input.trim())}&max_num=${maxNum}`
    const es = new EventSource(url)
    esRef.current = es

    es.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      if (msg.error) {
        es.close()
        setError(msg.error)
        setLoading(false)
        setProgress(null)
      } else if (msg.done) {
        es.close()
        setData(msg)
        setLoading(false)
        setProgress(null)
      } else if (msg.preliminary) {
        setData(msg)
        setProgress({ current: 0, total: 0, message: 'Refining with drive times…' })
      } else {
        setProgress(msg)
      }
    }

    es.onerror = () => {
      es.close()
      setError('Connection error — is the backend running?')
      setLoading(false)
      setProgress(null)
    }
  }, [input, maxNum])

  const stop = useCallback(() => {
    if (esRef.current) { esRef.current.close(); esRef.current = null }
    setLoading(false)
    setProgress(null)
  }, [])

  return (
    <div className="app">
      <header>
        <h1>🐦 Top Birding Spots</h1>
        <p className="subtitle">Find the best eBird hotspots near any location</p>
      </header>

      <form className="search-form" onSubmit={search}>
        <div className="input-wrap">
          <input
            type="text"
            placeholder={advanced ? 'Enter any address or city, e.g. Hoboken NJ' : 'ZIP or airport code, e.g. 07030 or EWR'}
            value={input}
            onChange={e => { setInput(e.target.value); setFormatError(null); fetchSuggestions(e.target.value) }}
            onBlur={() => setTimeout(() => setSuggestions([]), 150)}
            disabled={loading}
          />
          {suggestions.length > 0 && (
            <div className="suggestions">
              {suggestions.map(s => (
                <div key={s.code} className="suggestion-item" onMouseDown={() => pickSuggestion(s.code)}>
                  <span className="suggestion-code">{s.code}</span>
                  <span className="suggestion-name">{s.name}</span>
                  <span className="suggestion-city">{s.city}{s.subd ? `, ${s.subd}` : ''}{s.country !== 'US' ? ` (${s.country})` : ''}</span>
                </div>
              ))}
            </div>
          )}
        </div>
        <select
          value={maxNum}
          onChange={e => setMaxNum(Number(e.target.value))}
          disabled={loading}
          title="Number of spots to check"
          className="maxnum-select"
        >
          {Array.from({ length: 20 }, (_, i) => (i + 1) * 10).map(n => (
            <option key={n} value={n}>{n} spots</option>
          ))}
        </select>
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? 'Searching…' : 'Search'}
        </button>
      </form>
      {formatError && <p className="format-error">{formatError}</p>}
      <p className="advanced-toggle">
        <button type="button" className="link-btn" onClick={toggleAdvanced} disabled={loading}>
          {advanced ? '← Simple (ZIP / airport)' : 'Advanced: enter any address'}
        </button>
      </p>

      {loading && <ProgressBar progress={progress} onStop={stop} />}
      {error   && <div className="status error">{error}</div>}

      {data && (
        <>
          <p className="result-meta">
            {data.results.length} hotspots near <strong>{data.location}</strong>
            {' '}({data.lat.toFixed(4)}, {data.lon.toFixed(4)})
          </p>
          <HotspotCards
            results={data.results}
            weights={weights}
            onWeightsChange={setWeights}
            selectedBird={selectedBird}
            onBirdChange={setSelectedBird}
          />
        </>
      )}
    </div>
  )
}
