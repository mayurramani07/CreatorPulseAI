const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";


async function fetchJson(
  url,
  errorMessage
) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(
      `${errorMessage} (${response.status})`
    );
  }

  return response.json();
}


export async function analyzeVideo(
  videoId
) {
  const [
    videoResponse,
    analysisResponse,
  ] = await Promise.all([
    fetchJson(
      `${API_BASE_URL}/videos/${videoId}`,
      "Unable to fetch video information"
    ),

    fetchJson(
      `${API_BASE_URL}/videos/${videoId}/sample-comments`,
      "Unable to analyze audience"
    ),
  ]);

  const videoItem =
    videoResponse?.items?.[0];

  if (!videoItem) {
    throw new Error(
      "YouTube video could not be found."
    );
  }

  const snippet =
    videoItem.snippet ?? {};

  const statistics =
    videoItem.statistics ?? {};

  return {
    ...analysisResponse,

    video: {
      id:
        videoItem.id ??
        videoId,

      title:
        snippet.title ??
        "YouTube Video",

      channel_name:
        snippet.channelTitle ??
        "",

      thumbnail_url:
        snippet.thumbnails?.high?.url ??
        snippet.thumbnails?.medium?.url ??
        snippet.thumbnails?.default?.url ??
        "",

      view_count: Number(
        statistics.viewCount ?? 0
      ),

      like_count: Number(
        statistics.likeCount ?? 0
      ),

      total_comments: Number(
        statistics.commentCount ?? 0
      ),
    },
  };
}


export async function reanalyzeVideo(
  videoId
) {
  const response = await fetch(
    `${API_BASE_URL}/videos/${videoId}/reanalyze`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error(
      `Unable to re-analyze video (${response.status})`
    );
  }

  return response.json();
}