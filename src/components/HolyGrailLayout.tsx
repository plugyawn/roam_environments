import { useSceneManifest } from '../hooks/useSceneManifest'
import { ChatPane } from './ui/ChatPane'
import { Canvas3D } from './ui/Canvas3D'
import { Gallery } from './ui/Gallery'

function HolyGrailLayout() {
  const manifest = useSceneManifest()

  return (
    <div className="min-h-screen grid grid-cols-[320px_1fr_320px] bg-white">
      <aside className="border-r bg-white">
        <div className="h-screen">
          <ChatPane manifest={manifest} />
        </div>
      </aside>

      <main className="bg-slate-50">
        <div className="h-screen p-4">
          <div className="h-full rounded-lg overflow-hidden shadow-sm">
            <Canvas3D manifest={manifest} />
          </div>
        </div>
      </main>

      <aside className="border-l bg-white">
        <div className="h-screen">
          <Gallery manifest={manifest} />
        </div>
      </aside>
    </div>
  )
}

export default HolyGrailLayout
