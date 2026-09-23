import { Storage } from '@google-cloud/storage';
import { NextResponse } from 'next/server';

const assetsBucket = process.env.ASSETS_BUCKET || '';

function extensionFromType(type: string): string {
  if (type === 'image/jpeg') return 'jpg';
  if (type === 'image/webp') return 'webp';
  if (type === 'image/gif') return 'gif';
  return 'png';
}

export async function POST(request: Request) {
  if (!assetsBucket) {
    return NextResponse.json({ error: 'ASSETS_BUCKET not configured' }, { status: 500 });
  }

  let formData: FormData;
  try {
    formData = await request.formData();
  } catch {
    return NextResponse.json({ error: 'Invalid form data' }, { status: 400 });
  }

  const entry = formData.get('image');
  if (!entry || typeof entry === 'string') {
    return NextResponse.json({ error: 'No image file provided' }, { status: 400 });
  }

  const uploadFile = entry as File;
  if (!uploadFile.type.startsWith('image/')) {
    return NextResponse.json({ error: 'File must be an image' }, { status: 400 });
  }

  try {
    const buffer = Buffer.from(await uploadFile.arrayBuffer());
    const ext = extensionFromType(uploadFile.type);
    const objectName = `uploads/${Date.now()}-${uploadFile.name.replace(/[^a-zA-Z0-9._-]/g, '_') || `upload.${ext}`}`;

    const storage = new Storage();
    const gcsFile = storage.bucket(assetsBucket).file(objectName);

    await gcsFile.save(buffer, {
      contentType: uploadFile.type,
      metadata: { cacheControl: 'private, max-age=3600' },
    });

    const imageUrl = `https://storage.googleapis.com/${assetsBucket}/${objectName}`;

    return NextResponse.json({ objectName, imageUrl });
  } catch (err) {
    console.error('upload failed', err);
    const message = err instanceof Error ? err.message : 'upload failed';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
