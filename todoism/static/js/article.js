// static/js/article.js
(function () {
  const { createApp, ref } = Vue

  const server = window.__ARTICLE_DATA__ || { id: 0, likes: 0, comments: [] }
  const ARTICLE_ID = server.id
  const INITIAL_LIKES = server.likes
  const INITIAL_COMMENTS = server.comments

  createApp({
    setup() {
      const likes = ref(INITIAL_LIKES)
      const likeSubmitting = ref(false)

      const comments = ref(INITIAL_COMMENTS)
      const loadingComments = ref(false)

      const form = ref({ author: "", content: "" })
      const submitting = ref(false)
      const submitError = ref("")

      const base = `/api/articles/${ARTICLE_ID}`
      const headers = { "Content-Type": "application/json" }

      const onLike = async () => {
        if (likeSubmitting.value) return
        likeSubmitting.value = true
        const prev = likes.value
        likes.value = prev + 1
        try {
          const res = await fetch(`${base}/like`, { method: "POST" })
          const data = await res.json()
          if (!res.ok || !data.ok) throw new Error(data.error || "点赞失败")
          likes.value = data.data.likes
        } catch (err) {
          likes.value = prev
          console.error(err)
          alert("点赞失败，请稍后重试")
        } finally {
          likeSubmitting.value = false
        }
      }

      const refreshComments = async () => {
        if (loadingComments.value) return
        loadingComments.value = true
        try {
          const res = await fetch(`${base}/comments`)
          const data = await res.json()
          if (!res.ok || !data.ok) throw new Error(data.error || "获取评论失败")
          comments.value = data.data
        } catch (err) {
          console.error(err)
          alert("获取评论失败，请稍后重试")
        } finally {
          loadingComments.value = false
        }
      }

      const validate = () => {
        submitError.value = ""
        const a = form.value.author.trim()
        const c = form.value.content.trim()
        if (!a || !c) { submitError.value = "请填写昵称与评论内容"; return false }
        if (a.length > 32) { submitError.value = "昵称过长（最多 32 字）"; return false }
        if (c.length > 1000) { submitError.value = "评论过长（最多 1000 字）"; return false }
        return true
      }

      const onSubmit = async () => {
        if (submitting.value) return
        if (!validate()) return

        submitting.value = true
        submitError.value = ""

        const optimistic = {
          id: -Date.now(),
          author: form.value.author,
          content: form.value.content,
          created_at: new Date().toISOString().slice(0, 19).replace("T", " "),
        }
        comments.value = [optimistic, ...comments.value]

        try {
          const res = await fetch(`${base}/comments`, {
            method: "POST",
            headers,
            body: JSON.stringify({ author: form.value.author, content: form.value.content })
          })
          const data = await res.json()
          if (!res.ok || !data.ok) throw new Error(data.error || "提交失败")
          comments.value = comments.value.map(c => c.id === optimistic.id ? data.data : c)
          form.value.author = ""
          form.value.content = ""
        } catch (err) {
          comments.value = comments.value.filter(c => c.id !== optimistic.id)
          submitError.value = err.message || "提交失败，请稍后重试"
          console.error(err)
        } finally {
          submitting.value = false
        }
      }

      return {
        likes, likeSubmitting,
        comments, loadingComments,
        form, submitting, submitError,
        onLike, onSubmit, refreshComments
      }
    }
  }).mount('#interactive-root')
})()