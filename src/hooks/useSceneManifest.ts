import { useCallback, useEffect, useMemo, useState } from 'react'
import type { SceneManifest } from '../types'

type HookState = 'idle' | 'loading' | 'ready' | 'error' | 'empty'

type ScenePayload = SceneManifest & {
  snapshotUrl?: string
}

export function useSceneManifest() {
  const [state, setState] = useState<HookState>('idle')
  const [data, setData] = useState<SceneManifest | null>(null)
  const [requestId, setRequestId] = useState(0)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    const fetchManifest = async () => {
      setState('loading')
      setErrorMessage(null)
      try {
        const response = await fetch('/api/runs/latest')
        if (response.status === 404 || response.status === 204) {
          if (!cancelled) {
            setData(null)
            setState('empty')
          }
          return
        }
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`)
        }
        const json = (await response.json()) as SceneManifest
        if (!cancelled) {
          setData(json)
          setState('ready')
        }
      } catch (error) {
        if (!cancelled) {
          console.warn('Failed to load scene manifest', error)
          setState('error')
          setErrorMessage(error instanceof Error ? error.message : 'Unknown error')
        }
      }
    }

    fetchManifest()

    return () => {
      cancelled = true
    }
  }, [requestId])

  const payload = useMemo<ScenePayload | null>(() => {
    if (!data) return null
    const runId = data.run_id ?? (typeof data.metadata?.run_id === 'string' ? data.metadata.run_id : undefined)
    const snapshotUrl = runId ? `/api/snapshots/${runId}` : undefined
    return { ...data, run_id: runId, snapshotUrl }
  }, [data])

  const reload = useCallback(() => {
    setRequestId((id) => id + 1)
  }, [])

  return {
    scene: payload,
    status: state,
    reload,
    error: errorMessage,
  }
}

export type UseSceneManifestReturn = ReturnType<typeof useSceneManifest>
