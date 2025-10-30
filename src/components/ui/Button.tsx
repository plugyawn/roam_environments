import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type ButtonProps = PropsWithChildren<
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: 'default' | 'ghost' | 'outline'
  }
>

export function Button({ variant = 'default', className = '', children, ...props }: ButtonProps) {
  const base =
    'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none'
  const variants: Record<string, string> = {
    default: 'bg-sky-600 text-white hover:bg-sky-700 focus-visible:ring-sky-500',
    ghost: 'bg-transparent text-slate-900 hover:bg-slate-100 focus-visible:ring-slate-300',
    outline: 'border border-slate-200 text-slate-900 hover:bg-slate-50 focus-visible:ring-slate-300'
  }

  const cls = `${base} ${variants[variant]} ${className}`.trim()

  return (
    <button className={cls} {...props}>
      {children}
    </button>
  )
}

export default Button
