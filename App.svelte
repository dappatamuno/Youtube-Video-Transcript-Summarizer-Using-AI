<script>
  let videoUrl = '';
  let videoId = '';
  let question = '';
  let summary = '';
  let answer = '';
  let chatHistory = [];
  let loading = false;
  let error = '';

  async function transcribe() {
    loading = true;
    error = '';
    try {
      const res = await fetch("http://localhost:8000/transcribe/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ youtube_url: videoUrl })
      });
      if (!res.ok) throw new Error((await res.json()).detail);
      const data = await res.json();
      videoId = data.video_id;
      summary = data.summary;
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  async function ask() {
    loading = true;
    error = '';
    try {
      const res = await fetch("http://localhost:8000/ask/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_id: videoId, question })
      });
      if (!res.ok) throw new Error((await res.json()).detail);
      const data = await res.json();
      answer = data.answer;
      chatHistory = [...chatHistory, { q: question, a: answer }];
      question = '';
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<main class="p-6 max-w-xl mx-auto font-sans">
  <h1 class="text-2xl font-bold mb-4">🎥 YouTube Q&A</h1>

  <input bind:value={videoUrl} placeholder="Paste YouTube URL" class="input" />
  <button on:click={transcribe} class="btn mt-2">Transcribe & Summarize</button>

  {#if loading}
    <p class="text-blue-500 mt-2">⏳ Loading...</p>
  {/if}

  {#if error}
    <div class="text-red-500 mt-2">{error}</div>
  {/if}

  {#if summary}
    <div class="mt-4 p-2 bg-gray-100 rounded">{summary}</div>

    <div class="mt-4">
      <input bind:value={question} placeholder="Ask a question..." class="input" />
      <button on:click={ask} class="btn mt-2">Ask</button>
    </div>

    <div class="mt-6">
      {#each chatHistory as chat}
        <div class="mb-3">
          <p><strong>Q:</strong> {chat.q}</p>
          <p><strong>A:</strong> {chat.a}</p>
        </div>
      {/each}
    </div>
  {/if}
</main>

<style>
  .input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
  }
  .btn {
    background-color: #2563eb;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    cursor: pointer;
  }
</style>