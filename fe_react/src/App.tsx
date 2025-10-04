import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// API base URL - using Kubernetes service name for inter-service communication
// const API_BASE_URL = 'http://backend-dev:8000'

interface Item {
  id: number
  name: string
  description: string
  price: number
  is_available: boolean
}

function App() {
  const [count, setCount] = useState(0)
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(false)

  // Fetch items from FastAPI backend
  const fetchItems = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/items`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      console.log('Fetched items from API:', data)
      setItems(data)
    } catch (error) {
      console.error('Error fetching items:', error)
    } finally {
      setLoading(false)
    }
  }

  // Fetch health status
  const fetchHealth = async () => {
    try {
      const response = await fetch(`/api/health`)
      const data = await response.json()
      console.log('API Health Status:', data)
    } catch (error) {
      console.error('Error fetching health status:', error)
    }
  }

  // Create a new item
  const createItem = async () => {
    const newItem = {
      name: `Item ${Date.now()}`,
      description: 'Created from React frontend',
      price: Math.random() * 100,
      is_available: true
    }

    try {
      const response = await fetch(`/api/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newItem)
      })
      const data = await response.json()
      console.log('Created new item:', data)
      // Refresh the items list
      fetchItems()
    } catch (error) {
      console.error('Error creating item:', error)
    }
  }

  // Fetch data on component mount
  useEffect(() => {
    fetchHealth()
    fetchItems()
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React + FastAPI</h1>
      
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        
        <div style={{ marginTop: '20px' }}>
          <h3>FastAPI Integration</h3>
          <button onClick={fetchItems} disabled={loading}>
            {loading ? 'Loading...' : 'Fetch Items'}
          </button>
          <button onClick={createItem} style={{ marginLeft: '10px' }}>
            Create Random Item
          </button>
          <button onClick={fetchHealth} style={{ marginLeft: '10px' }}>
            Check API Health
          </button>
        </div>

        <div style={{ marginTop: '20px' }}>
          <h4>Items from API:</h4>
          {items.length === 0 ? (
            <p>No items found. Click "Fetch Items" or "Create Random Item"</p>
          ) : (
            <ul>
              {items.map((item) => (
                <li key={item.id}>
                  <strong>{item.name}</strong> - ${item.price} 
                  {item.description && ` (${item.description})`}
                  {item.is_available ? ' ✅' : ' ❌'}
                </li>
              ))}
            </ul>
          )}
        </div>
        
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      
      <p className="read-the-docs">
        Check the browser console to see API responses logged!
      </p>
    </>
  )
}

export default App
