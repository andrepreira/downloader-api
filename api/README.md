# FastAPI YouTube Downloader

This is a FastAPI application that allows you to download YouTube videos and retrieve video information.

## Endpoints

### 1. Download Video

**URL:** `/download/{resolution}`

**Method:** `POST`

**Request Body:**
```json
{
  "url": "string"
}
