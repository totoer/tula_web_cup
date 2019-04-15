import Vue from 'vue'
import Vuex from 'vuex'

import images from '@/store/modules/images'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    images: images

  }
});