export function Brand({ compact = false }: { compact?: boolean }) {
  return <a className={`brand ${compact ? 'compact' : ''}`} href="/" aria-label="DataDataEverywhere home"><span className="brand-mascot"><img src="/holy-sheet.png" alt="Holy Sheet! spreadsheet ghost with a golden halo" /></span><span className="wordmark">DataData<span>Everywhere</span><small>by aplyd</small></span></a>;
}
export function Mascot({ className = '' }: { className?: string }) { return <div className={`mascot ${className}`}><img src="/holy-sheet.png" alt="Holy Sheet! Our happy spreadsheet ghost" /></div>; }
