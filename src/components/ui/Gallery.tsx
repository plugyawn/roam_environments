import type { UseSceneManifestReturn } from '../../hooks/useSceneManifest'
import { Card } from './Card'
import { Button } from './Button'

type GalleryProps = {
  manifest: UseSceneManifestReturn
}

export function Gallery({ manifest }: GalleryProps) {
  const { scene, status, reload, error } = manifest

  return (
    <div className="flex flex-col h-full">
      <div className="p-3 border-b flex items-center justify-between gap-2">
        <div>
          <h3 className="text-lg font-semibold">Gallery</h3>
          <p className="text-xs text-slate-500">Visual outputs from the latest run</p>
        </div>
        <Button type="button" variant="outline" onClick={reload} className="h-8 px-3">
          Refresh
        </Button>
      </div>
      <div className="p-3 flex-1 overflow-y-auto space-y-3">
        {status === 'loading' && <Card className="text-sm text-slate-600">Loading gallery assets...</Card>}

        {status === 'error' && (
          <Card className="text-sm text-red-600">
            Failed to load manifest{error ? `: ${error}` : ''}. Please try refreshing.
          </Card>
        )}

        {!scene && status !== 'loading' && status !== 'error' && (
          <Card className="text-sm text-slate-600">Run the agent loop to populate gallery content.</Card>
        )}

        {scene && (
          <>
            <Card className="h-56 flex items-center justify-center overflow-hidden">
              {scene.snapshotUrl ? (
                <img src={scene.snapshotUrl} alt={scene.run_id ?? 'latest-run'} className="max-h-full w-full object-contain" />
              ) : (
                <p className="text-sm text-slate-600">Snapshot not available for this scene.</p>
              )}
            </Card>

            <Card>
              <h4 className="text-sm font-semibold text-slate-700">Assets ({scene.assets?.length ?? 0})</h4>
              <ul className="mt-2 space-y-2 text-sm text-slate-600">
                {(scene.assets ?? []).map((asset) => (
                  <li key={asset.id} className="flex items-center justify-between gap-4">
                    <span className="truncate font-medium text-slate-700">{asset.id}</span>
                    {asset.glb_path ? (
                      <a
                        className="text-sky-600 hover:text-sky-700"
                        href={`/api/assets/${asset.id}.glb`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Download GLB
                      </a>
                    ) : (
                      <span className="text-xs text-slate-400">GLB pending</span>
                    )}
                  </li>
                ))}
                {(!scene.assets || scene.assets.length === 0) && <li className="text-xs text-slate-500">Asset manifest empty.</li>}
              </ul>
            </Card>
          </>
        )}
      </div>
    </div>
  )
}

export default Gallery
