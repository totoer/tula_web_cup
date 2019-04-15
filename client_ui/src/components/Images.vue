<template>
  <div class="row">
    <div class="col-12">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">TulaWebCup</a>
        <span v-if="client">Привет {{ client.login }}</span>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item" v-if="client===null">
              <a class="nav-link" href="javascript:void(0)" @click="login">Вход</a>
            </li>
            <li class="nav-item" v-if="client!==null">
              <a class="nav-link" href="javascript:void(0)" @click="logout">Выход</a>
            </li>
            <li class="nav-item" v-if="client!==null">
              <a class="nav-link" href="javascript:void(0)" @click="showUploadForm">Загрузить изображение</a>
            </li>
            <!-- <li class="nav-item">
              <a class="nav-link" href="#">Link</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Dropdown
              </a>
              <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                <a class="dropdown-item" href="#">Action</a>
                <a class="dropdown-item" href="#">Another action</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="#">Something else here</a>
              </div>
            </li>
            <li class="nav-item">
              <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
            </li> -->
          </ul>
          <!-- <form class="form-inline my-2 my-lg-0">
            <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </form> -->
        </div>
      </nav>
    </div>
    <div class="col-12">
      <div class="card-columns">
        <div class="card" v-for="(image, index) in images.list" style="width: 18rem;">
          <img :src="image.href" class="card-img-top" @click="showViewWindow(index)" style="cursor: pointer;">
          <div class="card-body">
            <a href="javascript:void(0)" class="btn btn-primary" v-if="client!==null && (image.value===null || image.value===false)" @click="like(image, true)">Like</a><span v-if="image.value===true || client===null">Like:</span><span>{{ image.likecount }}</span>
            <a href="javascript:void(0)" class="btn btn-primary" v-if="client!==null && (image.value===null || image.value===true)" @click="like(image, false)">Dislike</a><span v-if="image.value===false || client===null">Dislike:</span><span>{{ image.dislikecount }}</span>
          </div>
        </div>
      </div>
    </div>
    <div ref="uploadForm" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Загрузить изображение</h5>
          </div>
          <div class="modal-body">
            <p>Выбрать изображение</p>
            <input type="file" name="image" ref="image">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="hideUploadForm">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="uploadImage">Загрузить</button>
          </div>
        </div>
      </div>
    </div>
    <div ref="viewWindow" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Изображение</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="hideViewModel">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" v-if="images.list[currentImageIndex]">
            <p>
              <span>Like:</span><span>{{ images.list[currentImageIndex].likecount }}</span>
              <span>Dislike:</span><span>{{ images.list[currentImageIndex].dislikecount }}</span>
            </p>
            <img :src="images.list[currentImageIndex].href" style="max-width: 100%; max-height: 15em; margin: 0 auto; display: block;">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="nextImage(-1)"><- Туда</button>
            <button type="button" class="btn btn-primary" @click="nextImage(1)">Сюда -></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import axios from 'axios';

export default {
  name: 'Images',
  data() {
    return {
      currentImageIndex: 0,
      client: null
    }
  },
  computed: {
    ...mapState({
      images: state => state.images
    })
  },
  beforeRouteEnter (to, from, next) {
    next(vm => vm.init())
  },
  methods: {
    init() {
      this.$store.dispatch('images/fetch');

      axios.get('/api/login').then((response) => {
        this.client = response.data;
      });

      let scrollLoaderFlag = false;

      document.addEventListener('scroll', (e) => {
        var scrolled = window.pageYOffset || document.documentElement.scrollTop,
          h = window.outerHeight * ((this.images.offset / this.images.limit) + 1);

        console.log(scrolled, h, scrolled / h);
        
        if((scrolled / h) > 0.99 && scrollLoaderFlag==false) {
          scrollLoaderFlag = true;
          this.$store.commit('images/SET_OFFSET', this.images.offset + this.images.limit);
          this.$store.dispatch('images/fetch').then(() => {
            scrollLoaderFlag = false;
          });
        }

      })
    },
    login() {
      window.location.assign("https://oauth.yandex.ru/authorize?response_type=code&client_id=e42c69e9344142478684742b834770b1&state="+window.location.href);
    },
    logout() {
      axios.get('/api/logout').then((response) => {
        this.client = null;
      })
    },
    like(image, value) {
      this.$store.dispatch('images/like', {image: image, value: value}).then(() => {
        this.$store.dispatch('images/fetch');
      });
    },
    showUploadForm() {
      this.$refs.uploadForm.style.display = 'block';
    },
    hideUploadForm() {
      this.$refs.uploadForm.style.display = 'none';
    },
    uploadImage() {
      if (this.$refs.image.files && this.$refs.image.files[0]) {
        this.$store.dispatch('images/upload', this.$refs.image).then(() => {
          this.$refs.uploadForm.style.display = 'none';
          this.$store.dispatch('images/fetch');
        });
      }
    },
    showViewWindow(index) {
      this.currentImageIndex = index;
      this.$refs.viewWindow.style.display = 'block';
    },
    hideViewModel() {
      this.currentImageIndex = 0;
      this.$refs.viewWindow.style.display = 'none';
    },
    nextImage(directions) {
      this.currentImageIndex += directions;
      
      if(this.currentImageIndex < 0) {
        this.currentImageIndex = 0;
      }

      if(this.currentImageIndex > (this.images.list.length - 1)) {
        this.currentImageIndex = this.images.list.length - 1;
      }
    }
  }
}
</script>