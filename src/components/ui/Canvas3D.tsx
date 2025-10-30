import { useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import type { UseSceneManifestReturn } from '../../hooks/useSceneManifest'
import type { ScenePlacement } from '../../types'

type Canvas3DProps = {
  className?: string
  manifest: UseSceneManifestReturn
}

export function Canvas3D({ className = '', manifest }: Canvas3DProps) {
  const mountRef = useRef<HTMLDivElement | null>(null)
  const sceneRef = useRef<THREE.Scene | null>(null)
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null)
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null)
  const frameRef = useRef<number>(0)
  const placementsGroupRef = useRef<THREE.Group | null>(null)

  useEffect(() => {
    const mount = mountRef.current
    if (!mount) return

    const width = mount.clientWidth || 640
    const height = mount.clientHeight || 480

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf8fafc)
    sceneRef.current = scene

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
    camera.position.set(6, 5, 6)
    cameraRef.current = camera

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(width, height)
    mount.appendChild(renderer.domElement)
    rendererRef.current = renderer

    const grid = new THREE.GridHelper(40, 40, 0x0ea5e9, 0x0ea5e9)
    if (Array.isArray(grid.material)) {
      grid.material.forEach((material) => {
        material.opacity = 0.15
        material.transparent = true
      })
    } else {
      grid.material.opacity = 0.15
      grid.material.transparent = true
    }
    scene.add(grid)

    const axes = new THREE.AxesHelper(4)
    scene.add(axes)

    const placementsGroup = new THREE.Group()
    placementsGroup.name = 'placements'
    placementsGroupRef.current = placementsGroup
    scene.add(placementsGroup)

    const light = new THREE.DirectionalLight(0xffffff, 1)
    light.position.set(5, 10, 7)
    scene.add(light)
    scene.add(new THREE.AmbientLight(0xffffff, 0.4))

    const animate = () => {
      renderer.render(scene, camera)
      frameRef.current = requestAnimationFrame(animate)
    }
    animate()

    const handleResize = () => {
      const w = mount.clientWidth || width
      const h = mount.clientHeight || height
      camera.aspect = w / h
      camera.updateProjectionMatrix()
      renderer.setSize(w, h)
    }

    const observer = new ResizeObserver(handleResize)
    observer.observe(mount)

    return () => {
      cancelAnimationFrame(frameRef.current)
      observer.disconnect()
      renderer.dispose()
      scene.clear()
      if (mount.contains(renderer.domElement)) {
        mount.removeChild(renderer.domElement)
      }
      placementsGroupRef.current = null
      rendererRef.current = null
      cameraRef.current = null
      sceneRef.current = null
    }
  }, [])

  useEffect(() => {
    const group = placementsGroupRef.current
    const threeScene = sceneRef.current
    const camera = cameraRef.current
    if (!group || !threeScene || !camera) {
      return
    }

    const disposeChild = (child: THREE.Object3D) => {
      const mesh = child as THREE.Mesh
      if (mesh.geometry) {
        mesh.geometry.dispose()
      }
      const material = mesh.material
      if (Array.isArray(material)) {
        material.forEach((mat) => mat?.dispose())
      } else {
        material?.dispose()
      }
    }

    while (group.children.length) {
      const child = group.children[group.children.length - 1]
      group.remove(child)
      disposeChild(child)
    }

    const placements = manifest.scene?.scene_graph?.placements ?? []

    if (placements.length === 0) {
      return
    }

    const palette = [0x0ea5e9, 0x1d4ed8, 0x22c55e, 0xf97316, 0x6366f1]
    const box = new THREE.Box3()
    placements.forEach((placement: ScenePlacement, index: number) => {
      const [x, y, z] = placement.transform.pos
      const scale = placement.transform.scale ?? 1
      const height = Math.max(0.5, scale)
      const geometry = new THREE.BoxGeometry(scale, height, scale)
      const color = palette[index % palette.length]
      const material = new THREE.MeshStandardMaterial({ color, opacity: 0.8, transparent: true })
      const mesh = new THREE.Mesh(geometry, material)
      mesh.position.set(x, y + height / 2, z)
      if (placement.transform.rotY) {
        mesh.rotation.y = placement.transform.rotY
      }
      mesh.userData.assetRef = placement.ref
      group.add(mesh)
      box.expandByObject(mesh)
    })

    if (!box.isEmpty()) {
      const sphere = new THREE.Sphere()
      box.getBoundingSphere(sphere)
      const padding = 3
      const radius = sphere.radius + padding
      const fovRadians = (camera.fov * Math.PI) / 180
      const distance = radius / Math.sin(fovRadians / 2)
      camera.position.set(sphere.center.x + distance * 0.45, sphere.center.y + distance * 0.35, sphere.center.z + distance)
      camera.lookAt(sphere.center)
    }
  }, [manifest.scene])

  const overlayMessage = useMemo(() => {
    if (manifest.status === 'loading') return 'Loading latest scene...'
    if (manifest.status === 'error') {
      return manifest.error ? `Unable to load scene: ${manifest.error}` : 'Unable to load scene. Try refreshing.'
    }
    if (manifest.status === 'empty') return 'No scene manifests yet. Run the agent loop and refresh.'
    if (!manifest.scene) return 'Run the agent loop to generate a scene.'
    const placements = manifest.scene.scene_graph?.placements ?? []
    if (placements.length === 0) {
      return 'Scene loaded without placements yet. Run a new agent loop to generate geometry.'
    }
    return null
  }, [manifest.error, manifest.scene, manifest.status])

  return (
    <div ref={mountRef} className={`relative w-full h-full ${className}`}>
      {overlayMessage && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-slate-900/40 text-white text-sm font-medium">
          {overlayMessage}
        </div>
      )}
    </div>
  )
}

export default Canvas3D
