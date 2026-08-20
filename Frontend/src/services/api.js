const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeVideo(videoId) {
  const response = await fetch(
    `${API_BASE_URL}/videos/${videoId}/sample-comments`
  );

  if (!response.ok) {
    throw new Error(
      `Analysis failed with status ${response.status}`
    );
  }

  return response.json();
}