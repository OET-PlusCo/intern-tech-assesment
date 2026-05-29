'use client';

import { useRef, useState } from 'react';

const greeting = process.env.NEXT_PUBLIC_APP_GREETING ?? '';

export default function HomePage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState('');
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [selectedName, setSelectedName] = useState<string | null>(null);

  async function uploadFile(file: File) {
    setStatus('Uploading…');
    setImageUrl(null);

    const body = new FormData();
    body.append('image', file);

    try {
      const res = await fetch('/api/upload', { method: 'POST', body });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || res.statusText);
      setStatus('Upload OK.');
      if (data.imageUrl) setImageUrl(data.imageUrl);
    } catch (e) {
      setStatus(`Error: ${e instanceof Error ? e.message : 'upload failed'}`);
    }
  }

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedName(file.name);
      void uploadFile(file);
    }
  }

  function onUploadClick() {
    fileInputRef.current?.click();
  }

  return (
    <>
      <h1>Hello World</h1>
      <p>
        Greeting:{' '}
        <strong style={{ background: '#e8f0fe', color: '#1967d2', padding: '0.25rem 0.5rem', borderRadius: 4 }}>
          {greeting}
        </strong>
      </p>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={onFileChange}
        style={{ display: 'none' }}
        aria-hidden
      />
      <button type="button" onClick={onUploadClick} style={{ marginTop: '1rem', padding: '0.5rem 1rem', cursor: 'pointer' }}>
        Upload image to Cloud Storage
      </button>
      {selectedName && (
        <p style={{ marginTop: '0.5rem', color: '#5f6368', fontSize: '0.9rem' }}>Selected: {selectedName}</p>
      )}
      {status && <p style={{ marginTop: '1rem', color: '#5f6368' }}>{status}</p>}
      {imageUrl && (
        <section style={{ marginTop: '1.5rem' }} aria-label="Uploaded image">
          <img
            src={imageUrl}
            alt="Uploaded from Cloud Storage"
            style={{ maxWidth: '100%', display: 'block', border: '1px solid #dadce0', borderRadius: 4 }}
          />
        </section>
      )}
    </>
  );
}
