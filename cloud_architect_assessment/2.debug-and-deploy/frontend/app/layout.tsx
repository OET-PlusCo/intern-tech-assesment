import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Assessment Webapp',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'system-ui, sans-serif', maxWidth: '40rem', margin: '2rem auto', padding: '0 1rem' }}>
        {children}
      </body>
    </html>
  );
}
