<template>
  <div class="post-item">
    <h2>{{ post.title }}</h2>
    <div v-if="detail">
      <p>
        <time :date-time="articleData.articleDateTime">{{ articleData.articleDate }}</time>, by
        <span class="author">{{ articleData.articleAuthor }}</span>
      </p>
    </div>
    <div v-else>
      <p>
        <router-link :to="{ name: 'PostDetail', params: { slug: post.meta.slug } }">
          <time :date-time="articleData.articleDateTime">{{ articleData.articleDate }}</time> </router-link>, by
        <span class="author">{{ articleData.articleAuthor }}</span>
      </p>
    </div>
    <div v-if="detail" v-html="post.html_detail" @click="handleClick"></div>
    <div v-else v-html="post.html_overview" @click="handleClick"></div>
    <!-- Podlove Players -->
    <div v-for="([elementId, apiUrl]) in podlovePlayers" :key="elementId">
      <podlove-player :element-id="elementId" :api-url="apiUrl"></podlove-player>
    </div>
    <!-- Comments -->
    <div v-if="post.comments" class="comments">
      <comment-list
        :comments="post.comments"
        :commentMeta="commentMeta"
        @comment-posted="handleCommentPosted">
      </comment-list>
    </div>
    <!-- Modal for Images / Galleries -->
    <div v-if="isModalOpen" id="modal-div" class="modal" @click="handleModalClick">
      <span class="close" @click="closeModal">&times;</span>
      <img id="modal-image" class="modal-content" :src="modalImage.src" :srcset="modalImage.srcset"
        :next="modalImage.next" :prev="modalImage.prev" alt="Full-sized image" />
    </div>
  </div>
</template>

<script lang="ts">
import config from '../config';
import { Post, ModalImage, CommentMeta, ArticleData } from "./types";
import CommentList from "./CommentList.vue";
import PodlovePlayer from "./PodlovePlayer.vue";


export default {
  mounted() {
    // Add event listener when the component is mounted
    window.addEventListener("keydown", this.handleKeyDown);
  },
  beforeUnmount() {
    // Remove event listener when the component is unmounted
    window.removeEventListener("keydown", this.handleKeyDown);
  },
  name: "PostItem",
  components: {
    CommentList,
    PodlovePlayer,
  },
  props: {
    post: {
      type: Object as () => Post,
      required: true,
    },
    detail: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isModalOpen: false,
      modalImage: {} as ModalImage,
    };
  },
  methods: {
    handleCommentPosted() {
      console.log("handleCommentPosted");
      this.$emit("comment-posted");
    },
    handleClick(e: Event) {
      // console.log("handleClick: ", e);
      if (!e.target) {
        return;
      }
      const clickedEl = e.target as HTMLImageElement;
      if (!(clickedEl.id)) {
        return;
      }
      if (!clickedEl.id.startsWith("gallery-image")) {
        return;
      }
      this.setModalFromImage(clickedEl);
    },
    setModalFromImage(clickedEl: HTMLImageElement) {
      const prev = clickedEl.getAttribute("data-prev");
      if (!prev) {
        return;
      }
      this.modalImage.prev = prev;
      const next = clickedEl.getAttribute("data-next");
      if (!next) {
        return;
      }
      this.modalImage.next = next;
      const fullSrc = clickedEl.getAttribute("data-fullsrc");
      if (!fullSrc) {
        return;
      }
      this.modalImage.src = fullSrc;
      const srcset = clickedEl.getAttribute("data-srcset");
      if (!srcset) {
        return;
      }
      this.modalImage.srcset = srcset;
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        this.closeModal();
      } else if (event.key === "ArrowLeft") {
        if (!this.isModalOpen || !this.modalImage.prev) {
          return;
        }
        const imageId = this.modalImage.prev.split("-")[1]
        const prevImage = document.getElementById("gallery-image-" + imageId) as HTMLImageElement;
        if (!prevImage) {
          return;
        }
        this.setModalFromImage(prevImage);
      } else if (event.key === "ArrowRight") {
        if (!this.isModalOpen || !this.modalImage.next) {
          return;
        }
        const imageId = this.modalImage.next.split("-")[1]
        const nextImage = document.getElementById("gallery-image-" + imageId) as HTMLImageElement;
        if (!nextImage) {
          return;
        }
        this.setModalFromImage(nextImage);
      }

    },
    handleModalClick(e: Event) {
      if (!e.target) {
        return;
      }
      const clickedEl = e.target as HTMLElement;
      // console.log("handleModalClick: ", clickedEl.id);
      if (clickedEl.id === "modal-div") {
        this.closeModal();
      } else if (clickedEl.id === "modal-image") {
        window.open(this.modalImage.src, '_blank');
      }
    }
  },
  computed: {
    articleData(): ArticleData {
      const dom = new DOMParser().parseFromString(this.post.html_detail, "text/html");
      const {
        articleDate = "",
        articleDateTime = "",
        articleAuthor = "",
      } = dom.getElementById("vue-article-data")?.dataset ?? {};
      return {
        articleDate,
        articleDateTime,
        articleAuthor,
      }
    },
    commentMeta(): CommentMeta {
      const postCommentUrl = config.postCommentUrl;
      const csrfToken = config.csrfToken;
      const commentMeta: CommentMeta = {
        ...this.post.comments_security_data,
        postCommentUrl,
        csrfToken,
        commentsAreEnabled: this.post.comments_are_enabled,
      }
      return commentMeta;
    },
    podlovePlayers(): [string, string][] {
      return this.post.podlove_players;
    },
  },
};
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.6);
}

.modal-content {
  margin: auto;
  display: block;
  width: 80%;
  max-width: 900px;
  max-height: 740px;
  object-fit: contain;
}

.close {
  position: absolute;
  top: 15px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  transition: 0.3s;
}

.close:hover,
.close:focus {
  color: #bbb;
  text-decoration: none;
  cursor: pointer;
}
</style>
