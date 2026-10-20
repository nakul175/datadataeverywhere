import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'DataDataEverywhere', description: 'Data, data everywhere. Finally, in one place.', icons: { icon: '/holy-sheet.png', apple: '/holy-sheet.png' } };
export default function Layout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><head><link rel="stylesheet" href="/fonts/public-sans.css" /></head><body>{children}</body></html>;
}
