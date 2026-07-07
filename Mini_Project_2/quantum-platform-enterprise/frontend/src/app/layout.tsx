import '@/styles/globals.css'

export const metadata = {
  title: 'Quantum Platform Enterprise',
  description: 'Enterprise Quantum Communication Dashboard',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
