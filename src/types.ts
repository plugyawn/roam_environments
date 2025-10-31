export type Vector3Tuple = [number, number, number]

export type ScenePlacement = {
  ref: string
  transform: {
    pos: Vector3Tuple
    rotY?: number
    scale?: number
  }
}

export type AssetManifest = {
  id: string
  glb_path?: string
  bbox?: number[]
  tags?: string[]
  recipe?: unknown
}

export type SceneGraph = {
  assets: string[]
  placements: ScenePlacement[]
  map?: unknown
  metadata?: Record<string, unknown>
}

export type ValidationIssue = {
  severity: 'info' | 'warn' | 'error'
  message: string
  context?: Record<string, unknown>
}

export type ValidationReport = {
  status: 'pass' | 'fail'
  issues: ValidationIssue[]
  metrics?: Record<string, unknown>
}

export type Requirement = {
  concept: string
  min_count?: number
  max_count?: number
  exactly?: number
  [key: string]: unknown
}

export type RequirementsLedger = {
  requirements: Requirement[]
}

export type SceneManifest = {
  run_id?: string
  prompt?: string
  manifest_path?: string
  snapshot_path?: string
  assets?: AssetManifest[]
  map_plan?: unknown
  scene_graph: SceneGraph
  requirements?: RequirementsLedger
  scene_spec?: Record<string, unknown>
  validation?: ValidationReport
  metadata?: Record<string, unknown>
}
