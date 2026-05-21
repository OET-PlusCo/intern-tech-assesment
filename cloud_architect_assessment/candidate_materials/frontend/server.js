const express = require('express');
const path = require('path');
const { Storage } = require('@google-cloud/storage');

const app = express();
const port = process.env.PORT || 8080;

const assetsBucket = process.env.ASSETS_BUCKET || '';

app.use(express.static(path.join(__dirname, 'public')));

app.get('/health', (_req, res) => res.json({ ok: true }));

app.post('/api/upload', async (_req, res) => {
  if (!assetsBucket) {
    return res.status(500).json({ error: 'ASSETS_BUCKET not configured' });
  }

  try {
    const storage = new Storage();
    const bucket = storage.bucket(assetsBucket);
    const objectName = `uploads/demo-${Date.now()}.txt`;
    const file = bucket.file(objectName);

    const pngBase64 =
      'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
    const buffer = Buffer.from(pngBase64, 'base64');

    await file.save(buffer, {
      contentType: 'image/png',
      metadata: { cacheControl: 'public, max-age=3600' },
    });

    // Private bucket: object is not world-readable. Candidate should add signed URL logic.
    const imageUrl = `https://storage.googleapis.com/${assetsBucket}/${objectName}`;

    return res.json({ objectName, imageUrl });
  } catch (err) {
    console.error('upload failed', err);
    return res.status(500).json({
      error: err.message || 'upload failed — check runtime service account IAM on the bucket',
    });
  }
});

app.listen(port, () => {
  console.log(`Listening on ${port}, bucket=${assetsBucket || '(none)'}`);
});
