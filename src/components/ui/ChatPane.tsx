import { useEffect, useRef } from 'react'
import type { FormEvent } from 'react'
import type { UseSceneManifestReturn } from '../../hooks/useSceneManifest'
import { Button } from './Button'
import { Card } from './Card'

type ChatPaneProps = {
  manifest: UseSceneManifestReturn
}

export function ChatPane({ manifest }: ChatPaneProps) {
  const messagesRef = useRef<HTMLDivElement | null>(null)
  const { scene, status, reload, error } = manifest

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight
    }
  }, [])

  return (
    <div className="h-full flex flex-col">
      <div className="p-3 border-b flex items-center justify-between gap-2">
        <div>
          <h3 className="text-lg font-semibold">Chat</h3>
          <p className="text-xs text-slate-500">Scene status: {status}</p>
        </div>
        <Button type="button" variant="outline" onClick={reload} className="h-8 px-3">
          Refresh
        </Button>
      </div>

      <div ref={messagesRef} className="flex-1 overflow-y-auto p-3 space-y-3 bg-slate-50">
        <Card>
          <p className="text-sm text-slate-700">
            <strong>Prompt:</strong> {scene?.prompt ?? 'Waiting for agent run to provide a prompt.'}
          </p>
        </Card>

        <Card className="bg-sky-600 text-white">
          Latest scene ID:{' '}
          <span className="font-semibold">{scene?.scene_id ?? 'not yet available'}</span>
        </Card>

        <Card>
          <p className="text-sm text-slate-700">
            {status === 'empty'
              ? 'No scene manifests yet. Run the agent loop to produce a scene and refresh.'
              : 'Updates arrive once the backend finishes materializing a scene. Use refresh if you run a new agent loop.'}
          </p>
          {status === 'error' && error && <p className="mt-2 text-xs text-red-600">Error: {error}</p>}
        </Card>
      </div>

      <div className="p-3 border-t">
        <form className="flex gap-2" onSubmit={(event: FormEvent<HTMLFormElement>) => event.preventDefault()}>
          <input
            aria-label="Message"
            className="flex-1 rounded-md border px-3 py-2"
            placeholder="Type a message..."
          />
          <Button type="submit">Send</Button>
        </form>
      </div>
    </div>
  )
}

export default ChatPane
