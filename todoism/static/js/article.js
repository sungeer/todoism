// static/js/article.js
(function () {
//  var csrf = document.querySelector('meta[name="csrf-token"]');
//  if (csrf && csrf.content) {
//    axios.defaults.headers.common["X-CSRF-Token"] = csrf.content;
//  }

  var createApp = Vue.createApp;
  var ref = Vue.ref;

  // 从服务端注入的全局数据读取
  var server = window.__ARTICLE_DATA__ || { id: 0, likes: 0, comments: [] };
  var ARTICLE_ID = server.id;
  var INITIAL_LIKES = server.likes;
  var INITIAL_COMMENTS = server.comments;

  createApp({
    setup: function () {
      var likes = ref(INITIAL_LIKES);
      var likeSubmitting = ref(false);

      var comments = ref(INITIAL_COMMENTS);
      var loadingComments = ref(false);

      var form = ref({ author: "", content: "" });
      var submitting = ref(false);
      var submitError = ref("");

      var base = "/api/articles/" + ARTICLE_ID;

      // 你也可以设置全局默认值：
      // axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
      var jsonHeaders = { "Content-Type": "application/json" };

      // 点赞
      function onLike() {
        if (likeSubmitting.value) return;

        likeSubmitting.value = true;
        var prev = likes.value;
        likes.value = prev + 1;

        axios.post(base + "/like")
          .then(function (res) {
            // 后端统一结构：{ ok: true, data: { likes: number } }
            if (!res || !res.data || res.data.ok !== true) {
              throw new Error((res && res.data && res.data.error) || "点赞失败");
            }
            likes.value = res.data.data.likes;
          })
          .catch(function (err) {
            likes.value = prev;
            console.error(err);
            alert("点赞失败，请稍后重试");
          })
          .finally(function () {
            likeSubmitting.value = false;
          });
      }

      function refreshComments() {
        if (loadingComments.value) return;

        loadingComments.value = true;

        axios.get(base + "/comments")
          .then(function (res) {
            if (!res || !res.data || res.data.ok !== true) {
              throw new Error((res && res.data && res.data.error) || "获取评论失败");
            }
            comments.value = res.data.data;
          })
          .catch(function (err) {
            console.error(err);
            alert("获取评论失败，请稍后重试");
          })
          .finally(function () {
            loadingComments.value = false;
          });
      }

      function validate() {
        submitError.value = "";
        var a = (form.value.author || "").trim();
        var c = (form.value.content || "").trim();
        if (!a || !c) { submitError.value = "请填写昵称与评论内容"; return false; }
        if (a.length > 32) { submitError.value = "昵称过长（最多 32 字）"; return false; }
        if (c.length > 1000) { submitError.value = "评论过长（最多 1000 字）"; return false; }
        return true;
      }

      function onSubmit() {
        if (submitting.value) return;
        if (!validate()) return;

        submitting.value = true;
        submitError.value = "";

        var optimistic = {
          id: -Date.now(),
          author: form.value.author,
          content: form.value.content,
          created_at: new Date().toISOString().slice(0, 19).replace("T", " ")
        };
        comments.value = [optimistic].concat(comments.value);

        axios.post(base + "/comments", {
          author: form.value.author,
          content: form.value.content
        }, { headers: jsonHeaders })
          .then(function (res) {
            if (!res || !res.data || res.data.ok !== true) {
              throw new Error((res && res.data && res.data.error) || "提交失败");
            }

            var real = res.data.data;
            // 用普通 for 循环替换乐观项
            var arr = comments.value.slice();
            for (var i = 0; i < arr.length; i++) {
              if (arr[i].id === optimistic.id) {
                arr[i] = real;
                break;
              }
            }
            comments.value = arr;

            form.value.author = "";
            form.value.content = "";
          })
          .catch(function (err) {
            // 回滚乐观更新
            var filtered = [];
            for (var i = 0; i < comments.value.length; i++) {
              var item = comments.value[i];
              if (item.id !== optimistic.id) filtered.push(item);
            }
            comments.value = filtered;

            submitError.value = (err && err.message) ? err.message : "提交失败，请稍后重试";
            console.error(err);
          })
          .finally(function () {
            submitting.value = false;
          });
      }

      return {
        likes: likes,
        likeSubmitting: likeSubmitting,
        comments: comments,
        loadingComments: loadingComments,
        form: form,
        submitting: submitting,
        submitError: submitError,
        onLike: onLike,
        onSubmit: onSubmit,
        refreshComments: refreshComments
      };
    }
  }).mount('#interactive-root');
})();