import type { PropsWithChildren } from 'react'

export function Card({ children, className = '' }: PropsWithChildren<{ className?: string }>) {
  return <div className={`bg-white dark:bg-slate-800 shadow-sm rounded-lg p-3 ${className}`}>{children}</div>
}

export default Card
